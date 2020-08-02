def flatten(dct:dict) -> dict:
    new_dict = {}
    for key, val in dct.items():
        if isinstance(val, dict):
            pass
        new_dict[key] = val