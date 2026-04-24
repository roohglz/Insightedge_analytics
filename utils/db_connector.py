import sqlalchemy as db
import pandas as pd

def get_engine():
    return db.create_engine('sqlite:///database/insightedge.db')

def run_query(query):
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(db.text(query), conn)