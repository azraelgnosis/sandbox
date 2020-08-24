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

def get(df:pd.DataFrame, column_name:str) -> pd.Series:
    return df[column_name]

def test_df(df, tests, data=None) -> bool:
    conjunctions = {
        'AND': all,
        'OR': any
    }
    operations = {
        "get": get,
        "groupby": pd.DataFrame.groupby,
        "len": len,
        'unique': pd.Series.unique,
        'sum': pd.Series.sum,
        '==': op.eq,  # pd.Series.eq
        'ge': op.ge,  # pd.Series.ge
        ">=": op.ge,  # pd.Series.ge
    }

    if isinstance(data, bool):  # while not isinstance(data, bool):
        return data

    if isinstance(tests, dict):
        for key, val in tests.items():
            if key in conjunctions:
                func = conjunctions.get(key)
                data = func([test_df(df, test) for test in val])
                return data                

            elif isinstance(val, dict):
                data = test_df(df, val, data)
                if (oper := key.split()[0]) in operations:
                    func = operations.get(oper)
                    try:
                        data = func(data, coerce_type(key.split()[1]))
                    except (KeyError, IndexError):
                        try:
                            data = func(data, val)
                        except TypeError:
                            data = func(data)                            
                    except TypeError:
                        data = func(data)
            else:
                if key in operations:
                    func = operations.get(key)
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
    "AND": [
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
    "AND": [
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
    "OR": [
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