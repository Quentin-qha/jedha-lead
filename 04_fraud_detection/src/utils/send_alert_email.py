import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_fraud_alert(transaction: dict, prediction: dict):
    smtp_host     = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port     = int(os.getenv("SMTP_PORT", "587"))
    smtp_user     = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_to      = os.getenv("ALERT_EMAIL_TO")

    if not all([smtp_user, smtp_password, alert_to]):
        print("Email alert skipped: SMTP_USER, SMTP_PASSWORD or ALERT_EMAIL_TO not set")
        return

    subject = f"🚨 Fraude détectée — Transaction {transaction['trans_num']}"

    body = f"""
Une transaction frauduleuse a été détectée par le modèle.

— Détails de la transaction —
Numéro        : {transaction['trans_num']}
Montant       : ${transaction['amt']}
Titulaire     : {transaction['first']} {transaction['last']}
Marchand      : {transaction['merchant']}
Catégorie     : {transaction['category']}

— Prédiction du modèle —
Score de fraude   : {prediction['fraud_probability']:.2%}
Décision          : FRAUDE
Temps d'inférence : {prediction['inference_ms']} ms
Run MLflow        : {prediction['run_id']}
"""

    msg = MIMEMultipart()
    msg["From"]    = smtp_user
    msg["To"]      = alert_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, alert_to, msg.as_string())

    print(f"Alert email sent to {alert_to} for transaction {transaction['trans_num']}")
