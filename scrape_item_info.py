from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

URL_BASE = "https://myanimelist.net/anime/"

ids = [i for i in range(100001)]


def scrape_item_info(itemIDs: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame()
    for id in itemIDs:
        url = URL_BASE + str(id)
        page = urlopen(url)
        item_info = extract_item_info(page)
        df.append(item_info)
    return df


def extract_item_info(page) -> dict:
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


if __name__ == "__main__":
    data = pd.read_csv("data/warehouse/reviews.csv", sep="|")
    df = scrape_item_info(data["itemID"])
    print(df)
