import restapi
from src.restGDF import Layer


print("hello world")

url = 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'

layer = Layer(url=url, layer_name='Water Main')

gdf = layer.get_gdf()

Layer.save_gdf(gdf, "Water Main")
