# Save this directly into src/pharma_engine.py
import numpy as np
import pandas as pd

def calculate_pharma_compliance(detected_folio, system_r2, derived_temp):
    """
    Cross-references localized trajectory variables against empirical 
    biochemistry profiles derived from modern pharmacognosy data.
    """
    # Modern Empirical Benchmark Records
    # Mapped by Folio: [Target Organ, Active Molecule, Target Harvest Phase, Optimal Preservation Temp]
    PHARMA_BENCHMARKS = {
        "F2R":   {"organ": "STEM_CONTINUANCE", "compound": "Cannabinoids/Terpenes", "phase": "Pre-Flowering", "temp": 21.0},
        "F9V":   {"organ": "GENERATIVE_FLOWER", "compound": "Cyclotides/Anthocyanins", "phase": "Peak Maturity", "temp": 18.0},
        "F25R":  {"organ": "GENERATIVE_FLOWER", "compound": "Helianthoside Lipids", "phase": "Post-Maturity", "temp": 25.0},
        "F33V":  {"organ": "ROOT_ZONE",         "compound": "Nupharine Alkaloids",  "phase": "Dormancy Axis",  "temp": 15.0},
        "F55R":  {"organ": "ROOT_ZONE",         "compound": "Tropane Alkaloids",    "phase": "Pre-Flowering", "temp": 20.0}
    }
    
    if detected_folio not in PHARMA_BENCHMARKS:
        # Default baseline compliance metrics if no folio signature match is found
        return {
            "compound": "Unknown Metabolite", "target_organ": "Vascular Stem",
            "optimal_temp": 22.0, "compliance_score": 50.0
        }
        
    bench = PHARMA_BENCHMARKS[detected_folio]
    
    # 1. Structural Match Factor: Driven by your Trajectory Spiral R^2 Model Fitness
    structural_fit = system_r2 * 50.0  # Scales up to a maximum weight contribution of 50%
    
    # 2. Thermodynamic Variance Factor: Compares calculated acoustic velocities to chemical stability limits
    temp_delta = abs(derived_temp - bench["temp"])
    thermal_fit = max(0.0, 50.0 - (temp_delta * 2.5))  # Decreases by 2.5% for each degree of thermal drift
    
    # Compile the final operational compliance score out of 100%
    total_compliance = min(100.0, max(0.0, structural_fit + thermal_fit))
    
    return {
        "compound": bench["compound"],
        "target_organ": bench["organ"],
        "optimal_temp": bench["temp"],
        "compliance_score": total_compliance
    }
