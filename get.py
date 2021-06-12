def get(obj, path, null=False, sep="."):
    """
    Retrieves attribute from `obj` following `sep`-separated `path`.
    :param obj: object (including dictionaries).
    :param path: str containing the path to desired object separated by `sep`
    :param null: If True, returns None instead of `path` or `obj` if invalid.
    :param sep: string to indicate separator between levels (default: ".")
    :return: object attribute
    """

    if isinstance(path, dict):
        obj = {key: get(obj, val, null, sep) for key, val in path.items()}
    elif isinstance(path, str):
        split_path = path.split(sep)
        try:
            for key in split_path:
                try:
                    obj = getattr(obj, key)
                except AttributeError:
                    obj = obj[key]
        except KeyError:
            obj = None if null else path
        except TypeError:
            obj = None if null else obj
    else:
        obj = None if null else path

    return obj
