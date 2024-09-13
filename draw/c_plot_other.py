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

path = '/tera11/zhwei/students/Xionghui/data/'

@timer
def plot(ax, xmin, xmax, ymin, ymax, name, level, cmap, norm):
    image = xr.open_dataset(f'{path}{name[0]}.nc').sel(lon=slice(xmin,xmax),lat=slice(ymin,ymax))
    s = image[f'{name[1]}']

    image.close()

    if (name[2]=='SbG') or (name[2]=='SpG'):
        s = np.where(s<=0, np.nan, s)   
    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  
    
    
    # img = ax.imshow(s, cmap=cmap,
    #                 extent=[xmin, xmax, ymax, ymin],
    #                 vmin=level[0], vmax=level[-1])
    
    img = ax.imshow(s, cmap=cmap,
                    extent=[xmin, xmax, ymax, ymin],
                    norm = norm)
        
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


def draw(name, level, cmap, norm):
    fig = plt.figure(figsize=(12, 6), dpi=2000)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)  # 创建2行3列的子图网格
    img = plot(fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree()), xmin, xmax, ymin, ymax, name, level, cmap, norm)

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

def define_colormap(level, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    color = cmap(np.linspace(0, 1, len(level) - 1))
    cmap_custom = colors.ListedColormap(color)
    cmap_custom.set_under(cmap(0))
    cmap_custom.set_over(color[-1])
    norm = colors.BoundaryNorm(level, cmap_custom.N)
    return cmap_custom, norm


level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)
level4 = np.arange(-100,125,25)
level5 = [0, 100, 150, 200, 220, 240, 300, 400, 700, 1000, 1500, 2000, 4000, 8000]

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BuGn'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)
cmap4 = "bwr"
cmap5 = 'RdBu_r'
cmap5,norm = define_colormap(level5,cmap5)

def DTBV1():
    # name = ['mask1/DTB_temp1', 'Band1', 'DTBV1', 'DTB (cm)']
    # level = level5
    # cmap = cmap5
    # draw(name,level,cmap, norm)
    name = ['mask1/DTB_temp3', 'Band1', 'DTBV1_rev', 'DTB (cm)']
    level = level5
    cmap = cmap5
    draw(name,level,cmap, norm)
    
def DTBV2():
    name = ['mask1/mask1V2/average_soil_and_sediment_remap_cm', 'Band1', 'DTBV2_av', 'DTB (cm)']
    level = level5
    cmap = cmap5
    draw(name,level,cmap,norm)
    name = ['mask1/mask1V2/upland_hillslope_regolith_remap_cm', 'Band1', 'DTBV2_re', 'DTB (cm)']
    level = level5
    cmap = cmap5
    draw(name,level,cmap,norm)    
    name = ['mask1/mask1V2/upland_hillslope_soil_remap_cm', 'Band1', 'DTBV2_so', 'DTB (cm)']
    level = level5
    cmap = cmap5
    draw(name,level,cmap,norm) 
    
def SsoilV2():
    name = ['Ssoil/SsoilV2/Global_climatic_plant_ava_remap', 'Band1', 'SsoilV2_c', 'Ssoil']
    level = level1
    cmap = cmap1
    draw(name,level,cmap,norm)
    name = ['Ssoil/SsoilV2/Global_potential_pasw_remap', 'Band1', 'SsoilV2_p', 'Ssoil']
    level = level1
    cmap = cmap1
    draw(name,level,cmap,norm)    
    
def SrV2():
    name = ['Sr/cwdx80', 'cwdx80', 'Sr_V2', 'Sr (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap,norm) 
    
DTBV1()
# DTBV2()
# SsoilV2()
# SrV2()