# plot_S_Global.py

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
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
import cmaps

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
    image = xr.open_dataset(f'{name[0]}.nc').sel(lon=slice(xmin,xmax),lat=slice(ymin,ymax))
    s = image[f'{name[1]}']
    print(image)
    print(s.min(),s.max())

    image.close()

    if (name[2]=='SbG') or (name[2]=='SpG'):
        s = np.where(s<=0, np.nan, s)   
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

    ax.set_extent([xmin,xmax,ymin,ymax])
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img


def draw(name, level, cmap):
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)  # 创建2行3列的子图网格
    img = plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), xmin, xmax, ymin, ymax, name, level, cmap)

    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) # 左下角x,y,宽,高
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

    plt.savefig(f"fig/p_{name[2]}.png")

level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)
level4 = np.arange(-100,125,25)


rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)
cmap4 = "bwr"

def Sr():
    name = ['Sr', 'Sr', 'SrG', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    name = ['Sr_temp1', 'Sr', 'SrG_all', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    
def Sb():
    name = ['Sbedrock', 'Sr', 'SbG', '$S_{{bedrock}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    name = ['Sbedrock', 'Sr', 'SbG_all_mask', '$S_{{bedrock}}$ (mm)']
    level = level2
    cmap = cmap2
    draw(name,level,cmap)
    name = ['Sbedrock_temp1', 'Sr', 'SbG_all', '$S_{{bedrock}}$ (mm)']
    level = level2
    cmap = cmap2
    draw(name,level,cmap)
    
def Sp():
    name = ['Sproportion', 'Sr', 'SpG', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    name = ['Sproportion', 'Sr', 'SpG_all_mask', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
    name = ['Sproportion_temp1', 'Sr', 'SpG_all', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
        
def Ss():
    name = ['Ssoil', 'Band1', 'SsG', '$S_{{soil}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    
def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)']
    level = np.arange(0,200,50)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.cmocean_matter
    draw(name,level,cmap)
    
def Ground():
    name = ['Aboveground', 'Band1', 'Ag', 'Aboveground Carbon Density (MgC $ha^{{-1}}$)']
    level = np.arange(0,1600,400)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    name = ['Belowground', 'Band1', 'Bg', 'Belowground Carbon Density (MgC $ha^{{-1}}$)']
    level = np.arange(0,400,100)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    
def IGBP_mask12():
    name = ['IGBP_mask12', 'Band1', 'IGBP_mask12', 'IGBP']
    level = np.arange(0,17,1)
    rgb_list = ['#05450a', '#086a10', '#54a708', '#78d203', '#009900', '#c6b044', '#dcd159', '#dade48', '#fbff13', '#b6ff05', '#27ff87',
            '#c24f44', '#a5a5a5', '#ff6d4c', '#69fff8', '#f9ffa4', '#1c0dff']
    cmap = colors.ListedColormap(rgb_list)
    draw(name,level,cmap)
    
# Sr()
# Sb()
# Sp()
# Ss()
# DTB()
Ground()
# IGBP_mask12()