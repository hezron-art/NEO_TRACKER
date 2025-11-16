import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from config import DB_PATH

st.set_page_config(page_title="NEO Tracker Dashboard", layout="wide")

# ---------------------------------------------------------
# Load Data Safely (SQLite + pandas)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM neo_data", conn)
    conn.close()
    return df

df = load_data()

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.title("🪐 NEO Tracker Dashboard")
st.write("Real-time analytics for Near-Earth Objects")

st.subheader("Dataset Overview")
st.dataframe(df.head())

# ---------------------------------------------------------
# Visualization
# ---------------------------------------------------------
st.subheader("NEO Magnitude Distribution")

fig, ax = plt.subplots()
sns.histplot(df["absolute_magnitude"], ax=ax)
st.pyplot(fig)

# ---------------------------------------------------------
# Filtering
# ---------------------------------------------------------
st.subheader("Filter by Hazardous Status")

status = st.selectbox("Select Hazardous Flag:", df["is_hazardous"].unique())
filtered_df = df[df["is_hazardous"] == status]

st.dataframe(filtered_df)
