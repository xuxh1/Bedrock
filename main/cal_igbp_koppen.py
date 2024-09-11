# count_LandCover_ClimateType.py
# 待更新
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import box
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
from math import radians, sin
import matplotlib
from pylab import rcParams
import pandas as pd
import netCDF4 as nc
import os

path = os.getcwd()+'/'
print("当前文件路径:", path)

font = {'family': 'Times New Roman'}
matplotlib.rc('font', **font)

params = {'backend': 'ps',
          'axes.labelsize': 25,
          'grid.linewidth': 0.2,
          'font.size': 25,
          'legend.fontsize': 18,
          'legend.frameon': False,
          'xtick.labelsize': 30,
          'xtick.direction': 'out',
          'ytick.labelsize': 30,
          'ytick.direction': 'out',
          'legend.handlelength': 1,
          'legend.handleheight': 1,
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          "mathtext.default":"regular",
          'text.usetex': False}
rcParams.update(params)



s = nc.Dataset(f'Sbedrock.nc')['Sr'][:,:].flatten()
lc = nc.Dataset(f'IGBP.nc')['LC'][0,:,:].flatten()
ct = nc.Dataset(f'Koppen.nc')['Band1'][:,:].flatten()
area = nc.Dataset(f'Area.nc')['area'][:,:].flatten()

print(s)

# exit(0)
df = pd.DataFrame()
df['Landcover'] = lc.astype(int)
df['Koppen'] = ct.astype(int)
df['Sbedrock'] = s
df['Area'] = area

df = df.dropna()
df = df[df >= 0].dropna()
df = df.clip(lower = 0)

# df = df[df['Koppen']<0]
# df = df[df['Koppen']>29]

df = df[df['Landcover']<10]
df = df[df['Landcover']>0]

print(df)
with open('LC.csv','w') as f:
    df.to_csv(f)



