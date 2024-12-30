import geopandas as gpd
import restapi
from restapi import MapService, MapServiceLayer
from typing import Union, Optional, Dict, List

def get_layer_data(mapserver: MapService, layer_name: str) -> Union[gpd.GeoDataFrame, None]:
    """
    Fetches all features from a mapserver layer.

    Args:
        mapserver: The MapService object.
        layer_name: The name of the layer to query.

    Returns:
        A GeoDataFrame containing all features from the layer if successful, 
        otherwise None.
    """
    try:
        layer: MapServiceLayer = mapserver.layer(layer_name)
        gdf = gpd.GeoDataFrame.from_features(
            layer.query(where="1=1", exceed_limit=True, outFields="*", 
                       returnGeometry=True, f="geojson")["features"], 
            crs="EPSG:4326"
        )
        return gdf
    except Exception as e:
        print(f"Error fetching layer data for '{layer_name}': {e}")
        return None

def get_layer_data_by_polygon(mapserver: MapService, layer_name: str, polygon: str) -> Union[gpd.GeoDataFrame, None]:
    """
    Fetches all features from a mapserver layer within a polygon.

    Args:
        mapserver: The MapService object.
        layer_name: The name of the layer to query.
        polygon: The polygon to filter the features by.

    Returns:
        A GeoDataFrame containing all features from the layer within the polygon if successful, 
        otherwise None.
    """
    try:
        layer: MapServiceLayer = mapserver.layer(layer_name)
        gdf = gpd.GeoDataFrame.from_features(
            layer.query(where="1=1", geometry=polygon, exceed_limit=True, outFields="*", 
                       returnGeometry=True, f="geojson")["features"], 
            crs="EPSG:4326"
        )
        return gdf
    except Exception as e:
        print(f"Error fetching layer data for '{layer_name}': {e}")
        return None

 
def save_gdf(gdf: gpd.GeoDataFrame,layer_name: str, 
              config: Dict = {
              "folder": ".",
              "format": "gpkg",

              }) -> None:
    """
    Saves a GeoDataFrame to a file.

    Args:
        gdf: The GeoDataFrame to save.
        config: A dictionary containing the following 
        fields:
            folder: The folder to save the file in.
            format: The format to save the file in.
    """

    try:
        if config["format"] == "gpkg":
            gdf.to_file(f"{config['folder']}/{layer_name}.gpkg", driver="GPKG")
        else :
            gdf.to_file(f"{config['folder']}/{layer_name}.shp")
    except Exception as e:
        print(f"Error saving GeoDataFrame: {e}")


