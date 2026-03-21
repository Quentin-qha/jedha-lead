from fastapi import FastAPI
from api.routes.fraud_detection_route import router as fraud_router
from api.routes.health_route import router as health_router

app = FastAPI(
    title="Fraud Detection API",
    version="1.0.0",
    description="""
## API de détection de fraude bancaire en temps réel

Cette API expose un modèle **RandomForestClassifier** entraîné sur 1,2 million de transactions bancaires.
Elle est utilisée par le pipeline Airflow qui tourne toutes les minutes pour analyser les nouvelles transactions.

### Fonctionnement
1. Le pipeline Airflow récupère une transaction depuis l'API Jedha
2. Il envoie la transaction brute à `POST /predict`
3. L'API effectue le feature engineering et retourne un score de fraude (~15ms)
4. Si `is_fraud = 1`, une alerte email est déclenchée

### Modèle
- **Algorithme** : RandomForestClassifier (scikit-learn)
- **Sélection** : meilleur run MLflow selon le F1-score
- **Gestion du déséquilibre** : `class_weight="balanced"` (0.58% de fraudes dans le dataset)
""",
    contact={
        "name": "Fraud Detection Pipeline",
    },
    license_info={
        "name": "Jedha Bootcamp — Lead Data Engineer",
    },
)

app.include_router(health_router)
app.include_router(fraud_router)
