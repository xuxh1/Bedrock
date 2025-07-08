import os
import numpy as np
import xarray as xr
import pandas as pd
import netCDF4 as nc
import geopandas as gpd
import rioxarray as rxr
from myfunc import timer
from myfunc import DirMan
from myfunc import load_and_flatten_data
import config

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# configuration
# resolution = "0p1"
resolution = "500"
region = [-180,180,-60,90]
data_path = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}/'
post_data_path = '/tera04/zhwei/xionghui/bedrock/'
shp_path = '/tera04/zhwei/xionghui/bedrock/Shp/'
fig_path = f'/home/xuxh22/stu01/Bedrock/fig/{resolution}/'
path = '/home/xuxh22/stu01/Bedrock/'
if resolution == "0p1":
    size = 0.1
elif resolution == "500":
    size = 0.0005

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/csv', exist_ok=True)

def Global():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        # ('Sbedrock', 'Sbedrock'),
        # ('Sr', 'Sr'),

        ('Sbedrock', 'Band1'),
        ('PR_mean', 'tp', 0),
        ('ET_mean', 'et', 0),
        # ('Dbedrock_Frequency', 'Band1'),
        ('Dbedrock_Frequency', 'Dbedrock'),
        ('Sr', 'Band1'),
        # ('Ssoil', 'Band1'),
        ('mask1234', 'Band1'),
        ('Area', 'area'),
        ('Koppen', 'Band1'),
        ('IGBP', 'LC', 0),
    ]

    for entry in file_variable_list:
        file = entry[0]
        variable_name = entry[1]  
        index = entry[2:] if len(entry) > 2 else None  
        if index:
            df[file] = load_and_flatten_data(file, variable_name, index[0])
        else:
            df[file] = load_and_flatten_data(file, variable_name)

    # df = df.dropna()
    # df = df[df['Sbedrock'] > 0]
    df = df[df['mask1234'] == 1]

    df.drop(labels='mask1234',axis=1,inplace=True)

    # df['Area'] = df['Area'].sum()/(1e12)

    shp1 = gpd.read_file(shp_path+'continent/continent.shp')
    shp2 = gpd.read_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

    df = df.reset_index(drop=True)
    gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']), crs='EPSG:4326')
    result1 = gpd.sjoin(gdf_points, shp1, how='left', predicate='within')
    result2 = gpd.sjoin(gdf_points, shp2, how='left', predicate='within')

    df['Continent'] = result1['CONTINENT']
    df['Subregion'] = result2['SUBREGION']
    df['Sovereignt'] = result2['SOVEREIGNT']

    df['Continent'] = df['Continent'].replace('Australia', 'Oceania')

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

    with open('csv/Global.csv','w') as f:
        df.to_csv(f)

    df1 = df[df['Sovereignt_short'] == 'USA']

    with open('csv/US.csv','w') as f:
        df1.to_csv(f)

Global()    