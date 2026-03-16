# Fraud Detection — Système de détection de fraude en temps réel

Projet de détection de fraude bancaire en temps réel, construit avec une architecture microservices complète : collecte automatisée, modèle ML, API de prédiction, stockage, alertes email et dashboard de monitoring.

---

## Architecture

```
Jedha API (source de données)
        │
        ▼  toutes les minutes
┌──────────────────────────────────────────────────────┐
│                   AIRFLOW (orchestrateur)             │
│  1. Collecte transaction (GET Jedha API)              │
│  2. Sauvegarde JSON brut → S3                         │
│  3. Nettoyage & feature engineering                   │
│  4. Prédiction → FastAPI                              │
│  5. Stockage → Supabase                               │
│  6. Alerte email si fraude détectée                   │
└──────────────────────────────────────────────────────┘
        │                    │                  │
        ▼                    ▼                  ▼
  ┌──────────┐        ┌──────────┐       ┌──────────────┐
  │  FastAPI │◄──────►│  MLflow  │       │   Supabase   │
  │ (predict)│        │ (modèle) │       │  (PostgreSQL)│
  └──────────┘        └──────────┘       └──────────────┘
                                                │
                                                ▼
                                        ┌──────────────┐
                                        │  Streamlit   │
                                        │ (dashboard)  │
                                        └──────────────┘
```

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Orchestration | Apache Airflow 2.10.3 |
| ML & tracking | scikit-learn, MLflow, XGBoost |
| API prédiction | FastAPI + Uvicorn |
| Base de données | Supabase (PostgreSQL) |
| Stockage objets | AWS S3 |
| Dashboard | Streamlit + Plotly |
| Containerisation | Docker + Docker Compose |
| Tests | pytest |

---

## Structure du projet

```
04_fraud_detection/
├── docker/                         # Dockerfiles par service
│   ├── Dockerfile.api
│   ├── Dockerfile.airflow
│   ├── Dockerfile.mlflow
│   └── Dockerfile.streamlit
│
├── services/
│   ├── api/                        # FastAPI — service de prédiction
│   │   ├── main.py
│   │   ├── models/                 # Modèles Pydantic (requête/réponse)
│   │   ├── routes/                 # Endpoints /predict et /health
│   │   ├── utils/                  # Chargement modèle MLflow + inférence
│   │   └── tests/                  # Tests unitaires avec pytest
│   │
│   ├── airflow/
│   │   └── dags/
│   │       └── fraud_detection_realtime.py   # DAG principal (1/min)
│   │
│   └── streamlit/
│       └── app.py                  # Dashboard de monitoring
│
├── src/
│   ├── pipeline/
│   │   ├── clean_datas.py          # Feature engineering (âge, distance, heure, métier)
│   │   └── train_model.py          # Entraînement RandomForest + log MLflow
│   └── utils/
│       ├── send_transaction_to_supabase.py   # Écriture en base
│       └── send_alert_email.py               # Alertes SMTP
│
├── libs/
│   ├── S3/s3.py                    # Upload/download S3
│   └── db/supabase.py              # Connexion PostgreSQL
│
├── exploration/                    # Notebooks Jupyter
│   ├── eda_csv.ipynb               # EDA complète avec visualisations
│   ├── eda_api.ipynb               # Exploration des données temps réel
│   ├── clean_code.ipynb            # Expérimentation du preprocessing
│   └── xgboost_optimisation.ipynb  # Optimisation hyperparamètres XGBoost
│
├── requirements/                   # Dépendances par service
│   ├── api_requirements.txt
│   ├── airflow_requirements.txt
│   ├── mlflow_requirements.txt
│   └── streamlit_requirements.txt
│
├── .env                            # Variables d'environnement (non versionné)
└── docker-compose.yml              # Orchestration des 6 services
```

---

## Services & ports

| Service | Port | Rôle |
|---------|------|------|
| Airflow Webserver | 8080 | Interface de gestion des DAGs |
| MLflow | 5000 | Suivi des expériences et modèles |
| FastAPI | 8000 | API de prédiction (POST /predict) |
| Streamlit | 8501 | Dashboard de monitoring |

---

## Installation et démarrage

### Prérequis

- Docker & Docker Compose
- Un compte AWS (S3)
- Un compte Supabase
- Un compte Gmail avec App Password (pour les alertes email)

### 1. Cloner le projet

```bash
git clone <repo-url>
cd 04_fraud_detection
```

### 2. Configurer Supabase

Trois bases de données (ou schémas) doivent être créés dans Supabase avant de démarrer :

**Schéma `public`** — données métier (créer manuellement dans l'éditeur SQL Supabase) :

```sql
-- Porteurs de carte
CREATE TABLE cardholders (
    id SERIAL PRIMARY KEY,
    cc_num TEXT UNIQUE NOT NULL,
    first TEXT, last TEXT,
    gender TEXT, street TEXT, city TEXT, state TEXT, zip TEXT,
    lat FLOAT, long FLOAT, city_pop INT, job TEXT, dob DATE
);

-- Marchands
CREATE TABLE merchants (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    category TEXT,
    lat FLOAT, long FLOAT
);

-- Transactions
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    trans_num TEXT UNIQUE NOT NULL,
    trans_at TIMESTAMPTZ,
    amt FLOAT,
    is_fraud BOOLEAN,
    cardholder_id INT REFERENCES cardholders(id),
    merchant_id INT REFERENCES merchants(id)
);

-- Versions du modèle MLflow
CREATE TABLE model_versions (
    id UUID PRIMARY KEY,
    mlflow_run_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    deployed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Prédictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(id),
    model_version_id UUID REFERENCES model_versions(id),
    fraud_score FLOAT,
    is_fraud BOOLEAN,
    inference_ms FLOAT,
    predicted_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alertes
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    prediction_id INT REFERENCES predictions(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Schéma `airflow`** — créé automatiquement par Airflow au premier démarrage (`airflow db init`). Il faut simplement que l'utilisateur Supabase ait les droits de création de schéma, ou créer le schéma manuellement :

```sql
CREATE SCHEMA airflow;
GRANT ALL ON SCHEMA airflow TO your_supabase_user;
```

La variable `AIRFLOW_DB_URL` doit pointer sur ce schéma :
```
postgresql://user:password@host:5432/postgres?options=-csearch_path%3Dairflow
```

**Schéma `mlflow`** — créé automatiquement par MLflow au premier démarrage (`mlflow server`). Créer le schéma manuellement au préalable :

```sql
CREATE SCHEMA mlflow;
GRANT ALL ON SCHEMA mlflow TO your_supabase_user;
```

La variable `MLFLOW_DB_URL` doit pointer sur ce schéma :
```
postgresql://user:password@host:5432/postgres?options=-csearch_path%3Dmlflow
```

---

### 3. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du dossier `04_fraud_detection/` :

```env
# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=eu-west-3

# S3
S3_BUCKET_NAME=your-bucket-name

# Supabase
SUPABASE_DATABASE_URL=postgresql://user:password@host:5432/db
DB_HOST=your-host
DB_NAME=your-db
DB_USER=your-user
DB_PASSWORD=your-password
DB_PORT=5432

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=fraud_detection
MLFLOW_DB_URL=postgresql://user:password@host:5432/mlflow
MLFLOW_BUCKET=s3://your-bucket/mlflow

# Airflow
AIRFLOW_DB_URL=postgresql://user:password@host:5432/airflow
AIRFLOW_FERNET_KEY=your_fernet_key
AIRFLOW_WEBSERVER_SECRET_KEY=your_secret_key
AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=admin
AIRFLOW_FIRSTNAME=Admin
AIRFLOW_LASTNAME=Admin

# SMTP (alertes email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL_TO=recipient@email.com
```

> Pour générer une Fernet key Airflow : `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

### 3. Démarrer tous les services

```bash
docker-compose up --build
```

### 4. Entraîner le modèle

Avant d'utiliser le pipeline temps réel, entraîner le modèle et l'enregistrer dans MLflow :

```bash
docker exec -it airflow-scheduler bash
python /opt/airflow/src/pipeline/train_model.py
```

Le modèle est automatiquement sauvegardé dans MLflow. FastAPI charge le run avec le meilleur F1-score au démarrage.

### 5. Activer le DAG

1. Ouvrir l'interface Airflow : [http://localhost:8080](http://localhost:8080)
2. Se connecter avec les credentials du `.env`
3. Activer le DAG `fraud_detection_realtime`

Le pipeline tourne ensuite automatiquement toutes les minutes.

---

## Pipeline de données

### Feature engineering (`clean_datas.py`)

| Feature | Description |
|---------|-------------|
| `age` | Âge du porteur calculé depuis `dob` |
| `distance_km` | Distance géodésique entre porteur et marchand |
| `trans_hour` | Heure de la transaction |
| `trans_day` | Jour de la transaction |
| `trans_month` | Mois de la transaction |
| `customer_job_category` | Métier regroupé en 16 catégories |

### Modèle

- **Algorithme** : RandomForestClassifier (scikit-learn)
- **Preprocessing** : StandardScaler (numériques) + OneHotEncoder (catégorielles)
- **Gestion du déséquilibre** : `class_weight="balanced"` (~0.58% de fraudes)
- **Métriques loggées** : accuracy, precision, recall, F1, ROC-AUC

---

## API

### `POST /predict`

Retourne la prédiction de fraude pour une transaction.

**Corps de la requête :**
```json
{
  "current_time": "2020-06-21 12:14:25",
  "cc_num": "2703186189652095",
  "trans_num": "abc123",
  "merchant": "fraud_Example Corp",
  "first": "Jane",
  "last": "Doe",
  "street": "123 Main St",
  "zip": "12345",
  "city": "Springfield",
  "category": "misc_net",
  "amt": 149.99,
  "gender": "F",
  "state": "CA",
  "city_pop": 50000,
  "lat": 37.77,
  "long": -122.41,
  "merch_lat": 37.80,
  "merch_long": -122.45,
  "dob": "1985-03-15",
  "job": "Software engineer"
}
```

**Réponse :**
```json
{
  "is_fraud": 0,
  "fraud_probability": 0.0312,
  "inference_ms": 14.5,
  "run_id": "abc123mlflow..."
}
```

### `GET /health`

```json
{ "status": "ok" }
```

---

## Tests

```bash
cd 04_fraud_detection
pip install pytest httpx
pytest services/api/tests/ -v
```

Les tests mockent MLflow — ils tournent sans Docker.

---

## Dashboard Streamlit

Accessible sur [http://localhost:8501](http://localhost:8501)

- **KPIs** : total transactions, fraudes réelles, fraudes détectées, alertes
- **Tableau filtrable** : par catégorie, date, type de fraude
- **Graphiques** : fraudes dans le temps, fraudes par catégorie
- **Performance modèle** : TP/FP/FN/TN, précision, rappel, F1-score

---

## Schéma de la base de données (Supabase)

```
cardholders      ← porteurs de carte
merchants        ← marchands
transactions     ← transactions brutes (avec is_fraud réel)
model_versions   ← runs MLflow utilisés pour les prédictions
predictions      ← prédictions du modèle (fraud_score, is_fraud)
alerts           ← alertes déclenchées sur prédictions positives
```

---

## Exploration des données (EDA)

Les notebooks dans `exploration/` documentent l'analyse du dataset :

- **Déséquilibre des classes** : 99.42% légitime / 0.58% fraude
- **Catégories à risque** : `shopping_net`, `grocery_net`, `misc_net`
- **Pattern temporel** : pic de fraude entre 22h et 4h
- **Profil ciblé** : personnes âgées (65+) légèrement plus exposées
- **Variable la plus corrélée** : `amt` (montant) et `hour` (heure)
