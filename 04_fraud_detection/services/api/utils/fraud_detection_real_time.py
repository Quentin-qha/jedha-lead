import os
import sys
import time
import joblib
import mlflow
import pandas as pd

sys.path.append("/app")
from src.pipeline.clean_datas import clean_datas_history

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT_NAME     = os.getenv("MLFLOW_EXPERIMENT_NAME", "fraud_detection")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Cache du modèle : chargé une seule fois au démarrage
_pipeline = None
_run_id = None


def get_pipeline():
    """Charge le pipeline depuis MLflow (meilleur F1). Mis en cache après le premier appel."""
    global _pipeline, _run_id
    if _pipeline is not None:
        return _pipeline

    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    if not experiment:
        raise RuntimeError(f"Experiment '{EXPERIMENT_NAME}' introuvable dans MLflow")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.f1 DESC"],
        max_results=1,
    )
    if not runs:
        raise RuntimeError("Aucun run trouvé dans MLflow")

    _run_id = runs[0].info.run_id
    local_path = mlflow.artifacts.download_artifacts(f"runs:/{_run_id}/model/model.pkl")
    _pipeline = joblib.load(local_path)
    return _pipeline


def fraud_detection_real_time(transaction: dict) -> dict:
    """
    Prend une transaction brute (dict), la nettoie et retourne la prédiction.

    Args:
        transaction: dict avec les champs bruts de la transaction

    Returns:
        dict: { is_fraud: 0|1, fraud_probability: float }
    """
    pipeline = get_pipeline()

    df = pd.DataFrame([transaction])
    # Accepte timestamp int (ms) ou string date
    df["current_time"] = pd.to_datetime(df["current_time"], unit="ms", errors="coerce").fillna(
        pd.to_datetime(df["current_time"], errors="coerce")
    )
    df["dob"] = pd.to_datetime(df["dob"])

    df_clean = clean_datas_history(df, call_type="api")

    t0 = time.time()
    prediction  = pipeline.predict(df_clean)[0]
    probability = pipeline.predict_proba(df_clean)[0][1]
    inference_ms = round((time.time() - t0) * 1000, 2)

    return {
        "is_fraud": int(prediction),
        "fraud_probability": round(float(probability), 4),
        "inference_ms": inference_ms,
        "run_id": _run_id,
    }
