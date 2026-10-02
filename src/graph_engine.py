import numpy as np
import pandas as pd

def parse_plant_topology(file_path):
    """
    Ingests 3D plant node listings from TomatoWUR schema format.
    Translates topological edge attributes directly into 4x4 matrix states.
    """
    # 0: CONTINUE, 1: BRANCH, 2: ATTACH, 3: TERMINATE
    matrix = np.zeros((4, 4), dtype=np.float64)
    
    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Return fallback stochastic matrix if file is missing
        return np.eye(4)
        
    # Mapping table rules to structural engine vocabulary
    # '<' = CONTINUE, '+' = BRANCH, 'new_axis' = ATTACH, 'dead_end' = TERMINATE
    tag_map = {'<': 0, '+': 1, 'new_axis': 2, 'dead_end': 3}
    
    if 'edge_type' not in df.columns:
        return np.eye(4)
        
    # Map edges to operators
    df['op_id'] = df['edge_type'].map(tag_map).fillna(0).astype(int)
    operators = df['op_id'].tolist()
    
    # Generate conditional sequence tracking
    for i in range(len(operators) - 1):
        matrix[operators[i], operators[i+1]] += 1
        
    # Row normalization step
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    
    # Fix uniform tracking parameters for zero-exit terminal states
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
