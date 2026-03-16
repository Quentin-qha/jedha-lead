import os
import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🔍",
    layout="wide",
)

# --- Connexion ---
def get_conn():
    return psycopg2.connect(os.getenv("SUPABASE_DATABASE_URL"))

@st.cache_data(ttl=60)
def load_data():
    conn = get_conn()
    query = """
        SELECT
            t.id            AS transaction_id,
            t.trans_at,
            t.trans_num,
            t.amt,
            t.is_fraud      AS actual_fraud,
            c.first || ' ' || c.last AS cardholder,
            c.cc_num,
            c.city          AS cardholder_city,
            c.state,
            m.name          AS merchant,
            m.category,
            p.fraud_score,
            p.is_fraud      AS predicted_fraud,
            p.inference_ms,
            a.id IS NOT NULL AS alert_triggered
        FROM transactions t
        JOIN cardholders c  ON c.id = t.cardholder_id
        JOIN merchants m    ON m.id = t.merchant_id
        LEFT JOIN predictions p ON p.transaction_id = t.id
        LEFT JOIN alerts a      ON a.prediction_id = p.id
        ORDER BY t.trans_at DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df["trans_at"] = pd.to_datetime(df["trans_at"])
    return df

# --- Header ---
st.title("🔍 Fraud Detection Dashboard")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

if st.button("🔄 Rafraîchir"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df.empty:
    st.warning("Aucune donnée disponible.")
    st.stop()

# --- KPIs ---
total       = len(df)
fraud_actual   = df["actual_fraud"].sum()
fraud_predicted = df["predicted_fraud"].sum() if "predicted_fraud" in df.columns else 0
alerts_count   = df["alert_triggered"].sum()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total transactions", total)
col2.metric("Fraudes réelles", int(fraud_actual), f"{fraud_actual/total*100:.1f}%")
col3.metric("Non-fraudes", int(total - fraud_actual), f"{(total-fraud_actual)/total*100:.1f}%")
col4.metric("Détectées par le modèle", int(fraud_predicted))
col5.metric("Alertes déclenchées", int(alerts_count))

st.divider()

# --- Filtres ---
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    show_only_fraud = st.checkbox("Afficher uniquement les fraudes réelles", value=True)
with col_f2:
    categories = ["Toutes"] + sorted(df["category"].dropna().unique().tolist())
    selected_cat = st.selectbox("Catégorie marchande", categories)
with col_f3:
    date_range = st.date_input(
        "Période",
        value=(df["trans_at"].min().date(), df["trans_at"].max().date()),
        max_value=datetime.today().date(),
    )

# Application des filtres
df_filtered = df.copy()
if show_only_fraud:
    df_filtered = df_filtered[df_filtered["actual_fraud"] == True]
if selected_cat != "Toutes":
    df_filtered = df_filtered[df_filtered["category"] == selected_cat]
if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered["trans_at"].dt.date >= date_range[0]) &
        (df_filtered["trans_at"].dt.date <= date_range[1])
    ]

st.divider()

# --- Tableau des transactions frauduleuses ---
st.subheader("📋 Transactions à examiner")
st.caption(f"{len(df_filtered)} transaction(s) affichée(s)")

display_cols = {
    "trans_at"       : "Date",
    "cardholder"     : "Titulaire",
    "cc_num"         : "N° carte",
    "merchant"       : "Marchand",
    "category"       : "Catégorie",
    "amt"            : "Montant ($)",
    "fraud_score"    : "Score fraude",
    "predicted_fraud": "Détecté modèle",
    "actual_fraud"   : "Fraude réelle",
    "alert_triggered": "Alerte",
}

df_display = df_filtered[list(display_cols.keys())].rename(columns=display_cols).copy()
df_display["Score fraude"] = df_display["Score fraude"].apply(
    lambda x: f"{x:.2%}" if pd.notna(x) else "-"
)

def highlight_fraud(row):
    if row["Fraude réelle"] and not row["Détecté modèle"]:
        return ["background-color: #ff4b4b22"] * len(row)  # manquée
    if row["Fraude réelle"] and row["Détecté modèle"]:
        return ["background-color: #ffa50022"] * len(row)  # détectée
    return [""] * len(row)

st.dataframe(
    df_display.style.apply(highlight_fraud, axis=1),
    use_container_width=True,
    height=400,
)
st.caption("🟠 Fraude détectée par le modèle  |  🔴 Fraude manquée par le modèle")

st.divider()

# --- Graphiques ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📈 Fraudes dans le temps")
    df_time = df.copy()
    df_time["date"] = df_time["trans_at"].dt.date
    df_time_grouped = (
        df_time.groupby("date")
        .agg(total=("transaction_id", "count"), fraudes=("actual_fraud", "sum"))
        .reset_index()
    )
    fig_time = go.Figure()
    fig_time.add_bar(x=df_time_grouped["date"], y=df_time_grouped["total"], name="Total", marker_color="#636EFA")
    fig_time.add_bar(x=df_time_grouped["date"], y=df_time_grouped["fraudes"], name="Fraudes", marker_color="#EF553B")
    fig_time.update_layout(barmode="overlay", xaxis_title="Date", yaxis_title="Nb transactions", height=300)
    st.plotly_chart(fig_time, use_container_width=True)

with col_g2:
    st.subheader("🏷️ Fraudes par catégorie")
    df_cat = (
        df[df["actual_fraud"] == True]
        .groupby("category")
        .size()
        .reset_index(name="fraudes")
        .sort_values("fraudes", ascending=True)
    )
    fig_cat = px.bar(df_cat, x="fraudes", y="category", orientation="h", height=300)
    st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# --- Performance du modèle ---
st.subheader("🤖 Performance du modèle")

df_perf = df.dropna(subset=["predicted_fraud", "actual_fraud"])
if not df_perf.empty:
    tp = int(((df_perf["actual_fraud"] == True)  & (df_perf["predicted_fraud"] == True)).sum())
    fp = int(((df_perf["actual_fraud"] == False) & (df_perf["predicted_fraud"] == True)).sum())
    fn = int(((df_perf["actual_fraud"] == True)  & (df_perf["predicted_fraud"] == False)).sum())
    tn = int(((df_perf["actual_fraud"] == False) & (df_perf["predicted_fraud"] == False)).sum())

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    col_p1.metric("Vrais positifs (TP)", tp, help="Fraude réelle, détectée")
    col_p2.metric("Faux négatifs (FN)", fn, help="Fraude réelle, manquée ⚠️", delta=-fn, delta_color="inverse")
    col_p3.metric("Faux positifs (FP)", fp, help="Non-fraude, détectée à tort")
    col_p4.metric("Vrais négatifs (TN)", tn, help="Non-fraude, correctement ignorée")

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Précision", f"{precision:.1%}")
    col_m2.metric("Rappel",    f"{recall:.1%}")
    col_m3.metric("F1-Score",  f"{f1:.1%}")
else:
    st.info("Pas encore assez de données pour évaluer la performance.")
