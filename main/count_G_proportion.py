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

resolution     = config.resolution
name           = config.name
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

dir_man = DirMan(data_path)
dir_man.enter()

@timer
def count_G_proportion():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('Sbedrock', 'Sr'),
        ('mask123', 'Band1'),

        ('Dbedrock_Frequency', 'Dr'),
        ('Proportion/Proportion1', 'Sr'),
        ('Proportion/Proportion2_median', 'Sr'),
        ('Proportion/Proportion3_median', 'tp'),
        ('Proportion/Proportion4_median', 'et'),
        ('Proportion/Proportion5_median', 'Sr'),
        ('Proportion/Proportion6_median', 'et'),
        ('Proportion/Proportion7_median', 'Band1')
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

    with open('csv/Global_proportion.csv','w') as f:
        df.to_csv(f)

if __name__=='__main__':
    count_G_proportion()
