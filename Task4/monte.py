#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def monte():
    f = input("Function:")
    a = float(input("Lower Boundry:"))
    b = float(input("Upper Boundry:"))
    
    n = 100000
    x = np.random.uniform(a,b,n)
    
    y = eval(f, {"x": x, "np": np})
    
    integral = (b - a) * np.mean(y)
    
    print(integral)

monte()

