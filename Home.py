import streamlit as st
import leafmap.foliumap as leafmap
from restGDF.src.restGDF import Layer
from restGDF.src.MapData import MapDataStore, MapLayer, PointLayer
st.set_page_config(layout="wide")

ws_point_url = "https://services6.arcgis.com/EU3vB12T67eDdisL/ArcGIS/rest/services/WaterPoint/FeatureServer/27"
ws_point_layer = Layer(url=ws_point_url)

ws_point_maplayer = PointLayer(
        data=ws_point_layer.get_gdf(),
        name=ws_point_layer.feature_layer.get('name', 'Water Point Layer')
)
data_store = MapDataStore(
    layers={
        ws_point_maplayer.name: ws_point_maplayer
    }
)

st.session_state["data_store"] = data_store

# Customize the sidebar
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Streamlit for Geospatial Applications")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/opengeos/streamlit-map-template).
    """
)

st.header("Instructions")

markdown = """
1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
