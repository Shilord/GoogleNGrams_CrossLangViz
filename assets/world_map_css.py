world_map_css = """
<style>
/* Match Streamlit theme */
.folium-map, .leaflet-container {
    background-color: #0d1118 !important;
}

.leaflet-tile-pane {
    opacity: 0 !important;
}

/* Keep legend on the right side, adjust vertical position */
.leaflet-control-container .leaflet-top.leaflet-right {
    top: 60px !important;
    right: 20px !important;
}


</style>
"""