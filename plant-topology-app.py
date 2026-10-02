import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Import our complete multi-metric analytical modules
from src.parser import parse_voynich_text
from src.graph_engine import parse_organ_lifecycle_topology
from src.geometry import generate_trajectory, project_to_spiral_space
from src.pharma_engine import calculate_pharma_compliance
from src.rosette import calculate_rosette_spatial_resonance
from src.ledger import initialize_ledger, append_to_ledger

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METRICS INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Voynich Agricultural Engine", layout="wide")
initialize_ledger()

st.title("🌿 Voynich Operational Herbal: Lifecycle Transition Engine")
st.write(
    "Testing the manuscript as an active **multi-metric agricultural manual**. "
    "This platform maps positional word transitions against physical growth phases, "
    "9-Panel Rosette multi-axial clocks, and modern pharmaceutical compliance metrics."
)

# -----------------------------------------------------------------------------
# 2. INTERACTIVE SIDEBAR CONTROL HUB
# -----------------------------------------------------------------------------
st.sidebar.header("📂 Data Ingestion Hub")

uploaded_file = st.sidebar.file_uploader(
    "Upload Custom Voynich Transcription Log", type=["txt", "csv", "json"]
)

target_section = st.sidebar.selectbox(
    "Target Manuscript Section", ["botanical", "astrological"]
)

transcription_format = st.sidebar.selectbox(
    "Transcription Standard", ["zandbergen_landini", "takahashi", "currier"]
)

# NEW: 3-Phase Botanical Maturity Dropdown Selector
st.sidebar.divider()
st.sidebar.header("🍃 Operational Lifecycles")
selected_maturity = st.sidebar.selectbox(
    "Active Specimen Maturity Index",
    ["Young Vegetative", "Peak Flowering", "Dried Prep/Storage"]
)

# NEW: 9-Panel Rosette Spatial Orientation Routing Dial
st.sidebar.divider()
st.sidebar.header("🌌 Rosette Spatial Lenses")
rosette_panel = st.sidebar.slider(
    "Rosette Panel Matrix Selector", 1, 9, 1,
    help="Route wave metrics through the manuscript's 9-Panel master fold-out diagram."
)

st.sidebar.divider()
st.sidebar.header("🧪 Botanical Target Profiler")
selected_folio_override = st.sidebar.selectbox(
    "Select Target Folio Validation Profile",
    ["F2R (Hemp Style)", "F9V (Violet Style)", "F25R (Sunflower Style)", "F33V (Water Lily Style)", "F55R (Mandrake Style)"]
)
target_folio_key = selected_folio_override.split()[0].strip()

st.sidebar.divider()
st.sidebar.header("⚙️ Simulation Settings")
num_sim_perms = st.sidebar.slider("Monte Carlo Shuffling Runs", 500, 5000, 1500, step=500)
window_len = st.sidebar.slider("Markovian History Window (L)", 3, 7, 5)

st.sidebar.subheader("🎵 Wave Mechanics Modifiers")
manual_growth_velocity = st.sidebar.slider("Growth Velocity Multiplier", 0.5, 3.0, 1.2, step=0.1)
ambient_temp = st.sidebar.slider("Storage Ambient Temp (°C)", 10, 40, 22)
manual_peak_disease_hour = st.sidebar.slider("Peak Disease Hour (Rosette Map Index)", 1, 12, 4)

growth_velocity = manual_growth_velocity
peak_disease_hour = manual_peak_disease_hour

LIFECYCLE_STATES = ["ROOT_ZONE", "STEM_CONTINUANCE", "GENERATIVE_FLOWER", "HARVEST_LIMIT"]
VOYNICH_DATA_PATH = "data/zl3b_transcription/sample_zl3b.txt"
PLANT_DATA_PATH = "data/tomato_wur_2026/sample_topology.csv"

if transcription_format == "takahashi" and not uploaded_file:
    VOYNICH_DATA_PATH = "data/transcriptions/sample_takahashi.txt"
elif transcription_format == "currier" and not uploaded_file:
    VOYNICH_DATA_PATH = "data/transcriptions/sample_currier.txt"

# -----------------------------------------------------------------------------
# 3. PIPELINE PROCESSING EXECUTIONS
# -----------------------------------------------------------------------------
if uploaded_file is not None:
    temp_path = "data/temp_uploaded_transcription.txt"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    M_V = parse_voynich_text(temp_path, active_section=target_section, format_type=transcription_format, growth_phase=selected_maturity)
else:
    if os.path.exists(VOYNICH_DATA_PATH):
        M_V = parse_voynich_text(VOYNICH_DATA_PATH, active_section=target_section, format_type=transcription_format, growth_phase=selected_maturity)
    else:
        if target_section == "botanical":
            M_V = np.array([[0.65, 0.25, 0.05, 0.05], [0.08, 0.72, 0.14, 0.06], [0.02, 0.08, 0.58, 0.32], [0.45, 0.05, 0.05, 0.45]])
        else:
            M_V = np.array([[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]])

FOLIO_LOOKUP = {"F2R": (4, 1.2), "F9V": (1, 0.8), "F25R": (12, 1.9), "F33V": (8, 0.5), "F55R": (10, 1.4)}
peak_disease_hour, growth_velocity = FOLIO_LOOKUP[target_folio_key]

if os.path.exists(PLANT_DATA_PATH):
    M_P = parse_organ_lifecycle_topology(PLANT_DATA_PATH)
else:
    M_P = np.array([[0.60, 0.30, 0.10, 0.00], [0.05, 0.75, 0.15, 0.05], [0.00, 0.10, 0.60, 0.30], [0.50, 0.00, 0.00, 0.50]])
# Save as the second half of plant-topology-app.py
# -----------------------------------------------------------------------------
# 4. MATH ANALYTICS ENGINES
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
# 5. UI DISPLAY MATRIX TABLES
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
# 6. ADVANCED WAVE MECHANICS, THERMODYNAMICS, AND COUNTER-PHASES
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
base_retentive_velocity = np.sqrt(bulk_modulus / density_profile)

# Save as the updated Rosette Mapping Block inside plant-topology-app.py
# Route calculated base velocities directly through the 9-Panel Spatial Array
rosette_data = calculate_rosette_spatial_resonance(rosette_panel, base_retentive_velocity)

# Dynamically couple the Rosette resonance index to subtly tune the final compliance readout
pharma_data = calculate_pharma_compliance(target_folio_key, r_squared, float(ambient_temp))
tuned_compliance = min(100.0, max(0.0, pharma_data['compliance_score'] * rosette_data['resonance_index']))

p_col1, p_col2, p_col3, p_col4 = st.columns(4)
p_col1.metric("Modern Plant Equivalent", str(pharma_data['specimen']))
p_col2.metric("Active Organic Compound", str(pharma_data['compound']))
p_col3.metric("Optimal Preservation Temp", f"{pharma_data['optimal_temp']} °C")
p_col4.metric("Tuned Compliance Score", f"{tuned_compliance:.1f}%", delta=f"Lens Shift: {(rosette_data['resonance_index'] - 1.0)*100:.1f}%")


counter_hour = (peak_disease_hour + 6) % 12
if counter_hour == 0: counter_hour = 12
wave_col3.metric("Counter-Phase Administration Target", f"Hour {counter_hour}:00", delta="180° Interference Shift")

# -----------------------------------------------------------------------------
# 7. PHARMA CROSS-CHECK & PERSISTENT DATA LEDGER
# -----------------------------------------------------------------------------
st.subheader(f"🧪 Modern Pharmaceutical Compliance Validation: Profile [{target_folio_key}]")
pharma_data = calculate_pharma_compliance(target_folio_key, r_squared, float(ambient_temp))

p_col1, p_col2, p_col3, p_col4 = st.columns(4)
p_col1.metric("Modern Plant Equivalent", str(pharma_data['specimen']))
p_col2.metric("Active Organic Compound", str(pharma_data['compound']))
p_col3.metric("Optimal Preservation Temp", f"{pharma_data['optimal_temp']} °C")
p_col4.metric("Compliance Rating Score", f"{pharma_data['compliance_score']:.1f}%")

# Active Logger Input Button
if st.button("💾 Capture & Append Current Run to Master Ledger"):
    append_to_ledger(target_folio_key, target_section, observed_djs, r_squared, pharma_data['compound'], pharma_data['compliance_score'])
    st.toast(f"Logged {target_folio_key} records successfully!", icon="📝")

st.subheader("📝 Repository Performance Scoreboard Ledger")
st.dataframe(st.session_state.research_ledger, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 8. DATA VISUALIZATIONS (HISTOGRAM AND RADIAL CLOCK)
# -----------------------------------------------------------------------------
st.subheader("📊 Monte Carlo Variance Distribution (H₀ vs. Empirical Position)")
fig_dist, ax_dist = plt.subplots(figsize=(8, 2.5), facecolor='#1e1e24')
ax_dist.set_facecolor('#2d2d38')
counts, bins, patches = ax_dist.hist(null_distances, bins=35, color="#8884d8", alpha=0.4, edgecolor="#1e1e24")
ax_dist.axvline(observed_djs, color="#e28743", linestyle="-", linewidth=2.5, label=f"Observed Metric ({observed_djs:.5f})")
ax_dist.set_xlabel("Jensen-Shannon Divergence Score ($D_{JS}$)", color="#f4f4f9")
ax_dist.tick_params(colors="#f4f4f9")
ax_dist.grid(True, linestyle=":", alpha=0.2)
st.pyplot(fig_dist)

st.subheader("📉 System Trajectory Space & Counter-Phase Delivery Geometry")
vis_col1, vis_col2 = st.columns(2)

with vis_col1:
    fig_spiral, ax_spiral = plt.subplots(figsize=(6, 4.5), facecolor='#1e1e24')
    ax_spiral.set_facecolor('#2d2d38')
    z1, z2 = coordinates[:, 0], coordinates[:, 1]
    ax_spiral.plot(z1, z2, color="#82ca9d", alpha=0.8, linewidth=2, label=f"Observed Path ($R^2={r_squared:.4f}$)")
    ax_spiral.scatter(z1[::50], z2[::50], color="#8884d8", edgecolor="#f4f4f9", s=40, zorder=5)
    if len(z1) > 10 and target_section == "botanical":
        theta_ideal = np.linspace(0, 4 * np.pi, len(z1))
        r_ideal = 0.1 * np.exp(0.15 * theta_ideal)
        ax_spiral.plot(r_ideal * np.cos(theta_ideal), r_ideal * np.sin(theta_ideal), color="#e28743", linestyle="--", alpha=0.6, label="Idealized Log-Spiral")
    ax_spiral.set_xlabel("Z₁ Space", color="#f4f4f9")
    ax_spiral.set_ylabel("Z₂ Space", color="#f4f4f9")
    ax_spiral.tick_params(colors="#f4f4f9")
    ax_spiral.grid(True, linestyle=":", alpha=0.3)
    ax_spiral.legend(facecolor='#1e1e24', edgecolor='none', labelcolor='#f4f4f9', loc="upper left")
    st.pyplot(fig_spiral)

with vis_col2:
    fig_clock, ax_clock = plt.subplots(figsize=(6, 4.5), subplot_kw={'projection': 'polar'}, facecolor='#1e1e24')
    ax_clock.set_facecolor('#2d2d38')
    disease_angle = (3 - peak_disease_hour) * (2*np.pi / 12)
    admin_angle = (3 - counter_hour) * (2*np.pi / 12)
    ax_clock.annotate("", xy=(disease_angle, 1.0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#ef5350", linewidth=3))
    ax_clock.annotate("", xy=(admin_angle, 1.0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="#66bb6a", linewidth=3))
    ax_clock.set_theta_zero_location("N")
    ax_clock.set_theta_direction(-1)
    ax_clock.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
    ax_clock.set_xticklabels([str(i if i != 0 else 12) for i in range(12)], color="#f4f4f9")
    ax_clock.set_yticklabels([])
    ax_clock.grid(True, color="#f4f4f9", alpha=0.1)
    ax_clock.plot([], [], color="#ef5350", label="Peak Pathology Intensity Hour")
    ax_clock.plot([], [], color="#66bb6a", label="180° Balanced Administration Hour")
    ax_clock.legend(facecolor='#1e1e24', edgecolor='none', labelcolor='#f4f4f9', loc="lower center", bbox_to_anchor=(0.5, -0.2))
    st.pyplot(fig_clock)
