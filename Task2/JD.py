#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math

def jd(y,m,d):
    t1 = 367 * y
    t2 = (7 * (y + (m + 9) / 12)) / 4
    t3 = (3 * ((y + (m - 9) / 7) / 100 +1)) / 4
    t4 = (275 * m) / 9
    jda = t1 - t2 - t3 + t4 + d + 1721029 - 0.5
    return jda

y1 = float(input("Year 1:"))
m1 = float(input("Month 1:"))
d1 = float(input("Day 1:"))

y2 = float(input("Year 2:"))
m2 = float(input("Month 2:"))
d2 = float(input("Day 2:"))

date1 = jd(y1,m1,d1)
date2 = jd(y2,m2,d2)

print(f"Days difference: {date1-date2}" )
