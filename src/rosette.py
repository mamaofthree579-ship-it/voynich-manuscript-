# Save this directly into src/rosette.py
import numpy as np

def calculate_rosette_spatial_resonance(panel_index, base_velocity):
    """
    Models the 9-Panel Rosette Map as a multi-axial acoustic array.
    Calculates localized acoustic tuning shifts based on geometric panel positioning.
    """
    # Geometric multi-axial alignment weights for the 9 unique fold-out panels
    PANEL_GEOMETRIES = {
        1: {"name": "Central Core Axis",  "shift": 1.000},
        2: {"name": "North Vent Channel",  "shift": 1.045},
        3: {"name": "Northeast Radiant",  "shift": 0.982},
        4: {"name": "East Conduction Node","shift": 1.012},
        5: {"name": "Southeast Radiant",  "shift": 0.954},
        6: {"name": "South Drainage Axis", "shift": 0.890},
        7: {"name": "Southwest Radiant",  "shift": 0.975},
        8: {"name": "West Absorption Node","shift": 1.030},
        9: {"name": "Northwest Radiant",  "shift": 1.018}
    }
    
    p = PANEL_GEOMETRIES.get(panel_index, {"name": "Unmapped Sector", "shift": 1.0})
    
    # Calculate localized wave tuning variables using the panel's spatial multiplier
    localized_velocity = base_velocity * p["shift"]
    harmonic_resonance = (localized_velocity / 343.0)  # Standard atmospheric Mach ratio reference
    
    return {
        "panel_name": p["name"],
        "tuned_velocity": localized_velocity,
        "resonance_index": harmonic_resonance
    }
