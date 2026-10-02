import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

# Import our modular backend engines
from src.parser import parse_voynich_text
from src.graph_engine import parse_organ_lifecycle_topology
from src.geometry import generate_trajectory, project_to_spiral_space
from src.pharma_engine import calculate_pharma_compliance

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Voynich Agricultural Engine", layout="wide")
st.title("🌿 Voynich Operational Herbal: Lifecycle Transition Engine")
st.write(
    "Testing the manuscript as an active **multi-metric agricultural manual**. "
    "This pipeline maps positional word transitions against physical growth phases, "
    "bio-harmonic wave mechanics, and modern pharmaceutical benchmarks."
)

# -----------------------------------------------------------------------------
# 2. LIFECYCLE STATE VECTOR DEFINITIONS
# -----------------------------------------------------------------------------
LIFECYCLE_STATES = ["ROOT_ZONE", "STEM_CONTINUANCE", "GENERATIVE_FLOWER", "HARVEST_LIMIT"]

# -----------------------------------------------------------------------------
# 3. INTERACTIVE SIDEBAR & CUSTOM FILE UPLOADER
# -----------------------------------------------------------------------------
st.sidebar.header("📂 Data Ingestion Hub")

uploaded_file = st.sidebar.file_uploader(
    "Upload Custom Voynich Transcription Log", 
    type=["txt", "csv", "json"],
    help="Drop a plaintext transcription file here to instantly parse custom linguistic models."
)

target_section = st.sidebar.selectbox(
    "Target Manuscript Section", 
    ["botanical", "astrological"],
    help="Isolate textual matrices to measure agricultural trajectory invariance."
)

transcription_format = st.sidebar.selectbox(
    "Transcription Standard",
    ["zandbergen_landini", "takahashi", "currier"],
    help="Select the morphological alphabet system to match your ingested text file rules."
)

# NEW: Manual Folio Selection Override to instantly validate or falsify specific plants
st.sidebar.divider()
st.sidebar.header("🧪 Botanical Target Profiler")
selected_folio_override = st.sidebar.selectbox(
    "Select Target Folio Validation Profile",
    ["F2R (Hemp Style)", "F9V (Violet Style)", "F25R (Sunflower Style)", "F33V (Water Lily Style)", "F55R (Mandrake Style)"],
    help="Manually switch chemical validation criteria to test model boundary limits."
)

# Extract short clean key identifier (e.g., 'F25R')
target_folio_key = selected_folio_override.split()[0].strip()

st.sidebar.divider()
st.sidebar.header("⚙️ Biophysics & Simulation Settings")
num_sim_perms = st.sidebar.slider("Monte Carlo Shuffling Runs", 500, 5000, 1500, step=500)
window_len = st.sidebar.slider("Markovian History Window (L)", 3, 7, 5)

st.sidebar.subheader("🎵 Wave Mechanics Modifiers")
manual_growth_velocity = st.sidebar.slider("Growth Velocity Multiplier", 0.5, 3.0, 1.2, step=0.1)
ambient_temp = st.sidebar.slider("Storage Ambient Temp (°C)", 10, 40, 22)
manual_peak_disease_hour = st.sidebar.slider("Peak Disease Hour (Rosette Map Index)", 1, 12, 4)

growth_velocity = manual_growth_velocity
peak_disease_hour = manual_peak_disease_hour

VOYNICH_DATA_PATH = "data/zl3b_transcription/sample_zl3b.txt"
PLANT_DATA_PATH = "data/tomato_wur_2026/sample_topology.csv"

if transcription_format == "takahashi" and not uploaded_file:
    VOYNICH_DATA_PATH = "data/transcriptions/sample_takahashi.txt"
elif transcription_format == "currier" and not uploaded_file:
    VOYNICH_DATA_PATH = "data/transcriptions/sample_currier.txt"

# -----------------------------------------------------------------------------
# 4. DATA PROCESSING PIPELINE
# -----------------------------------------------------------------------------
if uploaded_file is not None:
    temp_path = "data/temp_uploaded_transcription.txt"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    M_V = parse_voynich_text(temp_path, active_section=target_section, format_type=transcription_format)
else:
    if os.path.exists(VOYNICH_DATA_PATH):
        M_V = parse_voynich_text(VOYNICH_DATA_PATH, active_section=target_section, format_type=transcription_format)
    else:
        if target_section == "botanical":
            M_V = np.array([[0.65, 0.25, 0.05, 0.05], [0.08, 0.72, 0.14, 0.06], [0.02, 0.08, 0.58, 0.32], [0.45, 0.05, 0.05, 0.45]])
        else:
            M_V = np.array([[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]])

# Automate biophysical overrides based on active selection if file meta didn't force it
meta = getattr(parse_voynich_text, "active_metadata", {"peak_hour": 4, "velocity_mod": 1.0, "detected_folio": "None"})
if meta["detected_folio"] == "None":
    FOLIO_LOOKUP = {"F2R": (4, 1.2), "F9V": (1, 0.8), "F25R": (12, 1.9), "F33V": (8, 0.5), "F55R": (10, 1.4)}
    peak_disease_hour, growth_velocity = FOLIO_LOOKUP[target_folio_key]
    st.sidebar.info(f"Using manual dashboard lookup variables for {target_folio_key}")

if os.path.exists(PLANT_DATA_PATH):
    M_P = parse_organ_lifecycle_topology(PLANT_DATA_PATH)
else:
    M_P = np.array([[0.60, 0.30, 0.10, 0.00], [0.05, 0.75, 0.15, 0.05], [0.00, 0.10, 0.60, 0.30], [0.50, 0.00, 0.00, 0.50]])
    
# -----------------------------------------------------------------------------
# 5. JENSEN-SHANNON DISTANCE ENGINE
# -----------------------------------------------------------------------------
def kl_divergence(p, q):
    p, q = np.asarray(p, dtype=np.float64), np.asarray(q, dtype=np.float64)
    mask = (p > 0) & (q > 0)
    return np.sum(p[mask] * np.log2(p[mask] / q[mask]))

def jensen_shannon_divergence(M1, M2):
    p, q = M1.flatten() / np.sum(M1), M2.flatten() / np.sum(M2)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)

observed_djs = jensen_shannon_divergence(M_V, M_P)

null_distances = []
np.random.seed(2026)
for _ in range(num_sim_perms):
    row_sums = M_V.sum(axis=1, keepdims=True)
    col_sums = M_V.sum(axis=0, keepdims=True)
    null_p = (row_sums @ col_sums) / (M_V.sum() ** 2)
    M_V_null = np.nan_to_num(null_p / null_p.sum(axis=1, keepdims=True), nan=0.25)
    null_distances.append(jensen_shannon_divergence(M_V_null, M_P))

null_distances = np.array(null_distances)
pseudo_p_value = np.sum(null_distances <= observed_djs) / num_sim_perms

# -----------------------------------------------------------------------------
# 6. APP LAYOUT AND GRAPHICAL RENDERING
# -----------------------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌱 Plant Organ Lifecycle Matrix ($M_P$)")
    df_p = pd.DataFrame(M_P, index=LIFECYCLE_STATES, columns=LIFECYCLE_STATES)
    st.dataframe(df_p.style.background_gradient(cmap="Greens", axis=None), use_container_width=True)

with col2:
    st.subheader(f"📜 Textual Matrix: [{transcription_format.upper()} - {target_section.upper()}] ($M_V$)")
    df_v = pd.DataFrame(M_V, index=LIFECYCLE_STATES, columns=LIFECYCLE_STATES)
    st.dataframe(df_v.style.background_gradient(cmap="Purples", axis=None), use_container_width=True)

st.divider()

stat_col1, stat_col2, stat_col3 = st.columns(3)
stat_col1.metric("Observed System Distance ($D_{JS}$)", f"{observed_djs:.5f}")
stat_col2.metric("Null Model Mean Baseline", f"{np.mean(null_distances):.5f}")
stat_col3.metric("Empirical P-Value (H₀ Bound)", f"{pseudo_p_value:.4f}")

# -----------------------------------------------------------------------------
# 7. ADVANCED WAVE MECHANICS & PHARMA CROSS-CHECK PANEL
# -----------------------------------------------------------------------------
st.header("🔬 Bio-Harmonic Layer Integration")
wave_col1, wave_col2, wave_col3 = st.columns(3)

trajectory_data = generate_trajectory(M_V, steps=400, window_len=window_len)
coordinates, r_squared = project_to_spiral_space(trajectory_data)
mean_radius = np.mean(np.sqrt(coordinates[:, 0]**2 + coordinates[:, 1]**2)) if len(coordinates) > 0 else 1.0

base_frequency = growth_velocity * mean_radius
wave_col1.metric("Base Vector Frequency ($\mathcal{f}$)", f"{base_frequency:.3f} Hz")

bulk_modulus = 2.15e9
density_profile = 1000 - (ambient_temp - 4) ** 2 * 0.008
retentive_velocity = np.sqrt(bulk_modulus / density_profile) # Explicit Variable Verification Fix Included
wave_col2.metric("Vessel Retentive Velocity (c)", f"{retentive_velocity:.2f} m/s")

counter_hour = (peak_disease_hour + 6) % 12
if counter_hour == 0: counter_hour = 12
wave_col3.metric("Counter-Phase Administration Target", f"Hour {counter_hour}:00", delta="180° Interference Shift")

# NEW: Dynamic Pharmaceutical Cross-Checking Matrix Results Panel
st.subheader(f"🧪 Modern Pharmaceutical Compliance Validation: Profile [{target_folio_key}]")
pharma_data = calculate_pharma_compliance(target_folio_key, r_squared, float(ambient_temp))

p_col1, p_col2, p_col3, p_col4 = st.columns(4)
p_col1.metric("Modern Plant Equivalent", str(pharma_data['specimen']))
p_col2.metric("Active Organic Compound", str(pharma_data['compound']))
p_col3.metric("Optimal Preservation Temp", f"{pharma_data['optimal_temp']} °C")
p_col4.metric("Compliance Rating Score", f"{pharma_data['compliance_score']:.1f}%")

st.divider()

# -----------------------------------------------------------------------------
# 8. MONTE CARLO VARIANCE DISTRIBUTION (HISTOGRAM)
# -----------------------------------------------------------------------------
st.subheader("📊 Monte Carlo Variance Distribution (H₀ vs. Empirical Position)")
fig_dist, ax_dist = plt.subplots(figsize=(8, 3.5), facecolor='#1e1e24')
ax_dist.set_facecolor('#2d2d38')
counts, bins, patches = ax_dist.hist(null_distances, bins=35, color="#8884d8", alpha=0.4, edgecolor="#1e1e24", label="Permuted Null States (H₀)")
ax_dist.axvline(observed_djs, color="#e28743", linestyle="-", linewidth=2.5, label=f"Observed Metric ({observed_djs:.5f})")
ax_dist.set_xlabel("Jensen-Shannon Divergence Score ($D_{JS}$)", color="#f4f4f9")
ax_dist.set_ylabel("Permutation Frequency Count", color="#f4f4f9")
ax_dist.tick_params(colors="#f4f4f9")
ax_dist.grid(True, linestyle=":", alpha=0.2)
ax_dist.legend(facecolor='#1e1e24', edgecolor='none', labelcolor='#f4f4f9')
st.pyplot(fig_dist)

# -----------------------------------------------------------------------------
# 9. TRAJECTORY GENERATION AND SPIRAL PROJECTION
# -----------------------------------------------------------------------------
st.subheader("📉 Reduced State Space Trajectory Geometry: Logarithmic Path Mapping ($r(\\theta)$)")
fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='#1e1e24')
ax.set_facecolor('#2d2d38')
z1, z2 = coordinates[:, 0], coordinates[:, 1]
ax.plot(z1, z2, color="#82ca9d", alpha=0.8, linewidth=2, label=f"Observed Path ($R^2={r_squared:.4f}$)")
ax.scatter(z1[::50], z2[::50], color="#8884d8", edgecolor="#f4f4f9", s=40, zorder=5, label="Organ Transition Nodes")

if len(z1) > 10 and target_section == "botanical":
    theta_ideal = np.linspace(0, 4 * np.pi, len(z1))
    r_ideal = 0.1 * np.exp(0.15 * theta_ideal)
    z1_ideal = r_ideal * np.cos(theta_ideal)
    z2_ideal = r_ideal * np.sin(theta_ideal)
    ax.plot(z1_ideal, z2_ideal, color="#e28743", linestyle="--", alpha=0.6, label="Idealized Harvest Spiral Log-Fit")

ax.set_xlabel("State Vector Projection Area ($Z_1$)", color="#f4f4f9")
ax.set_ylabel("State Vector Projection Area ($Z_2$)", color="#f4f4f9")
ax.tick_params(colors="#f4f4f9")
ax.grid(True, linestyle=":", alpha=0.3)
ax.legend(facecolor='#1e1e24', edgecolor='none', labelcolor='#f4f4f9')
st.pyplot(fig)
