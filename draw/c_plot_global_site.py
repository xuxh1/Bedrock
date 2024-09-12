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
from math import radians, sin
import matplotlib
from pylab import rcParams
import pandas as pd
import netCDF4 as nc
import seaborn as sns
import os
from plotnine import *
from shapely.geometry import Point



path = os.getcwd()+'/'
print("当前文件路径:", path)

path = '/tera11/zhwei/students/Xionghui/data/field/DTB/'
df = pd.read_csv(f'{path}new_literature_compilation.csv', encoding='latin-1')

shp_path = '/home/xuxh22/stu01/Bedrock/data/Shp/No_antarctica_continent/'
shp = gpd.GeoDataFrame.from_file(shp_path+'no_antarctica.shp')
# shp = gpd.read_file(shp_path+'ne_10m_admin_0_countries_chn.shp')

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
def point_map():
    df_map = shp
    long_mar=np.arange(105,135, 0.6)
    lat_mar=np.arange(30,60, 0.8)
    X,Y=np.meshgrid(long_mar,lat_mar)
    df_grid =pd.DataFrame({'long':X.flatten(),'lat':Y.flatten()})

    geom  = gpd.GeoSeries([Point(x, y) for x, y in zip(df_grid.long.values, df_grid.lat.values)])
    df_grid=gpd.GeoDataFrame(df_grid,geometry=geom)


    inter_point=df_map['geometry'].intersection(df_grid['geometry'].unary_union).tolist()

    print(inter_point)
    # exit(0)
    # point_x=[]
    # point_y=[]
    # for i in range(len(inter_point)):
    #     if inter_point[i].is_empty:
    #         continue  # 如果几何对象为空，则跳过这个点
    #     # elif (str(type(inter_point[i]))!="<class 'shapely.geometry.point.Point'>"):
    #     #     point_x=point_x+[item.x for item in inter_point[i]]
    #     #     point_y=point_y+[item.y for item in inter_point[i]]
    #     else:
    #         point_x=point_x+[inter_point[i].x]
    #         point_y=point_y+[inter_point[i].y]

    df_pointmap =pd.DataFrame({'long':inter_point.x,'lat':inter_point.y})
    print(df_pointmap)
    plot_base=(ggplot() +
            geom_map(df_map,fill='white',color='k')+
            geom_point(df_pointmap,aes(x='long',y='lat'),fill='k',size=3,shape='o',stroke=0.1)+
            theme(
                axis_title=element_text(size=15, face="plain", color="black"),
                axis_text=element_text(size=12, face="plain", color="black"),
                legend_title=element_text(size=14, face="plain", color="black"),
                legend_background=element_blank(),
                legend_position=(0.8, 0.2),
                aspect_ratio=1.15,
                figure_size=(6, 4),
                dpi=50
            )+
            xlim(-180, 180)+
            ylim(-90, 90)   
            )
    plot_base.save('fig3/test.png', dpi=300)
    
point_map() 
    
def plot(ax, name, level, cmap):
    image = xr.open_dataset(f'{name[0]}.nc').sel(lon=slice(xmin,xmax),lat=slice(ymin,ymax))
    s = image[f'{name[1]}']
    
    image.close()

    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  
    

    lat = nc.Dataset(f'Sbedrock.nc')['lat'][:].flatten()
    lon = nc.Dataset(f'Sbedrock.nc')['lon'][:].flatten()
    s = nc.Dataset(f'Sbedrock.nc')['Sr'][:,:].flatten()
    latf = np.repeat(lat, len(lon))
    lonf = np.tile(lon, len(lat))
    
    df = pd.DataFrame()
    df['lat'] = latf.round(2)
    df['lon'] = lonf.round(2)
    df['Sbedrock'] = s
    
    df = df.dropna()
    df = df[df['Sbedrock'] > 0]
    
    scatter = ax.scatter(df['lon'], df['lat'], c=df['Sbedrock'], 
                     s=1, linewidths=0.01, edgecolors="k",cmap=cmap,zorder=2,vmin=level[0],vmax=level[-1])
    
    # img = ax.imshow(s, cmap=cmap,
    #                 extent=[xmin, xmax, ymax, ymin],
    #                 vmin=level[0], vmax=level[-1])
    
    # lat = df['Latitude']
    # lon = df['Longitude']
    # ax.plot(lon, lat, 'o', markersize=2,color='grey')
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # arr_x = np.arange(xmin,xmax+1,60)
    # arr_y = np.arange(ymin,ymax+1,30)
    
    # ax.set_title(f'Sbedrock', fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    
    # ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    ax.set_extent([xmin,xmax,ymin-30,ymax])
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return scatter

def draw(name, level, cmap):
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)  # 创建2行3列的子图网格
    # img = plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), name, level, cmap)
    img =plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), name, level, cmap)
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) # 左下角x,y,宽,高
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]} (mm)', fontsize=30, fontweight='bold')

    plt.savefig(f"fig3/p_test.png")
    
name = ['Sr', 'Sr', 'SrG', '$S_{{r}}$']
level = np.arange(0,500,50)
rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap = colors.ListedColormap(rgb_list)
# draw(name,level,cmap)