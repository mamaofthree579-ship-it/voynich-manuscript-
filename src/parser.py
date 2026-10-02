# Save this directly into src/parser.py
import numpy as np
import pandas as pd
import re

def parse_voynich_text(file_path, active_section="botanical", format_type="zandbergen_landini", growth_phase="Peak Flowering"):
    """
    Ingests text transcriptions, utilizing advanced multi-token sub-rule sets 
    to unpack hyphenated joints within the Takahashi corpus format.
    """
    matrix = np.zeros((4, 4), dtype=np.float64)
    
    FOLIO_BIOPHYSICS = {
        "f2r":  {"peak_hour": 4,  "velocity_mod": 1.2},
        "f9v":  {"peak_hour": 1,  "velocity_mod": 0.8},
        "f25r": {"peak_hour": 12, "velocity_mod": 1.9},
        "f33v": {"peak_hour": 8,  "velocity_mod": 0.5},
        "f55r": {"peak_hour": 10, "velocity_mod": 1.4}
    }
    
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
                # Clean standard structural errors but preserve hyphens for Takahashi rules
                if format_type == "takahashi":
                    word = re.sub(r'[\.\,\?\!\\*]', '', word).lower()
                else:
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
            
        # ADVANCED RUN ROUTINE: Scaled Takahashi sub-token evaluation
        if format_type == "takahashi" and "-" in curr_token:
            # Explode the compound string along its internal structural boundary joints
            sub_segments = curr_token.split("-")
            prefix, suffix = sub_segments[0], sub_segments[-1]
            
            # Isolated transition evaluation rules for complex string boundaries
            if suffix.endswith('edy') or suffix.endswith('ey'):
                operators.append(2) # GENERATIVE_FLOWER
            elif prefix.startswith('qo') or prefix.startswith('ot'):
                operators.append(1) # STEM_CONTINUANCE state reinforcement
            else:
                operators.append(0) # ROOT_ZONE fallback
            continue

        # Standard Parsing Rules (Currier / Zandbergen-Landini Fallbacks)
        is_branch = curr_token.endswith(('dy', 'ey')) and next_token.startswith('qo')
        is_vascular = curr_token.endswith(('d', 'l', 'r', 's', 'n'))
        
        if growth_phase == "Young Vegetative":
            if is_vascular: operators.append(1)
            else: operators.append(0)
        elif growth_phase == "Dried Prep/Storage":
            if is_branch: operators.append(3)
            else: operators.append(1)
        else:
            if is_branch: operators.append(2)
            elif is_vascular: operators.append(1)
            else: operators.append(0)

    for idx in range(len(operators) - 1):
        matrix[operators[idx], operators[idx+1]] += 1
        
    row_sums = matrix.sum(axis=1, keepdims=True)
    matrix = np.divide(matrix, row_sums, out=np.zeros_like(matrix), where=row_sums!=0)
    matrix[matrix.sum(axis=1) == 0] = [0.25, 0.25, 0.25, 0.25]
    
    return matrix
