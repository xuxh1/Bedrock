# plot_area.py

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
import seaborn as sns
import os
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
from shapely.geometry import Point
from plotnine import *
import sys
sys.path.append('/home/xuxh22/anaconda3/lib/mylib/')
from myfunc import timer

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

path = '/home/xuxh22/stu01/Bedrock/data/field/'
df = pd.read_csv(f'{path}new_literature_compilation.csv', encoding='latin-1')

s1 = nc.Dataset('Sbedrock_temp1.nc', 'r')
s2 = nc.Dataset('Ssoil.nc', 'r')
s3 = nc.Dataset('DTB.nc', 'r')
s4 = nc.Dataset('mask1.nc', 'r')
s5 = nc.Dataset('mask2.nc', 'r')
s6 = nc.Dataset('mask3.nc', 'r')
s7 = nc.Dataset('mask123.nc', 'r')

lat = df['Latitude']
lon = df['Longitude']
ssa = df['Same Site As']
# print(lat,lon)

lat1 = s1.variables['lat'][:]
lon1 = s1.variables['lon'][:]
# print(lat1,lon1)

df2 = pd.DataFrame()
j = 0
for i in range(len(lat)):
    if not isinstance(ssa[i], str):
        print('-----------------------------------------------')
        
        lat1_index = np.argmin(np.abs(lat1 - lat[i]))
        lon1_index = np.argmin(np.abs(lon1 - lon[i]))
        lat1_target = lat1[lat1_index]
        lon1_target = lon1[lon1_index]
        # print(lat[i])
        # print(lon[i])
        print('find ')
        # print(lat1_target)
        # print(lon1_target)
        print('-----------------------------------------------')
        
        df2.loc[j, 'Measure'] = df.loc[i, 'Measurement or Estimate of RM Contribution to ET?']
        df2.loc[j, 'lat'] = lat[i]
        df2.loc[j, 'lon'] = lon[i]
        df2.loc[j, 'Sbedrock_field_min'] = df.loc[i, 'Minimum']
        df2.loc[j, 'Sbedrock_field_max'] = df.loc[i, 'Maximum']
        df2.loc[j, 'Sbedrock'] = s1['Sr'][lat1_index,lon1_index]
        df2.loc[j, 'Ssoil'] = s2['Band1'][lat1_index,lon1_index]
        df2.loc[j, 'Soil_depth'] = df.loc[i, 'SoilDepth_Numberline_cm']
        df2.loc[j, 'DTB'] = s3['Band1'][lat1_index,lon1_index]
        df2.loc[j, 'mask1'] = s4['Band1'][lat1_index,lon1_index]
        df2.loc[j, 'mask2'] = s5['LC'][0,lat1_index,lon1_index]
        df2.loc[j, 'mask3'] = s6['et'][0,lat1_index,lon1_index]
        df2.loc[j, 'mask'] = s7['Band1'][lat1_index,lon1_index]
        
        
        
        j += 1

df3 = df2.groupby(['lat', 'lon']).first().reset_index()
# df3.fillna(0, inplace=True)
df3['num'] = range(len(df3['lat']))
with open('site.csv','w') as f:
    df3.to_csv(f)
    
print(df3)
# df['Median_D_bedrock_mm']
## df['S_soil_mm']
# df['Minimum']
# df['Maximum']
# df['Latitude']
# df['Longitude']
## df['Mean annual precipitation (MAP) (mm)']
# df['SoilDepth_Numberline_cm']




# for i in df.index:
#     print(i)
#     print(df['Median_D_bedrock_mm'][i])