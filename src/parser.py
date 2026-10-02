import numpy as np
import pandas as pd
import re

def parse_voynich_text(file_path):
    """
    Parses ZL3b-formatted text streams. Separates words into morphological classes
    and constructs the empirical text transition operator matrix.
    """
    # Operator mappings
    # 0: CONTINUE, 1: BRANCH, 2: ATTACH, 3: TERMINATE
    matrix = np.zeros((4, 4), dtype=np.float64)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        # Fallback to prevent app crashes if data isn't mounted yet
        return np.eye(4)

    tokens = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'): # Skip comments/metadata
            continue
            
        # Clean line tokens
        words = line.split()
        for word in words:
            # Strip common transcription punctuation
            word = re.sub(r'[\.\,\?\!]', '', word).lower()
            if word:
                tokens.append(word)
        tokens.append("LINE_BREAK") # Mark structural boundary

    # Determine sequence of operators based on Level 1 / Level 2 rules
    operators = []
    for i in range(len(tokens) - 1):
        curr_token = tokens[i]
        next_token = tokens[i+1]
        
        if curr_token == "LINE_BREAK":
            operators.append(2) # ATTACH (Context Reset)
            continue
            
        if next_token == "LINE_BREAK":
            operators.append(3) # TERMINATE (Hard structural limit)
            continue
            
        # Level 1/2 Rules: Morphological Hand-offs
        if curr_token.endswith('dy') and next_token.startswith('qo'):
            operators.append(1) # BRANCH
        elif curr_token.endswith('ey') and next_token.startswith('qo'):
            operators.append(1) # BRANCH
        elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
            operators.append(0) # CONTINUE
        else:
            operators.append(0) # Default step propagation

    # Build Transition Frequencies
    for idx in range(len(operators) - 1):
        matrix[operators[idx], operators[idx+1]] += 1
        
    # Row normalize to convert frequencies to conditional probabilities
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    
    # Handle zero rows by providing flat distribution
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
