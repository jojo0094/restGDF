import ast
import leafmap
from numpy import DataSource
import streamlit as st
# import leafmap.foliumap as leafmap
import leafmap.kepler as leaftmap
import requests
import geopandas as gpd
import restapi
from restGDF.src import MapData
from restGDF.src.MapData import MapDataStore


import os
os.environ['RESTAPI_USE_ARCPY'] = 'FALSE'
os.environ['RESTAPI_VERIFY_CERT'] = 'FALSE'

# now import restapi
import restapi



st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

data_store:MapDataStore = st.session_state.get("data_store", None)
layer_list = data_store.list_layers()

@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("ArcGIS Rest Servers")
st.markdown(
    """
[to write later] This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service
in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services to find
some WMS URLs if needed.
"""
)

row1_col1, row1_col2 = st.columns([3, 1])
#add h2 header
row1_col1.header("Map")
width = None
height = 600
layers = None


with row1_col2:

    esa_landcover = 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'
 
    url = st.text_input(
        "Enter a WMS URL:", value= 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'
    )
    empty = st.empty()

    if data_store:
        options = layer_list
        default = None
        # watermap_sever = restapi.MapService(url)
        # options = watermap_sever.list_layers()
        # # options = get_layers(url)

        # if url == esa_landcover:
        #     default = "Water Main"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
        add_legend = st.checkbox("Add a legend to the map", value=True)
        if default == "Water Main":
            legend = str(leafmap.builtin_legends["ESA_WorldCover"])
        else:
            legend = ""
        if add_legend:
            legend_text = st.text_area(
                "Enter a legend as a dictionary {label: color}",
                value=legend,
                height=200,
            )

        #get
    
        with row1_col1:
            #{"type":"Point","coordinates":[535.286865,-37.78374]}}
            m = leafmap.Map(center=(-37.78374, 535.286865), zoom=12)
            #use folium map instead
            # import folium
            # m = folium.Map(location=[-37.78374, 535.286865], zoom_start=12)

            if layers is not None:
                layer_row_count = {}
                for layer in layers:
                    layer_to_add = None


                    # layer_to_add = get_layer_data(url, layer)
                    # layer_to_add = get_layer_data(watermap_sever, layer)
                    layer_to_add = data_store.get_gdf_by_name(layer)
                    # layer_to_add = layer_to_add[:1000]
                    layer_row_count[layer] = len(layer_to_add)
                    # layer_chosen = watermap_sever.layer(layer)
                    # total_features = layer_chosen.query(where="1=1", returnCountOnly=True)["count"]
                    # layer_row_count[layer] = total_features
                    #add card with layer name and count
                    #change to web crs
                    layer_to_add = layer_to_add.to_crs("EPSG:4326")

                    # m.add_gdf(layer_to_add, layer_name=layer)
                    # folium.GeoJson(layer_to_add).add_to(m)

                    # m.add_wms_layer(
                    #     url, layers=layer, name=layer, attribution=" ", transparent=True
                    # )
            # if add_legend and legend_text:
            #     legend_dict = ast.literal_eval(legend_text)
            #     m.add_legend(legend_dict=legend_dict)
                cols = st.columns(len(layer_row_count))
                for i, (layer_name,row_count) in enumerate(layer_row_count.items()):
                    with cols[i]:
                        st.write(f"Layer: {layer_name} - Count: {row_count}")

            
            m.add_gdf(layer_to_add[:100], layer_name=layer)
            m.to_streamlit(width, height)

        # with row1_col1:
        #     m = leafmap.Map(center=(36.3, 0), zoom=2)
        #
        #     if layers is not None:
        #         for layer in layers:
        #             layerToAdd = watermap_sever.layer(layer)
        #             m.
        #             m.add_wms_layer(
        #                 url, layers=layer, name=layer, attribution=" ", transparent=True
        #             )
        #     if add_legend and legend_text:
        #         legend_dict = ast.literal_eval(legend_text)
        #         m.add_legend(legend_dict=legend_dict)
        #
        #     m.to_streamlit(width, height)
    else:
        st.header("Add the WMS link first above")
