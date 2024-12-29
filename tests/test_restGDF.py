import pytest
from src.restGDF import Layer
import geopandas as gpd
from unittest.mock import patch
from src.utils import save_gdf, get_layer_data

# Mock MapService for testing
class MockMapService:
    def __init__(self, url):
        pass

    def list_layers(self):
        return ["layer1", "layer2"]

    def layer(self, layer_name):
        if layer_name == "layer1":
            # Create a sample GeoJSON feature for testing
            feature = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [0, 0]},
                "properties": {"id": 1}
            }
            return {"features": [feature]} 
        else:
            return None

# Test the `__post_init__` method
def test_post_init():
    layer = Layer(url="http://example.com/wms", layer_name="layer1")
    assert layer.mapserver is not None
    assert layer.layer is not None

# Test the `list_layers` method
def test_list_layers():
    layer = Layer(url="http://example.com/wms", layer_name="layer1")
    assert layer.list_layers() == ["layer1", "layer2"]

# Test the `get_gdf` method
def test_get_gdf():
    layer = Layer(url="http://example.com/wms", layer_name="layer1")
    gdf = layer.get_gdf()
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 1

# Test the `get_gdf` method with an invalid layer
def test_get_gdf_invalid_layer():
    layer = Layer(url="http://example.com/wms", layer_name="invalid_layer")
    gdf = layer.get_gdf()
    assert gdf is None

# Test the `save_gdf` static method (requires mocking)
@patch('your_module.utils.save_gdf')  # Replace with the actual import path for save_gdf
def test_save_gdf(mock_save_gdf):
    gdf = gpd.GeoDataFrame({'geometry': gpd.points_from_xy([0], [0])})
    Layer.save_gdf(gdf, "test_layer")
    mock_save_gdf.assert_called_once_with(gdf, "test_layer", {"folder": ".", "format": "gpkg"})

# Run the tests
if __name__ == "__main__":
    pytest.main()
