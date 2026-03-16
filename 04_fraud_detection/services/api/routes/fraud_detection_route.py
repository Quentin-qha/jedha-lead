from fastapi import APIRouter, HTTPException
from api.models.fraud_detection_models import TransactionRequest, PredictionResponse
from api.utils.fraud_detection_real_time import fraud_detection_real_time

router = APIRouter(tags=["Fraud Detection"])


@router.post("/predict", response_model=PredictionResponse)
def predict(transaction: TransactionRequest):
    """Prédit si une transaction est frauduleuse."""
    try:
        result = fraud_detection_real_time(transaction.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
