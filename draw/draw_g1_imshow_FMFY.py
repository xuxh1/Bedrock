import os
import cmaps
import salem
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from pylab import rcParams
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
name       = config.name
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path

print('python draw_g1_imshow_FDFMFY.py')

shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

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

def data_process(name):
    image = xr.open_dataset(f'{data_path}/{name[0]}.nc').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    s = image[f'{name[1]}']
    s = s.salem.roi(shape=shp)
    print(image)
    print(s.min(),s.max())

    s = np.where(s<=0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  
    image.close()
    return s

def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.02, right=0.98, 
                    bottom=0.02, top=0.98, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,s,cmap,level):
    img = ax.imshow(s, cmap=cmap,
                    extent=[region[0], region[1], region[3], region[2]],
                    vmin=level[0], vmax=level[-1])
    
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent(region)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())


    return img

def set_colorbar(name,img,level,fig):
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

def set_legend(ax,name):
    FM_list = ['FM_mean', 'FM_mean_nm']
    FY_list = ['FY', 'FY_nm']
    if name[2] in FM_list:
        RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', '≥Jun']
        legend_patches = [mpatches.Patch(color=color, label=label) 
                        for color, label in zip(RGBs, labels)]
        ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(0, 0.01),
                fontsize=16, title="First Month" ,title_fontsize=20,
                frameon=False, edgecolor='black', ncol=3, columnspacing=1)
    elif name[2] in FY_list:
        RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
        labels = ['2003', '2004', '2005', '2006', '2007', '≥2008']
        legend_patches = [mpatches.Patch(color=color, label=label) 
                        for color, label in zip(RGBs, labels)]
        ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(0, 0.01),
                fontsize=16, title="First Year" ,title_fontsize=20,
                frameon=False, edgecolor='black', ncol=3, columnspacing=1)       

def draw(name,level,cmap):
    df1 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,cmap,level)
    set_legend(ax,name)


    plt.savefig(f"{fig_path}/g1_{name[2]}.png")
    plt.close(fig)

RGBs =['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
cmap1 = colors.ListedColormap(RGBs)

def F():
    name = ['FY', 'FD', 'FY', 'First Year']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['FY_temp2_2020', 'FD', 'FY_nm', 'First Year']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['FM_mean', 'FD', 'FM_mean', 'Mean First Month']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['FM_mean_temp2_12', 'FD', 'FM_mean_nm', 'Mean First Month']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)

def draw_F():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    F()


if __name__=='__main__':
    draw_F()