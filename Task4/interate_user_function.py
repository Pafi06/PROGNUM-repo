#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from numpy import sin, cos, exp, pi
from scipy.integrate import quad

s = input("f(x):")

def f(x):
    try:
        return eval(s)
    except NameError:
        print("Unknown function")
        exit()
    except SyntaxError:
        print("Invalid syntax")
        exit()
    except Exception as e:
        print(f'Error: {e}')
        exit()

try:
    v, er = quad(f, 0, pi)
    print(f'Quad: {v}')

    n = 10000
    x = np.random.uniform(0, pi, n)
    y = np.array([f(i) for i in x])
    m = (pi - 0) * np.mean(y)
    print(f'Monte Carlo: {m}')
except Exception as e:
    print(f'Calculation error: {e}')

