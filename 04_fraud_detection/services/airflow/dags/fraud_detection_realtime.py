import json
import os
import requests
import psycopg2
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import sys
sys.path.append("/opt/airflow")

from libs.S3.s3 import s3_client, s3_bucket, s3_send_datas
from src.pipeline.clean_datas import clean_datas_history
from src.utils.send_transaction_to_supabase import process_and_store
from src.utils.send_alert_email import send_fraud_alert


JEDHA_API_URL = "https://sdacelo-real-time-fraud-detection.hf.space/current-transactions"


def predict_fraud():
    # 1. Récupérer la transaction depuis Jedha
    response = requests.get(JEDHA_API_URL)
    response.raise_for_status()
    data = response.json()
    # L'API retourne parfois un JSON doublement encodé (string dans string)
    if isinstance(data, str):
        data = json.loads(data)
    print(data)

    # Convertir format "split" → dict
    df = pd.DataFrame(data["data"], columns=data["columns"])
    transaction = df.iloc[0].to_dict()
    print(transaction)

    # 2. Sauvegarder le JSON brut en S3
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    s3_key = f"realtime_transactions/{timestamp}.json"

    s3_send_datas("jedha-fraud-detection-qha", s3_key, transaction)

    # Clean transaction
    df_transaction = pd.DataFrame([transaction])
    transaction_clean = clean_datas_history(df_transaction, call_type="api")
    # transaction_clean_json = transaction_clean.iloc[0].to_dict()
    print("transaction_clean")
    print(transaction_clean.iloc[0].to_dict())
    
    # Send to model with api
    API_URL = "http://api:8000/predict"

    response = requests.post(API_URL, json=transaction)
    response.raise_for_status()
    prediction = response.json()
    print(prediction)

    # Send to database
    process_and_store(transaction, prediction, prediction['run_id'])

    # Send email alert if fraud detected
    if prediction['is_fraud']:
        send_fraud_alert(transaction, prediction)

    return prediction


with DAG(
    dag_id="fraud_detection_realtime",
    schedule_interval="* * * * *",  # toutes les minutes
    start_date=days_ago(1),
    catchup=False,
    tags=["fraud", "realtime"],
) as dag:

    poll_task = PythonOperator(
        task_id="predict_fraud",
        python_callable=predict_fraud,
    )
