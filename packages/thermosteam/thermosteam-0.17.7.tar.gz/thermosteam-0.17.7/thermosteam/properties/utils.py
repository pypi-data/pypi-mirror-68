# -*- coding: utf-8 -*-
'''
All data and methods for the internal retrieval of data from CAS numbers.
'''

from bisect import bisect_left
import os
import pandas as pd
import numpy as np
from typing import Dict


__all__ = ('CASDataReader', 
           'CASDataSource', 
           'get_from_retrievers',
           'MultiCheb1D',
           'CAS2int', 
           'int2CAS', 
           'to_nums')

class CASDataReader:
    
    def __init__(self, __file__, folder, parent="Data"):
        fpath = os.path
        join = fpath.join
        parent_path = join(fpath.dirname(__file__), parent)
        self.folder = join(parent_path, folder)
    
    def __call__(self, file, sep='\t', index_col=0,  **kwargs):
        df = pd.read_csv(os.path.join(self.folder, file),
                         sep=sep, index_col=index_col,
                         engine='python', **kwargs)
        return CASDataSource(df)
    

class CASDataSource:
    __slots__ = ('df', 'index', 'values')
    def __init__(self, df):
        self.df = df
        self.index = df.index
        self.values = df.values
    
    def retriever(self, var):
        return CASDataRetriever(self.df, var)
    
    def retrieve(self, CASRN, var):
        df = self.df
        if CASRN in df.index:
            value = df.at[CASRN, var]
            return None if np.isnan(value) else float(value)
        else:
            return None    
    
    @property
    def at(self):
        return self.df.at
    
    def __getitem__(self, CAS):
        return self.values[self.index.get_loc(CAS)]
    
    def __contains__(self, CAS):
        return CAS in self.index
    

class CASDataRetriever:
    __slots__ = ('df', 'var')
    
    def __init__(self, df, var):
        self.df = df
        self.var = var
        
    def __call__(self, CASRN):
        df = self.df
        if CASRN in df.index:
            value = df.at[CASRN, self.var]
            return None if np.isnan(value) else float(value)
        else:
            return None

CASDataSources = Dict[str, CASDataSource]
CASDataRetrievers = Dict[str, CASDataRetriever]

def retrievers_from_data_sources(sources: CASDataSources, var: str) -> dict:
    return {name: source.retriever(var)
            for name, source in sources.items()}

def get_from_retrievers(retrievers: CASDataRetrievers, CASRN: str, method:str):
    if method == 'All':
        value = {i: j(CASRN) for i,j in retrievers.items()}
    elif method == 'Any':
        for retriever in retrievers.values():
            value = retriever(CASRN)
            if value: break
    else:
        try:
            retriever = retrievers[method]
        except:
            raise ValueError("invalid method; method must be one of the following: "
                            f"{', '.join(retrievers)}.")
        value = retriever(CASRN)
    return value

def get_from_data_sources(sources: CASDataSources, CASRN: str, var: str, method:str):
    if method == 'All':
        value = {i: j.retrieve(CASRN, var) for i,j in sources.items()}
    elif method == 'Any':
        for source in sources.values():
            value = source.retrieve(CASRN, var)
            if value: break
    else:
        try:
            source = sources[method]
        except:
            raise ValueError("invalid method; method must be one of the following: "
                            f"{', '.join(sources)}.")
        value = source.retrieve(CASRN, var)
    return value


class MultiCheb1D(object):
    '''Simple class to store set of coefficients for multiple chebyshev 
    approximations and perform calculations from them.
    '''
    def __init__(self, points, coeffs):
        self.points = points
        self.coeffs = coeffs
        self.N = len(points)-1
        
    def __call__(self, x):
        coeffs = self.coeffs[bisect_left(self.points, x)]
        return coeffs(x)
#        return self.chebval(x, coeffs)
                
    @staticmethod
    def chebval(x, c):
        # copied from numpy's source, slightly optimized
        # https://github.com/numpy/numpy/blob/v1.13.0/numpy/polynomial/chebyshev.py#L1093-L1177
        x2 = 2.*x
        c0 = c[-2]
        c1 = c[-1]
        for i in range(3, len(c) + 1):
            tmp = c0
            c0 = c[-i] - c1
            c1 = tmp + c1*x2
        return c0 + c1*x

def CAS2int(i):
    r'''Converts CAS number of a compounds from a string to an int. This is
    helpful when storing large amounts of CAS numbers, as their strings take up
    more memory than their numerical representational. All CAS numbers fit into
    64 bit ints.

    Parameters
    ----------
    CASRN : string
        CASRN [-]

    Returns
    -------
    CASRN : int
        CASRN [-]

    Notes
    -----
    Accomplishes conversion by removing dashes only, and then converting to an
    int. An incorrect CAS number will change without exception.

    Examples
    --------
    >>> CAS2int('7704-34-9')
    7704349
    '''
    return int(i.replace('-', ''))

def int2CAS(i):
    r'''Converts CAS number of a compounds from an int to an string. This is
    helpful when dealing with int CAS numbers.

    Parameters
    ----------
    CASRN : int
        CASRN [-]

    Returns
    -------
    CASRN : string
        CASRN [-]

    Notes
    -----
    Handles CAS numbers with an unspecified number of digits. Does not work on
    floats.

    Examples
    --------
    >>> int2CAS(7704349)
    '7704-34-9'
    '''
    i = str(i)
    return i[:-3]+'-'+i[-3:-1]+'-'+i[-1]

def to_nums(values):
    r'''Legacy function to turn a list of strings into either floats
    (if numeric), stripped strings (if not) or None if the string is empty.
    Accepts any numeric formatting the float function does.

    Parameters
    ----------
    values : list
        list of strings

    Returns
    -------
    values : list
        list of floats, strings, and None values [-]

    Examples
    --------
    >>> to_num(['1', '1.1', '1E5', '0xB4', ''])
    [1.0, 1.1, 100000.0, '0xB4', None]
    '''
    return [to_num(i) for i in values]

def to_num(value):
    try:
        return float(value)
    except:
        if value == '':
            return None
        else:
            return value.strip()