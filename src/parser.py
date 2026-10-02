# Save this directly into src/parser.py
import numpy as np
import pandas as pd
import re

def parse_voynich_text(file_path, active_section="botanical"):
    """
    Ingests ZL3b transcription text and uses folio metadata markers 
    to filter transitions based on specific functional manuscript sections.
    """
    matrix = np.zeros((4, 4), dtype=np.float64)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return np.eye(4)

    tokens = []
    current_line_is_target = True

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Example folio section classification headers: e.g., # SECTION: BOTANICAL
        if line.startswith('#'):
            if "SECTION" in line.upper():
                if active_section.upper() in line.upper():
                    current_line_is_target = True
                else:
                    current_line_is_target = False
            continue
            
        # If the line belongs to our targeted manual section, parse its tokens
        if current_line_is_target:
            words = line.split()
            for word in words:
                word = re.sub(r'[\.\,\?\!]', '', word).lower()
                if word:
                    tokens.append(word)
            tokens.append("LINE_BREAK")

    if not tokens:
        return np.eye(4)

    # Convert word morphology down to 4 lifecycle operator classifications
    operators = []
    for i in range(len(tokens) - 1):
        curr_token = tokens[i]
        next_token = tokens[i+1]
        
        if curr_token == "LINE_BREAK":
            operators.append(2) # ROOT_ZONE / ATTACH
            continue
        if next_token == "LINE_BREAK":
            operators.append(3) # HARVEST_LIMIT / TERMINATE
            continue
            
        # Context-dependent morphological hand-offs
        if curr_token.endswith('dy') and next_token.startswith('qo'):
            operators.append(2) # GENERATIVE_FLOWER transition point
        elif curr_token.endswith('ey') and next_token.startswith('qo'):
            operators.append(2) # GENERATIVE_FLOWER transition point
        elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
            operators.append(1) # STEM_CONTINUANCE vascular loop
        else:
            operators.append(0) # ROOT_ZONE baseline propagation

    # Build matrix sequence
    for idx in range(len(operators) - 1):
        matrix[operators[idx], operators[idx+1]] += 1
        
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
