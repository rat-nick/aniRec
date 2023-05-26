import pandas as pd
from sqlalchemy import create_engine

import config


class DataAccessLayer:
    def __init__(self):
        self.df = pd.read_csv(config.WAREHOUSE_PATH + "/clean_items.csv")

    def search(self, term):
        df = self.df
        mask = df.applymap(lambda x: term in str(x).lower())
        return df[mask.any(axis=1)]

    def get_info(self, itemID):
        return self.df.loc[itemID]
