import geopandas as gpd
import pandas as pd

# Lecture du fichier Excel
df = pd.read_excel("export.xlsx")

# Renommage sûr des colonnes
df = df.rename(
    columns={
        "lng": "lon",
    }
)

# Cast explicite
df["lat"] = df["lat"].astype(float)
df["lon"] = df["lon"].astype(float)

# Suppression des lignes invalides
df = df.dropna(subset=["lat", "lon"])

# Création du GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326"
)

# Export GeoJSON
gdf.to_file("export.geojson", driver="GeoJSON")
