"""Michelin restaurants scraper module."""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from typing import Dict, Any

URL_ROOT = "https://guide.michelin.com"
URL_PAGES = f"{URL_ROOT}/fr/fr/restaurants/page"


def extract_restaurants_etoiles(verbose: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Scrape starred restaurants from Michelin guide.
    
    Args:
        verbose: Print restaurant info during scraping if True
        
    Returns:
        Dictionary of restaurants indexed by ID
    """
    data = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Charge la première page pour obtenir la pagination
        page.goto(f"{URL_ROOT}/fr/fr/restaurants")
        page.wait_for_selector(".js-restaurant__bottom-pagination", timeout=10000)
        
        # Parse avec BeautifulSoup
        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        pagination = soup.select_one(".js-restaurant__bottom-pagination")
        
        if pagination is None:
            print("❌ Pagination non trouvée même avec Playwright")
            browser.close()
            return data
        
        pages = [int(a.text) for a in pagination.find_all("a") if a.text.strip().isdigit()]
        last_page = max(pages) if pages else 1
        
        if verbose:
            print(f"📄 Total: {last_page} pages")
        
        for page_num in range(1, last_page + 1):
            if verbose:
                print(f"Scraping page {page_num}/{last_page}...")
            
            page.goto(f"{URL_PAGES}/{page_num}")
            page.wait_for_selector(".col-md-6.col-lg-4.col-xl-3", timeout=5000)
            
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            cards = soup.select(".col-md-6.col-lg-4.col-xl-3")
            
            if verbose:
                print(f"  → {len(cards)} restaurants trouvés")

            for card in cards:
                bloc = card.select_one(".js-restaurant__list_item")
                if not bloc:
                    continue

                restaurant_id = bloc.get("data-id")

                lien_element = card.find("a", href=True)
                if not lien_element:
                    continue
                    
                lien_fr = URL_ROOT + lien_element["href"]

                nom_elem = card.find("h3")
                localisation_elem = card.select_one(".card__menu-footer--score")
                
                if not nom_elem or not localisation_elem:
                    continue

                restaurant = {
                    "nom": nom_elem.get_text(strip=True),
                    "localisation": localisation_elem.get_text(strip=True),
                    "lat": bloc.get("data-lat"),
                    "lng": bloc.get("data-lng"),
                    "etoiles": bloc.get("data-map-pin-name"),
                    "lien_michelin": lien_fr,
                    "telephone": None,
                    "site_web": None,
                }
                
                # Visite la page du restaurant
                page.goto(lien_fr)
                page.wait_for_load_state("networkidle")
                
                resto_html = page.content()
                resto_soup = BeautifulSoup(resto_html, 'html.parser')
                infos = resto_soup.select_one("div.filter-bar__container")

                if infos:
                    for a in infos.select("a[href]"):
                        href = a["href"]

                        if href.startswith("http"):
                            restaurant["site_web"] = href

                        elif href.startswith("tel:"):
                            restaurant["telephone"] = href.replace("tel:", "")

                if verbose:
                    print(f"  ✓ {restaurant['nom']}")
                data[restaurant_id] = restaurant
        
        browser.close()

    return data
