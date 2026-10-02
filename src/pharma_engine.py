# Save this directly into src/pharma_engine.py
import numpy as np
import pandas as pd

def calculate_pharma_compliance(detected_folio, system_r2, derived_temp):
    """
    Cross-references localized trajectory variables against empirical 
    biochemistry profiles derived from modern pharmacognosy data.
    """
    # Expanded Modern Empirical Benchmark Records
    PHARMA_BENCHMARKS = {
        "F2R":   {"specimen": "Cannabis Sativa (Hemp Stalk)", "organ": "STEM_CONTINUANCE", "compound": "Cannabinoids / Terpene Volatiles", "phase": "Pre-Flowering Core Max", "temp": 21.0},
        "F9V":   {"specimen": "Viola Tricolor (Wild Pansy)", "organ": "GENERATIVE_FLOWER", "compound": "Thermolabile Cyclotide Proteins", "phase": "Peak Flower Maturity", "temp": 18.0},
        "F25R":  {"specimen": "Helianthus Annuus (Sunflower)", "organ": "GENERATIVE_FLOWER", "compound": "Helianthoside Seed Lipids", "phase": "Post-Maturity Seed Drop", "temp": 25.0},
        "F33V":  {"specimen": "Nymphaea Alba (Water Lily)", "organ": "ROOT_ZONE",         "compound": "Nupharine Sedative Alkaloids",  "phase": "Subterranean Dormancy", "temp": 15.0},
        "F55R":  {"specimen": "Mandragora Officinarum",      "organ": "ROOT_ZONE",         "compound": "Tropane Anticholinergic Alkaloids", "phase": "Pre-Flowering Root Inversion", "temp": 20.0}
    }
    
    # Standardize string inputs to avoid key mismatches
    folio_key = str(detected_folio).upper().strip()
    
    if folio_key not in PHARMA_BENCHMARKS:
        return {
            "specimen": "Unknown Botanical Archetype", "compound": "Unmapped Secondary Metabolite", 
            "target_organ": "Vascular Stem", "optimal_temp": 22.0, "compliance_score": 50.0
        }
        
    bench = PHARMA_BENCHMARKS[folio_key]
    
    # 1. Structural Match Factor: Weight contribution driven by your Trajectory Spiral R^2 Fitness (50% max)
    structural_fit = system_r2 * 50.0  
    
    # 2. Thermodynamic Variance Factor: Compares calculated velocities to real chemical stability limits (50% max)
    temp_delta = abs(derived_temp - bench["temp"])
    thermal_fit = max(0.0, 50.0 - (temp_delta * 2.5))  # Drops by 2.5% per degree of drift
    
    total_compliance = min(100.0, max(0.0, structural_fit + thermal_fit))
    
    return {
        "specimen": bench["specimen"],
        "compound": bench["compound"],
        "target_organ": bench["organ"],
        "optimal_temp": bench["temp"],
        "compliance_score": total_compliance
    }
