import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Master Config
st.set_page_config(page_title="Voynich Master Bio-Harmonic Engine", layout="wide")
st.title("📜 Voynich Manuscript Master Bio-Harmonic Engine")
st.caption("Comprehensive GitHub Build: Integrating Foliar Spirals, Multi-Plant Compounding, Variable Fluid Mediums, and Interactive SVG Seal Drafting.")

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

st.sidebar.header("3. Medium & Extraction Vehicle")
fluid_medium = st.sidebar.selectbox("Fluid Extraction Medium", ["Water-Based Infusion", "Wine/Alcohol Carrier", "Infused Vegetable Oil Base"])

st.sidebar.header("4. Cosmic Gearing & Resonator")
planetary_body = st.sidebar.selectbox("Planetary Macro-Multiplier", ["Moon (4:3 Ratio)", "Sun (3:2 Ratio)", "Saturn/Mars (25:16 Ratio)"])
vessel_material = st.sidebar.selectbox("Vessel Composition Matrix", ["Thick Monastic Clay", "Early Venetian Glass"])
neck_geometry = st.sidebar.selectbox("Neck Geometry (Acoustic Transformer)", ["Cylindrical Restricted", "Exponential Flared"])
wall_thickness = st.sidebar.slider("Wall Thickness (mm)", 2.0, 15.0, 8.0, step=0.5)
ambient_temp = st.sidebar.slider("Storage Cellar Temperature (°C)", 0.0, 50.0, 15.0, step=1.0)

# --- Dynamic Automated Presets ---
if pathology == "Neurological Overdrive (CNS Burnout)":
    disease_peak = 4  # Noon
elif pathology == "Hepatic Stagnation (Tissue Hardening)":
    disease_peak = 6  # Sunset
elif pathology == "Respiratory Degradation (Elasticity Loss)":
    disease_peak = 1  # Dawn
else:
    disease_peak = st.sidebar.slider("Manual Disease Peak Position (Panel 1-9)", 1, 9, 4, step=1)

# --- Core Wave Mechanics Processing Engine ---
f1 = 440.0 * (plant_a_factor / 0.22)
f2 = 440.0 * (plant_b_factor / 0.22) if compounding_mode else 0.0
target_freq = abs(f1 - f2) if compounding_mode else f1

# Base Thermodynamic Shifting (Water vs Alcohol vs Oil)
if fluid_medium == "Wine/Alcohol Carrier":
    base_density = 789.0; base_bulk = 1.06e9; optimal_speed = 1162.0
elif fluid_medium == "Infused Vegetable Oil Base":
    base_density = 915.0; base_bulk = 1.86e9; optimal_speed = 1424.0
else: # Water Baseline
    base_density = 1000.0; base_bulk = 2.15e9; optimal_speed = 1466.3

fluid_density = base_density - (0.2 * (ambient_temp - 20))
bulk_modulus = base_bulk * (1.0 + 0.003 * (ambient_temp - 20))
wave_speed = np.sqrt(bulk_modulus / fluid_density)

k_val = 0.2 if vessel_material == "Thick Monastic Clay" else 0.9
thermal_buffering = (wall_thickness / 1000.0) / k_val
retention_hours = thermal_buffering * 100.0

counter_hour = (disease_peak + 4) if disease_peak <= 4 else (disease_peak - 4)
if disease_peak == 9: counter_hour = 9

# --- Dynamic Triple-Circle Seal Calculations ---
wavelength_mm = (wave_speed / target_freq) * 1000.0
r1 = 25.0 
r2 = r1 * np.sqrt(2)
r3 = r1 * 1.618

depth1 = (wavelength_mm / 4.0)
while depth1 > 5.0:  
    depth1 /= 2.0
depth2 = depth1 / 2.0

# --- Render Dashboard UI Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Integrated Biophysics Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Target Output Freq", f"{target_freq:.1f} Hz")
    m2.metric("Liquid Wave Velocity", f"{wave_speed:.1f} m/s")
    m3.metric("Insulation Buffer", f"{retention_hours:.1f} Hrs")
    
    st.write("#### Boundary Standing Wave Interference Plot")
    x = np.linspace(0, 10, 500)
    k_factor = 1.5 if neck_geometry == "Exponential Flared" else 1.0
    active_wave = np.sin(x * (2 * np.pi * target_freq / wave_speed)) * np.exp(-x * 0.02 * k_factor)
    ideal_wave = np.sin(x * (2 * np.pi * 440 / optimal_speed))
    
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, ideal_wave, color="teal", alpha=0.4, linestyle="--", label="Target Medium Baseline")
    ax.plot(x, active_wave, color="#FF4B4B", label="Active Extraction Output")
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.legend(labelcolor='white')
    st.pyplot(fig)

with col2:
    st.subheader("⏳ Cosmological Time Shift Matrix")
    panels = ["Dawn", "Sunrise", "Morning", "Noon", "Evening", "Sunset", "Dusk", "Midnight", "Core Neutral Anchor"]
    
    for idx, name in enumerate(panels, 1):
        if idx == disease_peak:
            st.markdown(f"🔴 **Panel {idx} ({name})** \(\rightarrow\) **Disease Max Amplitude**")
        elif idx == counter_hour:
            st.markdown(f"🟢 **Panel {idx} ({name})** \(\rightarrow\) **180° Counter-Hour Infusion Vector**")
        else:
            st.text(f"    ⚪ Panel {idx} ({name})")

    # Render Vector Blueprint Section
    st.write("#### 🔘 Interactive Triple-Circle Seal SVG Blueprint")
    st.caption(f"Medium Channel Profile: {fluid_medium} | Inner Ring Cut Depth: {depth1:.2f}mm")
    
    svg_blueprint = f"""
    <svg width="100%" height="200" viewBox="0 0 200 200" xmlns="http://w3.org">
        <rect width="100%" height="100%" fill="#0e1117"/>
        <circle cx="100" cy="100" r="{r3 * 1.5}" stroke="#FF4B4B" stroke-width="1.5" fill="none" stroke-dasharray="4"/>
        <circle cx="100" cy="100" r="{r2 * 1.5}" stroke="teal" stroke-width="2" fill="none"/>
        <circle cx="100" cy="100" r="{r1 * 1.5}" stroke="white" stroke-width="3" fill="none"/>
        <circle cx="100" cy="100" r="3" fill="#FF4B4B"/>
        <text x="10" y="20" fill="white" font-size="10" font-family="monospace">Medium Checked: {fluid_medium[:12]}...</text>
    </svg>
    """
    st.components.v1.html(svg_blueprint, height=210)
