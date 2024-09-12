# plot_field_Depth_to_Bedrock.py

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

path = os.getcwd()+'/'
print("当前文件路径:", path)

path = '/tera11/zhwei/students/Xionghui/data/field/DTB/'
roots = pd.read_csv(f'{path}DTB2.csv', encoding='latin-1')

def fDTB():
    barplot = pd.DataFrame()
    barplot = roots[['Citation','Number_For_Plotting','SoilDepth_Numberline_cm','SoilGrids250m','gNATSGO','SoilGrids250m_rev']].copy()
    #barplot = barplot.dropna()
    barplot['Name'] = (barplot['Number_For_Plotting']).astype(str) # make name column string

    barplot = barplot[0:20]
    barplot = barplot.sort_values(by = 'Number_For_Plotting')
    barplot = barplot.dropna()
    print(barplot)

    # Make labels for X-axis to have accurate Ssoil and Dbedrock meanings
    # soillabels = list(np.arange(150, -50, step=-50))
    dlabels = list(np.arange(0, 1600, step=200))
    # labels = soillabels + dlabels
    labels = dlabels

    # Plot figure
    plt.figure(figsize = (3, 2.5), dpi=300)
    #plt.barh(barplot['Name'],barplot['Mean_D_bedrock_mm'], xerr = barplot['Stdev_D_bedrock_mm'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['SoilGrids250m'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['SoilGrids250m_rev'], color = '#91755a',alpha=0.5)

    plt.plot(barplot['SoilDepth_Numberline_cm'],barplot['Name'], 'o', ms=5, markerfacecolor="black", markeredgecolor='black', markeredgewidth=0.5)
    plt.plot(barplot['gNATSGO'],barplot['Name'],'o', ms=5, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.5)

    # plt.xticks(np.arange(-150, 2050, step=50), labels = labels)
    plt.xticks(np.arange(0, 1600, step=200), labels = labels)

    # plt.xlim(-150, 2000)
    plt.xlim(0, 1400)
    plt.gca().invert_yaxis()
    plt.xticks(rotation=90)
    plt.tight_layout()

    ## Uncomment for downloading fig
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig("fig/p_fDTB.pdf", transparent=True)
    # files.download("doublebar.pdf")
    
path = '/tera11/zhwei/students/Xionghui/data/field/Sbedrock/'
roots = pd.read_csv(f'{path}Sbedrock_new2.csv', encoding='latin-1')
print(roots)

def fSb():
    ## Extract Columns for Barplot (NOTE: Must exclude first header row manually)
    barplot = pd.DataFrame()
    barplot = roots[['Citation','Number_For_Plotting','Minimum','Maximum','S_soil_mm','Sbedrock']].copy()
    print(barplot)
    #barplot = barplot.dropna()
    barplot['S_soil_mm'] = barplot['S_soil_mm'] * -1
    barplot['Name'] = (barplot['Number_For_Plotting']).astype(str) # make name column string

    barplot = barplot[0:20]
    barplot = barplot.sort_values(by = 'Number_For_Plotting')
    # barplot = barplot.dropna()
    print(barplot)

    # Make labels for X-axis to have accurate Ssoil and Dbedrock meanings
    soillabels = list(np.arange(300, -100, step=-100))
    dlabels = list(np.arange(100, 600, step=100))
    labels = soillabels + dlabels

    # Plot figure
    plt.figure(figsize = (3, 2.5), dpi=300)
    #plt.barh(barplot['Name'],barplot['Mean_D_bedrock_mm'], xerr = barplot['Stdev_D_bedrock_mm'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['S_soil_mm'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['Sbedrock'], color = '#91755a',alpha=0.5)

    plt.plot(barplot['Minimum'],barplot['Name'], 'o', ms=5, markerfacecolor="black", markeredgecolor='black', markeredgewidth=0.5)
    plt.plot(barplot['Maximum'],barplot['Name'],'o', ms=5, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.5)

    # plt.xticks(np.arange(-150, 2050, step=50), labels = labels)
    # plt.xticks(np.arange(0, 1600, step=200), labels = labels)

    plt.xticks(np.arange(-300, 600, step=100), labels = labels)
    plt.xlim(-300, 500)
    plt.gca().invert_yaxis()
    plt.xticks(rotation=90)
    plt.tight_layout()

    ## Uncomment for downloading fig
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig("fig/p_fSb.pdf", transparent=True)
    
fDTB()
fSb()
