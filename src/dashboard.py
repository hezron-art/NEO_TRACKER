import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from config import DB_PATH

st.title("Near-Earth Object (NEO) Tracker Dashboard")

engine = create_engine(f"sqlite:///{DB_PATH}")
df = pd.read_sql("SELECT * FROM neo_data", con=engine)

st.sidebar.header("Filters")
min_risk = st.sidebar.slider("Minimum Risk Score", 0.0, float(df["risk_score"].max()), 0.0)
max_risk = st.sidebar.slider("Maximum Risk Score", 0.0, float(df["risk_score"].max()), float(df["risk_score"].max()))

filtered_df = df[(df["risk_score"] >= min_risk) & (df["risk_score"] <= max_risk)]
st.subheader("Filtered NEO Data")
st.dataframe(filtered_df)

st.subheader("Risk Score vs Miss Distance (km)")
plt.figure(figsize=(10,5))
sns.scatterplot(data=filtered_df, x="miss_distance_km", y="risk_score",
                hue="max_diameter_km", palette="viridis", size="max_diameter_km", sizes=(20,200))
plt.xlabel("Miss Distance (km)")
plt.ylabel("Risk Score")
plt.title("NEO Risk vs Proximity")
st.pyplot(plt)

st.subheader("Summary Statistics")
st.write(filtered_df.describe())
