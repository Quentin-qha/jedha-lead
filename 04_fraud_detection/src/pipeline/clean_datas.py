import pandas as pd
from geopy.distance import geodesic

def categorize_job(job):
    job = job.lower()
    if any(w in job for w in ["engineer", "developer", "data", "software", "tech", "it", "programmer", "web", "seismic", "geophysic", "statistician", "cartographer"]):
        return "tech"
    elif any(w in job for w in ["health", "ambulance" "doctor", "nurse", "surgeon", "therapist", "medical", "paramedic", "radiograph", "optometrist", "chiropodist", "audiolog", "oncologist", "osteopath", "podiatrist", "pathologist", "immunologist", "physiologist", "toxicologist", "embryologist", "biochemist", "pharmacolog", "psychiatrist", "psychologist", "counsell", "optician", "herbalist", "acupuncturist", "orthoptist", "occupational hygienist", "clinical"]):
        return "health"
    elif any(w in job for w in ["teacher", "professor", "lecturer", "educator", "tutor", "librarian", "archivist", "education", "mentor", "learning"]):
        return "education"
    elif any(w in job for w in ["manager", "director", "officer", "executive", "ceo", "administrator", "coordinator", "comptroller", "company secretary", "chief of staff"]):
        return "management"
    elif any(w in job for w in ["accountant", "financial", "banker", "analyst", "tax", "insurance", "broker", "pensions", "economist", "futures trader", "dealer", "claims inspector", "loss adjuster"]):
        return "finance"
    elif any(w in job for w in ["driver", "delivery", "transport", "pilot", "freight", "air broker", "cabin crew", "air cabin"]):
        return "transport"
    elif any(w in job for w in ["designer", "artist", "musician", "journalist", "media", "broadcast", "photographer", "ceramics", "jewellery", "animator", "illustrator", "producer", "radio producer", "camera operator", "gaffer", "television", "curator", "conservator"]):
        return "creative"
    elif any(w in job for w in ["lawyer", "barrister", "legal", "conveyancer", "loss adjuster", "attorney", "patent", "trade mark"]):
        return "legal"
    elif any(w in job for w in ["scientist", "researcher", "geologist", "ecologist", "geneticist", "geochemist", "hydrogeologist", "archaeologist", "oceanographer", "hydrologist", "chemist", "metallurgist", "mudlogger"]):
        return "science"
    elif any(w in job for w in ["surveyor", "planner", "architect", "contractor", "building", "land"]):
        return "construction"
    elif any(w in job for w in ["consultant", "adviser", "advisor"]):
        return "consulting"
    elif any(w in job for w in ["firefighter", "police", "security", "military", "warden", "ranger"]):
        return "public_safety"
    elif any(w in job for w in ["farmer", "agricultural", "horticulturist", "arboriculturist"]):
        return "agriculture"
    elif any(w in job for w in ["buyer", "merchandiser", "retail", "bookseller", "barista", "dealer"]):
        return "commerce"
    elif any(w in job for w in ["aid worker", "development worker", "volunteer", "charity"]):
        return "social"
    elif any(w in job for w in ["sport", "exercise", "fitness"]):
        return "sport"
    else:
        return "other"

def clean_datas_history(df, call_type="csv"):
    if df.shape[0] > 0:

        # Drop useless columns
        if call_type == "csv":
            drop_cols = ["Unnamed: 0", "cc_num", "merchant", "first", "last", "street", "zip", "unix_time", "trans_num", "city"]

            # Split date time columns in day, month, year, hour
            df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])

            df["trans_hour"]  = df["trans_date_trans_time"].dt.hour
            df["trans_day"]   = df["trans_date_trans_time"].dt.day
            df["trans_month"] = df["trans_date_trans_time"].dt.month
            #df["trans_year"]  = df["trans_date_trans_time"].dt.year #Not keeped because all the date are in 2020

            df = df.drop(columns=["trans_date_trans_time"])
        elif call_type == "api":
            drop_cols = ["cc_num", "trans_num", "merchant", "first", "last", "street", "zip", "trans_num", "city"]

            # Split date time columns in day, month, year, hour
            #df["current_time"] = pd.to_datetime(df["current_time"])

            df["trans_hour"]  = df["current_time"].dt.hour
            df["trans_day"]   = df["current_time"].dt.day
            df["trans_month"] = df["current_time"].dt.month
            #df["trans_year"]  = df["trans_date_trans_time"].dt.year #Not keeped because all the date are in 2020


        df = df.drop(columns=drop_cols)

        #Customer age
        df["dob"] = pd.to_datetime(df["dob"])
        df["age"] = pd.Timestamp.now().year - df["dob"].dt.year

        df = df.drop(columns=["dob"])

        # Distance between merchant and customer (km)
        df["distance_km"] = df.apply(
            lambda row: int(geodesic(
                (row["lat"], row["long"]), 
                (row["merch_lat"], row["merch_long"])
            ).km), axis=1
        )

        drop_loc_cols = ["lat", "long", "merch_lat", "merch_long"]
        df = df.drop(columns=drop_loc_cols)

        

        # Categorise customer jobs
        df["customer_job_category"] = df["job"].apply(categorize_job)
        df = df.drop(columns=["job"])

        return df
    else:
        print("No datas in the dataframe")