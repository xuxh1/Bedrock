# plot_S_Region.py

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
# import geopandas as gpd
# from shapely.geometry import box
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
import matplotlib
from pylab import rcParams
import sys
sys.path.append('/home/xuxh22/anaconda3/lib/mylib/')
from myfunc import timer
import os

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

xmin,xmax,ymin,ymax = -180,180,-60,90

@timer
def plot(ax, xmin, xmax, ymin, ymax, name, level, cmap):
    image = xr.open_dataset(f'{name[0]}_0p1.nc').sel(lon=slice(xmin,xmax),lat=slice(ymin,ymax))
    s = image[f'{name[1]}'] 
    image.close()

    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  
    
    img = ax.imshow(s, cmap=cmap,
                    extent=[xmin, xmax, ymax, ymin],
                    vmin=level[0], vmax=level[-1])
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # arr_x = np.arange(xmin,xmax+1,60)
    # arr_y = np.arange(ymin,ymax+1,30)
    
    # ax.set_title(f'Sbedrock', fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    
    ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    # ax.set_extent([xmin,xmax,ymin,ymax])
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img


def draw(boundary, name, level, cmap):
    fig = plt.figure(figsize=(12, 6), dpi=2000)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)  # 创建2行3列的子图网格
    xmin,xmax,ymin,ymax = boundary[0],boundary[1],boundary[2],boundary[3]
    img = plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), xmin, xmax, ymin, ymax, name, level, cmap)

    plt.savefig(f"fig/p_{name[2]}_{name[4]}.png")


    
level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)

boundary1 = [-125,-75,10,40]
boundary2 = [-72,-35,-20,7]
boundary3 = [-20,50,-17,13]
boundary4 = [70,110,8,30]

name5 = ['SbNA','SbSA','SbA','SbSeA']
boundary = [boundary1, boundary2, boundary3, boundary4]
    

# def Sr_all():
#     name = ['Sr_temp1', 'Sr', 'SrG_all', '$S_{{r}}$']
#     level = level1
#     cmap = cmap1
#     for i in range(4):
#         name.append(name5[i])
#         draw(boundary[i], name, level, cmap)
#         del name[-1]

# def Sr():
#     name = ['Sr', 'Sr', 'SrG', '$S_{{r}}$']
#     level = level1
#     cmap = cmap1
#     for i in range(4):
#         name.append(name5[i])
#         draw(boundary[i], name, level, cmap)
#         del name[-1]
        
# def Sb_all_mask():
#     name = ['Sbedrock', 'Sr', 'SbG_all_mask', '$S_{{bedrock}}$']
#     level = level2
#     cmap = cmap2
#     for i in range(4):
#         name.append(name5[i])
#         draw(boundary[i], name, level, cmap)
#         del name[-1]

# def Sb_all():
#     name = ['Sbedrock_temp1', 'Sr', 'SbG_all', '$S_{{bedrock}}$']
#     level = level2
#     cmap = cmap2
#     for i in range(4):
#         name.append(name5[i])
#         draw(boundary[i], name, level, cmap)
#         del name[-1]
    
def Sb():
    name = ['Sbedrock', 'Sr', 'SbR', '$S_{{bedrock}}$']
    level = level1
    cmap = cmap1
    for i in range(4):
        name.append(name5[i])
        draw(boundary[i], name, level, cmap)
        del name[-1]
        
def Sp():
    name = ['Sproportion', 'Sr', 'SpR', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level3
    cmap = cmap3
    for i in range(4):
        name.append(name5[i])
        draw(boundary[i], name, level, cmap)
        del name[-1]
        
# def Ss():
#     name = ['Ssoil', 'Band1', 'SsG', '$S_{{soil}}$']
#     level = level1
#     cmap = cmap1
#     for i in range(4):
#         name.append(name5[i])
#         draw(boundary[i], name, level, cmap)
#         del name[-1]
    


if __name__=='__main__':
    # Sr()
    # Sr_all()
    # Sb_all_mask()
    # Sb_all()
    Sb()
    Sp()
    # Ss()