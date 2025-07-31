import restapi  
from dataclasses import dataclass
from restapi import MapService, MapServiceLayer, FeatureService, FeatureLayer
from restapi import RestAPIException
from typing import Union, Optional, Dict, List
# from . import utils
import geopandas as gpd


#sw_point_url = 'https://services6.arcgis.com/EU3vB12T67eDdisL/ArcGIS/rest/services/StormWaterPoint/FeatureServer'$sw_point_url = 'https://services6.arcgis.com/EU3vB12T67eDdisL/ArcGIS/rest/services/StormWaterPoint/FeatureServer'
#: so write string validator for url. it has to be FeatureServer. for that use pydantic or dataclass with a validator.



@dataclass
class FeatureLayerContainer:
    # do documentation for this class including the methods and attributes
    """A container for managing multiple FeatureLayer objects from a Feature Service.
    Attributes:
        url (str): The URL of the Feature Service.
        feature_service (FeatureService): The FeatureService object initialized with the provided URL.
    Methods:
        get_container() -> Dict[str, FeatureLayer]: Returns a dictionary of layer names and their corresponding FeatureLayer objects.
    """
    url: str

    def __post_init__(self):
        try:
            self.feature_service = FeatureService(self.url)
        except Exception as e:
            #NOTE: Orignally, it is shown as RecurrsionError, but I wrapped it to ValueError pointing to the user that the URL is invalid.
            raise ValueError(f"Invalid Feature Service URL: {self.url}. Error: {e}")

    def get_container(self) -> Dict[str, FeatureLayer]:
        """
        Returns a dictionary of layer names and their corresponding FeatureLayer objects.
        """
        # return {layer_name: self.feature_service.layer(layer_name) for layer_name in self.feature_service.list_layers()}
        #init Layer(feature_layer) for each layer in the feature service
        return {layer_name: Layer(feature_layer=self.feature_service.layer(layer_name)) for layer_name in self.feature_service.list_layers()}

@dataclass
class Layer:
    """A class representing a single Feature Layer from a Feature Service.
    Attributes:
        url (str): The URL of the Feature Layer.
        feature_layer (FeatureLayer): The FeatureLayer object initialized with the provided URL.
    Methods:
    
    """
    url: Optional[str] = None
    feature_layer: Optional[Union[FeatureLayer, MapServiceLayer]] = None
    
    def __post_init__(self):
        if not self.feature_layer:
            if not self.url:
                raise ValueError("URL must be provided to initialize the Feature Layer.")
            else:
                try:
                    self.feature_layer = FeatureLayer(self.url)
                except RestAPIException as e:
                    raise ValueError(f"Invalid Feature Layer URL: {self.url}. Error: {e}")

    def get_gdf(self, crs:str="EPSG:4326", batch_size:int=1000) -> gpd.GeoDataFrame:
        """
        Retrieves the GeoDataFrame for the Feature Layer.
        Returns:
            gpd.GeoDataFrame: The GeoDataFrame containing the features of the layer.
        """
        return self._get_all_features_paginated(batch_size=batch_size, crs=crs)

    def _get_all_features_paginated(self, batch_size:int=1000, crs:str="EPSG:4326") -> gpd.GeoDataFrame:
        """
        Retrieves all features from the Feature Layer in a paginated manner.
        Args:
            batch_size (int): The number of features to retrieve in each batch.
        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing all features from the layer.
        """
        offset = 0
        all_features = []
        while True:
            result = self.feature_layer.query(
                where="1=1",
                outFields="*",
                returnGeometry=True,
                resultOffset=offset,
                resultRecordCount=batch_size,
                f="geojson"
            )
            features = result.get("features", [])
            # check possible of empty features; raise ValueError if empty
            if not features:
                raise ValueError(f"No features found in the layer: {self.url}")
            if len(features) < batch_size:
                all_features.extend(features) #NOTE: This is ugly;
                break
            all_features.extend(features) #NOTE: see the above comment
            offset += batch_size
        return gpd.GeoDataFrame.from_features(all_features, crs=crs)

    def get_gdf_by_polygon(self, polygon: str, crs:str="EPSG:4326", batch_size:int=1000) -> gpd.GeoDataFrame:
        """
        Retrieves the GeoDataFrame for the Feature Layer filtered by a polygon.
        Args:
            polygon (str): The polygon to filter the features by.
            crs (str): The coordinate reference system for the GeoDataFrame.
            batch_size (int): The number of features to retrieve in each batch.
        Returns:
            gpd.GeoDataFrame: The GeoDataFrame containing the features of the layer within the polygon.
        """
        return self._get_all_features_paginated_by_polygon(polygon=polygon, batch_size=batch_size, crs=crs)
    def _get_all_features_paginated_by_polygon(self, polygon: str, batch_size:int=1000, crs:str="EPSG:4326") -> gpd.GeoDataFrame:
        """
        Retrieves all features from the Feature Layer within a polygon in a paginated manner.
        Args:
            polygon (str): The polygon to filter the features by.
            batch_size (int): The number of features to retrieve in each batch.
            crs (str): The coordinate reference system for the GeoDataFrame.
        Returns:
            gpd.GeoDataFrame: A GeoDataFrame containing all features from the layer within the polygon.
        """
        offset = 0
        all_features = []
        while True:
            result = self.feature_layer.query(
                where="1=1",
                geometry=polygon,
                outFields="*",
                returnGeometry=True,
                resultOffset=offset,
                resultRecordCount=batch_size,
                f="geojson"
            )
            features = result.get("features", [])
            # check possible of empty features; raise ValueError if empty
            if not features:
                raise ValueError(f"No features found in the layer: {self.url} within the polygon: {polygon}")
            if len(features) < batch_size:
                all_features.extend(features)
                break
            all_features.extend(features)
            offset += batch_size
        return gpd.GeoDataFrame.from_features(all_features, crs=crs)

# @dataclass
# class Layer_old:
#     url : str
#     layer_name : str
#     layer : Optional[MapServiceLayer] = None
#
#     def __post_init__(self):
#         self.mapserver = MapService(self.url)
#         self.layer = self.mapserver.layer(self.layer_name)
#
#     def list_layers(self) -> List[str]:
#         return self.mapserver.list_layers()
#
#     def get_gdf(self) -> Union[gpd.GeoDataFrame, None]:
#         return utils.get_layer_data(mapserver=self.mapserver, layer_name=self.layer_name)
#
#     def get_gdf_by_polygon(self, polygon: str) -> Union[gpd.GeoDataFrame, None]:
#         return utils.get_layer_data_by_polygon(mapserver=self.mapserver, layer_name=self.layer_name, polygon=polygon)
#
#     def get_all_features_paginated(self, batch_size=1000):
#         offset = 0
#         all_features = []
#         while True:
#             result = self.layer.query(
#                 where="1=1",
#                 outFields="*",
#                 returnGeometry=True,
#                 resultOffset=offset,
#                 resultRecordCount=batch_size,
#                 f="geojson"
#             )
#             features = result.get("features", [])
#             all_features.extend(features)
#             if len(features) < batch_size:
#                 break  # No more features
#             offset += batch_size
#
#         return gpd.GeoDataFrame.from_features(all_features, crs="EPSG:4326")
#
#     @staticmethod
#     def save_gdf(gdf: gpd.GeoDataFrame, layer_name: str, 
#                   config: Dict = {
#                   "folder": ".",
#                   "format": "gpkg",
#                   }) -> None: # kwargs** will be suited? 
#         utils.save_gdf(gdf, layer_name, config) # need to know what utils.save_gdf does
#
#
