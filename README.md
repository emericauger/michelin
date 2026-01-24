Scraping des informations des restaurants étoilés Michelin. Les données sont récupérées du site guide.michelin.com.

Déployé sur https://restos-etoiles.surge.sh

## Build

Pour regénérer les données (scrape → GeoJSON → JavaScript) :

```bash
npm run build
```

Cela exécute l'ensemble du pipeline en une seule commande :
1. Scrape le site Michelin
2. Génère `export.xlsx`
3. Convertit en `export.geojson`
4. Génère `front/data.js` automatiquement

Vous pouvez aussi exécuter les étapes individuellement :
- `npm run scrape` – Scrape seulement
- `npm run geojson` – Excel → GeoJSON seulement

## Décharge

Les données récupérées sont la propriété de Michelin. Le but de ce dépôt est éducatif. 


