# def f(v):
#     if "." in str(v):
#         try:
#             v = float(v)
#         except ValueError:
#             pass
#     else:
#         try:
#             v = int(v)
#         except ValueError:
#             pass
#         except TypeError:
#             pass

#     return v

def coerce_type(cls, val, separator=",", none=None):
    """
    Coerces `val` as a float or int if applicable,
    if `val` is None, returns the value of `none`
    else returns original value.

    :param val: Value to coerce.
    """

    if val is None:
        val = none
    elif isinstance(val, str):
        if len(coll := val.split(separator)) > 1:
            val = [cls._coerce_type(elem.strip()) for elem in coll]

        try:
            if "." in str(val):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                val = float(val)
            else:
                val = int(val)
        except (TypeError, ValueError):
            pass

    return val


def check(input, correct_val, correct_type, nested_type=None, func=_coerce_type):
    output = func(input)
    assert type(output) is correct_type, f"{output} is not {correct_type}"
    assert output == correct_val, f"{output} != {correct_val}"
    if nested_type:
        assert all(type(elem) is nested_type for elem in output)

check(None, None, type(None))
check(1, 1, int)
check(2.0, 2.0, float)
check(2.2, 2.2, float)
check("1", 1, int)
check("2.2", 2.2, float)
check("2.0", 2.0, float)
check("1.2.3", "1.2.3", str)
check("str", "str", str)
check("Yup.", "Yup.", str)
check("J.R.R. Tolkien", "J.R.R. Tolkien", str)
check("123, 234", [123, 234], list, int)
check("abc, bcd", ["abc", "bcd"], list, str)
check("abc,", ["abc", ""], list, str)
    
print("Done")