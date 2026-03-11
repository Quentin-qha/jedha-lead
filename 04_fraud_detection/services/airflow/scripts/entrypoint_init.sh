#!/usr/bin/env bash
set -euo pipefail

echo "[airflow-init] DB migrate..."
airflow db migrate

echo "[airflow-init] Creating admin user (idempotent)..."
airflow users create \
    --username "$${AIRFLOW_USERNAME}"
    --password "$${AIRFLOW_PASSWORD}"
    --firstname "$${AIRFLOW_FIRSTNAME}"
    --lastname "$${AIRFLOW_LASTNAME}"
    --role Admin \
    --email admin@example.com \
    || true

echo "[airflow-init] Done."