def _whereA(conditions) -> str:
        """
        Creates an SQL WHERE clause based on `conditions`.
        If conditions is an instance of:
            str: returns conditions
            dict: returns AND-joined series where 'key = val'
            list:
                if 1-D:
                    if size 3: joins elements of list
                    if size 2: joins elements of list with =
                if 2-D: recursively calls _where()

        :param conditions: A string, dict, or list of conditions.
        :return: String of SQL WHERE clause.
        """

        WHERE = ""
        if isinstance(conditions, str):
            WHERE = conditions
        elif isinstance(conditions, dict):
            WHERE += \
                " AND ".join([f"{key} = '{val}'" for key, val in conditions.items()]) #? val is always a string
        elif isinstance(conditions, list):
            if isinstance(conditions[0], list):
                WHERE += \
                    " AND ".join([_whereA(condition for condition in conditions)])
            elif len(conditions) == 3:
                WHERE += " ".join(conditions)
            elif len(conditions) == 2:
                WHERE += " = ".join(conditions)
        
        return WHERE

def _whereB(condition, pk="id", val="val") -> str:
    """
    If `condition` is an int, returns '`pk` = `condition`'.
    If `condition` is a str without spaces, returns '`name` = `condition`'
    If `condition` is a str with spaces, returns `condition` as is.
    If `condition` is a 1-dimensional list of size 2, returns 'elem[0] = elem[1]'
    If `condition` is a 1-dimensional list of size 3, returns 'elem[0] elem[1] elem[2]',
        assuming elem[1] is a comparison operator.
    If `condition` is a multi-dimensional list, returns a series of conditions conjoined
        by 'AND'.
    """

    if not condition: return

    clause = ""
    try:
        condition = int(condition)
        clause += f"{pk} = {condition}"
    except ValueError:
        if isinstance(condition, str):
            clause += f"{val} = '{condition}'"
    except TypeError:
        if isinstance(condition, list):
            if isinstance(condition[0], list):
                clause += " AND ".join([_whereB(case, pk, val) for case in condition])
            elif len(condition) == 2:
                clause += "=".join(str(elem) for elem in condition) # f"{condition[0]} = {condition[1]}"            
            elif len(condition) == 3:
                clause += " ".join(condition)

    return clause



def where(condition, pk='id', val='val'):
    comparators = ['=']
    conjunctions = ('AND', 'OR', 'NOT')
    WHERE = ""
    try:
        WHERE = f"{pk} = {int(condition)}"
    except ValueError:
        if isinstance(condition, str):
            if any(True for comparison in comparators if comparison in condition):
                WHERE = condition
            else:
                WHERE = f"{val} = {condition}"
    except TypeError:
        if isinstance(condition, dict):
            key = [*condition][0]
            if isinstance(key, tuple):
                WHERE += str(condition[key]).join(str(k) for k in key)
            elif isinstance(key, str) and key.upper() in conjunctions:
                WHERE += " ".join(list(condition.items())[0])
            WHERE += " AND ".join([f"{key} = {val}" for key, val in condition.items()]) #? val is always a string
        elif hasattr(condition, "__iter__"):
            WHERE += "".join([where(c) for c in condition])
            # if hasattr(condition[0], "__iter__") and not isinstance(condition[0], str):
            #     WHERE += " AND ".join([where(case, pk, val) for case in condition])
            # elif len(condition) == 2:  # and all(isinstance(elem, str) for elem in condition):
            #     WHERE += f"{condition[0]} = {condition[1]}"
            # elif len(condition) == 3:
            #     WHERE += " ".join(condition)
    
    return WHERE
        
assert where(4) == "id = 4"
assert where("5") == "id = 5"
assert where("Iroh") == "val = Iroh"
assert where("name = Iroh") == "name = Iroh"
assert where({'name': 'Iroh'}) == "name = Iroh"
assert where({'length': 6}) == "length = 6"
assert where({'width': '7'}) == "width = 7"
# assert where(("color", "red")) == "color = red"
# assert where({("height", 6): ">="}) == "height >= 6"
assert where([("color", "red"), ("height", ">=", "6")]) == "color = red AND height >= 6"
assert where([('Yoda'), {'or': 'Iroh'}]) == "val = Yoda OR val = Iroh"

print("done")