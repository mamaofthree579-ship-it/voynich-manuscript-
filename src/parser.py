# Save this directly into src/parser.py
import numpy as np
import pandas as pd
import re

def parse_voynich_text(file_path, active_section="botanical", format_type="zandbergen_landini"):
    """
    Ingests alternative transcription text models and scans for specific 
    botanical folio markers to extract automated 180-degree phase signatures.
    """
    matrix = np.zeros((4, 4), dtype=np.float64)
    
    # Pre-calculated folio biophysics lookup tables
    FOLIO_BIOPHYSICS = {
        "f2r":  {"peak_hour": 4,  "velocity_mod": 1.2},
        "f9v":  {"peak_hour": 1,  "velocity_mod": 0.8},
        "f25r": {"peak_hour": 12, "velocity_mod": 1.9},
        "f33v": {"peak_hour": 8,  "velocity_mod": 0.5},
        "f55r": {"peak_hour": 10, "velocity_mod": 1.4}
    }
    
    # Store globally accessible state metadata dictionary inside the engine
    parse_voynich_text.active_metadata = {"peak_hour": 4, "velocity_mod": 1.0, "detected_folio": "None"}

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
            
        # Parse folio metadata tags (e.g., # FOLIO: f25r)
        if line.startswith('#'):
            if "FOLIO" in line.upper():
                for folio_id, traits in FOLIO_BIOPHYSICS.items():
                    if folio_id in line.lower():
                        parse_voynich_text.active_metadata["peak_hour"] = traits["peak_hour"]
                        parse_voynich_text.active_metadata["velocity_mod"] = traits["velocity_mod"]
                        parse_voynich_text.active_metadata["detected_folio"] = folio_id.upper()
            
            if "SECTION" in line.upper():
                if active_section.upper() in line.upper():
                    current_line_is_target = True
                else:
                    current_line_is_target = False
            continue
            
        if current_line_is_target:
            if format_type == "currier":
                line = re.sub(r'^<f\d+[rv]\.[p\d]+>\s*', '', line)
            
            words = line.split()
            for word in words:
                word = re.sub(r'[\.\,\?\!\\-\\\=\\*]', '', word).lower()
                if word:
                    tokens.append(word)
            tokens.append("LINE_BREAK")

    if not tokens:
        return np.eye(4)

    # Determine state operator array sequences
    operators = []
    for i in range(len(tokens) - 1):
        curr_token = tokens[i]
        next_token = tokens[i+1]
        
        if curr_token == "LINE_BREAK":
            operators.append(2)
            continue
        if next_token == "LINE_BREAK":
            operators.append(3)
            continue
            
        if format_type == "takahashi":
            if curr_token.endswith('edy') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith('ey') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n', 't')):
                operators.append(1)
            else:
                operators.append(0)
        elif format_type == "currier":
            if curr_token.endswith(('dy', 'ey')) and next_token.startswith(('qo', 'ch')):
                operators.append(2)
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
                operators.append(1)
            else:
                operators.append(0)
        else:
            if curr_token.endswith('dy') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith('ey') and next_token.startswith('qo'):
                operators.append(2)
            elif curr_token.endswith(('d', 'l', 'r', 's', 'n')):
                operators.append(1)
            else:
                operators.append(0)

    for idx in range(len(operators) - 1):
        matrix[operators[idx], operators[idx+1]] += 1
        
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
