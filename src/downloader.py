import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
from enum import Enum
import geopandas as gpd
from pydantic import BaseModel

from src.restGDF import Layer #NOTE: currently at layer level only.


class Config(BaseModel):
    folder: Path = Path("output")
    format: str = "geojson"
    query_polygon: Optional[Path] = None
    reporting: bool = False
    layers: List[str] = field(default_factory=list)

    # def __post_init__(self):
    #     self.folder.mkdir(parents=True, exist_ok=True)
    #     if self.query_polygon:
    #         self.query_polygon = self.query_polygon.resolve()
    #         if not self.query_polygon.exists():
    #             raise FileNotFoundError(f"Query polygon file does not exist: {self.query_polygon}")

def json_loader(file_path: Union[str, Path]) -> Config: #NOTE: to move to utils
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return Config(**data)

# {
#   "reporting": true,
#   "query_polygon": "clip_polygon.shp",
#   "layers": [
#     "https://services6.arcgis.com/EU3vB12T67eDdisL/ArcGIS/rest/services/WaterLine/FeatureServer/488",
#   ]
# }

@dataclass
class BulkDownloader:

    config_path: Path = Path("config.json")
    output_folder: Path = Path("output")
    query_polygon: Optional[Path] = None
    reporting: bool = False

    layers: Dict[str, Layer] = field(init=False, default_factory=dict)
    dataframes: Dict[str, gpd.GeoDataFrame] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        self.load_config()
        if self.query_polygon:
            self.query_polygon = self.query_polygon.resolve()
            if not self.query_polygon.exists():
                raise FileNotFoundError(f"Query polygon file does not exist: {self.query_polygon}")

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

    def download_layers(self):
        for layer_url in self.config.get("layers", []):
            layer = Layer(url=layer_url)
            if self.query_polygon:
                gdf = layer.get_gdf_by_polygon(self.query_polygon, crs="EPSG:4326")
                
            else:
                gdf = layer.get_gdf(crs="EPSG:4326")
            self.dataframes[layer.name] = gdf
            if self.reporting:
                print(f"Downloaded {len(gdf)} features from {layer.name}")
