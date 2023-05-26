import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

import config

load_dotenv()
pw = os.getenv("SQL_ROOT_PASS")

# Create a MySQL connection
engine = create_engine(f"mysql+mysqlconnector://root:{pw}@localhost:13306/aniRec")

df = pd.read_csv(config.WAREHOUSE_PATH + "/clean_items.csv")
# Convert the DataFrame to a MySQL table
df.to_sql("items", con=engine, if_exists="append", index=False)
