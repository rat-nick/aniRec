import glob
import random
from multiprocessing import Pool

import pandas as pd
from bs4 import BeautifulSoup

LAKE_PATH = "data/lake/items"
WAREHOUSE_PATH = "data/warehouse"


def extract_item_info(html) -> dict:
    data = {}
    soup = BeautifulSoup(html, "html.parser")
    data["title"] = soup.find("h1", {"class": "title-name"}).text
    data["synopsis"] = soup.find("p", {"itemprop": "description"}).text
    data["poster_url"] = soup.find("img", {"itemprop": "image"})
    if data["poster_url"] != None:
        data["poster_url"] = data["poster_url"]["data-src"]
    info = soup.find_all("div", {"class": "spaceit_pad"})

    for i in info:
        element = i.find("span", {"class": "dark_text"})

        if element == None:
            continue

        tag = element.text.lower().replace(":", "")

        txt = i.text.replace("\n", "")
        txt = txt.split(":")
        txt[0] = txt[0].lower()
        data[txt[0]] = txt[1].lower()

    sequel = soup.find(lambda tag: tag.name == "td" and tag.text == "Sequel:")
    if sequel != None:
        sequel = sequel.next.next.find("a").get("href")
        sequel_id = sequel.split("/")[2]
        data["sequel_id"] = sequel_id

    prequel = soup.find(lambda tag: tag.name == "td" and tag.text == "Prequel:")
    if prequel != None:
        prequel = prequel.next.next.find("a").get("href")
        prequel_id = prequel.split("/")[2]
        data["prequel_id"] = prequel_id

    return data


def extract(page):
    with open(page, "r") as f:
        data = extract_item_info(f)
        id = int(page.split("/")[3].split(".")[0])
        data["id"] = id
    return data


if __name__ == "__main__":

    pages = glob.glob(f"{LAKE_PATH}/*.html")
    # pages = random.sample(pages, 200)
    with Pool() as pool:
        results = pool.map(extract, pages)
    df = pd.DataFrame(results)
    df.to_csv(f"{WAREHOUSE_PATH}/items.csv")
