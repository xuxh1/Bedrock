# plot_Dbedrock_Frequency_Global.py

import xarray as xr
import numpy as np
from shapely.geometry import box
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
# import cmaps
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from pylab import rcParams
import os

path = os.getcwd()+'/'
print("当前文件路径:", path)

# matplotlib.use('QT5Agg')
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


var = 'Dbedrock'

# Create a GeoAxes instance
fig = plt.figure(figsize=(14, 4), dpi=2000)
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

fig.subplots_adjust(left=0.01, right=0.68, 
                    bottom=0.02, top=0.98, hspace=0.25) 

# cmap = cmaps.BlueDarkOrange18
level = np.arange(0.5, 5, 1)

rgb_list = ['#69aa4c','#CC0000','#ebc874','#8ec0cb']
# 创建 colormap 对象
cmap = colors.ListedColormap(rgb_list)
cmap.set_under('#FFFFFF')
cmap.set_over('#FFFFFF')


def plot_image(image, ax, cmap, level):
    
    s = image['Dr'][::-1,:]

    print(s.min().values,s.max().values)
    lat = image['lat']
    lon = image['lon']
    xmin,xmax = lon.min(),lon.max()
    ymin,ymax = lat.min(),lat.max()
    
    vmin,vmax = level.min(),level.max()
    
    img = ax.imshow(s, cmap=cmap, 
                    extent=[xmin, xmax, ymin, ymax], 
                    vmin=vmin, vmax=vmax)
    return img,xmin,xmax,ymin,ymax

def drawmap(xmin,xmax,ymin,ymax):
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.spines['top'].set_linewidth(2)    # 顶部边框
    ax.spines['bottom'].set_linewidth(2) # 底部边框
    ax.spines['left'].set_linewidth(2)   # 左侧边框
    ax.spines['right'].set_linewidth(2)  # 右侧边框
    
    ax.xaxis.set_tick_params(width=2.0, color='black')  # X轴线型和颜色
    ax.yaxis.set_tick_params(width=2.0, color='black') 
    arr_x = np.arange(xmin+5,xmax,20)
    arr_y = np.arange(ymin+5,ymax+1,10)

    # ax.set_xlabel('Longitude', fontsize=24, labelpad=10)
    # ax.set_ylabel('Latitude', fontsize=24, labelpad=10)
    # ax.set_title(var, fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    # 添加海岸线特征
    ax.add_feature(cfeature.COASTLINE)

    # 设置图形范围为全球
    # ax.set_global()
    
def colorbar(fig, img, level, ax, var):
    rect = [0.1, 0.09, 0.8, 0.04]  #左下角x,y,宽,高
    cbar_ax = fig.add_axes(rect,frameon = False)
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'Depth to {var}', fontsize=18, fontweight='bold')
    
def draw(boundary,name):
#_____________________________'Dbedrock_Frequency.nc'____________________________________________
    with xr.open_dataset('Dbedrock_Frequency_0p1.nc') as image:
        # 获取 's' 变量
        s1 = image['Dr']

        img,xmin,xmax,ymin,ymax = plot_image(image, ax, cmap, level)
    
        # xmin, xmax, ymin, ymax = (-20, 50, -5, 20)
        # xmin,xmax,ymin,ymax =-180,180,-60,90
        xmin,xmax,ymin,ymax = boundary[0],boundary[1],boundary[2],boundary[3]
        
        drawmap(xmin,xmax,ymin,ymax)
        # colorbar(fig, img, level, ax, var)

    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    plt.savefig(f"fig/p_DFR_{name}.png")
    
def north_america():
    xmin,xmax,ymin,ymax = -125,-75,10,40
    name = 'SbNA'
    boundary = [xmin,xmax,ymin,ymax]
    draw(boundary,name)
    
def south_america():
    xmin,xmax,ymin,ymax = -72,-35,-20,7
    name = 'SbSA'
    boundary = [xmin,xmax,ymin,ymax]
    draw(boundary,name)
 
def africa():
    xmin,xmax,ymin,ymax = -20,50,-17,13
    name = 'SbA'
    boundary = [xmin,xmax,ymin,ymax]
    draw(boundary,name)

def southeast_asia():
    xmin,xmax,ymin,ymax = 70,110,8,30
    name = 'SbSeA'
    boundary = [xmin,xmax,ymin,ymax]
    draw(boundary,name)
    
def region(num):
    if num ==1:
        north_america()
    elif num ==2:
        south_america()
    elif num ==3:
        africa()
    else:
        southeast_asia()
        
       
if __name__=='__main__':
    for i in range(4):
        region(i)

        
