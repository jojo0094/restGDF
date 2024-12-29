import requests
import geopandas as gpd
from shapely.geometry import shape

# Define the Map Service URL and the layer endpoint
base_url = "https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer"
layer_name = "Water Valve"  # Layer name to query
layer_url = f"{base_url}/layers"  # Append layer endpoint

# Get layer list and find "Water Valve" layer ID
response = requests.get(layer_url, params={"f": "json"})
layers = response.json().get("layers", [])

layer_id = None
for layer in layers:
    if layer.get("name") == layer_name:
        layer_id = layer.get("id")
        break

if layer_id is not None:
    # Construct URL for the specific layer
    layer_query_url = f"{base_url}/{layer_id}/query"
    
    # Set up parameters for the query
    params = {
        "where": "1=1",           # Query all features
        "outFields": "*",          # Get all fields
        "f": "geojson"             # Request response in GeoJSON format
    }
    
    # Query the layer
    response = requests.get(layer_query_url, params=params)
    data = response.json()  # GeoJSON data

    # Convert GeoJSON to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(data["features"], crs=2193)
    print(gdf.head())
else:
    print(f"Layer '{layer_name}' not found.")



#write the above code in a functio

