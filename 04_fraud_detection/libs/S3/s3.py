import os
import boto3
import pandas as pd
from io import StringIO
import json
from dotenv import load_dotenv

def s3_get_datas(bucket_url, bucket_key):
    load_dotenv()

    session = boto3.Session(
        aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name           = os.getenv("AWS_DEFAULT_REGION")
    )

    s3 = session.client("s3")

    # bucket = "jedha-fraud-detection-qha"
    # key    = "model_datas/fraudTest.csv"

    obj = s3.get_object(Bucket=bucket_url, Key=bucket_key)
    df  = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))

    return df

def s3_send_datas(bucket_url, bucket_key, file):
    load_dotenv()

    session = boto3.Session(
        aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name           = os.getenv("AWS_DEFAULT_REGION")
    )

    s3 = session.client("s3")
    
    s3.put_object(
        Bucket=bucket_url,
        Key=bucket_key,
        Body=json.dumps(file),
        ContentType="application/json"
    )
    print('Sended to S3')

def s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
    )

def s3_bucket() -> str:
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        raise RuntimeError("S3_BUCKET is not set")
    return bucket