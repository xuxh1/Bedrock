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

print('python draw_r2_scatter.py')

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

@timer
def data_process(name):
    df = pd.read_csv(f'{data_path}US.csv')

    df_s = pd.read_csv(f'{data_path}site.csv')

    df1 = df.copy()
    df2 = df_s.copy()

    # print(df1)
    # print(name[0])
    df1 = df1[df1[name[0]] > 0]
    df1 = df1[df1['State'] == name[4]]
    return df1,df2

@timer
def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

@timer
def set_ax(ax,df1,df2,name,cmap,region,level):
    shp = gpd.GeoDataFrame.from_file(shp_path+f'US/States/{name[4]}.shp')
    shp.boundary.plot(ax=ax, edgecolor='black', linewidth=1)

    if name[2] == 'Sb':
        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors="#153aab")
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors='none')

        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors="red")
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors='none')
        
        ax.legend(fontsize=12 ,bbox_to_anchor=(0.29, 0.379))

    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[0]], 
                    s=10, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])

    
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    # ax.add_feature(cfeature.COASTLINE)
    ax.set_extent(region)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img

@timer
def set_other(name,img,level,fig):
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

@timer
def draw(region,name,level,cmap):
    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,name,cmap,region,level)
    # set_other(name,img,level,fig)

    plt.savefig(f"{fig_path}/r2_{name[2]}.png")
    plt.close(fig)

level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)
level4 = np.arange(-100,125,25)
level5 = np.arange(0,300,50)

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)
cmap4 = "bwr"

region1 = [-125, -114, 32, 42]
region2 = [-106.5, -93.5, 25.8, 36.5]

def Sb():
    name = [f'Sbedrock', 'Sr', f'Sbedrock_Ca', f'$S_{{bedrock}}$ (mm)','California']
    region = region1
    level = level1
    cmap = cmap1
    draw(region, name, level, cmap)

    name = [f'Sbedrock', 'Sr', f'Sbedrock_Tx', f'$S_{{bedrock}}$ (mm)','Texas']
    region = region2
    level = level1
    cmap = cmap1
    draw(region, name, level, cmap)

@timer
def draw_R():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    Sb()

if __name__=='__main__':
    draw_R()