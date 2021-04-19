import re

bread = {
    "cymraeg": ["/ˈbara/", "/ˈbaːra/", "/ˈbara/"],
    "brezhoneg": ["/ˈba.ʁa/"],
    "kernowek": ["['bara]", "['bærɐ]"],
    "gaeilge": ["/əˈɾˠɑːn̪ˠ/", "/əˈɾˠɑːn/", "/ˈɾˠɑːn/", "/ˈɾˠɑːnˠ/", "/ˈaɾˠænˠ/"],
    "gaidhlig": ["[ˈaɾan]"]
}

test = """
bak
b
a
k
ba
bk
ak
xbak
bxak
baxk
bakx
bbak
babk
bakb
abak
baak
baka
kbak
bkak
bakk
babak
bakak
"""

pattern = 'bak'
test2 = "fenlbkdcveacverwcvdv"

def subdivide(pattern:str, text:str) -> list:
    remaining = text
    result = []
    for char in pattern:
        parts = remaining.split(char, 1)
        if not parts[0] == remaining:
            result.append(parts[0])
            result.append(char)
        else:
            result.append("")
            result.append("")
        remaining = parts[-1]

    result.append(remaining)
    return result

subdivisions = [subdivide(pattern, elem) for elem in test.splitlines()]
    

print("done")