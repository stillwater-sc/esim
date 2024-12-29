# Simplest decorator
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called")
        func()
        print("Something is happening after the function is called")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# When we call say_hello(), it prints:
# Something is happening before the function is called
# Hello!
# Something is happening after the function is called

def decorator_with_args(func):
    def wrapper(*args, **kwargs):    # *args and **kwargs let you pass any arguments
        print("Before function")
        result = func(*args, **kwargs)
        print("After function")
        return result
    return wrapper

@decorator_with_args
def add_numbers(a, b):
    return a + b

# Now you can call: add_numbers(3, 5)

def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello {name}")

# When called with greet("Alice"), it will print "Hello Alice" three times

import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to run")
        return result
    return wrapper

@measure_time
def slow_function():
    time.sleep(1)
    return "Done!"


# To preserve the original function's metadata (like docstrings and function name),
# you should use the @functools.wraps decorator:

from functools import wraps

def my_decorator(func):
    @wraps(func)  # This preserves the original function's metadata
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper



if __name__ == "__main__":
    say_hello()
    print("\n\n")
    print(f'Result : ' + str(add_numbers(3, 5)))
    print("\n\n")
    greet("Alice")
    print("\n\n")
    slow_function()