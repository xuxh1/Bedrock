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
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from myfunc import timer
from myfunc import DirMan
import config
import matplotlib.font_manager as fm

resolution = config.resolution
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path
size       = config.size

casename1 = 'bedrock_1'
path1 = f'{data_path}/cases/{casename1}/'
casename2 = 'bedrock_2'
path2 = f'{data_path}/cases/{casename2}/'
casename3 = 'bedrock_3'
path3 = f'{data_path}/cases/{casename3}/'

print('python draw_g2_scatter_cases.py')

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
font_properties = fm.FontProperties(weight='bold')

def data_process(name):
    df = pd.read_csv(f'{data_path}csv/Global_cases.csv')

    df1 = df.copy()
    df1['diff'] = df[name[0]] - df[name[1]]

    return df1

def set_fig(name):
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
    
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,df1,name,cmap,level):
    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1['diff'], 
                    s=size, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, vmin=level[0], vmax=level[-1])

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(2) 

    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    # coastline = cfeature.NaturalEarthFeature('physical', 'coastline', '50m', edgecolor='0.6', facecolor='none')
    rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '110m', edgecolor='0.6', facecolor='none')
    ax.add_feature(cfeature.LAND, facecolor='0.95')
    # ax.add_feature(coastline, linewidth=0.6)
    ax.add_feature(cfeature.LAKES, alpha=1, facecolor='white', edgecolor='white')
    ax.add_feature(rivers, linewidth=0.8)
    # ax.gridlines(draw_labels=False, linestyle=':', linewidth=0.7, color='grey', alpha=0.8)

    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent(region)
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img

def set_colorbar(name,img,level,fig):
    # From the bottom left corner x, y, width, height
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')

    cb.ax.tick_params(labelsize=20)
    cb.ax.yaxis.set_tick_params(direction='out', width=1.5)
    for label in cb.ax.get_xticklabels() + cb.ax.get_yticklabels():
        label.set_fontproperties(font_properties)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

# def set_legend(ax,name):
#     FM_list = ['FM_mean', 'FM_mean_nm']
#     FY_list = ['FY', 'FY_nm']
#     if name[2] in FM_list:
#         RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
#         labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', '≥Jun']
#         legend_patches = [mpatches.Patch(color=color, label=label) 
#                         for color, label in zip(RGBs, labels)]
#         ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(0, 0.01),
#                 fontsize=16, title="First Month" ,title_fontsize=20,
#                 frameon=False, edgecolor='black', ncol=3, columnspacing=1)
#     elif name[2] in FY_list:
#         RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
#         labels = ['2003', '2004', '2005', '2006', '2007', '≥2008']
#         legend_patches = [mpatches.Patch(color=color, label=label) 
#                         for color, label in zip(RGBs, labels)]
#         ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(0, 0.01),
#                 fontsize=16, title="First Year" ,title_fontsize=20,
#                 frameon=False, edgecolor='black', ncol=3, columnspacing=1)  

def draw(name,level,cmap):
    df1 = data_process(name)
    fig,ax = set_fig(name)
    img = set_ax(ax,df1,name,cmap,level)

    set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/global_map_2/g2_{name[2]}_diff.png")
    plt.close(fig)


level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(-100,125,25)

cmap1 = cmaps.cmocean_curl

# def Ssoil_case1():
#     name = [f'{path1}Ssoil_mean', 'Ssoil', 'Ssoil_case1', '(model case1 Ssoil) - (Kogusi Ssoil)']
#     level = level2
#     cmap = cmap1
#     draw(name,level,cmap)
        
# def Ssoil_case2():
#     name = [f'{path2}Ssoil_mean', 'Ssoil', 'Ssoil_case2', '(model case2 Ssoil) - (Kogusi Ssoil)']
#     level = level2
#     cmap = cmap1
#     draw(name,level,cmap)

# def Ssoil_case3():
#     name = [f'{path3}Ssoil_mean', 'Ssoil', 'Ssoil_case3', '(model case3 Ssoil) - (Kogusi Ssoil)']
#     level = level2
#     cmap = cmap1
#     draw(name,level,cmap)

def Sr_case1():
    name = [f'{path1}Sr_mean', 'Sr', 'Sr_case1', '(model case1 Sr) - (our calculated Sr)']
    level = level2
    cmap = cmap1
    draw(name,level,cmap)
        
def Sr_case2():
    name = [f'{path2}Sr_mean', 'Sr', 'Sr_case2', '(model case2 Sr) - (our calculated Sr)']
    level = level2
    cmap = cmap1
    draw(name,level,cmap)

def Sr_case3():
    name = [f'{path3}Sr_mean', 'Sr', 'Sr_case3', '(model case3 Sr) - (our calculated Sr)']
    level = level2
    cmap = cmap1
    draw(name,level,cmap)

# def PSr_case1():
#     name = [f'{path1}PSr_mean', 'Sr', 'PSr', '(model case1 PSr) - (our calculated PSr)']
#     level = level3
#     cmap = cmap1
#     draw(name,level,cmap)
        
# def PSr_case2():
#     name = [f'{path2}PSr_mean', 'Sr', 'PSr', '(model case1 PSr) - (our calculated PSr)']
#     level = level3
#     cmap = cmap1
#     draw(name,level,cmap)

# def PSr_case3():
#     name = [f'{path3}PSr_mean', 'Sr', 'PSr', '(model case1 PSr) - (our calculated PSr)']
#     level = level3
#     cmap = cmap1
    draw(name,level,cmap)

if __name__=='__main__':
    # Ssoil_case1()
    # Ssoil_case2()
    # Ssoil_case3()
    Sr_case1()
    Sr_case2()
    Sr_case3()
    # PSr_case1()
    # PSr_case2()
    # PSr_case3()