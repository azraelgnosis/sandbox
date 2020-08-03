def flatten(dct:dict) -> dict:
    new_dict = {}
    for key, val in dct.items():
        if isinstance(val, dict):
            for key, val in flatten(val).items():
                new_dict[key] = val
        new_dict[key] = val

    return new_dict


d = {
    'a': {
        'aye': 'ei',
        'ah': 'a',
        'a': 'ae',
    },
    'b': 'bee'
}

flat_d = flatten(d)
print(flat_d)

print("done")