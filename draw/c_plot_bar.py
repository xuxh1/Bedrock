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
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
name = config.name
data_path = config.data_path
post_data_path = config.post_data_path
fig_path = config.fig_path

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

df = pd.read_csv(f'{data_path}/Global.csv')
rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
cmap = colors.ListedColormap(rgb_list)

def plot_bar():
    df_area = df.copy()
    df1 = pd.DataFrame()
    df1['Sr'] = df_area.groupby('Continent')['Sr'].mean()
    df1['Sbedrock'] = df_area.groupby('Continent')['Sbedrock'].mean()
    df1['Ssoil'] = df_area.groupby('Continent')['Ssoil'].mean()
    df1['Continent'] = df1.index
    print(df1)
    df2 = df1.set_index('Continent').transpose()
    print(df2)
    df2['name'] = df2.index
    for column in [col for col in df2.columns if 'name' not in col]:
        print(column)
        print(df2[column])
        # exit(0)
        base_hist = (ggplot(df2, aes(x=df2['name'],y=df2[column], fill=df2['name'])) +
                    geom_col(stat="identity", position="dodge")+
                    # scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl') +
                    theme(
            text=element_text(size=13, color="black"),
            plot_title=element_text(size=15),
            aspect_ratio=1.15,
            figure_size=(5, 5)
        )+
        ylim(0, 400)+  
        labs(x=None, y="mean value (mm)")+
        guides(fill=False)+
        scale_fill_gradient(name=cmap)
        # ggtitle(column)
        )
        base_hist.save(f'{fig_path}/test/{column}.png')

plot_bar()