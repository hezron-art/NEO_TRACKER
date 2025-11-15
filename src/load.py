import pandas as pd
from sqlalchemy import create_engine
from config import DB_PATH

def load_csv_to_db(csv_file="data/neo_transformed.csv"):
    df = pd.read_csv(csv_file)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("neo_data", con=engine, if_exists="replace", index=False)
    print(f"Data loaded into database: {DB_PATH} (table: neo_data)")

def test_query():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_sql("SELECT * FROM neo_data LIMIT 5", con=engine)
    print(df)

if __name__ == "__main__":
    load_csv_to_db()
    test_query()
