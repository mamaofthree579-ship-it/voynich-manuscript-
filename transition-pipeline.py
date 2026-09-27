import numpy as np
import pandas as pd
from scipy.spatial.distance import jensenshannon
from collections import defaultdict
import random

class VoynichStateProcessor:
    def __init__(self, token_df):
        """
        token_df columns: ['token', 'folio', 'section', 'hand', 'currier_lang']
        """
        self.df = token_df
        self.vocab = token_df['token'].unique()
        
    def classify_terminal(self, token):
        """Hierarchical Level Classification"""
        if not isinstance(token, str) or len(token) == 0:
            return 'OTHER'
        if token.endswith('edy'): return 'EDY'
        if token.endswith('ey'): return 'EY'
        if token.endswith('dy'): return 'DY'
        if token.endswith('y'): return 'TERM_Y'
        for c in ['d', 'l', 'r', 's', 'n']:
            if token.endswith(c): return f'TERM_{c.upper()}'
        return 'OTHER'

    def classify_initial(self, token):
        if not isinstance(token, str) or len(token) == 0:
            return 'OTHER'
        if token.startswith('qo'): return 'INIT_QO'
        if token.startswith('ot'): return 'INIT_OT'
        return 'OTHER'

    def build_transition_matrix(self, df_context):
        """Generates P(Initial_t+1 | Terminal_t)"""
        transitions = defaultdict(int)
        term_counts = defaultdict(int)
        
        # Group by folio/section to respect page boundaries
        grouped = df_context.groupby(['folio', 'section'])
        for _, group in grouped:
            tokens = group['token'].tolist()
            for i in range(len(tokens) - 1):
                t_curr = self.classify_terminal(tokens[i])
                t_next = self.classify_initial(tokens[i+1])
                transitions[(t_curr, t_next)] += 1
                term_counts[t_curr] += 1
                
        # Convert to conditional probability matrix
        states_term = ['EDY', 'EY', 'DY', 'TERM_Y', 'TERM_D', 'TERM_L', 'TERM_R', 'TERM_S', 'TERM_N', 'OTHER']
        states_init = ['INIT_QO', 'INIT_OT', 'OTHER']
        
        M = np.zeros((len(states_term), len(states_init)))
        for i, t_c in enumerate(states_term):
            denom = term_counts[t_c]
            if denom == 0: continue
            for j, t_n in enumerate(states_init):
                M[i, j] = transitions[(t_c, t_n)] / denom
        return M, states_term, states_init

    def generate_constrained_null(self):
        """
        Permutes tokens while strictly preserving:
        1. Folio/Section membership boundaries
        2. Global token frequencies
        3. Word-level structural mappings
        """
        null_df = self.df.copy()
        # Shuffle tokens within their respective Currier-language/section pools
        # to preserve marginal frequencies and structural constraints
        grouped = null_df.groupby(['section', 'currier_lang'])
        shuffled_series = []
        
        for _, group in grouped:
            tokens = group['token'].tolist()
            random.shuffle(tokens)
            shuffled_series.append(pd.Series(tokens, index=group.index))
            
        null_df['token'] = pd.concat(shuffled_series).sort_index()
        return null_df


class TomatoWURGraphProcessor:
    def __init__(self, graph_df):
        """
        graph_df columns: ['plant_id', 'edge_id', 'source_v', 'target_v', 'edge_type']
        edge_type map: '+' -> BRANCH, '<' -> CONTINUE, 'terminal_node' -> TERMINATE
        """
        self.df = graph_df
        
    def extract_topological_operators(self):
        """Maps graph transitions cleanly to continuous structural states"""
        operators = []
        # Structural transitions are built sequentially along the phyllotactic/growth path
        grouped = self.df.groupby('plant_id')
        for _, plant in grouped:
            # Sort edges by topology path (from root outward)
            sorted_edges = plant.sort_values(by=['source_v', 'target_v'])
            types = sorted_edges['edge_type'].tolist()
            for i in range(len(types) - 1):
                operators.append((types[i], types[i+1]))
        return operators

    def build_plant_matrix(self, operators):
        states = ['CONTINUE', 'BRANCH', 'ATTACH', 'TERMINATE']
        state_map = {'<': 'CONTINUE', '+': 'BRANCH', 'a': 'ATTACH', 't': 'TERMINATE'}
        
        counts = defaultdict(int)
        row_totals = defaultdict(int)
        for op_curr, op_next in operators:
            c = state_map.get(op_curr, 'TERMINATE')
            n = state_map.get(op_next, 'TERMINATE')
            counts[(c, n)] += 1
            row_totals[c] += 1
            
        M = np.zeros((len(states), len(states)))
        for i, s_c in enumerate(states):
            denom = row_totals[s_c]
            if denom == 0: continue
            for j, s_n in enumerate(states):
                M[i, j] = counts[(s_c, s_n)] / denom
        return M, states
