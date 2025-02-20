import os
import cmaps
import salem
import numpy as np
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
# region     = config.region
# data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path
size       = config.size

print('python draw_r1_scatter_US_nature.py')

# shp = gpd.GeoDataFrame.from_file('/tera11/zhwei/students/Xionghui/data/Shp/Conus/Conus.shp')
shp = gpd.GeoDataFrame.from_file(shp_path+'US/USA_adm0.shp')


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

def data_process(name,region):
    image = xr.open_dataset(f'/tera11/zhwei/students/Xionghui/data/US/{name[0]}.nc').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    s = image[f'{name[1]}']
    s = s.salem.roi(shape=shp)
    lon = image['lon'][:].flatten()
    lat = image['lat'][:].flatten()

    image.close()

    if ((name[1]=='LC') or (name[1]=='tp') or (name[1]=='et')):
        s = s[0,:,:]

    if (name[2]=='Sb') or (name[2]=='Sp') or (name[1]=='FD') or (name[1]=='Dr'):
        s = np.where(s<=0, np.nan, s)   
    if (name[2]=='P1'):
        s = s*100
    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  
    return s,lon,lat

def set_fig():
    fig = plt.figure(figsize=(12, 7), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,lon,lat,s,cmap,region,level):
    # Set drawing mode(note:extent's lat from positive to negative)
    # img = ax.imshow(s, cmap=cmap,
    #                 extent=[region[0], region[1], region[3], region[2]],
    #                 vmin=level[0], vmax=level[-1])
    lat_new = np.repeat(lat, len(lon))
    lon_new = np.tile(lon, len(lat))
    
    img = ax.scatter(lat_new, lon_new, c=s[:,:].flatten(), 
                    s=size, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])
    
    shp.boundary.plot(ax=ax, edgecolor='black', linewidth=0.75, alpha=1)

    arr_x = np.arange(region[0]+4.8, region[1], 10)
    arr_y = np.arange(region[2]+0.5, region[3]+1, 10)

    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.set_xticks(arr_x)
    ax.set_xticklabels(arr_x,fontsize=24)
    ax.set_yticks(arr_y)
    ax.set_yticklabels(arr_y,fontsize=24)
    
    # ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, facecolor='gray')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    # ax.set_extent(region)
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    return img

def set_other(name,img,level,fig):
    # From the bottom left corner x, y, width, height
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=24)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')
    for spine in cb.ax.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color('black')

@timer
def draw(name,region,level,cmap):
    legend_list = ['mask1', 'mask2', 'mask3', 'mask12', 'mask123']

    s,lon,lat = data_process(name,region)
    fig,ax = set_fig()
    img = set_ax(ax,lon,lat,s,cmap,region,level)

    if name[2] in legend_list:
        print('no use colorbar')
    else:
        set_other(name,img,level,fig)

    plt.savefig(f"{fig_path}/r2_{name[2]}_US_nature.png")
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

region = [-124.8,-66.95,24.5,49.4]


def Sb():
    name = ['deficits/Sbedrock', 'Band1', 'Sb', '$S_{{bedrock}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,region,level,cmap)
    
def Sr():
    name = ['deficits/Sr', 'Band1', 'Sr', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,region,level,cmap)
    
def Ss():
    name = ['products_used/gNATSGO/Ssoil_500m', 'Band1', 'Ss', '$S_{{soil}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,region,level,cmap)

def mask():
    name = ['masks/masks_all_combined', 'Band1', 'mask123', 'masks_all_combined']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,region,level,cmap)
    name = ['masks/mask_shallowBedrock', 'Band1', 'mask1', 'mask_shallowBedrock']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,region,level,cmap)
    name = ['masks/mask_woodyVeg', 'Band1', 'mask2', 'mask_woodyVeg']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,region,level,cmap)
    name = ['masks/mask_ET_gt_P', 'Band1', 'mask3', 'mask_ET_gt_P']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,region,level,cmap)

def P1():
    name = ['deficits/Sbedrock_dividedby_Sr', 'Band1', 'P1', '$S_{{bedrock}}$/$S_{{r}}$ (%)']
    level = level3
    cmap = cmaps.StepSeq25_r
    draw(name,region,level,cmap)

@timer
def draw_R():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Sb()
    # Sr()
    # Ss()
    # mask()
    P1()

if __name__=='__main__':
    draw_R()