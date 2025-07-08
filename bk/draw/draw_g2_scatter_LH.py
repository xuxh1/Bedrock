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
size       = config.size

print('python draw_g1_imshow_LH.py')

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
    lon = image['lon'][:].flatten()
    lat = image['lat'][:].flatten()
    print(image)
    print(s.min(),s.max())

    image.close()
 
    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  

    return s,lon,lat

def set_fig():
    fig = plt.figure(figsize=(12, 7), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,s,lon,lat,cmap,level):
    # Set drawing mode(note:extent's lat from positive to negative)
    lat_new = np.repeat(lat, len(lon))
    lon_new = np.tile(lon, len(lat))
    
    img = ax.scatter(lat_new, lon_new, c=s[:,:].flatten(), 
                    s=size, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])
    
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    # arr_x = np.arange(region[0],region[1]+1,60)
    # arr_y = np.arange(region[2],region[3]+1,30)
    
    # ax.set_title(f'Sbedrock', fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    
    ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    ax.set_extent(region)
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img

def set_colorbar(name,img,level,fig):
    # From the bottom left corner x, y, width, height
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

def set_legend(fig,name):
    if name[2]=='IGBP':
        RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
                '#009900','#c6b044', '#dcd159', '#dade48',  
                '#fbff13','#b6ff05', '#27ff87', '#c24f44', 
                '#a5a5a5', '#ff6d4c','#69fff8', '#f9ffa4', 
                '#1c0dff', 'white', 'white', 'white']
        labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
                 'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
                'Savannas', 'Grasslands', 'Permanent Wetlands', 'Croplands',
                 'Urban and Built-up Lands', 'Cropland/Natural Vegetation Mosaics','Permanent Snow and Ice', 'Barren',
                 'Water Bodies', '', '', '']
        # RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
        #         '#009900','#c6b044', '#dcd159', '#dade48',  
        #         '#fbff13']
        # labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
        #          'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
        #         'Savannas']
        # From the bottom left corner x, y, width, height
        legend_ax = fig.add_axes([0, 0.03, 1, 0.06], frameon=False)
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(RGBs, labels)]

        legend = legend_ax.legend(handles=legend_patches, loc='center', fontsize=12, frameon=False, ncol=5, edgecolor='black', columnspacing=1.5)
    elif name[2]=='Koppen':
        RGBs = ['#0000FF', '#0078FF', '#46AAFA', 'white', '#FF0000', '#FF9696', '#F5A500', '#FFDC64', '#FFFF00', '#C8C800', '#969600', 'white', '#96FF96',
                '#64C864', '#329632', 'white', '#C8FF50', '#64FF32', '#32C800', 'white', '#FF00FF', '#C800C8', '#963296', '#966496', '#AAAFFF', '#5A78DC',
                '#4B50B4', '#320087', '#00FFFF', '#37C8FF', '#007D7D', '#00465F', '#B3B3B3', '#666666', 'white', 'white']
        labels = ['Af', 'Am', 'Aw', '', 'BWh', 'BWk', 'BSh', 'BSk', 'Csa', 'Csb', 'Csc', '', 'Cwa', 'Cwb', 'Cwc', '', 'Cfa', 'Cfb', 'Cfc', '', 'Dsa', 
                  'Dsb', 'Dsc', 'Dsd', 'Dwa', 'Dwb', 'Dwc', 'Dwd', 'Dfa', 'Dfb', 'Dfc', 'Dfd', 'ET', 'EF', '', '', ]
        # From the bottom left corner x, y, width, height
        legend_ax = fig.add_axes([0, 0.02, 1, 0.06], frameon=False)
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(RGBs, labels)]

        legend = legend_ax.legend(handles=legend_patches, loc='center', fontsize=16, frameon=False, ncol=9, edgecolor='black', columnspacing=2)

    legend_ax.set_xticks([])
    legend_ax.set_yticks([])
    legend_ax.set_xticklabels([])
    legend_ax.set_yticklabels([])

@timer
def draw(name,level,cmap):
    legend_list1 = ['IGBP', 'Koppen']
    legend_list2 = ['mask1', 'mask2', 'mask3', 'mask12', 'mask123']

    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,cmap,level)
    if name[2] in legend_list1:
        set_legend(fig,name)
    elif name[2] in legend_list2:
        print('no use colorbar')
    else:
        set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/g2/LH/g2_{name[2]}.png")
    plt.close(fig)

def LH_Sbedrock():
    name = ['LH/LH', 'Ee', 'LH', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,50,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['LH/LH_temp1', 'Ee', 'LH_nm', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,50,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    
def LH_Dbedrock_median():
    name = ['LH/LH_median', 'Ee', 'LH_median', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,50,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)

def LH_Dbedrock_mon_median():
    for mon in range(1,13):
        name = [f'LH/LH_{mon}_median', 'Ee', f'LH_{mon}_median', 'Latent Heat (W/$m^{{2}}$)']
        level = np.arange(0,50,5)
        cmap = cmaps.WhiteBlue
        draw(name,level,cmap)

if __name__=='__main__':
    # LH_Sbedrock()
    LH_Dbedrock_median()
    # LH_Dbedrock_mon_median()