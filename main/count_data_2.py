import os
import numpy as np
import xarray as xr
import pandas as pd
import netCDF4 as nc
import geopandas as gpd
import rioxarray as rxr
from myfunc import timer
from myfunc import DirMan
import config

resolution     = config.resolution
name           = config.name
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

def load_and_flatten_data(file_name, variable_name, index=None):
    with nc.Dataset(f"{file_name}.nc") as dataset:
        if index is not None:
            data = dataset[variable_name][index, :, :].flatten()
        else:
            data = dataset[variable_name][:, :].flatten()
    return data

def count_G_statistics():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('Sbedrock', 'Sr'),
        ('mask123', 'Band1'),
        ('Area', 'area'),
        ('IGBP', 'LC', 0),
        ('Koppen', 'Band1'),
        ('Aboveground', 'Band1'),
        ('Belowground', 'Band1')
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
    
    print(f"the sum area is {df['Area'].sum()/(1e12)}")
    print(f"the sum aboveground is {df['Aboveground'].sum()}")
    print(f"the sum belowground is {df['Belowground'].sum()}")

    df = df.dropna()
    df = df[df['Sbedrock'] > 0]
    df = df[df['mask123'] == 1]
    
    print(f"after mask, the left sum area is {df['Area'].sum()/(1e12)}")
    print(f"after mask, the left sum aboveground is {df['Aboveground'].sum()}")
    print(f"after mask, the left sum belowground is {df['Belowground'].sum()}")

    with open('Global_statistics.csv','w') as f:
        df.to_csv(f)

def count_G_partition():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('Sbedrock', 'Sr'),
        ('mask123', 'Band1'),
        ('DTB', 'Band1'),
        ('ET', 'et', 0),
        ('PR', 'tp', 0),
        ('Q','tp', 0),
        ('LH','Ee'),
        ('FY','FD'),
        ('FM_mean','FD')
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

    df = df.dropna()
    df = df[df['Sbedrock'] > 0]
    df = df[df['mask123'] == 1]
    
    with open('Global_partition.csv','w') as f:
        df.to_csv(f)

@timer
def count_data():
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    count_G_statistics()
    count_G_partition()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

if __name__=='__main__':
    count_data()