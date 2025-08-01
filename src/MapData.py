from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import geopandas as gpd
from shapely.geometry import LineString, Point
from typing import Callable, Union, Dict, Any, Optional, List, Tuple


def fix_point_geometry(geom: Point) -> Point:
    pass

def fix_line_geometry(geom: LineString) -> LineString:
    pass 

class MapLayer(ABC):
    """
    Abstract base class for map layers.
    """
    data: gpd.GeoDataFrame = field(default_factory=gpd.GeoDataFrame)
    name: str = ""

    @abstractmethod
    def prep_crs(self, crs: str = "EPSG:2193") -> None:
        """
        Set the coordinate reference system for the layer.
        """
        pass

    @abstractmethod
    def is_valid_geometry(self) -> bool:
        """
        Validate the geometry of the layer.
        """
        pass

    @abstractmethod
    def fix_geometry(self, fn: Callable = None) -> None:
        """
        Fix the geometry of the layer if it is invalid.
        """
        pass

@dataclass
class LineLayer(MapLayer):
    """
    Class representing a line layer in a map.
    Attributes:
        data (gpd.GeoDataFrame): The GeoDataFrame containing the line data.
        name (str): The name of the line layer.
    """
    data: gpd.GeoDataFrame = field(default_factory=gpd.GeoDataFrame)
    name: str = ""
    def __post_init__(self):
        if not isinstance(self.data, gpd.GeoDataFrame):
            raise TypeError("data must be a GeoDataFrame")
        if self.data.crs is None:
            raise ValueError("GeoDataFrame must have a CRS set before using this class. Use MapLayer.get_gdf() to set it.")
        # if not self.is_valid_geometry():
        #     raise ValueError("Geometry is invalid. Please fix it before proceeding.")
    def prep_crs(self, crs: str = "EPSG:2193") -> None:
        """        Set the coordinate reference system for the line layer.
        Args:
            crs (str): The coordinate reference system to set.

        """
        if self.data.crs is None:
            raise ValueError("Data must have a CRS set before changing it. MapLayer.get_gdf() should have taken care of this.")
        self.data = self.data.to_crs(crs)
        return None
    def is_valid_geometry(self) -> None:
        """        Validate the geometry of the line layer.
        Raises:
            ValueError: If the geometry is invalid.
        """
        #check LIneString geometries
        if not all(isinstance(geom, LineString) for geom in self.data.geometry):
            return False
        else:
            return True
    def fix_geometry(self, fn: Callable = None) -> None:
        """
        Fix the geometry of the line layer if it is invalid.
        Args:
            fn (Callable): A function to apply to fix the geometry.
        """
        if not self.is_valid_geometry():
            if fn is not None:
                self.data.geometry = self.data.geometry.apply(fn)
            else:
                raise ValueError("Geometry is invalid and no fix function provided.")

@dataclass
class PointLayer(MapLayer):
    """
    Class representing a point layer in a map.
    Attributes:
        data (gpd.GeoDataFrame): The GeoDataFrame containing the point data.
        name (str): The name of the point layer.
    """
    def prep_crs(self, crs: str = "EPSG:2193") -> None:
        """        Set the coordinate reference system for the point layer.
        Args:
            crs (str): The coordinate reference system to set.
        """
        if self.data.crs is None:
            raise ValueError("Data must have a CRS set before changing it. MapLayer.get_gdf() should have taken care of this.")
        self.data = self.data.to_crs(crs)
        return None
    def is_valid_geometry(self) -> bool:
        """        Validate the geometry of the point layer.
        Returns:
            bool: True if all geometries are valid points, False otherwise.
        """
        return all(isinstance(geom, Point) for geom in self.data.geometry)
    def fix_geometry(self, fn: Callable = None) -> None:
        """
        Fix the geometry of the point layer if it is invalid.
        Args:
            fn (Callable): A function to apply to fix the geometry.
        """
        if not self.is_valid_geometry():
            if fn is not None:
                self.data.geometry = self.data.geometry.apply(fn)
            else:
                raise ValueError("Geometry is invalid and no fix function provided.")



@dataclass
class MapDataStore:
    """
    Class to manage a collection of map layers.
    """
    layers: dict[str, MapLayer] = field(default_factory=dict)

    def add_layer(self, name: str, layer: MapLayer) -> None:
        """
        Add a new layer to the data store.
        """
        self.layers[name] = layer

    def get_layer(self, name: str) -> MapLayer:
        """
        Retrieve a layer by its name.
        """
        return self.layers.get(name)

    def get_gdf_by_name(self, name: str) -> gpd.GeoDataFrame:
        """
        Get the GeoDataFrame of a layer by its name.
        """
        layer = self.get_layer(name)
        if layer is not None:
            return layer.data
        else:
            raise KeyError(f"Layer '{name}' not found in the data store.")
