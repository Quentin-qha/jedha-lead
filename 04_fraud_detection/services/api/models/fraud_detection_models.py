from pydantic import BaseModel, Field
from typing import Dict, List, Optional

"""
===========================================================
DEFINITION DES MODELES Pydantic (quiz_models)
===========================================================

Ce module contient l’ensemble des modèles de données utilisés par l’API.
Les modèles Pydantic permettent la validation, la sérialisation et la documentation automatique.

Contenu principal :
- Différents modèles de réponses HTTP : HealthResponse, ReadyResponse, etc.

Chaque modèle est typé, documenté et intègre des exemples pour la documentation Swagger.
"""

# Model de /health
class HealthResponse(BaseModel):
    status: str

# Model de /ready
class ReadyResponse(BaseModel):
    status: str
    quiz_count: Optional[int] = None
    reason: Optional[str] = None

# Model pour /clear
class ClearResponse(BaseModel):
    message: str

# Model pour /predict
class TransactionRequest(BaseModel):
    model_config = {"coerce_numbers_to_str": True}

    current_time: str
    cc_num: str
    trans_num: str
    merchant: str
    first: str
    last: str
    street: str
    zip: str
    city: str
    category: str
    amt: float
    gender: str
    state: str
    city_pop: int
    lat: float
    long: float
    merch_lat: float
    merch_long: float
    dob: str
    job: str
    trans_hour: Optional[int] = None
    trans_day: Optional[int] = None
    trans_month: Optional[int] = None

class PredictionResponse(BaseModel):
    is_fraud: int
    fraud_probability: float
    inference_ms: float
    run_id: str
