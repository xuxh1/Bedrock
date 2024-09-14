import os
import cmaps
import salem
import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import geopandas as gpd
from pylab import rcParams
from math import radians, sin
from shapely.geometry import box
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
name = config.name
region = config.region
data_path = config.data_path
shp_path = config.shp_path
fig_path = config.fig_path

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

def count_G():
    lat = nc.Dataset(f'Sbedrock.nc')['lat'][:].flatten()
    lon = nc.Dataset(f'Sbedrock.nc')['lon'][:].flatten()
    latf = np.repeat(lat, len(lon))
    lonf = np.tile(lon, len(lat))

    area = nc.Dataset(f'Area.nc')['area'][:,:].flatten()
    lc = nc.Dataset(f'IGBP.nc')['LC'][0,:,:].flatten()
    ct = nc.Dataset(f'Koppen.nc')['Band1'][:,:].flatten()


    dtb = nc.Dataset(f'DTB.nc')['Band1'][:,:].flatten()
    et = nc.Dataset(f'ET.nc')['et'][0,:,:].flatten()
    pr = nc.Dataset(f'PR.nc')['tp'][0,:,:].flatten()
    ag = nc.Dataset(f'Aboveground.nc')['Band1'][:,:].flatten()
    bg = nc.Dataset(f'Belowground.nc')['Band1'][:,:].flatten()
    
    s = nc.Dataset(f'Sbedrock.nc')['Sr'][:,:].flatten()
    s1 = nc.Dataset(f'Sr.nc')['Sr'][:,:].flatten()
    s2 = nc.Dataset(f'Ssoil.nc')['Band1'][:,:].flatten()
    s3 = nc.Dataset(f'Proportion1.nc')['Sr'][:,:].flatten()
    shp1 = gpd.read_file(shp_path+'continent/continent.shp')
    shp2 = gpd.read_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

    df = pd.DataFrame()
    df['lat'] = latf
    df['lon'] = lonf
    df['Area'] = area

    df['Landcover'] = lc.astype(int)
    df['Koppen'] = ct.astype(int)

    df['DTB'] = dtb
    df['ET'] = et
    df['PR'] = pr
    df['Aboveground'] = ag
    df['Belowground'] = bg

    df['Sbedrock'] = s
    df['Sr'] = s1
    df['Ssoil'] = s2
    df['Proportion1'] = s3
    
    print(df['Aboveground'].sum())
    print(df['Belowground'].sum())
    print(df['Area'].sum()/(1e12))
    
    df = df.dropna()
    df = df[df['Sbedrock'] > 0]
    df = df[df['Landcover']<10]
    df = df[df['Landcover']>0]
    df = df[df['Koppen'] != 0]
    
    print(df['Aboveground'].sum())
    print(df['Belowground'].sum())
    
    df = df.reset_index(drop=True)
    gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']), crs='EPSG:4326')
    result1 = gpd.sjoin(gdf_points, shp1, how='left', predicate='within')
    result2 = gpd.sjoin(gdf_points, shp2, how='left', predicate='within')

    df['Continent'] = result1['CONTINENT']
    df['Subregion'] = result2['SUBREGION']
    df['Sovereignt'] = result2['SOVEREIGNT']
    
    list1 = ['Asia','South America','Africa','Europe','North America','Oceania','Antarctica','Seven seas (open ocean)']
    list2 = ['AS','SA','AF','EU','NA','OC','AN','Seven seas (open ocean)']
    mapping = dict(zip(list1, list2))
    
    df['Continent_short'] = df['Continent'].map(mapping)

    list1 = ['South America','Australia and New Zealand','Southern Africa','Eastern Africa','Melanesia',
             'Western Europe','Polynesia','Middle Africa','South-Eastern Asia','Western Africa','Southern Asia',
             'Central America','Northern Africa', 'Caribbean', 'Western Asia', 'Eastern Asia','Northern America',
             'Southern Europe', 'Central Asia', 'Eastern Europe','Northern Europe']
    
    list2 = ['SA','ANZ','SAF','EAF','MEL',
             'WEU','Polynesias','MAF','SEA','WAF','SAS',
             'CAM','NAF','CAR','WAS','EAS','NA',
             'SEU','CAS','EEU','NEU']
    mapping = dict(zip(list1, list2))
    
    df['Subregion_short'] = df['Subregion'].map(mapping)
    df['Sovereignt_short'] = result2['ISO_A3']

    print(df['Area'].sum()/(1e12))

    df1 = df[df['DTB'] <= 150]
    print(df1['Area'].sum()/(1e12)) 
    
    df1 = df1[df1['Landcover']<10]
    df1 = df1[df1['Landcover']>0]   
    print(df1['Area'].sum()/(1e12)) 
       
    # df1 = df[df['Koppen'] != 0]
    # print(df1.groupby('Continent')['Area'].sum().div(1e12))
    # print(df1.groupby('Continent')['Area'].sum().sum()/(1e12))

    
    # df1 = df1[df1['Sbedrock']>=0]
    # print(df1.groupby('Continent')['Area'].sum().div(1e12))
    # print(df1.groupby('Continent')['Area'].sum().sum()/(1e12))
    

    # exit(0)
    with open('Global.csv','w') as f:
        df.to_csv(f)
        
    df1 = df[df['Sovereignt_short'] == 'USA']
    print(df1)

    with open('US.csv','w') as f:
        df1.to_csv(f)
    
# Reprocessing US statistical data(note:Save and reopen to remove zero values)
# from Sovereignt to state
def count_US():
    df = pd.read_csv('US.csv')
    print(df)

    shp = gpd.read_file(shp_path+'US/USA_adm1.shp')

    print(shp)

    gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']), crs='EPSG:4326')
    result1 = gpd.sjoin(gdf_points, shp, how='left', predicate='within')

    df['State'] = result1['NAME_1']

    print(df)

    with open('US.csv','w') as f:
        df.to_csv(f)

@timer
def count_data():
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)
    
    count_G()
    count_US()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    count_data()