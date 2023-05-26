from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup

URL_BASE = "https://myanimelist.net/profile/"


def scrape_page(page):
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")


df = pd.read_csv("reviews.csv", sep="|", header=0)
user = df.user[0]
url = URL_BASE + user
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())
