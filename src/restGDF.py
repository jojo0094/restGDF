import restapi  
from dataclasses import dataclass
from restapi import MapService, MapServiceLayer
from typing import Union, Optional, Dict, List
from . import utils
import geopandas as gpd

@dataclass
class Layer:
    url : str
    layer_name : str
    layer : Optional[MapServiceLayer] = None

    def __post_init__(self):
        self.mapserver = MapService(self.url)
        self.layer = self.mapserver.layer(self.layer_name)

    def list_layers(self) -> List[str]:
        return self.mapserver.list_layers()

    def get_gdf(self) -> Union[gpd.GeoDataFrame, None]:
        return utils.get_layer_data(mapserver=self.mapserver, layer_name=self.layer_name)

    def get_gdf_by_polygon(self, polygon: str) -> Union[gpd.GeoDataFrame, None]:
        return utils.get_layer_data_by_polygon(mapserver=self.mapserver, layer_name=self.layer_name, polygon=polygon)

    def get_all_features_paginated(self, batch_size=1000):
        offset = 0
        all_features = []
        while True:
            result = self.layer.query(
                where="1=1",
                outFields="*",
                returnGeometry=True,
                resultOffset=offset,
                resultRecordCount=batch_size,
                f="geojson"
            )
            features = result.get("features", [])
            all_features.extend(features)
            if len(features) < batch_size:
                break  # No more features
            offset += batch_size

        return gpd.GeoDataFrame.from_features(all_features, crs="EPSG:4326")

    @staticmethod
    def save_gdf(gdf: gpd.GeoDataFrame, layer_name: str, 
                  config: Dict = {
                  "folder": ".",
                  "format": "gpkg",
                  }) -> None: # kwargs** will be suited? 
        utils.save_gdf(gdf, layer_name, config) # need to know what utils.save_gdf does


