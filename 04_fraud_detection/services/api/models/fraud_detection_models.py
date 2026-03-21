from pydantic import BaseModel, Field
from typing import Optional

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
    status: str = Field(..., example="ok")


# Model pour /predict
class TransactionRequest(BaseModel):
    model_config = {"coerce_numbers_to_str": True}

    current_time: str = Field(..., description="Horodatage de la transaction (format ISO ou timestamp ms)", example="2020-06-21 12:14:25")
    cc_num: str = Field(..., description="Numéro de carte bancaire", example="2703186189652095")
    trans_num: str = Field(..., description="Identifiant unique de la transaction", example="2da90c7d74bd46a0caf3777415b3ebd3")
    merchant: str = Field(..., description="Nom du marchand", example="fraud_Rippin, Kub and Mann")
    first: str = Field(..., description="Prénom du porteur de carte", example="Jennifer")
    last: str = Field(..., description="Nom du porteur de carte", example="Banks")
    street: str = Field(..., description="Adresse du porteur", example="561 Perry Cove")
    zip: str = Field(..., description="Code postal du porteur", example="48053")
    city: str = Field(..., description="Ville du porteur", example="Moravian Falls")
    category: str = Field(..., description="Catégorie du marchand", example="misc_net")
    amt: float = Field(..., description="Montant de la transaction en USD", example=4.97)
    gender: str = Field(..., description="Genre du porteur (M/F)", example="F")
    state: str = Field(..., description="État américain du porteur", example="NC")
    city_pop: int = Field(..., description="Population de la ville du porteur", example=3495)
    lat: float = Field(..., description="Latitude du porteur", example=36.0788)
    long: float = Field(..., description="Longitude du porteur", example=-81.1781)
    merch_lat: float = Field(..., description="Latitude du marchand", example=36.011293)
    merch_long: float = Field(..., description="Longitude du marchand", example=-82.048315)
    dob: str = Field(..., description="Date de naissance du porteur (YYYY-MM-DD)", example="1988-03-09")
    job: str = Field(..., description="Métier du porteur", example="Psychologist, counselling")
    trans_hour: Optional[int] = Field(None, description="Heure de la transaction (calculée automatiquement si absente)")
    trans_day: Optional[int] = Field(None, description="Jour de la transaction (calculé automatiquement si absent)")
    trans_month: Optional[int] = Field(None, description="Mois de la transaction (calculé automatiquement si absent)")

    model_config = {
        "coerce_numbers_to_str": True,
        "json_schema_extra": {
            "example": {
                "current_time": "2020-06-21 12:14:25",
                "cc_num": "2703186189652095",
                "trans_num": "2da90c7d74bd46a0caf3777415b3ebd3",
                "merchant": "fraud_Rippin, Kub and Mann",
                "first": "Jennifer",
                "last": "Banks",
                "street": "561 Perry Cove",
                "zip": "48053",
                "city": "Moravian Falls",
                "category": "misc_net",
                "amt": 4.97,
                "gender": "F",
                "state": "NC",
                "city_pop": 3495,
                "lat": 36.0788,
                "long": -81.1781,
                "merch_lat": 36.011293,
                "merch_long": -82.048315,
                "dob": "1988-03-09",
                "job": "Psychologist, counselling"
            }
        }
    }


class PredictionResponse(BaseModel):
    is_fraud: int = Field(..., description="Résultat de la prédiction (0 = légitime, 1 = fraude)", example=0)
    fraud_probability: float = Field(..., description="Probabilité de fraude entre 0 et 1", example=0.0312)
    inference_ms: float = Field(..., description="Temps d'inférence en millisecondes", example=14.5)
    run_id: str = Field(..., description="Identifiant du run MLflow ayant produit cette prédiction", example="a1b2c3d4e5f6...")
