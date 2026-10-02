import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import sqlite3
import os

# --- 1. ENVIRONMENT & DATABASE INITIALIZATION MATRIX ---
os.makedirs("temp", exist_ok=True)
conn = sqlite3.connect("temp/voynich_database.db", check_same_thread=False)
cursor = conn.cursor()

# Create structural ledger table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    system_mode TEXT,
    pathology_or_circuit TEXT,
    plant_a REAL,
    plant_b REAL,
    fluid_medium TEXT,
    planetary_body TEXT,
    vessel_material TEXT,
    neck_geometry TEXT
)
""")
conn.commit()

# Automated Seed Engine: Populating the Master Historical Archetypes
default_presets = [
    ("Folio 2v: Neurological Overdrive", "Organ-Tissue Pathology", "Neurological Overdrive (CNS Burnout)", 0.22, 0.00, "Water-Based Infusion", "Sun (3:2 Ratio)", "Thick Monastic Clay", "Cylindrical Restricted"),
    ("Folio 78r: Lymphatic Circuit", "Balneological Fluid Circuits", "Clover Resonator (Folio 78r Preset)", 0.11, 0.05, "Wine/Alcohol Carrier", "Moon (4:3 Ratio)", "Early Venetian Glass", "Cylindrical Restricted"),
    ("Hepatic Tissue Hardening Matrix", "Organ-Tissue Pathology", "Hepatic Stagnation (Tissue Hardening)", 0.22, 0.00, "Wine/Alcohol Carrier", "Moon (4:3 Ratio)", "Early Venetian Glass", "Cylindrical Restricted")
]

for preset in default_presets:
    try:
        cursor.execute("""
        INSERT INTO profiles (name, system_mode, pathology_or_circuit, plant_a, plant_b, fluid_medium, planetary_body, vessel_material, neck_geometry)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, preset)
        conn.commit()
    except sqlite3.IntegrityError:
        # Preset already exists in ledger database; proceed silently
        pass


# Sidebar - System Configurations
st.sidebar.header("1. Framework System Mode")
system_mode = st.sidebar.selectbox("Select Analysis Matrix", [
    "Zodiac Carrier Modulators", 
    "Balneological Fluid Circuits", 
    "Organ-Tissue Pathology", 
    "Pharmaceutical Vessel Tuning"
])

if system_mode == "Organ-Tissue Pathology":
    pathology = st.sidebar.selectbox("Select Target Tissue System", [
        "General Baseline Tuning",
        "Neurological Overdrive (CNS Burnout)",
        "Hepatic Stagnation (Tissue Hardening)",
        "Respiratory Degradation (Elasticity Loss)"
    ])
elif system_mode == "Balneological Fluid Circuits":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌊 Hydro-Circuit Variables")
    pool_geometry = st.sidebar.selectbox("Manuscript Pool Geometry Blueprint", ["Clover Resonator (Folio 78r Preset)", "Semicircle Mixer", "Stepped Cascading Basin"])
    tube_diameter_mm = st.sidebar.slider("Tube Width Metric (D)", 1.0, 10.0, 2.8 if "Clover" in pool_geometry else 3.5, step=0.1)
    flow_velocity_mms = st.sidebar.slider("Biological Flow Velocity (v)", 0.5, 5.0, 1.4 if "Clover" in pool_geometry else 1.2, step=0.1)
elif system_mode == "Zodiac Carrier Modulators":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌌 Astrological Carrier Gearing")
    zodiac_axis = st.sidebar.selectbox("Zodiac Wheel Quadrant", ["Vernal Axis (Aries/Taurus)", "Autumnal Axis (Scorpio/Sagittarius)"])
    spoke_count = st.sidebar.slider("Illustrated Boundary Spokes", 12, 36, 30, step=2)
else:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚱️ Vessel Boundary Metrics")
    vessel_profile = st.sidebar.selectbox("Marginalia Drawing Style", ["Wide Cylindrical Base", "Narrow Tapered Amphora"])
    vessel_volume_ml = st.sidebar.slider("Calculated Chamber Volume (V)", 50, 1000, 250, step=50)
    neck_length_mm = st.sidebar.slider("Illustrated Throat Length (L)", 10, 100, 35, step=5)

st.sidebar.header("2. Triple-Plant Compounding Engine")
compounding_tier = st.sidebar.selectbox("Compounding Complexity", ["Single Herb Extract", "Dual-Plant Compounding", "Triple-Plant Envelope"])
plant_a_factor = st.sidebar.slider("Plant A Spiral Factor", 0.05, 0.50, 0.22, step=0.01)
plant_b_factor = st.sidebar.slider("Plant B Spiral Factor", 0.05, 0.50, 0.15, step=0.01) if compounding_tier != "Single Herb Extract" else 0.0
plant_c_factor = st.sidebar.slider("Plant C Spiral Factor", 0.05, 0.50, 0.11, step=0.01) if compounding_tier == "Triple-Plant Envelope" else 0.0

st.sidebar.header("3. Medium & Closure Mechanics")
fluid_medium = st.sidebar.selectbox("Fluid Extraction Medium", ["Wine/Alcohol Carrier", "Water-Based Infusion", "Infused Vegetable Oil Base"])
closure_type = st.sidebar.selectbox("Vessel Closure Cap Material", ["Pure Beeswax Hard Plug", "Compressed Porous Cork"])
storage_months = st.sidebar.slider("Intended Cellar Storage Duration (Months)", 0, 12, 3, step=1)

st.sidebar.header("4. Cosmic Gearing & Resonator")
planetary_body = st.sidebar.selectbox("Planetary Macro-Multiplier", ["Moon (4:3 Ratio)", "Sun (3:2 Ratio)", "Saturn/Mars (25:16 Ratio)"])
vessel_material = st.sidebar.selectbox("Vessel Composition Matrix", ["Thick Monastic Clay", "Early Venetian Glass"])
neck_geometry = st.sidebar.selectbox("Neck Geometry (Acoustic Transformer)", ["Cylindrical Restricted", "Exponential Flared"])
wall_thickness = st.sidebar.slider("Wall Thickness (mm)", 2.0, 15.0, 8.0, step=0.5)
ambient_temp = st.sidebar.slider("Storage Cellar Temperature (°C)", 0.0, 50.0, 15.0, step=1.0)

# --- Automated Physics Processing Engine ---
if system_mode == "Organ-Tissue Pathology":
    active_pathology_name = pathology
    if pathology == "Neurological Overdrive (CNS Burnout)": disease_peak = 4
    elif pathology == "Hepating Stagnation (Tissue Hardening)": disease_peak = 6
    elif pathology == "Respiratory Degradation (Elasticity Loss)": disease_peak = 1
    else: disease_peak = 4
else:
    active_pathology_name = system_mode
    disease_peak = 7 if system_mode == "Balneological Fluid Circuits" and "Clover" in pool_geometry else 3

f1 = 440.0 * (plant_a_factor / 0.22)
f2 = 440.0 * (plant_b_factor / 0.22) if compounding_tier != "Single Herb Extract" else 0.0
f3 = 440.0 * (plant_c_factor / 0.22) if compounding_tier == "Triple-Plant Envelope" else 0.0
target_freq = abs(f1 - f2 + f3) if compounding_tier == "Triple-Plant Envelope" else (abs(f1 - f2) if compounding_tier == "Dual-Plant Compounding" else f1)

if fluid_medium == "Wine/Alcohol Carrier":
    base_density = 789.0; base_bulk = 1.06e9; optimal_speed = 1162.0
elif fluid_medium == "Infused Vegetable Oil Base":
    base_density = 915.0; base_bulk = 1.86e9; optimal_speed = 1424.0
else:
    base_density = 1000.0; base_bulk = 2.15e9; optimal_speed = 1466.3

fluid_density = base_density - (0.2 * (ambient_temp - 20))
bulk_modulus = base_bulk * (1.0 + 0.003 * (ambient_temp - 20))
wave_speed = np.sqrt(bulk_modulus / fluid_density)

alpha = 0.02 if closure_type == "Pure Beeswax Hard Plug" else 0.18
amplitude_retention = math.exp(-alpha * storage_months) * 100.0

k_val = 0.2 if vessel_material == "Thick Monastic Clay" else 0.9
retention_hours = ((wall_thickness / 1000.0) / k_val) * 100.0
counter_hour_idx = (disease_peak + 4) if disease_peak <= 4 else (disease_peak - 4)

# Seal Boundary Measurements
wavelength_mm = (wave_speed / target_freq) * 1000.0
r1 = 25.0
r2 = r1 * np.sqrt(2)
r3 = r1 * 1.618

panels = ["Dawn", "Sunrise", "Morning", "Noon", "Evening", "Sunset", "Dusk", "Midnight", "Core Neutral Anchor"]
counter_hour_name = panels[counter_hour_idx - 1]

# --- Render UI Dashboard Layout ---
col1, col2 = st.columns(2)

with col1:
    if system_mode == "Organ-Tissue Pathology":
        st.subheader("📊 Integrated Biophysics Metrics")
    elif system_mode == "Balneological Fluid Circuits":
        st.subheader("🌊 Hydrodynamic Circuit Metrics")
        circuit_freq = (flow_velocity_mms / (2.0 * tube_diameter_mm)) * 1000.0
        st.metric("Streaming Target Freq", f"{circuit_freq:.1f} Hz")
    elif system_mode == "Zodiac Carrier Modulators":
        st.subheader("🌌 Astrological Alignment Metrics")
        phase_angle = 360.0 / spoke_count
        st.metric("Radial Vector Phase Angle Offset (Φ)", f"{phase_angle:.2f}°")
    else:
        st.subheader("⚱️ Pharmaceutical Volume Metrics")
        v_neck = (math.pi * (12.5**2) * neck_length_mm) / 1000.0
        st.metric("Acoustic Volume Co-efficient (Γ)", f"{vessel_volume_ml / v_neck:.2f}")

    m1, m2, m3 = st.columns(3)
    m1.metric("Calculated Target Freq", f"{target_freq:.1f} Hz")
    m2.metric("Wave Retention Potency", f"{amplitude_retention:.1f}%")
    m3.metric("Insulation Buffer", f"{retention_hours:.1f} Hrs")

    # Render Superposition Wave Graph
    st.write("#### Master Modulated Wave Envelope Display")
    t = np.linspace(0, 0.05, 1000)
    wave_y = np.sin(2 * np.pi * target_freq * t) * (amplitude_retention / 100.0)
    
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(t, wave_y, color="#FF4B4B")
    ax.set_facecolor('#0e1117'); fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    st.pyplot(fig)
    
    # Patient Profile Database Input Block
    st.markdown("---")
    st.subheader("💾 Patient Profile Ledger")
    patient_name = st.text_input("Enter Patient Name/Identifier:")
    if st.button("Commit Profile to Local Ledger"):
        if patient_name:
            cursor.execute('''
                INSERT INTO patient_profiles (name, pathology, fluid_medium, target_freq, counter_hour)
                VALUES (?, ?, ?, ?, ?)
            ''', (patient_name, active_pathology_name, fluid_medium, round(target_freq, 2), counter_hour_name))
            conn.commit()
            st.success(f"Profile for '{patient_name}' compiled and secured successfully.")
        else:
            st.warning("Please enter a valid patient identifier.")
            
    # View Logs
    if st.checkbox("Show Logged Patient Profiles"):
        profiles = cursor.execute("SELECT name, pathology, fluid_medium, target_freq, counter_hour FROM patient_profiles").fetchall()
        if profiles:
            for p in profiles:
                st.text(f"👤 {p[0]} | Path: {p[1]} | Med: {p[2]} | Freq: {p[3]}Hz | Time Slot: {p[4]}")
        else:
            st.caption("No profiles found in database ledger.")

with col2:
    st.subheader("⏳ G-Code Machine Simulation Preview")
    st.caption("Live feed tracing tool movements (Rapid movements vs. G02/G03 interpolations) directly inside the seal boundary.")
    
    # --- CNC Toolpath Visualizer Component ---
    theta_vals = np.linspace(0, 2 * np.pi, 200)
    
    fig_cnc, ax_cnc = plt.subplots(figsize=(6, 4.2))
    ax_cnc.set_facecolor('#0e1117')
    fig_cnc.patch.set_facecolor('#0e1117')
    
    ax_cnc.scatter(0, 0, color='lime', marker='+', s=150, label='Machine Zero (X0, Y0)')
    ax_cnc.plot([0, 0], [0, r3], color='orange', linestyle=':', alpha=0.7, label='G00 Rapid Feed Trajectory')
    
    ax_cnc.plot(r3 * np.cos(theta_vals), r3 * np.sin(theta_vals), color='#FF4B4B', linewidth=1.5, label='Outer Boundary Loop (Damping Rim)')
    ax_cnc.plot(r2 * np.cos(theta_vals), r2 * np.sin(theta_vals), color='teal', linewidth=2.0, label='Middle Circle Loop (Impedance Node)')
    ax_cnc.plot(r1 * np.cos(theta_vals), r1 * np.sin(theta_vals), color='white', linewidth=2.5, label='Inner Circle Loop (Phase Core)')
    
    ax_cnc.tick_params(colors='white')
    ax_cnc.axis('equal')
    ax_cnc.grid(color='gray', linestyle='--', alpha=0.3)
    ax_cnc.legend(labelcolor='white', loc='lower right', fontsize='small')
    st.pyplot(fig_cnc)

    st.write("#### 🔘 Interactive Triple-Circle Seal SVG Blueprint")
    svg_blueprint = f"""
    <svg width="100%" height="150" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#0e1117"/>
        <circle cx="100" cy="100" r="{r3 * 1.5}" stroke="#FF4B4B" stroke-width="1.5" fill="none" stroke-dasharray="4"/>
        <circle cx="100" cy="100" r="{r2 * 1.5}" stroke="teal" stroke-width="2" fill="none"/>
        <circle cx="100" cy="100" r="{r1 * 1.5}" stroke="white" stroke-width="3" fill="none"/>
    </svg>
    """
    st.components.v1.html(svg_blueprint, height=160)
