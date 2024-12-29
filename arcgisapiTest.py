from arcgis.gis import GIS
from arcgis.features import GeoAccessor, FeatureLayer
import geopandas as gpd

# Specify the Map Service URL
service_url = 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'

# Connect to ArcGIS and access the MapService
gis = GIS()
water_mapserver = FeatureLayer(service_url)

water_mapserver.properties

print(water_mapserver.properties)

# List all layers in the map service
# layers = water_mapserver.layers
# for layer in layers:
#     print(layer.properties.name)
#
# # Access the "Water Valve" layer by name
# valve_layer = None
# for layer in layers:
#     if layer.properties.name == "Water Valve":
#         valve_layer = layer
#         break
#
# # Query all features in the "Water Valve" layer
# if valve_layer:
#     # Query layer and get all features
#     valve_features = valve_layer.query(where="1=1", out_fields="*")
#
#     # Convert to a GeoDataFrame using GeoAccessor
#     gdf = valve_features.sdf  # Spatially enabled DataFrame (Esri's format)
#     gdf = GeoAccessor.to_geodataframe(gdf)  # Convert to GeoPandas GeoDataFrame
#
#     # Display the GeoDataFrame
#     print(gdf.head())
# else:
#     print("Water Valve layer not found.")
#
