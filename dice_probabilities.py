from collections import defaultdict
import matplotlib.pyplot as plt
from random import randint

def roll(num:int=1, sides:int=6, plus=0) -> int:
    return sum(randint(1, sides) for roll in range(num)) + plus

rolls = defaultdict(int)

# for i in range(pow(10, 6)):
#     rolls[roll(1, 20)] += 1

for i in range(pow(10, 6)):
    rolls[((roll(1, 4)-1)*5) + roll(1,5)] += 1

keys = rolls.keys()
graph = plt.bar(keys, [rolls[k] for k in keys])
plt.show()