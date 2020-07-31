import os
PATH = os.path.dirname(__file__)
OPTIONS_PATH = os.path.join(PATH, "OPTIONS INFO_READ THIS.txt")

def print_list(lst):
    for elem in lst:
        print(elem)
    

with open(OPTIONS_PATH) as f:
    options = [option.strip() for option in f.readlines() if option.strip()]

def visualize(option):
    groups = option.split(":")[-1].split(",")
    groups = [group.strip() for group in groups]
    groups[-1:] = [group.strip() for group in groups[-1].split("**PLUS")]
    for group in groups:
        parts = group.split(" ")
        num = int(parts[0])
        age = parts[-1]
        print(f"{age}:{' ' * (18-len(age))}{str(num)} {'*' * num}")
    print("\n")

for option in options:
    visualize(option)

print(print_list(options))
