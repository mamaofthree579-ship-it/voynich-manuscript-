# Save this directly into tests/test_harmonic_fractal.py
import os
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.pharma_engine import calculate_pharma_compliance

def test_just_intonation_resonance():
    print("🧪 Initiating Just Intonation Harmonic Fractal Verification Test...")
    
    # Test Run A: Simulating a clean, structurally aligned Botanical page layout (R2 ≈ 0.046)
    botanical_run = calculate_pharma_compliance(detected_folio="F2R", system_r2=0.046, derived_temp=21.0)
    print(f"🌿 Botanical compliance score calculated at: {botanical_run['compliance_score']}%")
    assert botanical_run['compliance_score'] == 60.6, "❌ Error: Botanical signature calculation drift detected."
    
    # Test Run B: Simulating a flat Astrological control page layout (R2 = 0.0)
    astrological_run = calculate_pharma_compliance(detected_folio="F2R", system_r2=0.0, derived_temp=21.0)
    print(f"🌌 Astrological compliance score calculated at: {astrological_run['compliance_score']}%")
    assert astrological_run['compliance_score'] == 50.0, "❌ Error: Astrological control verification drift detected."
    
    print("✅ All Just Intonation fractal ratio validation tests passed successfully.")

if __name__ == "__main__":
    test_just_intonation_resonance()
