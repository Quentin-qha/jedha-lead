import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

def process_and_store(raw, prediction, model_version_id):
    supabase = psycopg2.connect(os.getenv("SUPABASE_DATABASE_URL"))
    cur = supabase.cursor()
    
    # --- Mapping ---
    cardholder_data = {
        'cc_num'  : raw['cc_num'],
        'first'   : raw['first'],
        'last'    : raw['last'],
        'gender'  : raw['gender'],
        'dob'     : raw['dob'],
        'job'     : raw['job'],
        'street'  : raw['street'],
        'city'    : raw['city'],
        'state'   : raw['state'],
        'zip'     : raw['zip'],
        'lat'     : raw['lat'],
        'long'    : raw['long'],
        'city_pop': raw['city_pop'],
    }

    merchant_data = {
        'name'    : raw['merchant'],
        'category': raw['category'],
        'lat'     : raw['merch_lat'],
        'long'    : raw['merch_long'],
    }

    transaction_data = {
        'trans_num': raw['trans_num'],
        'amt'      : raw['amt'],
        'trans_at' : datetime.fromtimestamp(raw['current_time'] / 1000).isoformat(),
        'is_fraud' : bool(raw['is_fraud']),
    }

    # --- Envoi ---
    cur.execute("""
        INSERT INTO cardholders (cc_num, first, last, gender, dob, job, street, city, state, zip, lat, long, city_pop)
        VALUES (%(cc_num)s, %(first)s, %(last)s, %(gender)s, %(dob)s, %(job)s, %(street)s, %(city)s, %(state)s, %(zip)s, %(lat)s, %(long)s, %(city_pop)s)
        ON CONFLICT (cc_num) DO UPDATE SET
            first = EXCLUDED.first, last = EXCLUDED.last, gender = EXCLUDED.gender,
            dob = EXCLUDED.dob, job = EXCLUDED.job, street = EXCLUDED.street,
            city = EXCLUDED.city, state = EXCLUDED.state, zip = EXCLUDED.zip,
            lat = EXCLUDED.lat, long = EXCLUDED.long, city_pop = EXCLUDED.city_pop
        RETURNING id
    """, cardholder_data)
    cardholder_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO merchants (name, category, lat, long)
        VALUES (%(name)s, %(category)s, %(lat)s, %(long)s)
        ON CONFLICT (name) DO UPDATE SET
            category = EXCLUDED.category, lat = EXCLUDED.lat, long = EXCLUDED.long
        RETURNING id
    """, merchant_data)
    merchant_id = cur.fetchone()[0]

    transaction_data['cardholder_id'] = cardholder_id
    transaction_data['merchant_id']   = merchant_id

    cur.execute("""
        INSERT INTO transactions (trans_num, amt, trans_at, is_fraud, cardholder_id, merchant_id)
        VALUES (%(trans_num)s, %(amt)s, %(trans_at)s, %(is_fraud)s, %(cardholder_id)s, %(merchant_id)s)
        RETURNING id
    """, transaction_data)
    transaction_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO model_versions (id, mlflow_run_id, model_name, version, is_active, deployed_at)
        VALUES (%s::uuid, %s, 'fraud_detection', %s, true, NOW())
        ON CONFLICT (id) DO NOTHING
    """, (model_version_id, model_version_id, model_version_id))

    cur.execute("""
        INSERT INTO predictions (transaction_id, model_version_id, fraud_score, is_fraud, threshold_used, inference_ms)
        VALUES (%s, %s::uuid, %s, %s, %s, %s)
        RETURNING id
    """, (
        transaction_id,
        model_version_id,
        float(prediction['fraud_probability']),
        bool(prediction['is_fraud']),
        0.5,
        prediction['inference_ms'],
    ))
    prediction_id = cur.fetchone()[0]

    if prediction['is_fraud']:
        cur.execute("INSERT INTO alerts (prediction_id) VALUES (%s)", (prediction_id,))

    supabase.commit()
    cur.close()
    supabase.close()