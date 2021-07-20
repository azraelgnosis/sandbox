import pytest

from nonstaticmethod.nonstaticmethod import nonstaticmethod

SENTINEL = object()


class Success(BaseException):
    pass


class Point2D(object):
    """Just a quick example case."""

    axes = ['x', 'y']

    def __init__(self, x=0, y=0):
        self.position = dict.fromkeys(self.axes, 0)
        self.position['x'] = x
        self.position['y'] = y

    def __getattr__(self, attr, default=SENTINEL):
        try:
            return self.position[attr]
        except KeyError:
            if default is SENTINEL:
                return super().__getattribute__(attr)
            else:
                return super().__getattribute__(attr, default)

    def __getitem__(self, item, default=SENTINEL):
        try:
            return self.position[item]
        except KeyError:
            if default is SENTINEL:
                return super().__getattribute__(item)
            else:
                return super().__getattribute__(item, default)

    @nonstaticmethod
    def distance_nonstatic(cls, obj, other):
        """Method under consideration."""
        # squares = []
        # for axis in cls.axes:
        #     position_a = obj[axis]
        #     position_b = other[axis]
        #     squares.append(pow(position_b - position_a, 2))

        # return pow(sum(squares), 0.5)
        return pow(sum([pow(other[axis] - obj[axis], 2) for axis in cls.axes]), 0.5)

    def distance_instance(self, other):
        """By way of comparison."""
        return pow(sum([pow(other[axis] - self[axis], 2) for axis in self.axes]), 0.5)

    @classmethod
    def distance_class(cls, obj, other):
        """By way of comparison."""
        return pow(sum([pow(other[axis] - obj[axis], 2) for axis in cls.axes]), 0.5)


py_triple = {'x': 3, 'y': 4}
origin = {'x': 0, 'y': 0}
origin_point = Point2D(**origin)
triple_point = Point2D(**py_triple)

print(origin_point.distance_nonstatic(triple_point, ))
print(origin_point.distance_nonstatic(py_triple, ))
print(Point2D.distance_nonstatic(origin_point, triple_point, ))
print(Point2D.distance_nonstatic(origin_point, triple_point, ))
print(Point2D.distance_nonstatic(origin, triple_point, ))
print(Point2D.distance_nonstatic(origin, py_triple, ))


@pytest.mark.parametrize(['point', 'other', 'expected'], [(origin_point, triple_point, 5), (origin_point, py_triple, 5)])
def test_instance_call(point, other, expected):
    assert point.distance_nonstatic(other, ) == expected


@pytest.mark.parametrize(['obj_1', 'obj_2', 'expected'], [(origin_point, triple_point, 5), (origin_point, py_triple, 5), (origin, triple_point, 5), (origin, py_triple, 5)])
def test_class_call(obj_1, obj_2, expected):
    assert Point2D.distance_nonstatic(obj_1, obj_2, ) == expected


# just to demonstrate the "gap", as such

@pytest.fixture
def expected():
    return {
        (False, 'distance_class'): TypeError,
        (True, 'distance_instance', False): AttributeError,
    }


@pytest.mark.parametrize('func', ['distance_nonstatic', 'distance_instance', 'distance_class'])
@pytest.mark.parametrize('point', [origin_point])
@pytest.mark.parametrize('other', [triple_point, py_triple])
def test_instance_call2(func, point, other, expected):
    expected_exception = expected.get((isinstance(point, type), func), Success)
    with pytest.raises(expected_exception):
        assert getattr(point, func)(other) == 5
        raise Success


@pytest.mark.parametrize('func', ['distance_nonstatic', 'distance_instance', 'distance_class'])
@pytest.mark.parametrize('obj_1', [origin_point, origin])
@pytest.mark.parametrize('obj_2', [triple_point, py_triple])
def test_class_call2(func, obj_1, obj_2, expected):
    expected_exception = expected.get((isinstance(Point2D, type), func, isinstance(obj_1, Point2D)), Success)
    with pytest.raises(expected_exception):
        assert getattr(Point2D, func)(obj_1, obj_2) == 5
        raise Success
