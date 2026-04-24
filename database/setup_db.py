import pandas as pd
import sqlalchemy as db
import os

def setup_database():
    # Create DB
    engine = db.create_engine('sqlite:///database/insightedge.db')
    
    # Load CSV
    df = pd.read_csv('data/sales_data.csv')
    
    # Push to SQL
    df.to_sql('sales', engine, if_exists='replace', index=False)
    print("✅ Database created with 'sales' table")
    
    # Verify
    with engine.connect() as conn:
        result = conn.execute(db.text("SELECT COUNT(*) FROM sales"))
        print(f"✅ Total records in DB: {result.fetchone()[0]}")
        
        result = conn.execute(db.text("SELECT * FROM sales LIMIT 3"))
        for row in result:
            print(row)

if __name__ == '__main__':
    setup_database()