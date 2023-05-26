import csv
from urllib.request import urlopen

from bs4 import BeautifulSoup

URL_BASE = "https://myanimelist.net/reviews.php?t=anime&filter_check=&filter_hide=&preliminary=off&spoiler=off&p="


def scrape_page(page):
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    reviews = soup.select(".review-element")
    items = []
    i = 0
    for rv in reviews:
        items.append({})
        items[i]["item"] = rv.select_one(".title").text
        items[i]["item-link"] = rv.select_one(".title", href=True)["href"]
        items[i]["date"] = rv.select_one(".update_at").text
        items[i]["username"] = rv.select_one(".username").text.strip()
        items[i]["rating"] = rv.select_one(".num").text
        i += 1
    return items


for page in range(1, 1000000):
    url = URL_BASE + str(page)
    page = urlopen(url)
    results = scrape_page(page)
    with open("reviews.csv", "a+", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys(), delimiter="|")
        writer.writerows(results)
