import os
import numpy as np
import xarray as xr
from shapely.geometry import box
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from pylab import rcParams
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
# name       = config.name
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path

print('python draw_g1r1_DF.py')

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
def data_process(region):
    image = xr.open_dataset(f'{data_path}/Dbedrock_Frequency.nc4').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    # image = xr.open_dataset(f'{data_path}/../0p1_exp1/Dbedrock_Frequency.nc').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    
    s = image['Dbedrock'][::-1,:]
    # s = image['Dr'][::-1,:]

    return s

@timer
def set_fig():
    # Create a GeoAxes instance
    fig = plt.figure(figsize=(14, 4), dpi=500)

    fig.subplots_adjust(left=0.01, right=0.68, 
                    bottom=0.02, top=0.98, hspace=0.25) 
    
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    return fig,ax

@timer
def set_ax(ax,s,cmap,region,level):
    img = ax.imshow(s, cmap=cmap, 
                    extent=[region[0], region[1], region[2], region[3]], 
                    vmin=level[0], vmax=level[-1])
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.spines['top'].set_linewidth(2)    
    ax.spines['bottom'].set_linewidth(2) 
    ax.spines['left'].set_linewidth(2)   
    ax.spines['right'].set_linewidth(2)  
    
    ax.xaxis.set_tick_params(width=2.0, color='black') 
    ax.yaxis.set_tick_params(width=2.0, color='black') 
    # arr_x = np.arange(region[0]+5,region[1],20)
    # arr_y = np.arange(region[2]+5,region[3]+1,10)
    # ax.set_xlabel('Longitude', fontsize=24, labelpad=10)
    # ax.set_ylabel('Latitude', fontsize=24, labelpad=10)
    # ax.set_title(var, fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    ax.add_feature(cfeature.COASTLINE)
    return img

@timer
def set_other(ax):
    legend_labels = ['Bedrcok water withdrawn \nevery year from 2003 to 2020', 
                        'Bedrcok water withdrawn \nsome year(s) from 2003 to 2020', 
                        'Bedrcok water not needed to \nexplain ET over course of study', 
                        'Bedrock water use may occur, but \ncriteria for calculation are not met']
                        # 'Note classified as woody \nvegetation on shallow bedrock']

    rgb_list = ['#69aa4c','#CC0000','#ebc874','#8ec0cb']

    # legend_elements = [Patch(color=img.cmap(img.norm(level)), label=label) for level, label in zip(img.levels, legend_labels)]
    legend_elements = [Patch(color=color, label=label) for color, label in zip(rgb_list, legend_labels)]

    num=[1.02, 0.01, 3, 0]
    legend = ax.legend(handles=legend_elements, 
                        fontsize=14, 
                        labelspacing = 1.2,
                        handlelength = 4,
                        handleheight = 3,
                        frameon=False,
                        fancybox=True,
                        edgecolor = '#000000',
                        facecolor = '#ffffff',
                        shadow=True,
                        bbox_to_anchor=(num[0], num[1]), loc=num[2], borderaxespad=num[3])
    legend_fig = legend.get_figure()


@timer
def draw(region,name,level,cmap):
    s = data_process(region)
    fig,ax = set_fig()
    img = set_ax(ax,s,cmap,region,level)
    if region[0] == -180:
        set_other(ax)
        plt.savefig(f"{fig_path}/global_map_1/{name[1]}_{name[2]}.png")
    else:
        plt.savefig(f"{fig_path}/global_map_1/{name[1]}_{name[2]}_{name[3]}.png")

def draw_region(name,name4,region,level,cmap):
    for i in range(4):
        name.append(name4[i])
        print(region[i])
        draw(region[i], name, level, cmap)
        del name[-1]

def define_colormap(level, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, len(level) - 1))
    cmap_custom = ListedColormap(colors)
    cmap_custom.set_under('#FFFFFF')
    cmap_custom.set_over('#FFFFFF')
    norm = BoundaryNorm(level, cmap_custom.N)
    return cmap_custom, norm

level1 = np.arange(0.5, 5, 1)

rgb_list = ['#69aa4c','#CC0000','#ebc874','#8ec0cb']
cmap1 = colors.ListedColormap(rgb_list)
cmap1, norm= define_colormap(level1,cmap1)
# cmap = cmaps.BlueDarkOrange18

def DFG():
    name = ['Dbedrcok_Frequency', 'g1', 'DF']
    level = level1
    cmap = cmap1
    draw(region,name,level,cmap)

region1 = [-125,-75,10,40]
region2 = [-72,-35,-20,7]
region3 = [-20,50,-17,13]
region4 = [70,110,8,30]

name4 = ['SbNA','SbSA','SbA','SbSeA']
region_new = [region1, region2, region3, region4]

def DFR():
    name = ['Dbedrcok_Frequency', 'r1', 'DF']
    level = level1
    cmap = cmap1
    draw_region(name,name4,region_new,level,cmap)


def draw_DF():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    DFG()
    # DFR()

if __name__=='__main__':
    draw_DF()