import numpy as np
import operator as op
import pandas as pd

df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, None, 9]]),
                   columns=['a', 'b', 'c'])

def filter_df(df, filters:dict, exclude=False, func='isin'):
    funcs = {
        'isin': pd.Series.isin,
        'df_isin': pd.DataFrame.isin,
        'isna': pd.Series.isna,
        'notna': pd.Series.notna
    }

    vert = op.inv if exclude or 'not ' in str(func) else op.pos
    func = funcs.get(func, func)

    if isinstance(filters, dict):
        for col, val in filters.items():
            if isinstance(col, tuple):
                col = list(col)
                func = funcs.get(f"df_{func.__name__}", func)
            df = df[vert(func(df[col], val)).any(axis='columns')]
    elif hasattr(filters, '__iter__'):
        for col in filters:
            if hasattr(col, '__iter__'):
                col = list(col)
                func = funcs.get(f"df_{func.__name__}", func)
            df = df[vert(func(df[col]))]

    try:
        for col, val in filters.items():
            if isinstance(col, tuple):
                col = list(col)
                func = funcs.get(f"df_{func.__name__}", func)
            df = df[vert(func(df[col], val)).any(axis='columns')]
    except AttributeError:
        for col in filters:
            df = df[vert(func(df[col])).any(axis='columns')]

    return df

print(filter_df(df, filters={('a', 'b'): [2]}))
print()