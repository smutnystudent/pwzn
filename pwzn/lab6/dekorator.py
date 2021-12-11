import numpy as np
from time import time

def function(*args):
    n = args[0]
    a = np.random.random(n)
    a2 = a**2
    return a2

def decorator(repeat = 1):
    def inner(function):
        def wrapper(*args, **kwargs):
            sum_time = 0
            for i in range(repeat):
                t1 = time()
                function(*args, **kwargs)
                t2 = time()
                sum_time += (t2 - t1)
            print("średni czas wykonywania funkcji: ", sum_time/repeat)
        return wrapper
    return inner

decorator(10)(function)(10000)