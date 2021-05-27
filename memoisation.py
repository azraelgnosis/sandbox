def fibonacci(n):
    previous = 0
    current = 1
    result = 0
    for i in range(n-1):
        result = previous + current
        previous = current
        current = result
    return result

def memoize(function):
    memo = {}
    def wrapper(*args, **kwargs):
        if args in memo.keys():
            return memo[args]
        memo[args] = function(*args, **kwargs)
        return memo[args]
    return wrapper

@memoize
def fibonacci_r(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_r(n-1) + fibonacci_r(n-2)

def fibonacci_m(n, memo=None):
    memo = memo or {0: 0, 1:1}
    if n in memo.keys():
        return memo[n]
    memo[n] = fibonacci_m(n-1, memo) + fibonacci_m(n-2, memo)
    return memo[n]
    

if __name__ == "__main__":
    num = 10
    print(fibonacci(num))
    print(fibonacci_m(num))
    print(fibonacci_r(num))

    print("done")
