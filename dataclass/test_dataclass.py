import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

import __init__
from dataclass.dataclass import dataclass, Dataclass


@pytest.fixture
def dataclass_parameters():
    return {
        'params': ['id', 'name', 'age'],
        'default': {'age': 0, 'species': 'Human', 'limbs': 4, 'size': 'Medium'},
        'default_none': ['gender', 'offspring', 'hair_color', 'eye_color', 'size', 'species'],
        'dtypes': {'id': int, 'age': int, 'weight': float},
    }


@pytest.fixture
def TestClass(dataclass_parameters):
    @dataclass(**dataclass_parameters)
    class Zeta(object):
        pass
    return Zeta


@pytest.fixture
def dataclass_args():
    return 1, 'Dijkstra'


@pytest.fixture
def dataclass_kwargs():
    return {'eye_color': 'Grey'}


@pytest.fixture
def test_instance(TestClass, dataclass_args, dataclass_kwargs):
    return TestClass(*dataclass_args, **dataclass_kwargs)


def test_repr(test_instance):
    assert repr(test_instance) == f"Dataclass: {test_instance.__class__.__name__}"


def test_empty_df(test_instance):
    assert_frame_equal(
        test_instance.empty_df,
        pd.DataFrame(columns=test_instance.data_columns).astype(test_instance.dtypes))


def test_default(test_instance, dataclass_parameters):
    expected_default = dataclass_parameters['default']
    actual_default = test_instance.collect(expected_default.keys(), return_type=dict)
    assert actual_default == expected_default


def test_default_none(test_instance): return
def test_init(test_instance): return
def test_get(test_instance): return
def test_to_series(test_instance): return
def test_to_dict(test_instance): return


def test_empty_decorator():
    @dataclass()
    class EmptyDecorator(object):
        pass
    b = EmptyDecorator()


def test_args():
    @dataclass('one', 'two', 'three')
    class Args(object):
        pass

    a = Args(1, 2, 3)

    assert a.to_dict() == {'one': 1, 'two': 2, 'three': 3}


def test_params():
    @dataclass(['one', 'two'])
    class Params(object):
        pass

    p = Params(1, 2)

    assert p.to_dict() == {'one': 1, 'two': 2}


@pytest.mark.parametrize('dataclass_args,instance_args,instance_kwargs', [
    pytest.param(['one', 'two', 'three'], [1], {'three': 3}, id='missing_arguments'),
    pytest.param(['one', 'two', 'three'], [1, 2, 3, 4, 5, 6, 7], {'two': 2, 'three': 3, 'four': 4, 'five': 5},
                 id='extra_arguments'),
])
def test_arguments(dataclass_args, instance_args, instance_kwargs):
    with pytest.raises(ValueError) as e:
        @dataclass(dataclass_args)
        class TestClass(object):
            pass

        TestClass(*instance_args, **instance_kwargs)


def test_from_dict(TestClass):
    tc = TestClass.from_dict({'id': 3, 'name': 'blah', 'age': 54})
    assert tc.collect(['id', 'name', 'age'], return_type=dict) == {'id': 3, 'name': 'blah', 'age': 54}


def test_getattr(test_instance, dataclass_kwargs):
    attr = next(iter(dataclass_kwargs))
    assert getattr(test_instance, attr) == dataclass_kwargs[attr]


def test_getitem(test_instance, dataclass_kwargs):
    attr = next(iter(dataclass_kwargs))
    assert test_instance[attr] == dataclass_kwargs[attr]


def test_setattr(test_instance):
    test_instance.name = "Zhao"
    assert test_instance.name == "Zhao"


def test_setitem(test_instance):
    test_instance['name'] = "Zhao"
    assert test_instance['name'] == "Zhao"


def test_null_types(test_instance):
    test_instance.age = None
    assert test_instance.age is pd.np.nan


def test_dtype_fail(test_instance):
    with pytest.raises(TypeError):
        test_instance.age = 'Eleventy-One'


if __name__ == "__main__":
    pytest.main(['./testing/test_dataclass.py'])
