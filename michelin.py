import time
import mechanicalsoup
import pandas as pd
from typing import Dict, Any

browser = mechanicalsoup.StatefulBrowser()

URL_ROOT = "https://guide.michelin.com"
URL_PAGES = f"{URL_ROOT}/fr/fr/restaurants/restaurants-etoiles/page"


def extract_restaurants_etoiles() -> Dict[str, Dict[str, Any]]:
    data = {}

    browser.open(f"{URL_ROOT}/fr/fr/restaurants/restaurants-etoiles")

    pagination = browser.page.select_one(".js-restaurant__bottom-pagination")
    pages = [
    int(a.text)
    for a in pagination.find_all("a")
    if a.text.strip().isdigit()
]

    last_page = max(pages)

    for page in range(1, last_page + 1):
        browser.open(f"{URL_PAGES}/{page}")
        cards = browser.page.select(".col-md-6.col-lg-4.col-xl-3")

        for card in cards:
            bloc = card.select_one(".js-restaurant__list_item")
            if not bloc:
                continue

            restaurant_id = bloc.get("data-id")

            lien_fr = URL_ROOT + card.find("a", href=True)["href"]

            restaurant = {
                "nom": card.find("h3").get_text(strip=True),
                "localisation": card.select_one(".card__menu-footer--score").get_text(strip=True),
                "lat": bloc.get("data-lat"),
                "lng": bloc.get("data-lng"),
                "etoiles": bloc.get("data-map-pin-name"),
                "lien_michelin": lien_fr,
                "telephone": None,
                "site_web": None,
            }

            browser.open(lien_fr)

            infos = browser.page.select("div.d-flex")
            for div in infos:
                text = div.get_text(strip=True)
                if text.startswith("+"):
                    restaurant["telephone"] = text
                link = div.find("a", href=True)
                if link and "http" in link["href"]:
                    restaurant["site_web"] = link["href"]

            data[restaurant_id] = restaurant
            time.sleep(0.5)  # respect du site

    return data


def main():
    data = extract_restaurants_etoiles()
    df = pd.DataFrame.from_dict(data, orient="index")
    df.to_excel("export.xlsx", index_label="id")


if __name__ == "__main__":
    main()
