import os
import numpy as np
import pandas as pd
from pylab import rcParams
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
name       = config.name
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path

print('python draw_l2_latlon.py')

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

df = pd.read_csv(f'{data_path}Global.csv')

def plot_line(title, ax, x, y1, y2, color):
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(ls = "--", lw = 0.25, color = "#4E616C")
    y1 = y1.rolling(window = 5, min_periods = 0).mean()
    ax.plot(x, y1, mfc = "white",lw = 0.8, ms = 2, color = color[0], label=title[1])
        
    ax.set_ylim(0)
    
    if x.min() < -90:
        interval = 60
        xmin,xmax = -180,180
    else:
        interval = 30
        xmin,xmax = -90,90
    xlevel = np.arange(xmin, xmax+interval, interval)
    xlevel_narrow = np.arange(xmin+interval, xmax, interval)
    
    ax.xaxis.set_major_locator(ticker.MultipleLocator(interval))
    ax.xaxis.set_ticks(xlevel_narrow)
    ticks_degrees = xlevel_narrow
    
    if x.min() < -90:
        tick_labels = [f"{abs(int(deg))}°{'E' if deg > 0 else ('W' if deg < 0 else '')}" for deg in ticks_degrees]
    else:
        tick_labels = [f"{abs(int(deg))}°{'N' if deg > 0 else ('S' if deg < 0 else '')}" for deg in ticks_degrees]
        
    ax.xaxis.set_ticklabels(tick_labels)
    ax.xaxis.set_tick_params(length = 2, color = "#4E616C", labelcolor = "#4E616C", labelsize = 12)
    ax.set_xlim(xlevel[0],xlevel[-1])
    
    if x.min() < -90:
        interval = 1000
    else:
        interval = 2000
    y1level = np.arange(0,y1.max()+interval,interval)
    # print(y1level)
    y1level_narrow = np.arange(interval,y1.max(),interval)
    ax.set_ylim(0, y1level[-1])
    ax.yaxis.set_ticks(y1level_narrow)
    ax.yaxis.set_ticklabels(int(j) for j in y1level_narrow)
    ax.yaxis.set_tick_params(length = 2, color = "#4E616C", labelcolor = "#4E616C", labelsize = 12)

    ax2 = ax.twinx()
    interval = 100
    y2level = np.arange(0, y2.max() + interval, interval)
    y2level_narrow = np.arange(interval,y2.max(),interval)
    
    ax2.set_xlim(xlevel[0],xlevel[-1])
    ax2.set_ylim(0, y2level[-1])
    ax2.yaxis.set_ticks(y2level_narrow)
    ax2.yaxis.set_ticklabels(int(j) for j in y2level_narrow)
    ax2.yaxis.set_tick_params(length=2, color="#4E616C", labelcolor="#4E616C", labelsize=12)
    y2 = y2.rolling(window = 20, min_periods = 0).mean()
    ax2.plot(x, y2, mfc = "white",lw = 0.8, ms = 2, color = color[1], label=title[1])

    
    # ax.axvline(x=0, color="#4E616C",lw = 0.2, linestyle='-')
    ax.spines["bottom"].set_edgecolor("#4E616C")


    y1 = y1.iloc[-1]
    ax.text(x = ax.get_xlim()[0] - ax.get_xlim()[1]/20, y = ax.get_ylim()[1] + ax.get_ylim()[1]/10,
            s = f'{title[0]}',
            color = "#4E616C",
            va = 'center',
            ha = 'left',
            size = 14
            )
    
    ax.text(x = ax.get_xlim()[1] - ax.get_xlim()[1]/3, y = ax.get_ylim()[1] - ax.get_ylim()[1]/10,
            s = title[0].split('(')[0],
            color = color[0],
            va = 'center',
            ha = 'left',
            size = 12
            )
    
    y2 = y2.iloc[-1]
    ax.text(x = ax.get_xlim()[1] - ax.get_xlim()[1]/10, y = ax.get_ylim()[1] + ax.get_ylim()[1]/10,
            s = f'{title[1]}',
            color = "#4E616C",
            va = 'center',
            ha = 'left',
            size = 14
            )
    
    ax.text(x = -ax.get_xlim()[1]/8, y = ax.get_ylim()[1] - ax.get_ylim()[1]/10,
            s = title[1].split('(')[0],
            color = color[1],
            va = 'center',
            ha = 'left',
            size = 12
            )
    # handles1, labels1 = ax.get_legend_handles_labels()
    # handles2, labels2 = ax2.get_legend_handles_labels()
    # print(handles1)
    # handles = handles1 + handles2
    # print(handles)
    
    # labels = title  
    # custom_line1 = Line2D([0], [0], color=color[0], linewidth=2)
    # custom_line2 = Line2D([0], [0], color=color[1], linewidth=2)
    # handles = [custom_line1, custom_line2]
    # ax2.legend(handles=handles, labels=title,fontsize=8, bbox_to_anchor=(0.1, 1.02))
    
def lat():
    df_area = df.copy()

    # lat = pd.Series(np.arange(-89.997916666558, 90, 0.00416666688397527))
    lat = pd.Series((np.arange(-90, 90, 0.01)).round(2))
    
    lat_area = df_area.groupby('lat')['Area'].sum().div(1e6)
    lat_Sb = df_area.groupby('lat')['Sbedrock'].mean()
    lat_area_df = lat_area.reindex(lat, fill_value=0)
    lat_Sb_df = lat_Sb.reindex(lat, fill_value=0)
    
    print(lat_area.index)
    print(lat_area_df.index)
    print(lat_area_df)
    print(lat_Sb_df)
    fig = plt.figure(figsize=(6, 2), dpi=500)
    gs = GridSpec(1, 1)
    ax = fig.add_subplot(gs[:, :])
    
    plot_line(["Area ($km^2$)","$S_{{bedrock}}$ (mm)"], ax, lat_area_df.index, lat_area_df, lat_Sb_df, color = ["#153aab","#fdcf41"])

    plt.tight_layout()
    plt.savefig(f"{fig_path}/l2_lat.png",dpi=500, bbox_inches='tight')

def lon():
    df_area = df.copy()

    # lon = pd.Series(np.arange(-179.997916666558, 180, 0.00416666688397527))
    lon = pd.Series((np.arange(-180, 180, 0.01)).round(2))
    lon_area = df_area.groupby('lon')['Area'].sum().div(1e6)
    lon_Sb = df_area.groupby('lon')['Sbedrock'].mean()
    lon_area_df = lon_area.reindex(lon, fill_value=0)
    lon_Sb_df = lon_Sb.reindex(lon, fill_value=0)

    fig = plt.figure(figsize=(12, 2), dpi=500)
    gs = GridSpec(1, 1)
    ax = fig.add_subplot(gs[:, :])
    
    plot_line(["Area ($km^2$)","$S_{{bedrock}}$ (mm)"], ax, lon_area_df.index, lon_area_df, lon_Sb_df, color = ["#153aab","#fdcf41"])


    plt.tight_layout()
    plt.savefig(f"{fig_path}/l2_lon.png",dpi=500, bbox_inches='tight')
    

    
    
lat()
lon()