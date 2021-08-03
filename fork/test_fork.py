import pytest
from fork.fork import fork


def is_even(n): return not bool(n % 2)
def is_prime(n): return all(n % x for x in range(2, n))


fork_inputs = [
    pytest.param({
        'condition': is_even,
        'iterable': [1, 2, 3],
        "expected": [[2], [1, 3]]},
        id="condition_callable"),
    pytest.param({
        "condition": None,
        "iterable": [1, None, 2, 0, 3, []],
        "expected": [[1, 2, 3], [None, 0, []]]},
        id="condition_None"),
    pytest.param({
        'condition': [is_prime, is_even],
        'iterable': range(10),
        "expected": [[0, 1, 2, 3, 5, 7], [4, 6, 8], [9]]},
        id="condition_iterable"),
    pytest.param({
        'condition': [is_prime, is_even],
        'iterable': range(10),
        "replacement": True,
        "expected": [[0, 1, 2, 3, 5, 7], [0, 2, 4, 6, 8], [9]]},
        id="condition_iterable_replacement"),
    pytest.param(
        {"condition": {"prime": is_prime, "even": is_even},
         "iterable": range(10),
         "replacement": True,
         "expected": {"prime": [0, 1, 2, 3, 5, 7], "even": [0, 2, 4, 6, 8], None: [9]}},
        id="condition_dict"),
    pytest.param({
        "condition": [lambda x: x.endswith(".json"), lambda x: x.endswith(".sql") or x.endswith(".sql.gz")],
        "iterable": ["sdvwe.json", "asdf.sql", "fbtevqv.json", "sawetgz.sql.gz"],
        "expected": [["sdvwe.json", "fbtevqv.json"], ["asdf.sql", "sawetgz.sql.gz"], []]},
        id="use_case"),
]


@pytest.mark.parametrize(["kwargs"], fork_inputs)
def test_fork(kwargs):
    expected = kwargs.pop("expected")
    actual = fork(**kwargs)
    assert actual == expected
