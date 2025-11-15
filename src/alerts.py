import smtplib
from email.message import EmailMessage
import pandas as pd
from sqlalchemy import create_engine
from config import DB_PATH, EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL, RISK_THRESHOLD

def load_neo_data():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM neo_data", con=engine)
    return df

def check_high_risk(df):
    return df[df["risk_score"] >= RISK_THRESHOLD]

def send_email_alert(df):
    if df.empty:
        print("No high-risk NEOs today.")
        return
    msg = EmailMessage()
    msg["Subject"] = "High-Risk Near-Earth Object Alert!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    content = "High-Risk NEOs:\n\n"
    content += df[["name", "close_approach_date", "miss_distance_km", "risk_score",
                   "relative_velocity_km_s", "max_diameter_km", "orbiting_body"]].to_string(index=False)
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Email sent to {TO_EMAIL}")

if __name__ == "__main__":
    df = load_neo_data()
    high_risk = check_high_risk(df)
    send_email_alert(high_risk)
