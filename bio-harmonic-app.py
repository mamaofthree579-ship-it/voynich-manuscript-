import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# App Styling & Layout
st.set_page_config(page_title="Voynich Bio-Harmonic Dashboard", layout="wide")
st.title("📜 Voynich Manuscript Bio-Harmonic Wave Mechanics Engine")
st.caption("A multi-metric spatiotemporal decoder based on Archimedean spirals, Just Intonation, and Thermal Resonator Physics.")

# Sidebar Controls (The Metric Inputs)
st.sidebar.header("1. Foliar & Cosmic Inputs")
planetary_body = st.sidebar.selectbox("Planetary Macro-Gearing Target", ["Moon (4:3 - Fluidic Carrier)", "Sun (3:2 - Central Engine)", "Saturn/Mars (25:16 - Transmutation)"])
foliar_spiral_factor = st.sidebar.slider("Plant Archimedean Expansion Factor (b)", 0.05, 0.50, 0.22, step=0.01)

st.sidebar.header("2. Resonator Architecture")
vessel_material = st.sidebar.selectbox("Vessel Material Matrix", ["Thick Monastic Clay", "Early Venetian Glass"])
wall_thickness = st.sidebar.slider("Vessel Wall Thickness (mm)", 2.0, 15.0, 8.0, step=0.5)
ambient_temp = st.sidebar.slider("Ambient Storage Temperature (°C)", 0.0, 50.0, 20.0, step=1.0)

st.sidebar.header("3. Clinical Parameters")
disease_peak_panel = st.sidebar.slider("Disease Peak Clock Position (Panel 1-9)", 1, 9, 4, step=1)

# --- Mathematical Processing Engine ---
# 1. Base Frequency Calculation from Spiral Architecture
base_freq = 440.0 * (foliar_spiral_factor / 0.22)

# 2. Temperature Dependent Wave Speed Calculation (Newton-Laplace Fluid Mechanics)
# Base density of water ~1000 kg/m^3. Temperature expansion approximation used for bulk modulus shift.
fluid_density = 1000.0 - (0.2 * (ambient_temp - 20)) 
bulk_modulus = 2.15e9 * (1.0 + 0.003 * (ambient_temp - 20))
wave_speed = np.sqrt(bulk_modulus / fluid_density)

# Optimal wave velocity at 20°C calibrated baseline
optimal_wave_speed = 1466.3
wave_misalignment = abs(wave_speed - optimal_wave_speed)

# 3. Fourier's Law Thermal Dissipation Calculation
# Thermal conductivity (k): Clay = 0.2 W/mK, Glass = 0.9 W/mK
k_val = 0.2 if vessel_material == "Thick Monastic Clay" else 0.9
thermal_buffering_index = (wall_thickness / 1000.0) / k_val
retention_hours = thermal_buffering_index * 100.0 # Normalized systemic attenuation time scalar

# 4. Cosmological Phase Shift (180-Degree Counter-Hour Calibration)
# For a 9-panel clock wheel, 180 degrees opposite maps symmetrically.
counter_hour_panel = (disease_peak_panel + 4) if disease_peak_panel <= 4 else (disease_peak_panel - 4)
if disease_peak_panel == 9: 
    counter_hour_panel = 9 # Central neutral anchor point loops into itself

# --- Rendering the User Dashboard Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Harmonic Calculation Matrix")
    st.metric(label="Calculated Plant Oscillation", value=f"{base_freq:.2f} Hz")
    st.metric(label="Internal Fluid Wave Speed (c)", value=f"{wave_speed:.2f} m/s", delta=f"{wave_speed - optimal_wave_speed:.2f} m/s vs Baseline")
    st.metric(label="Vessel Thermal Retentivity Window", value=f"{retention_hours:.2f} Hours")

    # Wave-Node Realignment Visualization
    st.write("#### Boundary Standing Wave Node Alignment")
    x = np.linspace(0, 10, 500)
    ideal_wave = np.sin(x * (2 * np.pi * 440 / optimal_wave_speed))
    distorted_wave = np.sin(x * (2 * np.pi * base_freq / wave_speed))
    
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(x, ideal_wave, label="Optimal Node Target (3 Circles Etching)", color="teal", alpha=0.5)
    ax.plot(x, distorted_wave, label="Active Thermally-Drifted Wave", color="crimson")
    ax.set_facecolor('#0e1117')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    ax.legend(labelcolor='white')
    st.pyplot(fig)

with col2:
    st.subheader("⏳ Cosmological Phase Counter-Hour Timeline")
    st.info(f"Targeting Planetary Gearing Domain: **{planetary_body}**")
    
    # Text-Based Graphical representation of the 9-panel matrix
    st.write("#### 9-Panel Rosette Alignment Map")
    panels = ["P1: Dawn", "P2: Sunrise", "P3: Morning", "P4: Noon", "P5: Evening", "P6: Sunset", "P7: Dusk", "P8: Midnight", "P9: Core Neutral"]
    
    for idx, panel in enumerate(panels, 1):
        if idx == disease_peak_panel:
            st.markdown(f"🔴 **Panel {idx} ({panel})** \(\rightarrow\) **DISEASE PEAK HORIZON** (Maximum Systemic Disturbance)")
        elif idx == counter_hour_panel:
            st.markdown(f"🟢 **Panel {idx} ({panel})** \(\rightarrow\) **OPTIMAL CLINICAL DELIVERY SLOT** (180° Interference Neutralization)")
        else:
            st.text(f"⚪ Panel {idx} ({panel}): Baseline Vector")

    if wave_misalignment > 25.0:
        st.warning("⚠️ **CRITICAL WARNING:** High Thermal Wave Drift detected. The internal standing wave is misaligned with the vessel boundaries. Potency bleed occurring.")
    else:
        st.success("✅ **STABLE ENERGY PROFILE:** Standing wave node alignment locked within therapeutic tolerance parameters.")
