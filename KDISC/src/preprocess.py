import pandas as pd
import numpy as np

def splice_from_file(filename):
    """
    Load the genome splice dataset to pandas DataFrame
    """
    df = pd.read_csv(filename)
    df.columns = ['class', 'id', 'dna']
    return df

def get_split_col_names():
    """Creates list of the 60 column names in the form dna_1, dna_2, ..., dna_60
       Used for column names of the split dataframe object
    """
    return ['dna_%d' % (idx+1) for idx in range(60)]

def split_features(data):
    """Splits the DNA feature string into 60 columns for each of the 60 chars in DNA string
       Names of the columns are provided from get_split_col_names() function. It also removes
       id column.
       data - input dataframe from raw splice file, has columns class, id and dna
       return - resulting pandas DataFrame object
    """
    X = data.copy()
    #split nucleotid string (len=60) into a list of independent characters (DNA nucleotids)
    X['dna'] = X['dna'].map(lambda x : list(str(x).strip()))
    #create 60 new attributes (columns) for each DNA nucleotide index
    #each attribute has name dna_idx where idx is index (1-based) in the list above
    for idx in range(60):
        X['dna_%d' % (idx+1)] = X['dna'].map(lambda x : x[idx])
    #remove the old dna column (redundant information)
    del X['dna']
    #remove descriptor
    del X['id']
    
    return X


def separate_feature_class(data):
    """Separates data into atributes and class objects
    data - DataFrame object with 'class' and [dna_1, dna_2, ..., dna_60] attributes
    returns - pair of DataFrame objects, X containing attributes and y containing instance classes
    """
    data_c = data.copy()
    y = data_c.reindex(columns=['class'])
    X = data_c.drop(columns='class')
    return X,y

def count_unique_percent(df):
    """returns fractions of the unique values in the dataset"""
    #flatten DataFrame to one dimensional array and convert it to Series object
    series = pd.Series(df.as_matrix().reshape(-1))
    #count unique values percentage
    series.value_counts()
    unique_counts_pct = series.value_counts(normalize=True)
    return unique_counts_pct

def get_odd_nucleotide_rows(df):
    """creates dictionary of rows containing odd (non ATCG nucleotide)
       key - non ATCG nucleotide
       value - list of rows containing non ATCG nucleotide
    """
    
    odd_dict = {}
    odd_dict['N'] = df[df == 'N'].dropna(how='all').index.values.reshape(-1)
    odd_dict['R'] = df[df == 'R'].dropna(how='all').index.values.reshape(-1)
    odd_dict['S'] = df[df == 'S'].dropna(how='all').index.values.reshape(-1)
    odd_dict['D'] = df[df == 'D'].dropna(how='all').index.values.reshape(-1)
    return odd_dict

def remove_odd_nucleotide_rows(df, odd_rows_dict):

    to_remove_idx = np.concatenate(list(odd_rows_dict.values()))
    return df.drop(index = to_remove_idx.tolist())
