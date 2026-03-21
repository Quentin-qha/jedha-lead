import os
import sys

# Ajoute la racine du projet (04_fraud_detection/) au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

import joblib
import tempfile
import pandas as pd
import mlflow

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    roc_auc_score,
    classification_report,
)

from clean_datas import clean_datas_history
from libs.S3.s3 import s3_get_datas

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
EXPERIMENT_NAME     = os.getenv("MLFLOW_EXPERIMENT_NAME", "fraud_detection")
DATA_DIR            = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "../../datas"))
S3_BUCKET_NAME      = os.getenv("S3_BUCKET_NAME")

# TRAIN_CSV = os.path.join(DATA_DIR, "fraudTrain.csv")
# TEST_CSV  = os.path.join(DATA_DIR, "fraudTest.csv")

TARGET = "is_fraud"

# ---------------------------------------------------------------------------
# Load & clean
# ---------------------------------------------------------------------------
print("Loading data...")
df_train = s3_get_datas(S3_BUCKET_NAME, "model_datas/fraudTrain.csv")
df_test = s3_get_datas(S3_BUCKET_NAME, "model_datas/fraudTest.csv")

print("Cleaning data...")
df_clean_train = clean_datas_history(df_train, call_type="csv")
df_clean_test  = clean_datas_history(df_test,  call_type="csv")
print(df_clean_train.head())
print(df_clean_test.head())

X_train = df_clean_train.drop(columns=[TARGET])
y_train = df_clean_train[TARGET]

X_test = df_clean_test.drop(columns=[TARGET])
y_test = df_clean_test[TARGET]

# ---------------------------------------------------------------------------
# Preprocessor
# ---------------------------------------------------------------------------
numeric_features     = [c for c in X_train.columns if 'float' in str(X_train[c].dtype) or 'int' in str(X_train[c].dtype)]
categorical_features = [c for c in X_train.columns if X_train[c].dtype == "object"]

print(f"Numeric features:     {numeric_features}")
print(f"Categorical features: {categorical_features}")

numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("encoder", OneHotEncoder(drop="first", handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer,     numeric_features),
    ("cat", categorical_transformer, categorical_features),
])

# ---------------------------------------------------------------------------
# Model — RandomForest (meilleure précision sur la fraude, moins de faux positifs)
# ---------------------------------------------------------------------------
model_params = {
    "n_estimators": int(os.getenv("RF_N_ESTIMATORS", 100)),
    "max_depth":    int(os.getenv("RF_MAX_DEPTH",    20)),
    "class_weight": "balanced",
    "n_jobs":       -1,
    "random_state": 42,
}

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier",   RandomForestClassifier(**model_params)),
])

# ---------------------------------------------------------------------------
# MLflow
# ---------------------------------------------------------------------------
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run():
    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred      = pipeline.predict(X_test)
    y_pred_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy":  accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall":    recall_score(y_test, y_pred),
        "f1":        f1_score(y_test, y_pred),
        "roc_auc":   roc_auc_score(y_test, y_pred_prob),
    }

    # Params
    mlflow.log_params({
        "model":          "RandomForestClassifier",
        "n_estimators":   model_params["n_estimators"],
        "max_depth":      model_params["max_depth"],
        "class_weight":   model_params["class_weight"],
        "train_samples":  len(X_train),
        "test_samples":   len(X_test),
        "fraud_ratio_train": round(y_train.mean(), 4),
    })

    # Metrics
    mlflow.log_metrics(metrics)

    # Model artifact — sauvegarde joblib pour compatibilité avec le serveur MLflow
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "model.pkl")
        joblib.dump(pipeline, model_path)
        mlflow.log_artifact(model_path, artifact_path="model")

    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    print("\nMetrics logged to MLflow:")
    for k, v in metrics.items():
        print(f"  {k}: {v:.4f}")

    run_id = mlflow.active_run().info.run_id
    print(f"\nRun ID: {run_id}")
    print(f"MLflow UI: {MLFLOW_TRACKING_URI}")