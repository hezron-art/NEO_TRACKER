import requests
import pandas as pd
from datetime import datetime
from config import NASA_API_KEY, NASA_NEO_URL

def fetch_neo_data(start_date=None, end_date=None):
    if start_date is None:
        start_date = datetime.today().strftime('%Y-%m-%d')
    if end_date is None:
        end_date = start_date

    params = {"start_date": start_date, "end_date": end_date, "api_key": NASA_API_KEY}
    response = requests.get(NASA_NEO_URL, params=params)
    response.raise_for_status()
    data = response.json()

    neo_list = []
    for date, neos in data["near_earth_objects"].items():
        for neo in neos:
            neo_info = {
                "id": neo["id"],
                "name": neo["name"],
                "close_approach_date": date,
                "absolute_magnitude": neo["absolute_magnitude_h"],
                "estimated_diameter_min_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "estimated_diameter_max_km": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "relative_velocity_km_s": float(neo["close_approach_data"][0]["relative_velocity"]["kilometers_per_second"]),
                "miss_distance_km": float(neo["close_approach_data"][0]["miss_distance"]["kilometers"]),
                "orbiting_body": neo["close_approach_data"][0]["orbiting_body"]
            }
            neo_list.append(neo_info)
    df = pd.DataFrame(neo_list)
    return df

def save_to_csv(df, filename="data/neo_daily.csv"):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    df = fetch_neo_data()
    save_to_csv(df)
