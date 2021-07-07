import pandas as pd
from sys import version_info

from get import get, collect
from iterfy import  iterfy

if version_info < (3,):
    pass
else:
    unicode = str

SENTINEL = object()
NUMBER_TYPES = (int, float, complex, pd.Int64Dtype)
STRING_TYPES = (str, unicode)


class dataclass(object):
    default_values = {
        int: int(0),
        float: float(0),
        complex: complex(0),
        pd.Int64Dtype: int(0),
        str: str(''),
        unicode: unicode('')
    }

    loose_types = {
        int: NUMBER_TYPES,
        float: NUMBER_TYPES,
        str: STRING_TYPES,
    }

    null_types = {
        int: pd.np.nan,
        float: pd.np.nan,
        str: None,
    }

    @classmethod
    def __new__(cls, _=None, params=None, *args, **kwargs):
        params = params or []
        positional = iterfy(kwargs.pop('params', params)) + list(args)
        default_none = kwargs.pop('default_none', [])
        dtypes = kwargs.pop('dtypes', {})
        loose_types = cls.loose_types if kwargs.pop('loose_types', True) else {}
        # dtypes = {key: loose_types.get(val, val) for key, val in dtypes.items()}
        use_dtype_defaults = kwargs.pop('use_dtype_defaults', False)
        default = kwargs.pop('default', {})
        aliases = kwargs.pop('aliases', {})

        default.update(kwargs)

        positional_params = positional
        null_params = dict.fromkeys(default_none)
        dtype_params = {col: cls.default_values.get(col, None) for col in dtypes.keys()}
        default_params = {
            **null_params,
            **(dtype_params if use_dtype_defaults else {}),
            **default}

        data_columns = positional_params + list(default_params) + list(dtypes)

        cls._class_dict = {
            'positional_params': positional_params,
            'default_params': default_params,
            'dtypes': dtypes,
            'loose_types': cls.loose_types,
            'null_types': cls.null_types,
            'data_columns': data_columns,
            'aliases': aliases,
            **default_params
        }

        return super().__new__(cls)

    def __repr__(self): return self.__class__.__name__

    def __call__(self, class_, *args, **kwargs):
        new_dataclass = type(class_.__name__, (Dataclass, class_), self._class_dict)

        return new_dataclass


class Dataclass(object):
    positional_params = None
    default_params = None
    data_columns = None
    dtypes = None
    aliases = None
    errors = None

    def __init__(self, *args, **kwargs):
        self._validate_arguments(args, kwargs)

        init_values = {
            **dict(zip(self.positional_params, args)),
            **kwargs}
        for param, arg in init_values.items():
            setattr(self, param, arg)

        self._setup(args, kwargs)

    def _setup(self, *args, **kwargs): pass

    def _validate_arguments(self, args, kwargs):
        # if missing := [p for p in self.positional_params if p not in {**self.default_params, **kwargs}][len(args):]
        if missing := list(set(self.positional_params).difference(self.default_params).difference(kwargs))[len(args):]:
            raise ValueError("Missing arguments for parameters: ({})".format(", ".join(missing)))
        if extra := max(0, len(args) - len(self.positional_params)):
            raise ValueError(
                f"{repr(self)} accepts at most {len(self.positional_params)} positional arguments; {extra} provided")

    def __repr__(self):
        return f"{self.__class__.__base__.__name__}: {self.__class__.__name__}"

    def __getattr__(self, attr):
        return super().__getattribute__(self.aliases.get(attr, attr))

    def __getitem__(self, item):
        return getattr(self, self.aliases.get(item, item))

    def __setattr__(self, attr, val):
        attr = self.aliases.get(attr, attr)
        attr_type = self.dtypes.get(attr, None)
        loose_types = self.loose_types.get(attr_type, ())
        if attr_type:
            if val is None:
                val = self.null_types.get(attr_type, None)
            elif not isinstance(val, attr_type) or not isinstance(val, loose_types):
                raise TypeError
        super().__setattr__(attr, val)

    def __setitem__(self, item, val): setattr(self, item, val)

    def collect(self, paths, default=None, return_type=None):
        return collect(self, paths, default=default, return_type=return_type)

    def get(self, path, default=None):
        return get(obj=self, path=path, default=default)

    @property
    def empty_df(self):
        return pd.DataFrame(columns=self.data_columns).astype(self.dtypes)

    @classmethod
    def from_dict(cls, dct):
        return cls(**dict(zip(cls.data_columns, map(dct.get, cls.data_columns))))

    def to_dict(self):
        # return dict(zip(self.data_columns, map(self.get, self.data_columns)))
        # return {col: getattr(self, col) for col in self.data_columns}
        return self.collect(self.data_columns, return_type=dict)

    def to_series(self):
        # return pd.Series(data=map(self.get, self.data_columns), index=self.data_columns, name=self.__class__.__name__)
        return pd.Series(data=self.to_dict(), name=self.__class__.__name__, dtype=self.dtypes)
