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

print('python draw_g2_scatter.py')
dir_man = DirMan(data_path)
dir_man.enter()
os.makedirs(f'{fig_path}/global_map_2', exist_ok=True)


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
    df = pd.read_csv(f'{data_path}csv/Global_FDFMFY.csv')

    df_s = pd.read_csv(f'{data_path}csv/site.csv')

    df1 = df.copy()
    df2 = df_s.copy()

    df1 = df1[df1[name[0]] > 0]
    return df1,df2

def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,df1,df2,name,cmap,level):


    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[0]], 
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

    if name[2] == 'Sb':
        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors="#153aab", label='Report of roots \npenetrating bedrock, unmask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors='none', label='Report of roots \npenetrating bedrock, mask', zorder=2)

        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors="red", label='Report of bedrock water contribution \nto ET from unsaturated zone, unmask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors='none', label='Report of bedrock water contribution \nto ET from unsaturated zone, mask', zorder=2)
        
        ax.legend(fontsize=14, bbox_to_anchor=(-0.0145, 0.005), loc='lower left')
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
    cb.set_label(f'{name[3]}', fontsize=25, fontweight='bold')

def set_legend(ax,name,RGBs):
    FM_list = ['D_FM_mean']
    FY_list = ['S_FY']
    if name[2] in FM_list:
        # RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', '≥Jun']
        legend_patches = [mpatches.Patch(color=color, label=label) 
                        for color, label in zip(RGBs, labels)]
        ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(-0.01, 0.01),
                fontsize=16, title="" ,title_fontsize=20,
                frameon=False, edgecolor='black', ncol=3, columnspacing=1)
    elif name[2] in FY_list:
        # RGBs = ['#4B74B2', '#90BEE0', '#E6F1F3', '#FFDF92', '#FC8C5A', '#DB3124']
        labels = ['2003', '2004', '2005', '2006', '2007', '≥2008']
        legend_patches = [mpatches.Patch(color=color, label=label) 
                        for color, label in zip(RGBs, labels)]
        ax.legend(handles=legend_patches, loc='lower left', bbox_to_anchor=(-0.01, 0.01),
                fontsize=16, title="" ,title_fontsize=20,
                frameon=False, edgecolor='black', ncol=3, columnspacing=1)    


def draw(name,level,cmap,RGBs):
    FD_list = ['S_FD','D_FD_mean']

    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,name,cmap,level)
    if name[2] in FD_list:
        set_colorbar(name,img,level,fig)
    else:
        set_legend(ax,name,RGBs)

    plt.savefig(f"{fig_path}/global_map_2/g2_{name[2]}.png")
    plt.close(fig)

RGBs =['#4B74B2', '#EC7A8D', '#89DD8B', '#DFD987', '#A999CD', '#DB3124']
cmap1 = colors.ListedColormap(RGBs)

def S_FD():
    name = ['S_FD', 'S_FD', 'S_FD', 'the initial day utilizing bedrock water from 2003.01.01 to 2020.12.31']
    level = np.arange(0,6000,1000)
    cmap = cmaps.StepSeq25_r
    draw(name,level,cmap,RGBs)

def S_FY():
    name = ['S_FY', 'S_FY', 'S_FY', 'the initial year utilizing bedrock water from 2003 to 2020']
    level = np.arange(1,7,1)
    cmap = cmap1
    draw(name,level,cmap,RGBs)

def D_FD_mean():
    name = ['D_FD_mean', 'D_FD_mean', 'D_FD_mean', 'the initial day utilizing bedrock water in a year (mean from 2003 to 2020)']
    level = np.arange(0,300,50)
    cmap = cmaps.StepSeq25_r
    draw(name,level,cmap,RGBs)

def D_FM_mean():
    name = ['D_FM_mean', 'D_FM_mean', 'D_FM_mean', 'the initial month utilizing bedrock water in a year (mean from 2003-2020)']
    level = np.arange(1,7,1)
    cmap = cmap1
    draw(name,level,cmap,RGBs)

if __name__=='__main__':
    S_FD()
    S_FY()
    D_FD_mean()
    D_FM_mean()