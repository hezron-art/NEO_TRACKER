import pandas as pd

def load_csv(filename="data/neo_daily.csv"):
    df = pd.read_csv(filename)
    print(f"Loaded {len(df)} records from {filename}")
    return df

def clean_data(df):
    df = df.dropna().drop_duplicates()
    return df

def calculate_risk_score(df):
    df["max_diameter_km"] = df["estimated_diameter_max_km"]
    df["risk_score"] = df["max_diameter_km"] / df["miss_distance_km"]
    return df

def save_transformed(df, filename="data/neo_transformed.csv"):
    df.to_csv(filename, index=False)
    print(f"Transformed data saved to {filename}")

if __name__ == "__main__":
    df = load_csv()
    df = clean_data(df)
    df = calculate_risk_score(df)
    save_transformed(df)
