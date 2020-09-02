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