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

def set_plot_params(): 
    var = 'Dbedrock'

    # Create a GeoAxes instance
    fig = plt.figure(figsize=(14, 4), dpi=2000)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    fig.subplots_adjust(left=0.01, right=0.68, 
                        bottom=0.02, top=0.98, hspace=0.25) 

    rgb_list = ['#69aa4c','#CC0000','#ebc874','#8ec0cb']
    # 创建 colormap 对象
    cmap = colors.ListedColormap(rgb_list)
    
    # cmap = cmaps.BlueDarkOrange18
    level = np.arange(0.5, 5, 1)
    
    return var, fig, ax, cmap, level

def define_colormap(level, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, len(level) - 1))
    cmap_custom = ListedColormap(colors)
    cmap_custom.set_under('#FFFFFF')
    cmap_custom.set_over('#FFFFFF')
    norm = BoundaryNorm(level, cmap_custom.N)
    return cmap_custom, norm

def plot_image(image, ax, cmap, level, norm, s1):
    
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

def draw(xmin,xmax,ymin,ymax):
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
    
if __name__ == "__main__":
    var, fig, ax, cmap, level = set_plot_params()
    cmap, norm= define_colormap(level,cmap)
#_____________________________'Dbedrock_Frequency.nc'____________________________________________
    with xr.open_dataset('Dbedrock_Frequency_0p1.nc') as image:
        # 获取 's' 变量
        s1 = image['Dr']

        img,xmin,xmax,ymin,ymax = plot_image(image, ax, cmap, level, norm, s1)
    
        # xmin, xmax, ymin, ymax = (-20, 50, -5, 20)
        xmin,xmax,ymin,ymax =-180,180,-60,90
        
        draw(xmin,xmax,ymin,ymax)
        # colorbar(fig, img, level, ax, var)

    # 创建一个图例
    legend_labels = ['Bedrcok water withdrawn \nevery year from 2003 to 2020', 
                        'Bedrcok water withdrawn \nsome year(s) from 2003 to 2020', 
                        'Bedrcok water not needed to \nexplain ET over course of study', 
                        'Bedrock water use may occur, but \ncriteria for calculation are not met']
                        # 'Note classified as woody \nvegetation on shallow bedrock']

    rgb_list = ['#69aa4c','#CC0000','#ebc874','#8ec0cb']

    # legend_elements = [Patch(color=img.cmap(img.norm(level)), label=label) for level, label in zip(img.levels, legend_labels)]
    legend_elements = [Patch(color=color, label=label) for color, label in zip(rgb_list, legend_labels)]


    # # 添加图例到图中
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

        
    # 获取图例的图形对象
    legend_fig = legend.get_figure()
        
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    plt.savefig(f'fig/p_DFG.png')