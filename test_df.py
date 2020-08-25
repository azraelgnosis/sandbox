import inspect
import operator as op
import os
import pandas as pd

AGE = 'age'

CLASS = 'class'
THIRD = 'Third'

EMBARK_TOWN = 'embark_town'
SOUTHAMPTON = 'Southampton'

df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'titanic.csv'))

def is_iter(obj) -> bool:
    return hasattr(obj, '__iter__') and not isinstance(obj, str)

def coerce_type(obj):
    if isinstance(obj, str):
        try:
            if "." in obj:
                obj = float(obj)
            else:
                obj = int(obj)
        except (ValueError, TypeError):
                pass

    return obj

def get_num_args(func) -> int:
    try:
        num = len(inspect.getargspec(func).args)
    except TypeError:
        num = len(func.__text_signature__.split(",") - 2)

def test_df(df, tests, data=None) -> bool:
    conjunctions = ('and', 'or')
    operations = {
        'and': all,
        'or': any,
        "get": lambda df, column_name: df[column_name],
        "groupby": pd.DataFrame.groupby,
        'count': pd.DataFrame.count,
        'first': pd.core.groupby.GroupBy.first,
        'sum': pd.Series.sum,
        "len": len,
        'unique': pd.Series.unique,
        '==': op.eq,  # pd.Series.eq
        'ge': op.ge,  # pd.Series.ge
        ">=": op.ge,  # pd.Series.ge
    }

    if isinstance(data, bool):  # while not isinstance(data, bool):
        return data

    for key, val in tests.items():
        func = operations.get(key.split()[0].lower())
        if key.lower() in conjunctions:
            data = [test_df(df, test) for test in val]
            return func(data)

        elif isinstance(val, dict):
            data = test_df(df, val, data)
            try:
                data = func(data, coerce_type(key.split()[1]))
            except IndexError:
                try:
                    data = func(data, val)
                except TypeError:
                    data = func(data)                            

        else:
            try:
                data = func(df, val)
            except TypeError:
                data = func(df)
    
    return data

tests = {
    "== 3": {
        "len":{
            "groupby": "class"
        }
    }
}
assert test_df(df, tests) == True

tests = {
    "and": [
        {
            ">= 6": {
                "len": {
                    "groupby": "deck"
                }       
            }
        },
        {
            ">= 50": {
                "sum": {
                    "get": "survived"
                }
            }
        }
    ]
}
assert test_df(df, tests) == True

tests = {
    "and": [
        {
            ">= 10": {
                "len": {
                    "groupby": "deck"
                }       
            }
        },
        {
            ">= 50": {
                "sum": {
                    "get": "survived"
                }
            }
        }
    ]
}
assert test_df(df, tests) == False

tests = {
    "or": [
        {
            ">= 10": {
                "len": {
                    "groupby": "deck"
                }       
            }
        },
        {
            ">= 50": {
                "sum": {
                    "get": "survived"
                }
            }
        }
    ]
}
assert test_df(df, tests) == True

print("done")