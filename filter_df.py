from functools import reduce
import numpy as np
import operator as op
import os
import pandas as pd
from pandas.testing import assert_frame_equal

df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, None, 9]]),
                   columns=['a', 'b', 'c'])

AGE = 'age'

CLASS = 'class'
THIRD = 'Third'

EMBARK_TOWN = 'embark_town'
SOUTHAMPTON = 'Southampton'

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'titanic.csv'))

def is_iter(obj) -> bool:
    return hasattr(obj, '__iter__') and not isinstance(obj, str)

def filter_df(df:pd.DataFrame, filters:dict, exclude:bool=False, func:str='eq') -> pd.DataFrame:
    funcs = {
        'eq': pd.Series.eq,
        'not eq': lambda series,val: ~pd.Series.eq(series, val),
        'isin': pd.Series.isin,
        '==': pd.Series.eq,
        '>=': pd.Series.ge,
    }

    vert = op.inv if exclude or 'not ' in func else op.pos
    func = funcs.get(func, func)

    if isinstance(filters, dict):
        for key, val in filters.items():
            if key in funcs:
                try:
                    func = funcs.get(key)
                    df = df[vert(func(df[val[0]], val[1]))]
                except IndexError:
                    pass
            else:
                df = df[vert(func(df[key], val))]
    elif is_iter(filters):
        if any(is_iter(elem) for elem in filters):
            dfs = [filter_df(df, elem) for elem in filters]
            df = pd.concat(dfs)
            df = df.groupby(by=df.index).first()  # df[~df.index.duplicated()]

    return df

"'class' == 'Third'"
pd.testing.assert_frame_equal(
    filter_df(df, filters={CLASS: THIRD}), 
    df[df[CLASS].eq(THIRD)]
)

"'class' != 'Third'"
pd.testing.assert_frame_equal(
    filter_df(df, filters={CLASS: THIRD}, exclude=True), 
    df[df[CLASS] != THIRD]
)

"'class' != 'Third'"
pd.testing.assert_frame_equal(
    filter_df(df, filters={CLASS: THIRD}, func='not eq'), 
    df[df[CLASS] != THIRD]
)

"'class' == 'Third' AND embark_town' == 'Southamptom'"
pd.testing.assert_frame_equal(
    filter_df(df, filters={CLASS: THIRD, EMBARK_TOWN: SOUTHAMPTON}),
    df[(df[CLASS] == THIRD) & (df[EMBARK_TOWN] == SOUTHAMPTON)]
)

"'class' == 'Third' OR 'embark_town' == 'Southampton'"
pd.testing.assert_frame_equal(
    filter_df(df, filters=[{CLASS: THIRD}, {EMBARK_TOWN: SOUTHAMPTON}]),
    df[(df[CLASS] == THIRD) | (df[EMBARK_TOWN] == SOUTHAMPTON)]
)

age = 18
# 'age' >= 18
pd.testing.assert_frame_equal(
    filter_df(df, filters={">=": (AGE, age)}),
    df[df[AGE] >= age]
)

# 'age' >= 18 AND 'class' == 'Third
pd.testing.assert_frame_equal(
    filter_df(df, filters={'>=': (AGE, age), CLASS: THIRD}),
    df[(df[AGE] >= age) & (df[CLASS] == THIRD)]
)

# 'age' >= 18 OR 'class' == 'Third'
pd.testing.assert_frame_equal(
    filter_df(df, filters=[{'>=': (AGE, age)}, {CLASS: THIRD}]),
    df[(df[AGE] >= age) | (df[CLASS] == THIRD)]
)

print("done")