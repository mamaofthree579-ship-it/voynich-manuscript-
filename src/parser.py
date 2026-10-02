# Save this directly into src/parser.py
import numpy as np
import pandas as pd
import re

def parse_voynich_text(file_path, active_section="botanical", format_type="zandbergen_landini"):
    """
    Ingests alternative transcription text models (Zandbergen-Landini, Takahashi, Currier).
    Applies custom morphological class mappings adjusted for the specific alphabet/transcription rules.
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
            
        # Parse folio section identifiers
        if line.startswith('#'):
            if "SECTION" in line.upper():
                if active_section.upper() in line.upper():
                    current_line_is_target = True
                else:
                    current_line_is_target = False
            continue
            
        if current_line_is_target:
            # Handle format-specific line-stripping (e.g., Currier locators like <f1r.p1>)
            if format_type == "currier":
                line = re.sub(r'^<f\d+[rv]\.[p\d]+>\s*', '', line)
            
            words = line.split()
            for word in words:
                # Strip out punctuation markers specific to different transcription systems
                word = re.sub(r'[\.\,\?\!\\-\\\=\\*]', '', word).lower()
                if word:
                    tokens.append(word)
            tokens.append("LINE_BREAK")

    if not tokens:
        return np.eye(4)

    operators = []
    for i in range(len(tokens) - 1):
        curr_token = tokens[i]
        next_token = tokens[i+1]
        
        if curr_token == "LINE_BREAK":
            operators.append(2) # ROOT_ZONE
            continue
        if next_token == "LINE_BREAK":
            operators.append(3) # HARVEST_LIMIT
            continue
            
        # Format-specific morphological transition rules
        if format_type == "takahashi":
            # Takahashi specific boundary mappings (e.g., edy -> qo)
            if curr_token.endswith('edy') and next_token.startswith('qo'):
                operators.append(2) # GENERATIVE_FLOWER
            elif curr_token.endswith('ey') and next_token.startswith('qo'):
                operators.append(2) # GENERATIVE_FLOWER
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n', 't')):
                operators.append(1) # STEM_CONTINUANCE
            else:
                operators.append(0) # ROOT_ZONE
        elif format_type == "currier":
            # Currier specific alphabet boundaries
            if curr_token.endswith(('dy', 'ey')) and next_token.startswith(('qo', 'ch')):
                operators.append(2) # GENERATIVE_FLOWER
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
                operators.append(1) # STEM_CONTINUANCE
            else:
                operators.append(0) # ROOT_ZONE
        else: # Default Zandbergen-Landini rules
            if curr_token.endswith('dy') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith('ey') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
                operators.append(1)
            else:
                operators.append(0)

    # Compile transition distribution
    for idx in range(len(operators) - 1):
        matrix[operators[idx], operators[idx+1]] += 1
        
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
