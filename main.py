# oi, dis the main file, innit?

import geopandas as gpd

gdf = gpd.read_file("/home/kamal/Desktop/UIDAI-Hackathon-2026/data/external/INDIA_DISTRICTS.geojson")
print(len(gdf))
mid = len(gdf) // 2

gdf_1 = gdf.iloc[:mid]
gdf_2 = gdf.iloc[mid:]

gdf_1.to_file("/home/kamal/Desktop/UIDAI-Hackathon-2026/data/external/INDIA_DISTRICTS_0.geojson", driver="GeoJSON")
gdf_2.to_file("/home/kamal/Desktop/UIDAI-Hackathon-2026/data/external/INDIA_DISTRICTS_1.geojson", driver="GeoJSON")
