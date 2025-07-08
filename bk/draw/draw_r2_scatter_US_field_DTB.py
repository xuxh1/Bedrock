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

print('python draw_r2_scatter_US_field.py')
dir_man = DirMan(data_path)
dir_man.enter()

region = [-124.8,-66.95,24.5,49.4]


# shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')
shp = gpd.GeoDataFrame.from_file(shp_path+'US/USA_adm0.shp')

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
    df = pd.read_csv(f'{data_path}csv/Global_statistics.csv')

    df_s = pd.read_csv(f'{data_path}csv/DTB_US.csv')

    df1 = df.copy()
    df2 = df_s.copy()

    df1 = df1[df1[name[0]] > 0]
    return df1,df2

def set_fig():
    fig = plt.figure(figsize=(12, 7), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.04, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

def set_ax(ax,df1,df2,name,cmap,level,norm):
    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[0]], 
                    s=0.005, linewidths=0, edgecolors="k", 
                    cmap=cmap, zorder=1, norm=norm)
    # shp.boundary.plot(ax=ax, edgecolor='black', linewidth=0.75, alpha=1)

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

    # if name[2] == 'Sb':
    df3 = df2.copy() 
    df3 = df3.sort_values(by=['lon']).reset_index(drop=True)
    df3 = df3[(df3['lon'] < 0)]
    print(df3)
    ax.scatter(df3['lon'], df3['lat'], marker='o',
                    s=100, linewidths=1, edgecolors="black", facecolors="black", zorder=2)
    
    # for i, row in df3.iterrows():
    #     if i == 0:
    #         ax.text(row['lon'] , row['lat'] + 0.5, f'{i+1}', ha='center', va='bottom', fontsize=36, fontweight='bold')
    #     elif i == 5:
    #         ax.text(row['lon'] -0.6 , row['lat'] - 1.6, f'{i+1}', ha='center', va='bottom', fontsize=36, fontweight='bold')
    #     elif i == 8:
    #         ax.text(row['lon'] -0.5 , row['lat'] - 0.5, f'{i+1}', ha='center', va='bottom', fontsize=36, fontweight='bold')
    #     else:
    #         ax.text(row['lon'] + 0.5, row['lat'] + 0.5, f'{i+1}', ha='center', va='bottom', fontsize=36, fontweight='bold')

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
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')




def draw(name,level,cmap,norm):
    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,name,cmap,level,norm)
    # set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/r2_{name[2]}.png")
    plt.close(fig)

level1 = [0, 100, 150, 200, 220, 240, 300, 400, 700, 1000, 1500, 2000, 4000, 8000]

cmap = 'RdBu_r'

def define_colormap(level, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    color = cmap(np.linspace(0, 1, len(level) - 1))
    cmap_custom = colors.ListedColormap(color)
    cmap_custom.set_under(cmap(0))
    cmap_custom.set_over(color[-1])
    norm = colors.BoundaryNorm(level, cmap_custom.N)
    return cmap_custom, norm

cmap1, norm= define_colormap(level1,cmap)

def DTB():
    name = ['DTB', 'DTB', 'DTB_field', 'Depth to Bedrock (cm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap,norm)

if __name__=='__main__':
    DTB()