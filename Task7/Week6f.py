#!/usr/bin/env python
# coding: utf-8

# In[2]:


from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from mpl_toolkits.axes_grid1 import make_axes_locatable
import warnings

hdul = fits.open("m101.fits")
hdul.info()

hdr = hdul[0].header
keys = list(hdr.keys())
print(keys[:5])
print("BITPIX =", hdr["BITPIX"])

dat = hdul[0].data
print("Shape:", dat.shape)
print("dtype:", dat.dtype)

flat = dat.flatten()
print("min:", np.min(flat))
print("max:", np.max(flat))
print("mean:", np.mean(flat))
print("std:", np.std(flat))
print("median:", np.median(flat))
modeval = stats.mode(flat, keepdims=True).mode[0]
print("mode:", modeval)

fig, ax = plt.subplots()
ax.hist(flat, bins=100, color="steelblue")
ax.axvline(np.mean(flat), color="red", label="mean")
ax.axvline(np.median(flat), color="green", label="median")
ax.axvline(modeval, color="orange", label="mode")
ax.legend()
plt.tight_layout()
plt.show()

datf = np.asarray(dat, dtype=float)
med = np.median(datf)
 
fig, ax = plt.subplots()
im = ax.imshow(datf, vmin=med, origin="lower", cmap="jet")
ax.set_xlabel(hdr["CTYPE1"])
ax.set_ylabel(hdr["CTYPE2"])
 
div = make_axes_locatable(ax)
cax = div.append_axes("right", size="5%", pad=0.05)
cbar = fig.colorbar(im, cax=cax)
cbar.set_label(hdr.get("BUNIT", "Counts"))
 
plt.tight_layout()
plt.show()

hdr['BUNIT'] = 'Counts'

newhdu = fits.PrimaryHDU(data=datf, header=hdr)
newhdul = fits.HDUList([newhdu])

with warnings.catch_warnings():
    warnings.simplefilter('ignore', fits.verify.VerifyWarning)
    newhdul.writeto('m101_float.fits', overwrite=True, output_verify='silentfix')

with fits.open('m101_float.fits') as check:
    check.info()
    print(f"BUNIT = {check[0].header['BUNIT']}")
    print(f"dtype = {check[0].data.dtype}")

hdul.close()


# In[4]:





# In[26]:


from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

hdul = fits.open("m101.fits")
hdr = hdul[0].header
dat = np.asarray(hdul[0].data, dtype=float)
hdul.close()

sky = dat[50:70, 50:70]

fig, ax = plt.subplots()
med = np.median(dat)
im = ax.imshow(dat, origin="lower", cmap="gray", vmin=med, vmax=med+500)
rect = plt.Rectangle((50, 50), 20, 20, edgecolor="red", facecolor="none", lw=1.5)
ax.add_patch(rect)
ax.set_xlabel(hdr.get("CTYPE1", "x"))
ax.set_ylabel(hdr.get("CTYPE2", "y"))
div = make_axes_locatable(ax)
cax = div.append_axes("right", size="5%", pad=0.05)
fig.colorbar(im, cax=cax).set_label("counts")
plt.tight_layout()
plt.show()

flat = sky.flatten()
n = len(flat)
mean = np.mean(flat)
std = np.std(flat)
rms = np.sqrt(np.mean(flat**2))

print(f"pixels: {n}")
print(f"mean: {mean}")
print(f"std: {std}")
print(f"rms: {rms}")


# In[27]:


from astropy.io import fits
import numpy as np

d0 = fits.open("noisemap0.fits")[0].data
d1 = fits.open("noisemap1.fits")[0].data
d2 = fits.open("noisemap2.fits")[0].data

print("std d0:", np.std(d0))
print("std d1:", np.std(d1))
print("std d2:", np.std(d2))

stack = np.stack([d0, d1, d2], axis=0)
print("stack shape:", stack.shape)

mean = np.mean(stack, axis=0)
print("mean image shape:", mean.shape)

std_mean = np.std(mean)
print("std of mean image:", std_mean)

sig = (1/3) * np.sqrt(np.std(d0)**2 + np.std(d1)**2 + np.std(d2)**2)
print("theoretical std:", sig)


# In[9]:


from astropy.io import fits
from astropy.table import Table
import numpy as np

hdul = fits.open("APOGEE_stars.fits")
data = hdul[1].data
hdul.close()

t = Table(data)

sf   = np.array(t["STARFLAG"])
af   = np.array(t["ASPCAPFLAG"])
snr  = np.array(t["SNR"])
plx  = np.array(t["GAIAEDR3_PARALLAX"])
eplx = np.array(t["GAIAEDR3_PARALLAX_ERROR"])
g    = np.array(t["GAIAEDR3_PHOT_G_MEAN_MAG"])
bp   = np.array(t["GAIAEDR3_PHOT_BP_MEAN_MAG"])
rp   = np.array(t["GAIAEDR3_PHOT_RP_MEAN_MAG"])

flag = ((sf == 0)&(af == 0)&(snr > 10)&(plx > 0)&(plx / eplx > 5)&np.isfinite(g)&np.isfinite(bp)&np.isfinite(rp)).astype(int)

t["DATAFLAG"] = flag

absmag = np.full(len(t), -1.0)

good = flag == 1
dist = 1000.0 / plx[good]
absmag[good] = g[good] - 5.0 * np.log10(dist / 10.0)

t["ABS_MAG_G"] = absmag

t.write("APOGEE_update.fits", overwrite=True)

with fits.open("APOGEE_update.fits") as chk:
    chk.info()
    print("Columns:", chk[1].columns.names)


# In[29]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("gaiaTestData.csv")

idx = df["phot_g_mean_flux"].idxmax()
print("max flux:", df["phot_g_mean_flux"].max())
print(df.loc[idx])

df = df.sort_values("phot_g_mean_flux")

F = df["phot_g_mean_flux"].values
m = df["phot_g_mean_mag"].values

fig, ax = plt.subplots()
ax.scatter(F, m, s=5)
ax.set_xlabel("phot_g_mean_flux")
ax.set_ylabel("phot_g_mean_mag")
plt.tight_layout()
plt.show()

F0 = F / 10**(-m / 2.5)
print("mean F0:", np.mean(F0))
print("std  F0:", np.std(F0))


# In[30]:


from astroquery.gaia import Gaia
import pandas as pd

query = """
SELECT TOP 50
    source_id, ra, dec, parallax, parallax_error,
    phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag
FROM gaiadr3.gaia_source
WHERE parallax / parallax_error > 5
  AND phot_g_mean_mag IS NOT NULL
  AND phot_bp_mean_mag IS NOT NULL
  AND phot_rp_mean_mag IS NOT NULL
"""

job = Gaia.launch_job(query)
result = job.get_results()

df = result.to_pandas()
print(df)

result.write("astroquery_gaia.fits", overwrite=True)


# In[32]:


class Fibonacci:
    """Class for calculating Fibonacci sequence"""

    def nth(self, n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return a

    def divisible(self, n, m):
        result = []
        a, b = 0, 1
        for j in range(n):
            if a % m == 0:
                result.append(a)
            a, b = b, a + b
        return result

fib = Fibonacci()

print("100th Fibonacci number:", fib.nth(100))
print("Fibonacci numbers below N=100 divisible by M=7:", fib.divisible(100, 7))


# In[ ]:




