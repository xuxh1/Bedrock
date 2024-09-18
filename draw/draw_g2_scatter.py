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

shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

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
    df = pd.read_csv(f'{data_path}Global.csv')

    df_s = pd.read_csv(f'{data_path}site.csv')

    df1 = df.copy()
    df2 = df_s.copy()

    # print(df1)
    # print(name[0])
    df1 = df1[df1[name[0]] > 0]
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
def set_ax(ax,df1,df2,name,cmap,level):
    if name[2] == 'Sb':
        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors="#153aab", label='Report of roots \npenetrating bedrock, mask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors='none', label='Report of roots \npenetrating bedrock, unmask', zorder=2)

        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors="red", label='Report of bedrock water contribution \nto ET from unsaturated zone, mask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors='none', label='Report of bedrock water contribution \nto ET from unsaturated zone, unmask', zorder=2)
        
        ax.legend(fontsize=12 ,bbox_to_anchor=(0.29, 0.379))

    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[0]], 
                    s=0.1, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])

    
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    ax.add_feature(cfeature.COASTLINE)
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
def draw(name,level,cmap):
    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,name,cmap,level)
    set_other(name,img,level,fig)

    plt.savefig(f"{fig_path}/g2_{name[2]}.png")


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

def Sb():
    name = ['Sbedrock', 'Sr', 'Sb', '$S_{{bedrock}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    # name = ['Sbedrock', 'Sr', 'Sb_n2p', '$S_{{bedrock}}$ (mm)']
    # level = level2
    # cmap = cmap2
    # draw(name,level,cmap)

def Sr():
    name = ['Sr', 'Sr', 'Sr', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    
def Ss():
    name = ['Ssoil', 'Band1', 'Ss', '$S_{{soil}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)

def PR_ET_Q_LH():
    name = ['PR', 'tp', 'PR', 'Precipitation (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['ET', 'et', 'ET', 'Evapotranspiration (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['Q', 'tp', 'Q', 'Streamflow (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['LH', 'Ee', 'LH', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,100,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)

def P1():
    name = ['Proportion1', 'Sr', 'P1', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    # name = ['Proportion1', 'Sr', 'P1_n2p', '$S_{{bedrock}}$/$S_{{r}}$']
    # level = level4
    # cmap = cmap4
    # draw(name,level,cmap)
        
def P2():
    name = ['Proportion2', 'Sr', 'P2', '$S_{{bedrock}}$/ET']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    # name = ['Proportion2', 'Sr', 'P2_n2p', '$S_{{bedrock}}$/ET']
    # level = level4
    # cmap = cmap4
    # draw(name,level,cmap)

def P3():
    name = ['Proportion3', 'tp', 'P3', 'Q/PR']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    # name = ['Proportion3', 'tp', 'P3_n2p', 'Q/PR']
    # level = level4
    # cmap = cmap4
    # draw(name,level,cmap)
    
def FD():
    name = ['FD_mean', 'FD', 'FD', 'First Day']
    level = level5
    cmap = cmaps.StepSeq25
    draw(name,level,cmap)

def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)']
    level = np.arange(0,200,50)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.cmocean_matter
    draw(name,level,cmap)
    
def Biomass():
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
    
def IGBP():
    name = ['IGBP', 'LC', 'IGBP', 'IGBP']
    level = np.arange(0.5,18.5,1)
    rgb_list = ['#05450a', '#086a10', '#54a708', '#78d203', '#009900', '#c6b044', '#dcd159', '#dade48', '#fbff13', '#b6ff05', '#27ff87',
            '#c24f44', '#a5a5a5', '#ff6d4c', '#69fff8', '#f9ffa4', '#1c0dff']
    cmap = colors.ListedColormap(rgb_list)
    draw(name,level,cmap)
    
def Koppen():
    name = ['Koppen', 'Band1', 'Koppen', 'Koppen']
    level = np.arange(0,31,1)
    rgb_list = ['#ffffff','#0000FE','#0077FF','#46A9FA','#FE0000',
                '#FE9695','#F5A301','#FFDB63','#FDFD45','#C6C700',
                '#96FF96','#63C764','#329633','#C6FF4E','#66FF33',
                '#33C701','#FF00FE','#C600C7','#963295','#966495',
                '#ABB1FF','#5A77DB','#4C51B5','#320087','#18DCDC',
                '#38C7FF','#007E7D','#00455E','#B2B2B2','#686868']
    cmap = colors.ListedColormap(rgb_list)
    draw(name,level,cmap)

@timer
def draw_G():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    Sb()
    Sr()
    Ss()
    PR_ET_Q_LH()
    P1()
    P2()
    P3()
    FD()
    DTB()
    Biomass()
    IGBP()
    Koppen()

if __name__=='__main__':
    draw_G()