import os
os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'
os.environ['RESTAPI_VERIFY_CERT'] = 'FALSE'

# now import restapi
import restapi

# connect to esri's sample server 6
rest_url = 'https://maps.hamilton.govt.nz/server/rest/services'

# connect to restapi.ArcServer instance 
# ags = restapi.ArcServer(rest_url)
#
# print(ags.featureServices)


water_mapserver = restapi.MapService(url='https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer')


print(water_mapserver.list_layers())

# valve = water_mapserver.getLayerIdByName("Water Valve")
#
# print(valve)
# print(type(valve))

#
valve=water_mapserver.layer("Water Valve")

#query all features and fields

# print(valve.query(where="1=1", outFields="*", returnGeometry=True, f="geojson"))

#transform the geojson to geodataframe
import geopandas as gpd
gdf = gpd.GeoDataFrame.from_features(valve.query(where="1=1", outFields="*", returnGeometry=True, f="geojson")["features"], crs="EPSG:4326")
print(gdf)


#write a fucntion taht accpet mapsercies and layer name and return a geodataframe
def get_layer_data(mapserver, layer_name):
    layer = mapserver.layer(layer_name)
    return gpd.GeoDataFrame.from_features(layer.query(where="1=1", outFields="*", returnGeometry=True, f="geojson")["features"], crs="EPSG:4326")

# print(valve)
#
# print(type(valve.json))
# #
# import pandas as pd
#
# df = pd.DataFrame.from_dict(valve)

