import pandas as pd

from extract import extract_itemID

df = pd.read_csv("data/lake/reviews.csv", header=0, sep="|")
df["itemID"] = extract_itemID(df["itemLink"])
df = df.drop("itemLink", axis=1)
df.to_csv("data/warehouse/reviews.csv", index=False, sep="|")
