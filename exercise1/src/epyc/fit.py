import pandas as pd
import statsmodels.api as sm
import os

# Load datasets ────────────────────────────────────────────────────────────────
# nbft_file = 'datasets/nbft.csv'
#p2p_file = 'datasets/p2p.csv'

module_dir = os.path.dirname(os.path.abspath(__file__))
nbft_file = os.path.join(module_dir, 'nbft.csv')
nbft_reduce_file = os.path.join(module_dir, 'nbft_reduce.csv')
p2p_file = os.path.join(module_dir, 'p2p.csv')

try:
    nbft_df = pd.read_csv(nbft_file)
    nbft_reduce_df = pd.read_csv(nbft_reduce_file)
    p2p_df = pd.read_csv(p2p_file)
except:
    print("ERROR: Could not load the datasets in the src/ directory."
          " Make sure the paths are correct and the files exist.")
    exit(1)

# Splitted datasets ────────────────────────────────────────────────────────────
p2p_cache = p2p_df[p2p_df['mapby']=='cache'].copy()
p2p_core = p2p_df[p2p_df['mapby']=='core'].copy()
p2p_socket = p2p_df[p2p_df['mapby']=='socket'].copy()
p2p_node = p2p_df[p2p_df['mapby']=='node'].copy()
nbft_cache = nbft_df[nbft_df['mapby']=='cache'].copy()
nbft_core = nbft_df[nbft_df['mapby']=='core'].copy()
nbft_socket = nbft_df[nbft_df['mapby']=='socket'].copy()
nbft_node = nbft_df[nbft_df['mapby']=='node'].copy()
nbft_reduce_cache = nbft_reduce_df[nbft_reduce_df['mapby']=='cache'].copy()
nbft_reduce_core = nbft_reduce_df[nbft_reduce_df['mapby']=='core'].copy()
nbft_reduce_socket = nbft_reduce_df[nbft_reduce_df['mapby']=='socket'].copy()
nbft_reduce_node = nbft_reduce_df[nbft_reduce_df['mapby']=='node'].copy()

# Hockney fits for p2p communications ──────────────────────────────────────────

def fit_p2p():
    # Dictionary to store hockney model parameters
    hockney = {'cache': [], 'core': [], 'socket': [], 'node': []}

    # Add dummy variable and interaction term for big sizes
    p2p_cache['big'] = (p2p_cache['size'] > 2**17).astype(int)
    p2p_cache['big_size'] = p2p_cache['size'] * p2p_cache['big']
    p2p_core['big'] = (p2p_core['size'] > 2**17).astype(int)
    p2p_core['big_size'] = p2p_core['size'] * p2p_core['big']
    p2p_socket['big'] = (p2p_socket['size'] > 2**17).astype(int)
    p2p_socket['big_size'] = p2p_socket['size'] * p2p_socket['big']
    p2p_node['big'] = (p2p_node['size'] > 2**17).astype(int)
    p2p_node['big_size'] = p2p_node['size'] * p2p_node['big']

    # Fit
    y = p2p_cache['latency']
    X = p2p_cache[['size', 'big', 'big_size']]
    X = sm.add_constant(X)
    cache_model = sm.OLS(y, X).fit()
    hockney['cache'] = list(cache_model.params)

    y = p2p_core['latency']
    X = p2p_core[['size', 'big', 'big_size']]
    X = sm.add_constant(X)
    core_model = sm.OLS(y, X).fit()
    hockney['core'] = list(core_model.params)

    y = p2p_socket['latency']
    X = p2p_socket[['size', 'big', 'big_size']]
    X = sm.add_constant(X)
    socket_model = sm.OLS(y, X).fit()
    hockney['socket'] = list(socket_model.params)

    y = p2p_node['latency']
    X = p2p_node[['size', 'big', 'big_size']]
    X = sm.add_constant(X)
    node_model = sm.OLS(y, X).fit()
    hockney['node'] = list(node_model.params)

    return hockney

# NBFT fits ────────────────────────────────────────────────────────────────────

# (Broadcast)
def fit_nbft():
    # Dictionary to store the linear NBFT fit parameters
    nbft_coefficients = {'cache': {}, 'core': {}, 'socket': {}, 'node': {}}

    # For the cache channel, the values of the latency, for every possible size 
    # and every possible p, are directly copied from the dataset.
    sizes = nbft_cache['size'].unique()
    processes = nbft_cache['p'].unique()
    for size in sizes:
        nbft_coefficients['cache'][size] = {}
        for p in processes:
            nbft_coefficients['cache'][size][p] = nbft_cache[
                (nbft_cache['size']==size) & 
                (nbft_cache['p']==p)]['latency'].values[0]

    # Fit
    sizes = nbft_core['size'].unique()
    for size in sizes:
        y = nbft_core[nbft_core['size']==size]['latency']
        X = nbft_core[nbft_core['size']==size][['p']]
        X = sm.add_constant(X)
        core_model = sm.OLS(y, X).fit()
        nbft_coefficients['core'][size] = list(core_model.params)

    sizes = nbft_socket['size'].unique()
    for size in sizes:
        y = nbft_socket[nbft_socket['size']==size]['latency']
        X = nbft_socket[nbft_socket['size']==size][['p']]
        X = sm.add_constant(X)
        socket_model = sm.OLS(y, X).fit()
        nbft_coefficients['socket'][size] = list(socket_model.params)

    sizes = nbft_node['size'].unique()
    for size in sizes:
        y = nbft_node[nbft_node['size']==size]['latency']
        X = nbft_node[nbft_node['size']==size][['p']]
        X = sm.add_constant(X)
        node_model = sm.OLS(y, X).fit()
        nbft_coefficients['node'][size] = list(node_model.params)

    return nbft_coefficients

# (Reduce
def fit_nbft_reduce():
    # Dictionary to store the linear NBFT fit parameters
    nbft_coefficients = {'cache': {}, 'core': {}, 'socket': {}, 'node': {}}

    # For the cache channel, the values of the latency, for every possible size 
    # and every possible p, are directly copied from the dataset.
    sizes = nbft_reduce_cache['size'].unique()
    processes = nbft_reduce_cache['p'].unique()
    for size in sizes:
        nbft_coefficients['cache'][size] = {}
        for p in processes:
            nbft_coefficients['cache'][size][p] = nbft_reduce_cache[
                (nbft_reduce_cache['size']==size) & 
                (nbft_reduce_cache['p']==p)]['latency'].values[0]

    # Fit
    sizes = nbft_reduce_core['size'].unique()
    for size in sizes:
        y = nbft_reduce_core[nbft_reduce_core['size']==size]['latency']
        X = nbft_reduce_core[nbft_reduce_core['size']==size][['p']]
        X = sm.add_constant(X)
        core_model = sm.OLS(y, X).fit()
        nbft_coefficients['core'][size] = list(core_model.params)

    sizes = nbft_reduce_socket['size'].unique()
    for size in sizes:
        y = nbft_reduce_socket[nbft_reduce_socket['size']==size]['latency']
        X = nbft_reduce_socket[nbft_reduce_socket['size']==size][['p']]
        X = sm.add_constant(X)
        socket_model = sm.OLS(y, X).fit()
        nbft_coefficients['socket'][size] = list(socket_model.params)

    sizes = nbft_reduce_node['size'].unique()
    for size in sizes:
        y = nbft_reduce_node[nbft_reduce_node['size']==size]['latency']
        X = nbft_reduce_node[nbft_reduce_node['size']==size][['p']]
        X = sm.add_constant(X)
        node_model = sm.OLS(y, X).fit()
        nbft_coefficients['node'][size] = list(node_model.params)

    return nbft_coefficients
