# plot_LandCover_ClimateType.py

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

# font = {'family': 'Times New Roman'}
# matplotlib.rc('font', **font)

# params = {'backend': 'ps',
#           'axes.labelsize': 25,
#           'grid.linewidth': 0.2,
#           'font.size': 25,
#           'legend.fontsize': 18,
#           'legend.frameon': False,
#           'xtick.labelsize': 30,
#           'xtick.direction': 'out',
#           'ytick.labelsize': 30,
#           'ytick.direction': 'out',
#           'legend.handlelength': 1,
#           'legend.handleheight': 1,
#           'savefig.bbox': 'tight',
#           'axes.unicode_minus': False,
#           "mathtext.default":"regular",
#           'text.usetex': False}
# rcParams.update(params)

df = pd.read_csv('LC.csv')

def koppen():
    ## group together Koppen first and second letter groups
    df_Koppen = df.copy()
    df_Koppen = df_Koppen[df_Koppen['Koppen'] > 0]
    df_Koppen = df_Koppen[df_Koppen['Koppen'] < 29]
    df_Koppen['Koppen_Together'] = df_Koppen['Koppen'].replace(to_replace=[5, 7, 9, 10, 12, 13, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28], value=[4, 6, 8, 8, 11, 11, 14, 14, 17, 17, 17, 21, 21, 21, 25, 25, 25])

    # Grouped first and second letters of koppen climate types:
    #5 to 4
    #7 to 6
    #9, 10 to 8
    #13, 12 to 11
    #16, 15 to 14
    #20, 19, 18 to 17
    #24, 23, 22 to 21
    #28, 27, 26 to 25
    #29 alone

    ## Check that no Koppen groups have less than 200km area
    print('Area of each group (km^2):')
    # Remove 2 and 3
    # df_Koppen = df_Koppen[df_Koppen['Koppen_Together'] > 3]
    # df_Koppen = df_Koppen[df_Koppen['Koppen_Together'] != 21]
    
    print(df_Koppen.groupby('Koppen_Together')['Area'].sum())


    ## Check that no landcover groups have less than 2km area
    df_landcover = df.copy()
    #Remove landcover 3 = Deciduous needleleaf forest
    df_landcover = df_landcover[df_landcover['Landcover'] < 10]
    df_landcover = df_landcover[df_landcover['Landcover'] > 0]
    # df_landcover = df_landcover[df_landcover['Landcover'] != 3]
    
    print(df_landcover.groupby('Landcover')['Area'].sum())
    
    print(df_Koppen.groupby('Koppen_Together')['Area'].count())
    print(df_landcover.groupby('Landcover')['Area'].count())

    
    # Setup dataframe with all Koppen Groups, Values, and Colors
    KoppenColor = ['#0000FE','#0077FF','#46A9FA','#FE0000','#FE9695','#F5A301','#FFDB63','#FDFD45','#C6C700','#96FF96','#63C764','#329633','#C6FF4E','#66FF33','#33C701','#FF00FE','#C600C7','#963295','#966495','#ABB1FF','#5A77DB','#4C51B5','#320087','#18DCDC','#38C7FF','#007E7D','#00455E','#B2B2B2','#686868']
    KoppenList = ['Tropical Rainforest (Af)','Tropical Monsoon (Am)','Tropical Savanna (Aw)','Desert (BWh)','Arid (BWk)','Semi Arid (BSh)','Semi Arid (BSk)','Mediterranean (Csa)','Mediterranean (Csb)','Mediterranean (Csc)','Humid Subtropical (Cwa)','Oceanic (Cwb)','Ocanic (Cwc)','Humid Subtropical (Cfa)','Oceanic (Cfb)','Oceanic (Cfc)','Humid Continental (Dsa)','Humid Continental (Dsb)','Subarctic (Dsc)','Subarctic (Dsd)','Humid Continental (Dwa)','Humid Continental (Dwb)','Subarctic (Dwc)','Subarctic (Dwd)','Humid Continental (Dfa)','Humid Continental (Dfb)','Subarctic (Dfc)','Subarctic (Dfd)','Tundra (ET)']
    KoppenList_short = ['Tropical Rainforest (Af)','Tropical Monsoon (Am)','Tropical Savanna (Aw)','Desert & Arid (BW)','Arid (BWk)','Semi Arid (BS)','Semi Arid (BSk)','Mediterranean (Cs)','Mediterranean (Csb)','Mediterranean (Csc)','Humid Subtropical &\nOceanic (Cw)','Oceanic (Cwb)','Ocanic (Cwc)','Humid Subtropical &\nOceanic (Cf)','Oceanic (Cfb)','Oceanic (Cfc)','Humid Continental &\nSubarctic (Ds)','Humid Continental (Dsb)','Subarctic (Dsc)','Subarctic (Dsd)','Humid Continental &\nSubarctic (Dw)','Humid Continental (Dw)','Subarctic (Dwc)','Subarctic (Dwd)','Humid Continental &\nSubarctic (Df)','Humid Continental (Dfb)','Subarctic (Dfc)','Subarctic (Dfd)','Tundra (ET)']

    KoppenColors = pd.DataFrame()
    KoppenColors['color'] = KoppenColor
    KoppenColors['name'] = KoppenList_short
    KoppenColors['number'] = np.arange(1,30, step = 1)
    print(KoppenColors)
    
    # Filter Koppen data and aesthetics by group for plotting:
    koppen_ids = df_Koppen['Koppen_Together'].unique()
    aesthetics = KoppenColors[KoppenColors.number.isin(koppen_ids)]
    print(aesthetics)
    print(aesthetics['color'].tolist())
    cmap = colors.ListedColormap(aesthetics['color'].tolist())
    
    # set font size
    #plt.rc('xtick', labelsize=16) 
    #plt.rc('ytick', labelsize=16) 

    # set figure size
    f, ax = plt.subplots(figsize=(6, 4), dpi=300) 

    # seaborn 0.13.0
    # seaborn 0.13.2

    sns.boxplot(x="Koppen_Together", y="Sbedrock", hue = "Koppen_Together", data=df_Koppen, width=.6, linewidth = .7, palette=cmap, whis = 1.5, showfliers = False)
    plt.legend().set_visible(False)
    #sns.boxplot(x="Koppen_Together", y="Sbedrock", data=plotdf, width=.6,whis = 0, showfliers = False)
    # Tweak the visual presentation
    plt.xticks(np.arange(0, 11, step=1), labels = aesthetics['name'],rotation = 'vertical') # rotation='25', ha="right"
    ax.yaxis.grid(True)
    #ax.set_title('Köppen Climate Type')
    ax.set_axisbelow(True)
    #ax.set_xlabel(labels)
    ax.set_ylim(0, 600)
    ax.set_xlabel("")
    ax.set_ylabel("")
    #ax.set_ylabel('$S_{bedrock}$ (mm)')

    # Uncomment to download fig:
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig("fig/p_LCK.pdf", transparent=True, bbox_inches='tight')
    # plt.savefig('p_LCK.png', transparent=True, bbox_inches='tight')
    # files.download("koppen_boxes.pdf") 
    
    #   ___________________________________________landcover______________________________________
    lcoi = ['Evergreen Needleleaf\nForests','Evergreen Broadleaf\nForests','Deciduous Needleleaf\nForests','Deciduous Broadleaf\nForests','Mixed Forests','Closed Shrublands','Open Shrublands','Woody Savannas','Savannas','Grasslands']
    qgis_colors = ['#f8de85', '#FAC13E','#a5537f','#a52653','#c04a02','#A4B381','#52B33F','#74B3B8','#B183B8','#7846A8']
    landcoverList = ['Evergreen Needleleaf\nForests', 'Evergreen Broadleaf\nForests', 'Deciduous Needleleaf\nForests', 'Deciduous Broadleaf\nForests', 'Mixed Forests', 'Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 'Savannas', 'Grasslands', 'Permanent Wetlands', 'Croplands', 'Urban and Built-up Lands', 'Cropland/Natural Vegetation Mosaics', 'Permanent Snow and Ice', 'Barren', 'Water Bodies']
    land_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    land_aes = pd.DataFrame()
    land_aes['name'] = lcoi
    land_aes['number'] = land_numbers
    land_aes['color'] = qgis_colors

    # Filter Koppen data and aesthetics by group for plotting:
    landcover_ids = df_landcover['Landcover'].unique()
    land_aesthetics = land_aes[land_aes.number.isin(landcover_ids)]
    print(land_aesthetics)
    print(aesthetics['color'].tolist())
    cmap = colors.ListedColormap(land_aesthetics['color'].tolist())
    
    # Set fig size
    f, ax = plt.subplots(figsize=(6, 4),dpi=300)

    sns.boxplot(x="Landcover", y="Sbedrock", data=df_landcover, hue = "Landcover", width=.6, linewidth = .7, palette = cmap, whis = 1.5, showfliers = False)
    plt.legend().set_visible(False)
    plt.xticks(np.arange(0, 9, step=1), labels = land_aesthetics['name'], rotation = 'vertical') # rotation='25', ha="right"


    # Tweak the visual presentation
    plt.xticks(rotation='vertical')
    ax.set_axisbelow(True)
    #ax.set_title('Biome')
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.yaxis.grid(True)
    ax.set_ylim(0, 600)
    #ax.set_ylabel('$S_{bedrock}$ (mm)')

    # Uncomment to download fig:
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig("fig/p_LCI.pdf", transparent=True, bbox_inches='tight')
    # plt.savefig('p_LCI.png', transparent=True, bbox_inches='tight')
    # files.download("biome_boxes.pdf") 

koppen()