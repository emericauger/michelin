import mechanicalsoup
import pandas as pd
browser = mechanicalsoup.StatefulBrowser()

url_racine = "https://guide.michelin.com/fr/fr/restaurants/restaurants-etoiles/page/"
div_racine = 'col-md-6 col-lg-4 col-xl-3'
div_enfant = 'card__menu selection-card box-placeholder js-restaurant__list_item js-match-height js-map'



def extract_restaurants_etoiles():
    data = {}

    # Extraction de la longueur de la pagination

    browser.open('https://guide.michelin.com/fr/fr/restaurants/restaurants/restaurants-etoiles')
    # Sale ...
    div_pagination_last = int(browser.page.find_all('div', class_ = 'js-restaurant__bottom-pagination')[0].contents[1].contents[-1].previous)

    # Boucle pricipale

    for p in range(1, div_pagination_last + 1):
        browser.open(f"{url_racine}/{p}")
        divs_racine = browser.page.find_all('div', class_ = div_racine)
        for d in divs_racine:
            cle = d.find_all('div', class_= div_enfant)[0]['data-id']
            lat = d.find_all('div', class_= div_enfant)[0]['data-lat']
            lng = d.find_all('div', class_= div_enfant)[0]['data-lng']
            etoiles = d.find_all('div', class_= div_enfant)[0]['data-map-pin-name']
            localisation = d.find_all('div', class_='card__menu-footer--score pl-text')[0].get_text().strip()
            nom = d.find_all('h3')[0].get_text().strip()
            
            # Extraction du lien interne FR
            lien_fr_suffix = d.find_all('a', href=True, text=True)[0]['href']
            lien_fr = f'https://guide.michelin.com' + lien_fr_suffix
            
            # Extraction des informations du restaurant par accès à la page du restaurant
            browser.open(lien_fr)
            try: 
                tel = browser.page.find_all('div', class_ =  'd-flex')[2].text.strip()
            except:
                tel = None

            try:
                lien_ext_next_elements = browser.page.find_all('div', class_ =  'd-flex')[4].next_elements
                lien_ext = [l for l in lien_ext_next_elements][6]['href']
            except:
                lien_ext = None

            data[cle] = (nom, localisation,lat, lng, etoiles, lien_fr, tel, lien_ext)
        
    return data



def main():
    data = extract_restaurants_etoiles()
    df = pd.DataFrame.from_dict(data, orient = 'index')
    df.to_excel('./export.xlsx')    

if __name__ == '__main__':
    main()



