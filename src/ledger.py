# Save this directly into src/ledger.py
import streamlit as st
import pandas as pd

def initialize_ledger():
    """Initializes a persistent, in-app research logger within Session State."""
    if "research_ledger" not in st.session_state:
        st.session_state.research_ledger = pd.DataFrame(columns=[
            "Target Folio", "Section", "D_JS Distance", 
            "Spiral R² Fit", "Target Compound", "Pharma Compliance"
        ])

def append_to_ledger(folio, section, d_js, r2, compound, compliance):
    """Safely logs an individual multi-metric validation test flight run."""
    new_entry = pd.DataFrame([{
        "Target Folio": folio,
        "Section": section.upper(),
        "D_JS Distance": f"{d_js:.4f}",
        "Spiral R² Fit": f"{r2:.4f}",
        "Target Compound": compound,
        "Pharma Compliance": f"{compliance:.1f}%"
    }])
    
    st.session_state.research_ledger = pd.concat(
        [st.session_state.research_ledger, new_entry], 
        ignore_index=True
    ).drop_duplicates()
