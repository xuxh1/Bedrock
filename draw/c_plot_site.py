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

shp_path = '/home/xuxh22/stu01/Bedrock/data/Shp/US_conus/'
shp = gpd.GeoDataFrame.from_file(shp_path+'conus_ard_grid.shp')

df = pd.read_csv(f'site.csv', encoding='latin-1')
df1 = df.copy()
# df1.fillna(0, inplace=True)
print(df1)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
def map():
    df_map = shp
    df_map = df_map.to_crs(epsg=4326)
    print(df_map)
    df2 = df1.copy()
    df2.fillna(0)
    df2['mask123'] = df2['mask'].replace(to_replace=[0,1.0], value=['0','1'])
    print(df2)
    
    
    plot_base=(ggplot() +
            # geom_map(df_map,fill='white',color='k')+
            # geom_polygon(data=df_map, mapping=aes(x='geometry.x', y='geometry.y', group='group'), fill='white', color='black') +
            geom_map(world,fill='white', color='white') +
            geom_point(df2,aes(x='lon',y='lat', fill='Measure', shape='mask'),size=3,stroke=0.1)+
            scale_fill_manual(values={'Y': 'red', 'N': 'blue'}) +
            scale_shape_manual(values={'1': 'o', '0': '0'}) +
            theme(
                axis_title=element_text(size=15, face="plain", color="black"),
                
                axis_text=element_text(size=12, face="plain", color="black"),
                legend_title=element_text(size=14, face="plain", color="black"),
                legend_background=element_blank(),
                legend_position=(0.8, 0.3),
                aspect_ratio=0.5,
                figure_size=(12, 8),
                dpi=500
            )+
            xlim(-180, 180)   +
            ylim(-90, 90)   
            )
    plot_base.save('fig3/test.png')

def DTB():
    df1_rev = df1.dropna(subset=['Soil_depth'])
    print(df1_rev)
    for i in range(7):
        df2 = df1_rev.loc[10*i:10*(i+1),['num','DTB','Soil_depth']]
        df2.loc[df2['DTB'] > 500, 'DTB'] = 500
        # df = df.sort_values(by='Pensions', ascending=True)
        mydata = pd.melt(df2, id_vars='num')

        mydata['num'] = pd.Categorical(mydata['num'], categories=df2['num'], ordered=True)


        base_plot = (ggplot(mydata, aes('num', 'value', fill='variable')) +
                    geom_bar(stat="identity", color="black", position=position_dodge(), width=0.7, size=0.25) +
                    scale_fill_manual(values=("#00AFBB", "#FC4E07", "#E7B800")) +
                    coord_flip() +
                    theme(
            axis_title=element_text(size=15, face="plain", color="black"),
            axis_text=element_text(size=12, face="plain", color="black"),
            legend_title=element_text(size=14, face="plain", color="black"),
            legend_background=element_blank(),
            legend_position=(0.8, 0.2),
            aspect_ratio=1.15,
            figure_size=(6.5, 6.5),
            dpi=50
        )+
                    ylim(0, 500)   
                    )
        
        base_plot.save(f'fig5/site{i}.png')
    
    
def Sbedrock():
    df1_rev = df1.dropna(subset=['Sbedrock_field_min'])
    df1_rev.fillna(0)
    print(df1_rev)
    df1_rev['num_rev'] = df1_rev['num'].replace(to_replace=[54,51,44,41,32,36,12,14], value=[1,2,3,4,5,6,7,8])
    df1_rev = df1_rev.sort_values(by='num_rev', ascending=False).reset_index(drop=True)
    print(df1_rev)
    # exit(0)
    df2 = df1_rev.loc[:,['num_rev','Sbedrock','Ssoil','Sbedrock_field_min','Sbedrock_field_max']]
    df2.loc[df2['Sbedrock_field_min'] > 500, 'Sbedrock_field_min'] = 500
    df2.loc[df2['Sbedrock_field_max'] > 500, 'Sbedrock_field_max'] = 500
    
    # df = df.sort_values(by='Pensions', ascending=True)
    mydata = pd.melt(df2, id_vars='num_rev')

    mydata['num_rev'] = pd.Categorical(mydata['num_rev'], categories=df2['num_rev'], ordered=True)


    base_plot = (ggplot(mydata, aes('num_rev', 'value', fill='variable')) +
                geom_bar(stat="identity", color="black", position=position_dodge(), width=0.7, size=0.25) +
                scale_fill_manual(values=("#00AFBB", "#FC4E07", "#E7B800")) +
                coord_flip() +
                theme(
        axis_title=element_text(size=15, face="plain", color="black"),
        axis_text=element_text(size=12, face="plain", color="black"),
        legend_title=element_text(size=14, face="plain", color="black"),
        legend_background=element_blank(),
        legend_position=(0.8, 0.2),
        aspect_ratio=1.15,
        figure_size=(6.5, 6.5),
        dpi=50
    )+
                ylim(0, 500)   
                )
    
    base_plot.save(f'fig5/site_Sbedrock.png')
    return df1_rev  
    
xmin,xmax,ymin,ymax = -180,180,-60,90
def point_map(df_grid):
    df_map = shp

    plot_base=(ggplot() +
            # geom_map(df_map,fill='white',color='k')+
            geom_point(df_grid,aes(x='lon',y='lat'),fill='k',size=3,shape='o',stroke=0.1)+
            geom_text(df_grid,aes(x='lon',y='lat',label='num_rev'),size=8, color='blue', position=position_nudge(x=0.2, y=0.2))
            + theme(  # legend_position='none',
    text=element_text(size=12, colour="black")
    ))
    plot_base.save('fig5/test.png', dpi=300) 

map()
# DTB()
# df1_rev = Sbedrock()
# point_map(df1_rev)
