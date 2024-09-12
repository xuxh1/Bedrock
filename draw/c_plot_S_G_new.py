
# plot_S_Global.py

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
import pandas as pd
import cmaps

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

df = pd.read_csv('region2.csv')
xmin,xmax,ymin,ymax = -180,180,-60,90

df_s = pd.read_csv('site.csv')
print(df_s)

@timer
def plot(ax, xmin, xmax, ymin, ymax, name, level, cmap):
    # df2 = df_s.copy()
    # print(df2)
    # df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'Y')]
    # print(df3)
    # ax.scatter(df3['lon'], df3['lat'], marker='o',
    #                 s=20, linewidths=1, edgecolors="#153aab", facecolors="#153aab", label='Report of roots \npenetrating bedrock, mask', zorder=2)
    
    # df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'Y')]
    # print(df3)
    # ax.scatter(df3['lon'], df3['lat'], marker='o',
    #                 s=20, linewidths=1, edgecolors="#153aab", facecolors='none', label='Report of roots \npenetrating bedrock, unmask', zorder=2)

    # df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'N')]
    # print(df3)
    # ax.scatter(df3['lon'], df3['lat'], marker='o',
    #                 s=20, linewidths=1, edgecolors="red", facecolors="red", label='Report of bedrock water contribution \nto ET from unsaturated zone, mask', zorder=2)
    
    # df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'N')]
    # print(df3)
    # ax.scatter(df3['lon'], df3['lat'], marker='o',
    #                 s=20, linewidths=1, edgecolors="red", facecolors='none', label='Report of bedrock water contribution \nto ET from unsaturated zone, unmask', zorder=2)
    
    # ax.legend(fontsize=12 ,bbox_to_anchor=(0.29, 0.379))
    
    df1 = df.copy()
    df1 = df1[df1[name[4]] > 0]

    img = ax.scatter(df1['lon'], df1['lat'], c=df1[name[4]], 
                    s=1, linewidths=0, edgecolors="k",cmap=cmap,zorder=1,vmin=level[0],vmax=level[-1])
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([xmin,xmax,ymin,ymax])
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    

    return img

# def plot_site(ax, xmin, xmax, ymin, ymax, name, level, cmap):


def draw(name, level, cmap):
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    img = plot(ax, xmin, xmax, ymin, ymax, name, level, cmap)
    # plot_site(ax, xmin, xmax, ymin, ymax, name, level, cmap)
    
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) # 左下角x,y,宽,高
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

    plt.savefig(f"fig4/p_{name[2]}_test3.png")

level1 = np.arange(0,500,50)
# level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)
level4 = np.arange(-100,125,25)


# rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
#                                 '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
rgb_list = ['#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666','#606060']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)
cmap4 = "bwr"

def Sr():
    name = ['Sr', 'Sr', 'SrG', '$S_{{r}}$ (mm)','Sr']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    # name = ['Sr_temp1', 'Sr', 'SrG_all', '$S_{{r}}$','Sr']
    # level = level1
    # cmap = cmap1
    # draw(name,level,cmap)
    
def Sb():
    name = ['Sbedrock', 'Sr', 'SbG', '$S_{{bedrock}}$ (mm)','Sbedrock']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    # name = ['Sbedrock', 'Sr', 'SbG_all_mask', '$S_{{bedrock}}$','Sbedrock']
    # level = level2
    # cmap = cmap2
    # draw(name,level,cmap)
    # name = ['Sbedrock_temp1', 'Sr', 'SbG_all', '$S_{{bedrock}}$','Sbedrock']
    # level = level2
    # cmap = cmap2
    # draw(name,level,cmap)
    
def Sp():
    name = ['Sproportion', 'Sr', 'SpG', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    # name = ['Sproportion', 'Sr', 'SpG_all_mask', '$S_{{bedrock}}$/$S_{{r}}$']
    # level = level4
    # cmap = cmap4
    # draw(name,level,cmap)
    # name = ['Sproportion_temp1', 'Sr', 'SpG_all', '$S_{{bedrock}}$/$S_{{r}}$']
    # level = level4
    # cmap = cmap4
    # draw(name,level,cmap)
        
def Ss():
    name = ['Ssoil', 'Band1', 'SsG', '$S_{{soil}}$ (mm)','Ssoil']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    
def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)','DTB']
    level = np.arange(0,175,25)
    cmap = cmaps.cmocean_matter
    draw(name,level,cmap)
    
# Sr()
Sb()
# Sp()
# Ss()
# DTB()

