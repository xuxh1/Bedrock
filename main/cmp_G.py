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

# area_sum = 19.925158940748766

def DF():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Sbedrock', 'Sbedrock'),
        # ('Dbedrock_Frequency', 'Dbedrock'),

        ('Sbedrock', 'Band1'),
        ('Dbedrock_Frequency', 'Band1'),

        ('Area','area'),
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


    area_sum = df['Area'].sum()/1e12

    # df = df.dropna()
    # numeric_columns = df.select_dtypes(include=['float32']).columns
    # df[numeric_columns] = df[numeric_columns].round(1)

    df = df[df['mask1234'] == 1]
    # df['Dbedrock_Frequency'] = df['Dbedrock_Frequency'].round().astype(int)
    area_DF_sum = df['Area'].sum()/1e12

    d_f = (df.groupby('Dbedrock_Frequency')['Area'].sum()/1e12)

    print(area_sum)
    print(area_DF_sum)
    print(d_f)
    print(d_f/area_DF_sum)

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_DF.csv','w') as f:
        df.to_csv(f)


def biome():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Sbedrock', 'Sbedrock'),
        ('Sbedrock', 'Band1'),
        ('Area', 'area'),

        ('Aboveground', 'Band1'),
        ('Belowground', 'Band1'),
    ]

    for entry in file_variable_list:
        file = entry[0]
        variable_name = entry[1]  
        index = entry[2:] if len(entry) > 2 else None  
        if index:
            df[file] = load_and_flatten_data(file, variable_name, index[0])
        else:
            df[file] = load_and_flatten_data(file, variable_name)

    df['Aboveground_sum'] = df['Aboveground']*df['Area']
    df['Belowground_sum'] = df['Belowground']*df['Area']

    ag_sum = df['Aboveground_sum'].sum()
    bg_sum = df['Belowground_sum'].sum()

    # df = df.dropna()
    df = df[df['mask1234'] == 1]

    ag_mask = df['Aboveground_sum'].sum()
    bg_mask = df['Belowground_sum'].sum()

    print(ag_mask/ag_sum)
    print(bg_mask/bg_sum)

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_biome.csv','w') as f:
        df.to_csv(f)

def PR():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        ('Sbedrock', 'Band1'),
        ('Sr', 'Band1'),
        ('Dbedrock_Frequency', 'Band1'),
        # ('Sbedrock', 'Sbedrock'),
        # ('Sr', 'Sr'),
        ('PR_mean', 'tp', 0),
        ('ET_mean', 'et', 0),

        ('Area','area')
    ]

    for entry in file_variable_list:
        file = entry[0]
        variable_name = entry[1]  
        index = entry[2:] if len(entry) > 2 else None  

        # print(f"File: {file}, Variable: {variable_name}, Index: {index}")
        if index:
            df[file] = load_and_flatten_data(file, variable_name, index[0])
        else:
            df[file] = load_and_flatten_data(file, variable_name)

    # df = df.dropna()
    numeric_columns = df.select_dtypes(include=['float32']).columns
    df[numeric_columns] = df[numeric_columns].round(1)

    df = df[df['mask1234'] == 1]
    with open('csv/Global_PR.csv','w') as f:
        df.to_csv(f)

if __name__ == '__main__':
    DF()
    # biome()
    PR()