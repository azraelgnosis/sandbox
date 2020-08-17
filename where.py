def is_iter(obj):
    return hasattr(obj, "__iter__") and not isinstance(obj, str)

def contains(containing, contained) -> bool:
    return any(True for elem in contained if elem in containing)

def coerce_type(obj):
    try:
        if '.' in obj:
            obj = float(obj)
        else:
            obj = int(obj)
    except TypeError:
        obj = int(obj)
    except ValueError:
        obj = f"'{obj}'"

    return obj

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

def _whereC(table, condition, pk='id', val='val'):
    comparators = ['=', '!=', '>', '>=', '<', '<=', 'IS', 'IS NOT']
    conjunctions = ('AND', 'OR', 'NOT')
    WHERE = ""
    try:
        WHERE = f"{table}_{pk} = {int(condition)}"
    except ValueError:
        if isinstance(condition, str):
            if any(True for comparison in comparators if comparison in condition):
                WHERE = condition
            else:
                WHERE = f"{table}_{val} = {condition}"
    except TypeError:
        if isinstance(condition, dict):
            key = [*condition][0]
            if isinstance(key, tuple):
                WHERE += str(condition[key]).join(str(k) for k in key)
            elif isinstance(key, str) and key.upper() in conjunctions:
                WHERE += " ".join(list(condition.items())[0])
            WHERE += " AND ".join([f"{key} = {val}" for key, val in condition.items()]) #? val is always a string
        elif hasattr(condition, "__iter__"):
            if hasattr(condition[0], "__iter__") and not isinstance(condition[0], str):
                WHERE += " AND ".join([where(table, case, pk, val) for case in condition])
            elif len(condition) == 2:  # and all(isinstance(elem, str) for elem in condition):
                WHERE += f"{condition[0]} = {condition[1]}"
            elif len(condition) == 3:
                WHERE += " ".join(condition)
    
    return WHERE

def where(table:str, conditions, conjunction='AND'):
    comparators = ('=', '!=', '>', '>=', '<', '<=', 'IS', 'IS NOT')
    conjunctions = ('AND', 'OR', 'NOT')

    WHERE = ""
    if isinstance(conditions, (int, str)):
        try:
            # assumes must be an id: "42" -> "table_id = 42"
            WHERE = f"{table}_id = {int(conditions)}"  
        except ValueError:
            if contains(conditions, comparators):
                WHERE = conditions
            else:
                # or maybe a val: "Picard" -> "table_val = 'Picard'"
                WHERE = f"{table}_val = '{conditions}'"  
        except TypeError:
            print("Somethin's up!")
            raise TypeError

    elif isinstance(conditions, dict):
        temp = []
        for key, val in conditions.items():
            if key in conjunctions:
                temp.append(where(table, val, conjunction=key))
            elif isinstance(key, tuple):
                temp.append(f"{key[0]} {val} {coerce_type(key[1])}")
            else:
                temp.append(f"{key} = {coerce_type(val)}")

        WHERE = f" {conjunction} ".join(temp)

    elif is_iter(conditions):
        if any(is_iter(condition) for condition in conditions):
            temp = []
            for condition in conditions:
                temp.append(where(table, condition))
            WHERE = f" {conjunction} ".join(temp)
        else:
            if len(conditions) == 1:
                WHERE = where(table, conditions[0])
            elif len(conditions) == 2:
                WHERE = f"{conditions[0]} = {coerce_type(conditions[1])}"
            elif len(conditions) == 3:
                WHERE = f"{conditions[0]} {conditions[1]} {coerce_type(conditions[2])}"

    return WHERE

assert where('user', 4) == "user_id = 4"
assert where('user', "5") == "user_id = 5"
assert where('user', "Iroh") == "user_val = 'Iroh'"
assert where('user', "name = 'Iroh'") == "name = 'Iroh'"
assert where('user', {'name': 'Iroh'}) == "name = 'Iroh'"
assert where('user', {'length': 6}) == "length = 6"
assert where('user', {'width': '7'}) == "width = 7"
assert where('user', {'width': 7, 'color': 'red'}) == "width = 7 AND color = 'red'"
assert where('user', ("color", "red")) == "color = 'red'"
assert where('user', ('height', '>=', '6')) == 'height >= 6'
assert where('user', {("height", 6): ">="}) == "height >= 6"
assert where('user', [("color", "red"), ("height", ">=", "6")]) == "color = 'red' AND height >= 6"
dct = {
    'OR': [
        4, 
        ['name', 'Azula']
    ]
}
assert where('user', dct) == "user_id = 4 OR name = 'Azula'"
dct = {
    'OR': {
        'AND': [
            [4], 
            ['name', 'Azula']
        ],
        'OR': [
            'Zuko',
            ['toes', '>=', 5],
        ]
    }
}
assert where('user', dct) == "user_id = 4 AND name = 'Azula' OR user_val = 'Zuko' OR toes >= 5"

print("done")