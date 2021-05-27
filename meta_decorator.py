from memoisation import memoize

def meta_decorator(*decorators):
    def wrapper(function):
        for decorator in reversed(decorators):
            function = decorator(function)
        return function
    return wrapper

class Alpha:
    @meta_decorator(staticmethod, memoize)
    def fibonacci_r(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return Alpha.fibonacci_r(n-1) + Alpha.fibonacci_r(n-2)

print(Alpha.fibonacci_r(99))

print("done")
