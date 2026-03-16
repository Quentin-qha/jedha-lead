from fastapi import FastAPI
from api.routes.fraud_detection_route import router as fraud_router
from api.routes.health_route import router as health_router

app = FastAPI(title="Fraud Detection API", version="1.0.0")

app.include_router(health_router)
app.include_router(fraud_router)
