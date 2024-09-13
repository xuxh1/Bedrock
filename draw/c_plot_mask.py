# plot_mask.py

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import box
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
import matplotlib
from pylab import rcParams
import os
import config
import salem

resolution = config.resolution
name = config.name
region = config.region
data_path = config.data_path
shp_path = config.shp_path
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

shp_path   =  f'{shp_path}/World_CN/'
shp = gpd.read_file(shp_path+'ne_10m_admin_0_countries_chn.shp')
mode  = ['Mexico' , 'Central Africa' , 'South Asia']

xmin,xmax,ymin,ymax = -180,180,-60,90
level = np.arange(0,1,0.1)

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                              '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']

# 创建 colormap 对象
cmap = colors.ListedColormap(rgb_list)
cmap.set_under('#ffffff')
cmap.set_over('#CC0000')

def plot(ax, xmin, xmax, ymin, ymax,name,band):
    # 读取数据
    image = xr.open_dataset(f'{data_path}/{name}.nc').sel(lon=slice(xmin,xmax),lat=slice(ymin,ymax))
    # image = xr.open_dataset(f'Sr.nc')
    if name == 'mask2' or name == 'mask3':
        s = image[band][0,:,:]
    else:
        s = image[band][:,:]    
    s = s.salem.roi(shape=shp)

    print(s)
    lat = image['lat']
    
    
    lon = image['lon']
    # print(s)
    # print(lat)
    image.close()  # 关闭 xarray.Dataset 对象，释放资源
    s = np.ma.masked_where(np.isnan(s), s)  
    
    shp_fixed = shp.copy()
    shp_fixed['geometry'] = shp_fixed['geometry'].buffer(0)
    
    img = ax.imshow(s, cmap=cmap,
                    extent=[xmin, xmax, ymax, ymin],
                    vmin=0, vmax=1)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # arr_x = np.arange(xmin,xmax+1,60)
    # arr_y = np.arange(ymin,ymax+1,30)
    
    # ax.set_title(f'Sbedrock', fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    
        # 添加海岸线和陆地特征
    ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    # 自定义绘图
    ax.set_extent([xmin,xmax,ymin,ymax])
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img

# for year in range(2003,2018):
def draw(name,band):
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)  # 创建2行3列的子图网格
    img = plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), xmin, xmax, ymin, ymax,name,band)

    # rect1 = [0.1, 0.1, 0.8, 0.04]  #左下角x,y,宽,高
    # cbar_ax1 = fig.add_axes(rect1,frameon = False)
    # cb1 = fig.colorbar(img, 
    #                 drawedges=False,
    #                 ticks=level, 
    #                 cax=cbar_ax1, 
    #                 orientation='horizontal',
    #                 spacing='uniform')
    # cb1.ax.tick_params(labelsize=18)
    # cb1.set_label(name, fontsize=30, fontweight='bold')

    plt.savefig(f"{fig_path}/g4_{name}.png")
# print(year)

name = ['mask1','mask12','mask123','mask2','mask3']
band = ['Band1','Band1','Band1','LC','et']



for i in range(5):
    draw(name[i],band[i])
    
# name = ['mask1V2_so','mask1V2_av','mask1']
# band = ['Band1','Band1', 'Band1']

# for i in range(1):
#     draw(name[i],band[i])
