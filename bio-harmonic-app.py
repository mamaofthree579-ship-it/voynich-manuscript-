import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Master Config
st.set_page_config(page_title="Voynich Master Bio-Harmonic Engine", layout="wide")
st.title("📜 Voynich Manuscript Master Bio-Harmonic Engine")
st.caption("Comprehensive GitHub/Streamlit Build: Integrating Foliar Spirals, Multi-Plant Compounding, Resonator Impedance, and Organ Profiles.")

# Sidebar - System Configurations
st.sidebar.header("1. Clinical Pathology Profile")
pathology = st.sidebar.selectbox("Select Target Tissue System", [
    "General Baseline Tuning",
    "Neurological Overdrive (CNS Burnout)",
    "Hepatic Stagnation (Tissue Hardening)",
    "Respiratory Degradation (Elasticity Loss)"
])

st.sidebar.header("2. Botanical Compounding Engine")
compounding_mode = st.sidebar.checkbox("Enable Multi-Plant Compounding (Recipes Section)", value=False)
plant_a_factor = st.sidebar.slider("Plant A Spiral Factor", 0.05, 0.50, 0.22, step=0.01)
plant_b_factor = st.sidebar.slider("Plant B Spiral Factor (Ingredient B)", 0.05, 0.50, 0.15, step=0.01) if compounding_mode else 0.0

st.sidebar.header("3. Cosmic Gearing & Resonator")
planetary_body = st.sidebar.selectbox("Planetary Macro-Multiplier", ["Moon (4:3 Ratio)", "Sun (3:2 Ratio)", "Saturn/Mars (25:16 Ratio)"])
vessel_material = st.sidebar.selectbox("Vessel Composition Matrix", ["Thick Monastic Clay", "Early Venetian Glass"])
neck_geometry = st.sidebar.selectbox("Neck Geometry (Acoustic Transformer)", ["Cylindrical Restricted", "Exponential Flared"])
wall_thickness = st.sidebar.slider("Wall Thickness (mm)", 2.0, 15.0, 8.0, step=0.5)
ambient_temp = st.sidebar.slider("Storage Cellar Temperature (°C)", 0.0, 50.0, 15.0, step=1.0)

# --- Dynamic Automated Presets based on User Pathology Selection ---
if pathology == "Neurological Overdrive (CNS Burnout)":
    disease_peak = 4  # Noon
elif pathology == "Hepatic Stagnation (Tissue Hardening)":
    disease_peak = 6  # Sunset
elif pathology == "Respiratory Degradation (Elasticity Loss)":
    disease_peak = 1  # Dawn
else:
    disease_peak = st.sidebar.slider("Manual Disease Peak Position (Panel 1-9)", 1, 9, 4, step=1)

# --- Core Wave Mechanics Processing Engine ---
# Calculate Base Frequencies
f1 = 440.0 * (plant_a_factor / 0.22)
f2 = 440.0 * (plant_b_factor / 0.22) if compounding_mode else 0.0
target_freq = abs(f1 - f2) if compounding_mode else f1

# Fluid Thermodynamics (Newton-Laplace Equation)
fluid_density = 1000.0 - (0.2 * (ambient_temp - 20))
bulk_modulus = 2.15e9 * (1.0 + 0.003 * (ambient_temp - 20))
wave_speed = np.sqrt(bulk_modulus / fluid_density)
optimal_speed = 1466.3

# Fourier's Law Insulation Scalar
k_val = 0.2 if vessel_material == "Thick Monastic Clay" else 0.9
thermal_buffering = (wall_thickness / 1000.0) / k_val
retention_hours = thermal_buffering * 100.0

# 180-Degree Chrono-Shift Engine
counter_hour = (disease_peak + 4) if disease_peak <= 4 else (disease_peak - 4)
if disease_peak == 9: counter_hour = 9

# --- Render Dashboard UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Integrated Biophysics Metrics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Target Output Freq", f"{target_freq:.1f} Hz")
    m2.metric("Liquid Wave Velocity", f"{wave_speed:.1f} m/s")
    m3.metric("Insulation Buffer", f"{retention_hours:.1f} Hrs")
    
    if compounding_mode:
        st.caption(f"🧪 **Compounding Active:** Plant A ({f1:.1f} Hz) + Plant B ({f2:.1f} Hz) generates a **{target_freq:.1f} Hz Beat Envelope**.")

    # Live Waves Graph
    st.write("#### Boundary Standing Wave Interference Plot")
    x = np.linspace(0, 10, 500)
    # Generate wave geometry based on neck configuration
    k_factor = 1.5 if neck_geometry == "Exponential Flared" else 1.0
    active_wave = np.sin(x * (2 * np.pi * target_freq / wave_speed)) * np.exp(-x * 0.02 * k_factor)
    ideal_wave = np.sin(x * (2 * np.pi * 440 / optimal_speed))
    
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot(x, ideal_wave, label="Boundary Target (3 Circles)", color="teal", alpha=0.4, linestyle="--")
    ax.plot(x, active_wave, label="Active Resonator Output Wave", color="#FF4B4B")
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.legend(labelcolor='white')
    st.pyplot(fig)

with col2:
    st.subheader("🌌 Cosmological Time Shift Matrix")
    st.markdown(f"**Target System:** `{pathology}` | **Macro Multiplier Axis:** `{planetary_body}`")
    
    # 9-Panel Display Block
    panels = ["Dawn", "Sunrise", "Morning", "Noon", "Evening", "Sunset", "Dusk", "Midnight", "Core Neutral Anchor"]
    st.write("#### Timeline Vector Diagnostics")
    
    for idx, name in enumerate(panels, 1):
        if idx == disease_peak:
            st.markdown(f"🔴 **Panel {idx} ({name})** \(\rightarrow\) **Disease Maximum Amplitude**")
        elif idx == counter_hour:
            st.markdown(f"... 🟢 **Panel {idx} ({name})** \(\rightarrow\) **180° Counter-Hour Infusion Vector**")
        else:
            st.text(f"    ⚪ Panel {idx} ({name}): Neutral Gradient Vector")

    # Diagnostic Safeguards
    st.write("#### System Stability Diagnostics")
    drift = abs(wave_speed - optimal_speed)
    if drift > 30.0:
        st.error(f"❌ **THERMAL DRIFT CRITICAL:** Cellar temp ({ambient_temp}°C) and {vessel_material} choice cause severe wave distortion. Nodes have slipped off boundary markers.")
    else:
        st.success("✅ **RESONATOR STABLE:** Standing wave nodes safely locked into biological interface tolerance.")
