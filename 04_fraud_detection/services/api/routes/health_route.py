from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from api.models.fraud_detection_models import HealthResponse, ReadyResponse

"""
===========================================================
ROUTES DE SANTÉ ET DE READINESS (health_routes)
===========================================================

Ce module définit les routes de vérification de l’état de l’API.

Routes :
- GET /health → indique si l’API est en ligne (simple ping).
"""

router = APIRouter(tags=["Health"])

# Pour vérifier que l'api est en vie
@router.get("/health", response_model=HealthResponse)
def health():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok"}