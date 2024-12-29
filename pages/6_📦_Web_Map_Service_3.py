import ast
import streamlit as st
import leafmap.foliumap as leafmap
import requests
import geopandas as gpd
import restapi

def get_layer_data(mapserver, layer_name, result_limit=2000):
    """
    Fetches all features from a mapserver layer, handling potential 2000-row limits.

    Args:
        mapserver: The MapServer object.
        layer_name: The name of the layer to query.
        result_limit: The maximum number of features to fetch per request (default: 2000).

    Returns:
        A GeoDataFrame containing all features from the layer.
    """

    layer = mapserver.layer(layer_name)

    # Determine the total number of features (if available)
    try:
        total_features = layer.query(where="1=1", returnCountOnly=True)["count"]
    except KeyError:
        total_features = None

    all_features = []
    offset = 0

    while True:
        # Construct the query with result limit and offset
        query_result = layer.query(
            where="1=1",
            outFields="*",
            returnGeometry=True,
            f="geojson",
            resultOffset=offset,
            resultRecordCount=result_limit
        )

        # Append features to the list
        all_features.extend(query_result["features"])

        # Check if all features have been retrieved
        if total_features is not None:
            if offset >= total_features:
                break
        else:
            # If total_features is unknown, assume all features have been retrieved
            if len(query_result["features"]) < result_limit:
                break

        offset += result_limit

    return gpd.GeoDataFrame.from_features(all_features, crs="EPSG:4326")
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

def get_layer_data(mapserver, layer_name):
    layer = mapserver.layer(layer_name)
    return gpd.GeoDataFrame.from_features(layer.query(where="1=1",exceed_limit=True, outFields="*", returnGeometry=True, f="geojson")["features"], crs="EPSG:4326")
#
# def get_layer_data(base_url, layer_name):
#     # Define the Map Service URL and the layer endpoint
#     layer_url = f"{base_url}/layers"  # Append layer endpoint
#
#     # Get layer list and find "Water Valve" layer ID
#     response = requests.get(layer_url, params={"f": "json"})
#     layers = response.json().get("layers", [])
#
#     layer_id = None
#     for layer in layers:
#         if layer.get("name") == layer_name:
#             layer_id = layer.get("id")
#             break
#
#     if layer_id is not None:
#         # Construct URL for the specific layer
#         layer_query_url = f"{base_url}/{layer_id}/query"
#
#         # Set up parameters for the query
#         params = {
#             "where": "1=1",           # Query all features
#             "outFields": "*",          # Get all fields
#             "f": "geojson"             # Request response in GeoJSON format
#         }
#
#         # Query the layer
#         response = requests.get(layer_query_url, params=params)
#         data = response.json()  # GeoJSON data
#
#         # Convert GeoJSON to GeoDataFrame
#         gdf = gpd.GeoDataFrame.from_features(data["features"], crs="EPSG:4326") 
#         return gdf
#     else:
#         print(f"Layer '{layer_name}' not found.")

with row1_col2:

    esa_landcover = 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'
 
    url = st.text_input(
        "Enter a WMS URL:", value= 'https://maps.hamilton.govt.nz/server/rest/services/agol_3waters/Water/MapServer'
    )
    empty = st.empty()

    if url:
        watermap_sever = restapi.MapService(url)
        options = watermap_sever.list_layers()
        # options = get_layers(url)

        default = None
        if url == esa_landcover:
            default = "Water Main"
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
                    layer_to_add = get_layer_data(watermap_sever, layer)
                    # layer_to_add = layer_to_add[:1000]
                    layer_row_count[layer] = len(layer_to_add)
                    layer_chosen = watermap_sever.layer(layer)
                    total_features = layer_chosen.query(where="1=1", returnCountOnly=True)["count"]
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

            
            m.add_gdf(layer_to_add, layer_name=layer)
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
