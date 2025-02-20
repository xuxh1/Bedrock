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
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/csv', exist_ok=True)

def Global_S():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Sr', 'Sr'),
        ('Ssoil', 'Band1'),
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
    df.drop(labels='mask123',axis=1,inplace=True)

    with open('csv/Global_S.csv','w') as f:
        df.to_csv(f)
    
def Global_DF():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Dbedrock_Frequency', 'Dbedrock')
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
    # df = df[df['Sbedrock'] > 0]
    df = df[df['mask123'] == 1]
    df.drop(labels='mask123',axis=1,inplace=True)


    with open('csv/Global_DF.csv','w') as f:
        df.to_csv(f)

def Global_FDFMFY():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),

        ('S_FD', 'FD'),
        ('S_FY', 'FD'),
        ('D_FD_median', 'FD'),
        ('D_FM_median', 'FD'),
        ('Area', 'area')
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
    df.drop(labels='mask123',axis=1,inplace=True)

    print(df.groupby('S_FY')['Area'].sum()/1e12)
    print(df['Area'].sum()/1e12)
    df.drop(labels='Area',axis=1,inplace=True)

    with open('csv/Global_FDFMFY.csv','w') as f:
        df.to_csv(f)

def Global_index():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Dbedrock_Frequency', 'Dbedrock'),
        ('Area','area'),
        
        ('P/Sbedrock_div_Sr', 'Sbedrock'),
        ('P/Sbedrock_div_ET_mean', 'Sbedrock'),
        ('P/Sbedrock_div_PR_mean', 'Sbedrock'),
        ('P/ET_mean_div_PR_mean', 'et'),
        ('P/ET_mean_sub_Sbedrock_div_PR_mean', 'et'),
        ('P/Q_mean_div_PR_mean', 'tp'),
        ('P/PET_div_PR_mean', 'Band1')
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
    df = df[df['mask123'] == 1]
    df.drop(labels='mask123',axis=1,inplace=True)

    df = df[df['Sbedrock'] > 0]
    print(df.groupby('Dbedrock_Frequency')['Area'].sum()/1e12)
    print(df['Area'].sum()/1e12)
    # df.drop(labels='Sbedrock',axis=1,inplace=True)
    df.drop(labels='Area',axis=1,inplace=True)

    with open('csv/Global_index.csv','w') as f:
        df.to_csv(f)

def Global_Db():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Area','area'),

        ('Dbedrock_median', 'Dbedrock'),
        ('D/Dbedrock_2011', 'Dbedrock'),
        ('D/Dbedrock_2014', 'Dbedrock'),
        ('D/Dbedrock_2015', 'Dbedrock'),
        ('D/Dbedrock_2017', 'Dbedrock')
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
    # df = df[df['Sbedrock'] > 0]
    df = df[df['mask123'] == 1]
    df.drop(labels='mask123',axis=1,inplace=True)

    df = df[df['Sbedrock'] > 0]
    print(df.groupby('mask123')['Area'].sum()/1e12)
    print(df['Area'].sum()/1e12)
    df.drop(labels='Sbedrock',axis=1,inplace=True)
    df.drop(labels='Area',axis=1,inplace=True)

    with open('csv/Global_Db.csv','w') as f:
        df.to_csv(f)

def Global_igbp_koppen():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Area', 'area'),
        ('Koppen', 'Band1'),
        ('IGBP', 'LC', 0),
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
    df['Area'] = df['Area']/1e10
    df = df[df['Sbedrock'] > 0]
    df = df[df['mask123'] == 1]
    df.drop(labels='mask123',axis=1,inplace=True)
    # df.drop(labels='Sbedrock',axis=1,inplace=True)
    print(df['Area'].sum())
    df.drop(labels='Area',axis=1,inplace=True)



    with open('csv/Global_igbp_koppen.csv','w') as f:
        df.to_csv(f)

def Global_statistics():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Area', 'area'),

        ('Koppen', 'Band1'),
        ('IGBP', 'LC', 0),
        ('Aboveground', 'Band1'),
        ('Belowground', 'Band1'),
        ('DTB', 'Band1'),
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
    df.drop(labels='mask123',axis=1,inplace=True)
    df.drop(labels='Sbedrock',axis=1,inplace=True)

    print(df['Area'].sum())
    df.drop(labels='Area',axis=1,inplace=True)

    with open('csv/Global_statistics.csv','w') as f:
        df.to_csv(f)

def Global_DTB():
    df = pd.DataFrame()

    with nc.Dataset('mask123.nc4') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('mask123', 'Band1'),
        ('Sbedrock', 'Sbedrock'),
        ('Area', 'area'),

        ('DTB', 'Band1'),
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
    df.drop(labels='mask123',axis=1,inplace=True)
    df.drop(labels='Sbedrock',axis=1,inplace=True)

    print(df['Area'].sum()/1e12)
    df.drop(labels='Area',axis=1,inplace=True)

    with open('csv/Global_DTB.csv','w') as f:
        df.to_csv(f)

if __name__=='__main__':
    Global_S()
    Global_FDFMFY()
    Global_igbp_koppen()
    Global_Db()
    Global_DF()
    Global_DTB()
    Global_index()
    Global_statistics()
