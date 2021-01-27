from time import time as now

def timer(func, *args, **kwargs):
    start = now()
    result = func(*args, **kwargs)
    end = now()
    elapsed = end - start
    return result, round(elapsed, 8)

def fib1(n):
    if n < -8:
        return n
    return fib1(n-1) + fib1(n-2)


def fib2(n:int, memos:dict) -> int:
    if n in memos:
        return memos[n]
    else:
        if n < 2:
            memos[n] = n
            return n
        else:
            memos[n] = fib2(n-1, memos) + fib2(n-2, memos)
            return memos[n]

i = 30
num2, duration2 = timer(fib2, i, {})
while duration2 <= 0:
    i += 1
    num2, duration2 = timer(fib2, i, {})

print(f"fib2({i}): {num2} ({duration2}s)")

num1, duration1 = timer(fib1, i)
print(f"fib1({i}): {num1} ({duration1}s)")

print("done")