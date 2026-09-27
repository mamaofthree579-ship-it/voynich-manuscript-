# app.py
import streamlit as st
import pandas as pd
import json

# FIX 1: Set correct page config layout function
st.set_page_config(layout="wide")

st.title("Hope Jones: Multi-System Reconstruction Workspace")

# Ingestion block with explicit file verification fallback
try:
    with open("hope_jones_master_spatial_log.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Missing Database File: Please ensure 'hope_jones_master_spatial_log.json' is saved inside this exact directory path.")
    st.stop()

# Render Global Metrics in Sidebar Panel
st.sidebar.header("Pipeline Verification Diagnostics")
st.sidebar.metric("Target Dicot Alignment (JSD)", f"{data['global_metrics']['target_dicot_alignment_jsd']:.6f}")
st.sidebar.metric("Spiral Trajectory Fit (R²)", f"{data['global_metrics']['geometric_trajectory_fit_r2']:.4f}")

# Extract and Flatten Node Coordinates
nodes_list = data["trajectory_nodes"]
flattened_rows = []

for node in nodes_list:
    # FIX 2: Unpack discrete array vectors explicitly to prevent nested series column tracking crashes
    coords = node["coordinates"]
    
    flattened_rows.append({
        "Node": node["node_index"],
        "Glyph": node["glyph_token"],
        "Book Source": node["source_volume"],
        "Folio": node["folio_tag"],
        "Frequency (Hz)": node["frequency_hz"],
        "Ratio": node["ratio_fraction"],
        "X": float(coords[0]),
        "Y": float(coords[1]),
        "Z": float(coords[2])
    })

df = pd.DataFrame(flattened_rows)

# Render Data Table
st.subheader("Recovered Just-Intonation Node Table")
st.dataframe(df, use_container_width=True)

# Render 2D Plane Layout Projections
st.subheader("Spatial Trajectory Mapping Projections")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**XY Plane (Phyllotactic Spiral Footprint View)**")
    st.scatter_chart(df, x="X", y="Y", color="Frequency (Hz)", size="Node")

with col2:
    st.markdown("**XZ Plane (Acoustic Pitch Wave Profile Elevation)**")
    st.scatter_chart(df, x="X", y="Z", color="Frequency (Hz)", size="Node")
