# count_LandCover_ClimateType.py
# 待更新
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

def mkdir():
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
    s3 = nc.Dataset(f'Sproportion.nc')['Sr'][:,:].flatten()

    shp_path = '/home/xuxh22/stu01/Bedrock/data/Shp/continent/'
    shp1 = gpd.read_file(shp_path+'continent.shp')
    shp_path   =  '/home/xuxh22/stu01/Bedrock/data/Shp/World_CN/'
    shp2 = gpd.read_file(shp_path+'ne_10m_admin_0_countries_chn.shp')

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
    df['Sproportion'] = s3
    
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
    with open('region3.csv','w') as f:
        df.to_csv(f)
        
    df1 = df[df['Sovereignt_short'] == 'USA']
    print(df1)

    with open('US.csv','w') as f:
        df1.to_csv(f)
    
        
mkdir()
# def add():
#     df = pd.read_csv('your_file.csv')

#     new_column_data = [1, 2, 3, 4, 5]  
#     df['new_column'] = new_column_data

#     # 保存修改后的CSV文件
#     df.to_csv('new_file.csv', index=False)