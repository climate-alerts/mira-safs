import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import plotly.express as px
import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt

# Suppress specific warnings
warnings.filterwarnings('ignore', category=UserWarning)

def generate_colors(num_colors):
    """Generate a list of distinct colors."""
    cmap = plt.get_cmap('tab20')
    return [cmap(i / num_colors) for i in range(num_colors)]

def assign_colors(df, color_column):
    """Assign colors to unique values in the dataframe."""
    unique_values = df[color_column].unique()
    num_unique_values = len(unique_values)
    available_colors = generate_colors(num_unique_values)
    return dict(zip(unique_values, available_colors))

def analyze_area_statistics(geojson_path):
    """Analyze area statistics from GeoJSON."""
    try:
        gdf = gpd.read_file(geojson_path)
        
        if 'name' not in gdf.columns:
            st.warning("Expected column 'name' not found in GeoJSON file. Using default column names.")
            gdf['name'] = gdf.index.astype(str)
        
        if gdf.crs is None:
            st.error("CRS (Coordinate Reference System) is not defined in the GeoJSON file.")
            return {}, pd.DataFrame()
        
        if gdf.crs.to_string() != 'EPSG:3857':
            gdf = gdf.to_crs(epsg=3857)
        
        gdf['area_ha'] = gdf['geometry'].area / 10000
        
        total_area_ha = gdf['area_ha'].sum()
        num_features = len(gdf)
        
        areas = gdf[['name', 'area_ha']]
        
        stats = {
            'Total Area (hectares)': total_area_ha,
            'Number of Features': num_features
        }
        
        return stats, areas
    except Exception as e:
        st.error(f"Error analyzing area statistics: {e}")
        return {}, pd.DataFrame()

# Define a permanent legend dictionary
PERMANENT_LEGEND = {
    '10 Trees': '#006400',
    '20 Shrubland': '#ffbb22',
    '30 Grassland': '#ffff4c',
    '40 Cropland': '#f096ff',
    '50 Built-up': '#fa0000',
    '60 Barren / sparse vegetation': '#b4b4b4',
    '70 Snow and ice': '#f0f0f0',
    '80 Open water': '#0064c8',
    '90 Herbaceous wetland': '#0096a0',
    '95 Mangroves': '#00cf75',
    '100 Moss and lichen': '#fae6a0'
}

def app():
    st.title("Satellite Monitoring")

    map_width = None
    map_height = 700

    regions_path = 'assets/field.geojson'

    stats, areas = analyze_area_statistics(regions_path)
    
    color_map = assign_colors(areas, 'name')
    areas['color'] = areas['name'].map(color_map)
    areas = areas.sort_values(by='name')

    st.subheader("Map Controls")

    tab1, tab2 = st.tabs(["Marker Cluster", "WMS Layers"])

    with tab1:
        st.write("### Marker Cluster")
        m_marker = leafmap.Map(center=[40, -100], zoom=4)

        if not os.path.isfile(regions_path):
            st.error(f"GeoJSON file not found: {regions_path}")
        else:
            try:
                m_marker.add_geojson(
                    regions_path,
                    layer_name='Farm fields',
                    style_function=lambda feature: {
                        'fillColor': color_map.get(feature['properties']['name'], '#grey'),
                        'color': 'black',
                        'weight': 1,
                        'fillOpacity': 0.5
                    },
                    draw_export=True,
                    minimap_control=True
                )
            except Exception as e:
                st.error(f"Error adding GeoJSON: {e}")

        m_marker.to_streamlit(width=map_width, height=map_height)

    with tab2:
        st.write("### Web Map Service (WMS)")
        st.markdown(
            """
            This app demonstrates loading Web Map Service (WMS) layers. Enter the URL of the WMS service 
            in the text box below and press Enter to retrieve the layers. Go to https://apps.nationalmap.gov/services 
            to find some WMS URLs if needed.
            """
        )

        esa_landcover = "https://services.terrascope.be/wms/v2"
        url = st.text_input("Enter a WMS URL:", value=esa_landcover)
        empty = st.empty()

        if url:
            options = leafmap.get_wms_layers(url)
            default = "WORLDCOVER_2020_MAP" if url == esa_landcover else None
            layers = empty.multiselect(
                "Select WMS layers to add to the map:", options, default=default
            )
            add_legend = st.checkbox("Add a legend to the map", value=True)

            m_wms = leafmap.Map(center=(36.3, 0), zoom=2)
            if layers:
                for layer in layers:
                    m_wms.add_wms_layer(
                        url, layers=layer, name=layer, attribution=" ", transparent=True
                    )
            if add_legend:
                m_wms.add_legend(legend_dict=PERMANENT_LEGEND)

            m_wms.to_streamlit(width=map_width, height=map_height)

    st.subheader("Field Sizes Analysis")

    if not areas.empty:
        fig = px.bar(
            areas,
            x='name',
            y='area_ha',
            color='color',
            title='Field Sizes in Hectares',
            labels={'area_ha': 'Size (hectares)', 'name': 'Field Name'},
            height=500
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.write("### Area Statistics")
    st.json(stats)

if __name__ == "__main__":
    app()
