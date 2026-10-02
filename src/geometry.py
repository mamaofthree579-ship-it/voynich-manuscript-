import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

def generate_trajectory(matrix, steps=300, window_len=5):
    """
    Simulates a long-range Markov sequence from a transition matrix
    and embeds it into a higher-dimensional historical window space.
    """
    current_state = 0
    sequence = [current_state]
    
    # Generate Markov chain sequence
    for _ in range(steps - 1):
        next_state = np.random.choice([0, 1, 2, 3], p=matrix[current_state])
        sequence.append(next_state)
        current_state = next_state
        
    # Multi-dimensional trajectory matrix building (Window embedding)
    history_dim = 4 ** window_len
    history_matrix = []
    
    for i in range(len(sequence) - window_len):
        sub_seq = sequence[i:i+window_len]
        # Map unique history sequences to specific index locations
        idx = sum([val * (4 ** idx_w) for idx_w, val in enumerate(sub_seq)])
        vec = np.zeros(history_dim)
        vec[idx] = 1
        history_matrix.append(vec)
        
    return np.array(history_matrix)

def project_to_spiral_space(history_matrix):
    """
    Applies PCA dimensionality reduction to target trajectories,
    unfolds components to cylindrical planes, and checks log spiral fit.
    """
    if len(history_matrix) < 10:
        return np.zeros((100, 2)), 0.0
        
    # Reduce dimension components down to global variances (Z1, Z2)
    pca = PCA(n_components=2)
    z = pca.fit_transform(history_matrix)
    
    z1, z2 = z[:, 0], z[:, 1]
    
    # Transform coordinates from center point into Cylindrical values
    r = np.sqrt(z1**2 + z2**2)
    theta = np.arctan2(z2, z1)
    
    # Ensure theta runs forward monotonically instead of oscillation boundaries
    theta = np.unwrap(theta)
    
    # Standard linear regression fit evaluating: ln(r) = a + b*theta
    mask = r > 0
    if not np.any(mask):
        return z, 0.0
        
    ln_r = np.log(r[mask])
    th = theta[mask]
    
    if len(th) > 2:
        slope, intercept, r_value, _, _ = scipy_regression_fallback(th, ln_r)
        r_squared = r_value ** 2
    else:
        r_squared = 0.0
        
    return z, r_squared

def scipy_regression_fallback(x, y):
    """Clean isolated mathematical matrix calculation for tracking fitness coefficients."""
    n = len(x)
    xy = x * y
    xx = x * x
    
    denom = (n * xx.sum() - x.sum()**2)
    if denom == 0:
        return 0, 0, 0
    slope = (n * xy.sum() - x.sum() * y.sum()) / denom
    intercept = (y.sum() - slope * x.sum()) / n
    
    # Simple correlation assessment loop
    y_mean = y.mean()
    f = slope * x + intercept
    ss_reg = ((f - y_mean)**2).sum()
    ss_tot = ((y - y_mean)**2).sum()
    r_val = np.sqrt(ss_reg / ss_tot) if ss_tot > 0 else 0
    
    return slope, intercept, r_val
