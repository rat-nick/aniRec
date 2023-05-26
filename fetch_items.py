import glob
import os
import time
from multiprocessing import Pool
from urllib.error import HTTPError
from urllib.request import urlopen

URL_BASE = "https://myanimelist.net/anime/"
LAKE_PATH = "data/lake/items"
ids = [i for i in range(100001)]
html_files = glob.glob(LAKE_PATH + "/*.html")
fetched = [int(os.path.splitext(os.path.basename(file))[0]) for file in html_files]
ids = list(set(ids) - set(fetched))


def get_item_page(id):
    try:
        page = urlopen(f"{URL_BASE}/{id}")
        html = page.read().decode("utf-8")
        with open(f"{LAKE_PATH}/{id}.html", "w") as f:
            f.write(html)
    except HTTPError as e:
        print(f"{e.code}\t-\t{id}")
        if e.code == 429:
            time.sleep(20)
            try:
                get_item_page(id)
            except:
                pass


# for id in ids:
#     try:
#         get_item_page(id)
#     except HTTPError as e:
#         print(f"{e.code}\t-\t{id}")
#         if e.code == 429:
#             input()
#             try:
#                 get_item_page(id)
#             except:
#                 pass

if __name__ == "__main__":
    with Pool() as pool:
        pool.map(get_item_page, ids)
