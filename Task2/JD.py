#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math

def jd(y,m,d):
    t1 = 367 * y
    t2 = (7 * (y + (m + 9) // 12)) // 4
    t3 = (3 * ((y + (m - 9) // 7) // 100 +1)) // 4
    t4 = (275 * m) // 9
    jda = t1 - t2 - t3 + t4 + d + 1721029 - 0.5
    return jda

y = int(input("Year:"))
m = int(input("Month:"))
d = int(input("Day:"))

date = jd(y,m,d)
print(f"Julian date: {date}" )

