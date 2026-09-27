# app.py
import streamlit as st
import pandas as pd
import json

st.set_page_buffer_config = {"layout": "wide"}
st.title("Hope Jones: Multi-System Reconstruction Workspace")

# 1. Safe Ingestion Channel
with open("hope_jones_master_spatial_log.json", "r") as f:
    data = json.load(f)

# Display Global Verification Metrics
st.sidebar.header("Pipeline Verification Diagnostics")
st.sidebar.metric("Target Dicot Alignment (JSD)", f"{data['global_metrics']['target_dicot_alignment_jsd']:.6f}")
st.sidebar.metric("Spiral Trajectory Fit (R²)", f"{data['global_metrics']['geometric_trajectory_fit_r2']:.4f}")

# 2. Extract and Flatten Node Coordinates for Streamlit DataFrames
nodes_list = data["trajectory_nodes"]
flattened_rows = []

for node in nodes_list:
    flattened_rows.append({
        "Node": node["node_index"],
        "Glyph": node["glyph_token"],
        "Book Source": node["source_volume"],
        "Folio": node["folio_tag"],
        "Frequency (Hz)": node["frequency_hz"],
        "Ratio": node["ratio_fraction"],
        "X": node["coordinates"][0],
        "Y": node["coordinates"][1],
        "Z": node["coordinates"][2]
    })

df = pd.DataFrame(flattened_rows)

# 3. Render Interactive Live UI Layout
st.subheader("Recovered Just-Intonation Node Table")
st.dataframe(df, use_container_width=True)

# 4. Built-in Streamlit Native 3D Scatter Coordinates View
st.subheader("3-D Spatial Trajectory Mapping Field")
st.scatter_chart(df, x="X", y="Y", color="Frequency (Hz)", size="Node")
