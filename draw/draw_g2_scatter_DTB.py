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
import matplotlib.font_manager as fm

resolution = config.resolution
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path
size       = config.size

print('python draw_g2_scatter_statistics.py')
dir_man = DirMan(data_path)
dir_man.enter()
os.makedirs(f'{fig_path}/global_map_2', exist_ok=True)

shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

pd.set_option('display.max_columns', None)
font = {'family': 'Times New Roman'}
matplotlib.rc('font', **font)

params = {'backend': 'ps',
          'axes.labelsize': 25,
          'axes.linewidth': 1.2,
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

legend_list = ['IGBP', 'Koppen']
font_properties = fm.FontProperties(weight='bold')

def data_process(name):
    df = pd.read_csv(f'{data_path}csv/Global_DTB.csv')

    df1 = df.copy()
    df1 = df1[df1[name[0]] > 0]
    return df1

def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
    
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,df1,name,cmap,level):
    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[0]], 
                    s=size, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(2)  

    # coastline = cfeature.NaturalEarthFeature('physical', 'coastline', '50m', edgecolor='0.6', facecolor='none')
    rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '110m', edgecolor='0.6', facecolor='none')
    ax.add_feature(cfeature.LAND, facecolor='0.95')
    # ax.add_feature(coastline, linewidth=0.6)
    ax.add_feature(cfeature.LAKES, alpha=1, facecolor='white', edgecolor='white')
    ax.add_feature(rivers, linewidth=0.8)
    # ax.gridlines(draw_labels=False, linestyle=':', linewidth=0.7, color='grey', alpha=0.8)

    ax.add_feature(cfeature.COASTLINE)
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.set_extent(region)
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
    cb.ax.tick_params(labelsize=20)
    cb.ax.yaxis.set_tick_params(direction='out', width=1.5)
    for label in cb.ax.get_xticklabels() + cb.ax.get_yticklabels():
        label.set_fontproperties(font_properties)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

def set_legend(fig,name):
    if name[2]=='IGBP':
        # RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
        #         '#009900','#c6b044', '#dcd159', '#dade48',  
        #         '#fbff13','#b6ff05', '#27ff87', '#c24f44', 
        #         '#a5a5a5', '#ff6d4c','#69fff8', '#f9ffa4', 
        #         '#1c0dff', 'white', 'white', 'white']
        # labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
        #          'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
        #         'Savannas', 'Grasslands', 'Permanent Wetlands', 'Croplands',
        #          'Urban and Built-up Lands', 'Cropland/Natural Vegetation Mosaics','Permanent Snow and Ice', 'Barren',
        #          'Water Bodies', '', '', '']
        RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
                '#009900','#c6b044', '#dcd159', '#dade48',  
                '#fbff13']
        labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
                 'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
                'Savannas']
        # From the bottom left corner x, y, width, height
        legend_ax = fig.add_axes([0, 0.04, 1, 0.06], frameon=False)
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(RGBs, labels)]

        legend = legend_ax.legend(handles=legend_patches, loc='center', fontsize=16, frameon=False, ncol=3, edgecolor='black', columnspacing=1.5)
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

def draw(name,level,cmap):
    df1 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,name,cmap,level)
    if name[2] in legend_list:
        set_legend(fig,name)
    else:
        set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/g2_{name[2]}.png")
    plt.close(fig)

def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)']
    level = np.arange(0,300,25)
    cmap = cmaps.CBR_drywet
    draw(name,level,cmap)

if __name__=='__main__':
    DTB()