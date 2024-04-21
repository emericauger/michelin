import geopandas as gpd
import pandas as pd
data = pd.read_excel("export.xlsx")
data.columns = ["id", "nom", "localisation", "lat", "lon", "etoiles", "url_interne", "tel", "url_externe"]

gdf = gpd.GeoDataFrame(data, crs = 4326, geometry = gpd.points_from_xy(x = data['lon'], y= data["lat"]))
gdf.to_file("export.geojson", driver="GeoJSON")
