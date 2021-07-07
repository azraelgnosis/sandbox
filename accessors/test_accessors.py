import json
import operator as op
import os
import pytest

FOLDER_PATH = os.path.dirname(__file__)
BAD_COMBOS_PATH = os.path.join(FOLDER_PATH, "bad_combos.json")


def get_lambda_bytecode(lmbda):
    return op.attrgetter('co_code')(lmbda.__code__).decode('utf-8', 'replace')


class TestClass(object):
    def __new__(cls, x, y, getitem, get_attribute, get_attr):
        cls.__getitem__ = getitem
        cls.__getattribute__ = get_attribute
        cls.__getattr__ = get_attr

        return super().__new__(cls)

    def __init__(self, x, y, getitem, get_attribute, get_attr):
        self.x = x
        self.y = y


getitems = [
    # lambda self, item: raise AttributeError,
    pytest.param(lambda self, item: self.__getattribute__(item), id='self.__getattribute__(item)'),
    pytest.param(lambda self, item: super(TestClass, self).__getattribute__(item), id='super().__getattribute__(item)'),
    pytest.param(lambda self, item: self.__getitem__(item), id='self.__getitem__(item)'),
    pytest.param(lambda self, item: self.__getattr__(item), id='self.__getattr__(item)'),
    pytest.param(lambda self, item: self[item], id='self[item]'),
    pytest.param(lambda self, item: getattr(self, item), id='getattr(self, item)'),
]

getattributes = [
    pytest.param(lambda self, attribute: self.__getattribute__(attribute), id='self.__getattribute__(attribute)'),
    pytest.param(lambda self, attribute: super(TestClass, self).__getattribute__(attribute), id='super().__getattribute__(attribute)'),
    pytest.param(lambda self, attribute: self.__getitem__(attribute), id='self.__getitem__(attribute)'),
    pytest.param(lambda self, attribute: self.__getattr__(attribute), id='self.__getattr__(attribute)'),
    pytest.param(lambda self, attribute: self[attribute], id='self[attribute]'),
    pytest.param(lambda self, attribute: getattr(self, attribute), id='getattr(self, attribute)'),
]

getattrs = [
    pytest.param(lambda self, attr: self.__getattribute__(attr), id='self.__getattribute__(attr)'),
    pytest.param(lambda self, attr: super(TestClass, self).__getattribute__(attr), id='super().__getattribute__(attr)'),
    pytest.param(lambda self, attr: self.__getitem__(attr), id='self.__getitem__(attr)'),
    pytest.param(lambda self, attr: self.__getattr__(attr), id='self.__getattr__(attr)'),
    pytest.param(lambda self, attr: self[attr], id='self[attr]'),
    pytest.param(lambda self, attr: getattr(self, attr), id='getattr(self, attr)'),
]


# bad_combos = [
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_item': b't\x00\x83\x00\xa0\x01|\x01\xa1\x01S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_item': b'|\x00\xa0\x00|\x01\xa1\x01S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_item': b't\x00|\x00|\x01\x83\x02S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_item': b'|\x00|\x01\x19\x00S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b't\x00\x83\x00\xa0\x01|\x01\xa1\x01S\x00', 'get_item': b'|\x00\xa0\x00|\x01\xa1\x01S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b't\x00\x83\x00\xa0\x01|\x01\xa1\x01S\x00', 'get_item': b't\x00\x83\x00\xa0\x01|\x01\xa1\x01S\x00'},
#     {'get_attr': b'|\x00\xa0\x00|\x01\xa1\x01S\x00', 'get_attribute': b't\x00\x83\x00\xa0\x01|\x01\xa1\x01S\x00', 'get_item': b'|\x00|\x01\x19\x00S\x00'},
# ]


@pytest.mark.parametrize('get_item', getitems)
@pytest.mark.parametrize('get_attribute', getattributes)
@pytest.mark.parametrize('get_attr', getattrs)
def test_getters(get_item, get_attribute, get_attr):
    tc = TestClass(1, 5, get_item, get_attribute, get_attr)

    getter_dict = {
        'get_attr': get_lambda_bytecode(get_attr),
        'get_attribute': get_lambda_bytecode(get_attribute),
        'get_item': get_lambda_bytecode(get_item)}

    with open(BAD_COMBOS_PATH) as f:
        bad_combos = json.load(f)

    if any(combo == getter_dict for combo in bad_combos):
        raise OverflowError

    bad_combos.append(getter_dict)
    with open(BAD_COMBOS_PATH, "w") as f:
        json.dump(bad_combos, f, indent=4)

    try:
        assert tc.x, tc.y == (1, 5)
        assert tc['x'], tc['y'] == (1, 5)
        assert getattr(tc, 'x'), getattr(tc, 'y') == (1, 5)
        assert tc.__getattribute__('x'), tc.__getattribute__('y') == (1, 5)
        assert tc.__getitem__('x'), tc.__getitem__('y') == (1, 5)
        assert tc.__getattr__('x'), tc.__getattr__('y') == (1, 5)
    finally:
        with open(BAD_COMBOS_PATH) as f:
            bad_combos = json.load(f)
        bad_combos.pop()
        with open(BAD_COMBOS_PATH, "w") as f:
            json.dump(bad_combos, f, indent=4)
