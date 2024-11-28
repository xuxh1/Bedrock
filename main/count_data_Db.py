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

def count_G_Db():
    df = pd.DataFrame()

    with nc.Dataset('Dbedrock_2003.nc') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))
    
    with nc.Dataset('mask123.nc') as dataset:
        mask = dataset['Band1'][:,:].flatten()
        df['mask123'] = mask

    for year in range(2003, 2021):
        # Construct the filename dynamically using the current year
        filename = f'Dbedrock_{year}.nc'
        
        df1 = df.copy()
        # Open the netCDF file and read the 'Dr' variable
        with nc.Dataset(filename) as dataset:
            data = dataset['Dr'][:,:].flatten()  # Flatten the 2D array into 1D
            
            # Append the flattened data to the data_list
            df1[f'Dbedrock_{year}'] = data
    
        df1 = df1[df1['mask123'] == 1].dropna()        
        df1 = df1.reset_index(drop=True)
        df1.to_csv(f'Global_Db_{year}.csv', index=False)

@timer
def count_data():
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    count_G_Db()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

if __name__=='__main__':
    count_data()