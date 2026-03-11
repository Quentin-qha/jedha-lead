import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv())
load_dotenv()

def supabase_conn():
    url = os.getenv("SUPABASE_DATABASE_URL")
    if not url:
        raise RuntimeError("SUPABASE_DATABASE_URL is not set")
    print("Connected")
    return psycopg2.connect(url)
