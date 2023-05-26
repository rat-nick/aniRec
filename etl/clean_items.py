import pandas as pd

import config


def remove_blanks(col):
    return col.str.replace(" ", "")


def remove_double_words(s):
    words = s.split(",")
    half = lambda x: x[: len(x) // 2]
    return ",".join(map(half, words))


def categorical2onehot(
    column,
    prefix,
    rmd=True,
):
    column = remove_blanks(column)
    column.fillna("", inplace=True)
    if rmd:
        column = column.apply(remove_double_words)
    one_hot_encoded = (
        column.str.get_dummies(",").astype("int8").add_prefix(prefix, axis=1)
    )
    return one_hot_encoded


def transform(col, functions):
    for f in functions:
        try:
            col = f(col)
        except:
            col = col.apply(f)
    return col


df = pd.read_csv(config.WAREHOUSE_PATH + "/items.csv")

df = df.drop(columns="Unnamed: 0")
df = df.rename({"id": "malID"}, axis=1)
df.reset_index(inplace=True)
df = df.drop(columns="genre")
df.genres.fillna("", inplace=True)
df.genres = transform(
    df.genres,
    [
        remove_blanks,
        remove_double_words,
    ],
)
df = df.drop(columns="theme")
df.themes.fillna("", inplace=True)
df.themes = transform(
    df.themes,
    [
        remove_blanks,
        remove_double_words,
    ],
)
df = df.drop(columns="demographics")
df.demographic.fillna("", inplace=True)
df.demographic = transform(
    df.demographic,
    [
        remove_blanks,
        remove_double_words,
    ],
)

df.studios.replace(r"none found.*", "", inplace=True, regex=True)
df.producers.replace(r"none found.*", "", inplace=True, regex=True)
df.synopsis.replace(r"^No synopsis.*", "", inplace=True, regex=True)
df.synopsis.replace(r"\n", "", inplace=True, regex=True)

df["aired"] = df["aired"].str.replace("not available", "None")
df[["start", "end"]] = df["aired"].str.split(" to ", expand=True)
df["start"] = pd.to_datetime(df["start"], errors="coerce")
df["end"] = pd.to_datetime(df["end"], errors="coerce")
df["season"] = df["premiered"].str.extract(r"(fall|winter|spring|summer)")
df["start"] = df["start"].astype("datetime64[ns]")
df["end"] = df["end"].astype("datetime64[ns]")
df["favorites"] = df["favorites"].str.replace(",", "").astype("int")
df["members"] = df["members"].str.replace(",", "").astype("int")
df["popularity"] = df["popularity"].str.replace("#", "").astype("int")
df.to_csv(config.WAREHOUSE_PATH + "/clean_items.csv")
