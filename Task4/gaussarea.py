#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def gauss(x, A, x0, sigma, z0):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))+z0

A = float(input("A:"))
x0 = float(input("x0:"))
sig = float(input("sig:"))
z0 = float(input("z0:"))

low = float(input("Lower limit:"))
up = float(input("Upper limit:"))

x = np.linspace(-10, 10, 200)
y = gauss(x, A, x0, sig, z0)

a, er = quad(gauss, low, up, args=(A, x0, sig, z0))

plt.figure(figsize=(10, 8))
plt.plot(x, y, label=f'Gaussian (sigma={sig})')

xf = np.linspace(low, up, 100)
yf = gauss(xf, A, x0, sig, z0)
plt.fill_between(xf, yf, z0, alpha=0.2, label=f'Integrated Area: {a}')

plt.title("Area under Gaussian")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.axhline(z0, color="black", alpha=0.5)
plt.legend()
plt.grid(True, alpha=0.3)

print(f'Area: {a}')

plt.show()

