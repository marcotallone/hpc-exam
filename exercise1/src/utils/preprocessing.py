import pandas as pd
import numpy as np


# Function to preprocess single dataframes for each mapping and algorithm
def preproc(filename, mapping, algorithm=0):
    """Preprocess a single dataframe for a given mapping and algorithm.

    Parameters
    ----------
    filename : str
        The name of the file to read (ending in .csv).
    mapping : str
        The mapping method used to generate the data.
    algorithm : int, optional
        The algorithm used to generate the data. The default is 0.

    Returns
    -------
    df : pandas.DataFrame
        The preprocessed dataframe.

    Examples
    --------
    >>> preproc('data.csv', 'core', 0)
    """

    # Read the csv file
    df = pd.read_csv(filename)

    # Add the mapping column
    df['mapby'] = mapping

    # Convert the column to the appropriate data type
    df['algorithm'] = df['algorithm'].astype('int64')
    df['size'] = df['size'].astype('int64')
    df['latency'] = df['latency'].astype('float64')
    df['min'] = df['min'].astype('float64')
    df['max'] = df['max'].astype('float64')
    df['iterations'] = df['iterations'].astype('int64')
    df['cores'] = df['cores'].astype('int64')
    df['mapby'] = df['mapby'].astype('category')

    # Filter the dataframe by the algorithm
    # (this drops the rows relative to other algorithms)
    df = df[df['algorithm'] == algorithm]

    return df


# Function to merge different mapping dataframe of the same algorithm into a single dataframe
def merge(*dfs):
    # Unpack the list of dataframes
    dflist = list(dfs)

    # Merge the dataframes
    df = pd.concat(dflist)

    # Create a dummy variable for the 'mapby' column
    mapby_dummies = pd.get_dummies(df['mapby'], prefix='mapby', drop_first=False).astype(int)
    df = pd.concat([df, mapby_dummies], axis=1)

    # Create interaction terms
    df['cores_mapby_node'] = df['cores'] * df['mapby_node']
    df['cores_mapby_socket'] = df['cores'] * df['mapby_socket']
    df['cores_mapby_core'] = df['cores'] * df['mapby_core']

    return df

