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

def D_frequency_per_year():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Dbedrock_Frequency', 'Dbedrock'),
        ('Dbedrock_Frequency', 'Band1'),

        # ('D_frequency_per_year_mean','Frequency'),
        # ('D_frequency_per_year_max','Frequency'),

        ('D_frequency_per_year_mean','Band1'),
        ('D_frequency_per_year_max','Band1'),
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
    df = df[df['mask1234'] == 1]

    print(df['D_frequency_per_year_mean'].mean())
    print(df['D_frequency_per_year_max'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_frequency_per_year_mean'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_frequency_per_year_max'].mean())

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_D_frequency_per_year.csv','w') as f:
        df.to_csv(f)

def D_sum():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Dbedrock_Frequency', 'Dbedrock'),
        ('Dbedrock_Frequency', 'Band1'),

        # ('D_sum_frequency', 'Frequency'),
        # ('D_sum_duration', 'Duration'),

        ('D_sum_frequency', 'Band1'),
        ('D_sum_duration', 'Band1'),
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
    df = df[df['mask1234'] == 1]

    print(df['D_sum_frequency'].mean())
    print(df['D_sum_duration'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_sum_frequency'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_sum_duration'].mean())

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_D_sum.csv','w') as f:
        df.to_csv(f)

def D_duration_per_year():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Dbedrock_Frequency', 'Dbedrock'),
        ('Dbedrock_Frequency', 'Band1'),

        # ('D_duration_per_year_max', 'Duration'),
        # ('D_duration_per_year_mean', 'Duration'),

        ('D_duration_per_year_max', 'Band1'),
        ('D_duration_per_year_mean', 'Band1'),
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
    df = df[df['mask1234'] == 1]

    print(df['D_duration_per_year_max'].mean())
    print(df['D_duration_per_year_mean'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_duration_per_year_max'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_duration_per_year_mean'].mean())

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_D_duration_per_year.csv','w') as f:
        df.to_csv(f)

def D_duration_per_use():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Dbedrock_Frequency', 'Dbedrock'),
        ('Dbedrock_Frequency', 'Band1'),

        # ('D_duration_per_use_max', 'Duration'),
        # ('D_duration_per_use_mean', 'Duration'),

        ('D_duration_per_use_max', 'Band1'),
        ('D_duration_per_use_mean', 'Band1'),
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
    df = df[df['mask1234'] == 1]

    print(df['D_duration_per_use_max'].mean())
    print(df['D_duration_per_use_mean'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_duration_per_use_max'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_duration_per_use_mean'].mean())

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_D_duration_per_use.csv','w') as f:
        df.to_csv(f)

def D_first_day():
    df = pd.DataFrame()

    with nc.Dataset('mask1234.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask1234', 'Band1'),
        # ('Dbedrock_Frequency', 'Dbedrock'),
        ('Dbedrock_Frequency', 'Band1'),

        # ('D_first_day_min', 'First_Day'),
        # ('D_first_day_max_sub_min', 'First_Day'),

        ('D_first_day_min', 'Band1'),
        ('D_first_day_max_sub_min', 'Band1'),
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
    df = df[df['mask1234'] == 1]

    print(df['D_first_day_min'].mean())
    print(df['D_first_day_max_sub_min'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_first_day_min'].mean())
    print(df.groupby('Dbedrock_Frequency')['D_first_day_max_sub_min'].mean())

    df.drop(labels='mask1234',axis=1,inplace=True)
    with open('csv/Global_D_first_day.csv','w') as f:
        df.to_csv(f)

if __name__ == '__main__':
    D_frequency_per_year()
    D_sum()
    D_duration_per_year()
    D_duration_per_use()
    D_first_day()