import os
import numpy as np
import xarray as xr
from shapely.geometry import box
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from pylab import rcParams
from myfunc import timer
import config

resolution = config.resolution
name = config.name
region = config.region
data_path = config.data_path
fig_path = config.fig_path

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



@timer
def data_process(name,year):
    image = xr.open_dataset(f'{data_path}/{name[0]}_{year}.nc').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    s = image[f'{name[1]}']
    image.close()
    
    s = np.where(s<=0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s) 
    return s

@timer
def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
    
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6) 
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,s,cmap,level):
    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.imshow(s, cmap=cmap,
                    extent=[region[0], region[1], region[3], region[2]],
                    vmin=level[0], vmax=level[-1])

    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    # arr_x = np.arange(region[0],region[1]+1,60)
    # arr_y = np.arange(region[2],region[3]+1,30)
    
    # ax.set_title(f'Dbedrock {year}', fontsize=16, pad=10)
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

@timer
def set_other(name,img,level,fig,year):
    # From the bottom left corner x, y, width, height
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]} {year} (mm)', fontsize=30, fontweight='bold')


def draw(name,level,cmap):
    for year in range(2003,2021):
        print(year)
        s = data_process(name,year)
        fig,ax = set_fig()
        img = set_ax(ax,s,cmap,level)
        set_other(name,img,level,fig,year)
        
        plt.savefig(f"{fig_path}/g2_{name[2]}_{year}.png")
        plt.close()

level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)

def Db():
    name = ['Dbedrock', 'Dr', 'Db', '$D_{{bedrock}}$']
    level = level1
    cmap = cmap1
    draw(name, level, cmap)

@timer      
def draw_D_G():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    Db()

if __name__=='__main__':
    draw_D_G()