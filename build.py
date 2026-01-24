#!/usr/bin/env python3
"""
Build script: extracts Michelin restaurant data and generates data.js
Pipeline: scrape → export.xlsx → export.geojson → front/data.js
"""

import json
import sys
import geopandas as gpd
import pandas as pd
from scraper import extract_restaurants_etoiles


def build():
    """Complete build pipeline."""
    try:
        # Step 1: Scrape data
        print("Step 1: Scraping Michelin data...")
        data = extract_restaurants_etoiles(verbose=False)
        
        # Step 2: Convert to Excel
        print(f"Step 2: Converting to Excel ({len(data)} restaurants)...")
        df = pd.DataFrame.from_dict(data, orient="index")
        df.to_excel("export.xlsx", index_label="id")
        
        # Step 3: Convert to GeoJSON
        print("Step 3: Converting to GeoJSON...")
        df = pd.read_excel("export.xlsx")
        df = df.rename(columns={"lng": "lon"})
        df["lat"] = df["lat"].astype(float)
        df["lon"] = df["lon"].astype(float)
        df = df.dropna(subset=["lat", "lon"])
        
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326"
        )
        gdf.to_file("export.geojson", driver="GeoJSON")
        
        # Step 4: Convert GeoJSON to JavaScript
        print("Step 4: Generating data.js...")
        with open("export.geojson", "r") as f:
            geojson_data = json.load(f)
        
        js_content = "restaurants=" + json.dumps(geojson_data, indent=0, ensure_ascii=False)
        
        with open("front/data.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        
        print(f"✓ Build complete! Generated front/data.js with {len(geojson_data['features'])} restaurants")
        
    except Exception as e:
        print(f"✗ Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    build()
