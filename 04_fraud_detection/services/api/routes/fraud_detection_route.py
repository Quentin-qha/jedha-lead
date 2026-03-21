from fastapi import APIRouter, HTTPException
from api.models.fraud_detection_models import TransactionRequest, PredictionResponse
from api.utils.fraud_detection_real_time import fraud_detection_real_time

router = APIRouter(tags=["Fraud Detection"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Prédire si une transaction est frauduleuse",
    response_description="Score de fraude, probabilité, temps d'inférence et run MLflow utilisé",
)
def predict(transaction: TransactionRequest):
    """
    Analyse une transaction bancaire et retourne une prédiction de fraude.

    **Feature engineering appliqué automatiquement :**
    - `age` : calculé depuis `dob`
    - `distance_km` : distance géodésique entre le porteur et le marchand
    - `trans_hour / trans_day / trans_month` : extraits de `current_time`
    - `customer_job_category` : `job` regroupé en 16 catégories

    **Retourne :**
    - `is_fraud` : 0 (légitime) ou 1 (fraude)
    - `fraud_probability` : score entre 0 et 1
    - `inference_ms` : temps d'inférence en ms
    - `run_id` : identifiant MLflow du modèle utilisé
    """
    try:
        result = fraud_detection_real_time(transaction.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
