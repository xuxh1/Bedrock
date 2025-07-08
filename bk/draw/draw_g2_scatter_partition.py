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

print('python draw_g2_scatter_partition.py')

shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

pd.set_option('display.max_columns', None)
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

F_list = ['FM_mean', 'FM_mean_nm', 'FY', 'FY_nm']
def data_process(name):
    df = pd.read_csv(f'{data_path}Global_partition.csv')

    df1 = df.copy()
    df1 = df1[df1[name[0]] > 0]
    return df1

def set_fig(name):
    fig = plt.figure(figsize=(12, 6), dpi=500)
    if name[2] in F_list:        
        fig.subplots_adjust(left=0.02, right=0.98, 
                    bottom=0.02, top=0.98, hspace=0.25) 
    else:
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
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.add_feature(cfeature.COASTLINE)
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
    fig,ax = set_fig(name)
    img = set_ax(ax,df1,name,cmap,level)
    if name[2] in F_list: 
        set_legend(ax,name)
    else:
        set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/g2_{name[2]}.png")
    plt.close(fig)

def PR_ET_Q_LH():
    name = ['PR', 'tp', 'PR', 'Precipitation (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['ET', 'et', 'ET', 'Evapotranspiration (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['Q', 'tp', 'Q', 'Streamflow (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['LH', 'Ee', 'LH', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,55,5)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    
RGBs =['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
cmap1 = colors.ListedColormap(RGBs)

def FY():
    name = ['FY', 'FD', 'FY', 'First Year']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)

def FM_mean():
    name = ['FM_mean', 'FD', 'FM_mean', 'First Month']
    level = np.arange(0,7,1)
    cmap = cmap1
    draw(name,level,cmap)

def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)']
    level = np.arange(0,160,10)
    cmap = cmaps.MPL_gist_earth_r
    draw(name,level,cmap)

@timer
def draw_G():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    PR_ET_Q_LH()
    FY()
    FM_mean()
    DTB()

if __name__=='__main__':
    draw_G()