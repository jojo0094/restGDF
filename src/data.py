import restapi
import geopandas as gpd

def get_layer_data(mapserver, layer_name):
    layer = mapserver.layer(layer_name)
    return gpd.GeoDataFrame.from_features(layer.query(where="1=1", outFields="*", returnGeometry=True, f="geojson")["features"], crs="EPSG:4326")

def save_layer_data(mapserver, layer_name, path):
    gdf = get_layer_data(mapserver, layer_name)
    gdf.to_file(path, driver="geopackage")

url = 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'
watermap_sever = restapi.MapService(url)
layers = watermap_sever.list_layers()
for layer in layers:
    print(layer)
    layer_to_add = None


    # layer_to_add = get_layer_data(url, layer)
    layer_to_add = get_layer_data(watermap_sever, layer)


