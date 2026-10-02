# Save as tests/test_benchmarks.py
import time
import numpy as np
import os
import sys

# Append root path to resolve local modules cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.geometry import generate_trajectory, project_to_spiral_space

def test_computational_efficiency():
    """
    Stress-tests the trajectory dimension embedding and PCA calculation engines 
    to ensure live browser rendering stays under strict execution thresholds.
    """
    print("⏱️ Initiating Performance Benchmark Audit...")
    
    # Simulating a massive highly-complex state transition matrix
    mock_matrix = np.array([
        [0.4, 0.4, 0.1, 0.1],
        [0.1, 0.6, 0.2, 0.1],
        [0.05, 0.05, 0.7, 0.2],
        [0.3, 0.1, 0.1, 0.5]
    ])
    
    start_time = time.time()
    
    # Generate long-range trajectory matrix
    trajectory = generate_trajectory(mock_matrix, steps=1000, window_len=5)
    # Project vectors down into Cylindrical target spaces
    coords, r_sq = project_to_spiral_space(trajectory)
    
    end_time = time.time()
    execution_duration = end_time - start_time
    
    print(f"⚡ Processing completed in: {execution_duration:.4f} seconds.")
    
    # Asserting that complex processing loops complete in under 0.5 seconds for snappy UI response
    assert execution_duration < 0.5, "❌ Performance optimization failure: Math processing loops are too slow."
    print("✅ Benchmark passed: Calculation speeds are within optimal interactive rendering limits.")

if __name__ == "__main__":
    test_computational_efficiency()
