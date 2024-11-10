from leafmap import _use_folium
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to ArcGIS Online (or your specific GIS instance)
gis = GIS()

# Item ID for the specific content (e.g., 22856b4dde664824808c0de7965c5a5e)
item_id = "22856b4dde664824808c0de7965c5a5e"

# Retrieve the item using its ID
item = gis.content.get(item_id)
print(type(item))
print(item.keys())
print(item['property_name'])
# Access the feature layer(s) within the item
# Items can have multiple layers; we assume the first layer here
# feature_layer = item.layers[0]
#
# # Optional: Query the feature layer (e.g., to get features in New Zealand’s bounding box)
# nz_bounding_box = {
#     "xmin": 160.6,  # minimum longitude
#     "ymin": -49.2,  # minimum latitude
#     "xmax": 179.1,  # maximum longitude
#     "ymax": -33.9,  # maximum latitude
#     "spatialReference": {"wkid": 4326}  # WGS 84 spatial reference
# }
#
# # Create a query using the bounding box
# from arcgis.geometry import Geometry
#
# geometry = Geometry(nz_bounding_box)
# query_result = feature_layer.query(geometry_filter=geometry, return_geometry=True)
#
# # Display the query results
# for feature in query_result:
#     print(feature.attributes)
#     print(feature.geometry)

# def main():
#     print("Hello from wsnetbuilder!")
#
#
# if __name__ == "__main__":
#     main()
