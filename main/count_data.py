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

# Collect the global calculated data
def count_G():
    df = pd.DataFrame()

    with nc.Dataset('Sbedrock.nc') as dataset:
        lat = dataset['lat'][:].flatten()
        lon = dataset['lon'][:].flatten()
        df['lat'] = np.repeat(lat, len(lon))
        df['lon'] = np.tile(lon, len(lat))

    file_variable_list = [
        ('Sbedrock', 'Sr'),
        ('mask123', 'Band1'),

        ('Sr', 'Sr'),
        ('Ssoil', 'Band1'),
        ('Proportion1', 'Sr'),
        ('Proportion2', 'Sr'),
        ('Proportion3', 'tp', 0)
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
    
    shp1 = gpd.read_file(shp_path+'continent/continent.shp')
    shp2 = gpd.read_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

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

    with open('Global.csv','w') as f:
        df.to_csv(f)
        
    df1 = df[df['Sovereignt_short'] == 'USA']
    print(df1)

    with open('US.csv','w') as f:
        df1.to_csv(f)

# Reprocessing US statistical data(note:Save and reopen to remove zero values)
# from Sovereignt to state, based on the previous function
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

# Collect various data(global calculated data) at actual measurement sites
def count_site():
    df = pd.read_csv(f'{post_data_path}/field/new_literature_compilation.csv', encoding='latin-1')

    s1 = nc.Dataset('Sbedrock_temp1.nc', 'r')
    s2 = nc.Dataset('Ssoil.nc', 'r')
    s3 = nc.Dataset('DTB.nc', 'r')
    s4 = nc.Dataset('mask1.nc', 'r')
    s5 = nc.Dataset('mask2.nc', 'r')
    s6 = nc.Dataset('mask3.nc', 'r')
    s7 = nc.Dataset('mask123.nc', 'r')

    lat = df['Latitude']
    lon = df['Longitude']
    ssa = df['Same Site As']
    # print(lat,lon)

    lat1 = s1.variables['lat'][:]
    lon1 = s1.variables['lon'][:]
    # print(lat1,lon1)

    df2 = pd.DataFrame()
    j = 0
    for i in range(len(lat)):
        if not isinstance(ssa[i], str):
            print('-----------------------------------------------')
            
            lat1_index = np.argmin(np.abs(lat1 - lat[i]))
            lon1_index = np.argmin(np.abs(lon1 - lon[i]))
            lat1_target = lat1[lat1_index]
            lon1_target = lon1[lon1_index]
            print(lat[i])
            print(lon[i])
            print('find ')
            print(lat1_target)
            print(lon1_target)
            print('-----------------------------------------------')
            
            df2.loc[j, 'Measure'] = df.loc[i, 'Measurement or Estimate of RM Contribution to ET?']
            df2.loc[j, 'lat'] = lat[i]
            df2.loc[j, 'lon'] = lon[i]
            df2.loc[j, 'Sbedrock_field_min'] = df.loc[i, 'Minimum']
            df2.loc[j, 'Sbedrock_field_max'] = df.loc[i, 'Maximum']
            df2.loc[j, 'Sbedrock'] = s1['Sr'][lat1_index,lon1_index]
            df2.loc[j, 'Ssoil'] = s2['Band1'][lat1_index,lon1_index]
            df2.loc[j, 'Soil_depth'] = df.loc[i, 'SoilDepth_Numberline_cm']
            df2.loc[j, 'DTB'] = s3['Band1'][lat1_index,lon1_index]
            df2.loc[j, 'mask1'] = s4['Band1'][lat1_index,lon1_index]
            df2.loc[j, 'mask2'] = s5['LC'][0,lat1_index,lon1_index]
            df2.loc[j, 'mask3'] = s6['et'][0,lat1_index,lon1_index]
            df2.loc[j, 'mask'] = s7['Band1'][lat1_index,lon1_index]
            
            j += 1

    df3 = df2.groupby(['lat', 'lon']).first().reset_index()
    # df3.fillna(0, inplace=True)
    df3['num'] = range(len(df3['lat']))
    with open('site.csv','w') as f:
        df3.to_csv(f)
        
    print(df3)

# Collect the field DTB from 5 different data
# (Field,gNATSGO,SoilGrids250m,SoilGrids250m_rev,Pelletier)
def count_fDTB():
    file_path1 = f'{post_data_path}mask1/mask1_v1/BDTICM_M_1km_ll.tif'
    file_path2 = f'{post_data_path}DTB/gNATSGO/Bedrock_US_gNATSGO_90m-1.tif'
    file_path3 = f'{post_data_path}DTB/gNATSGO/Bedrock_US_gNATSGO_90m-6.tif'
    file_path4 = f'{post_data_path}mask1/mask1_v1/DTB_temp3.nc'
    file_path5 = f'{post_data_path}mask1/mask1_v3/DTB_temp1.nc'
    csv_file1 = f'{post_data_path}field/DTB/new_literature_compilation.csv'
    csv_file2 = f'{data_path}DTB.csv'

    s1 = rxr.open_rasterio(file_path1)
    s2 = rxr.open_rasterio(file_path2)
    s3 = rxr.open_rasterio(file_path3)
    s4 = xr.open_dataset(file_path4)
    s5 = xr.open_dataset(file_path5)
    csv1 = pd.read_csv(csv_file1, encoding='latin-1')

    lat2 = csv1['Latitude']
    lon2 = csv1['Longitude']
    sd = csv1['SoilDepth_Numberline_cm']
    ssa = csv1['Same Site As']

    # Set the DTB.csv
    csv2 = {
        'number':[],
        'lat':[],
        'lon':[],
        'Field':[],
        'gNATSGO':[],
        'SoilGrids250m':[],
        'SoilGrids250m_rev':[],
        'Pelletier':[]
    }
    csv2 = pd.DataFrame(csv2)

    a1 = csv2['gNATSGO']
    a2 = csv2['SoilGrids250m']
    a3 = csv2['SoilGrids250m_rev']
    a4 = csv2['Pelletier']

    # Renew the csv data in field
    j = 0
    for i in range(len(sd)):
        if sd[i] > 0 and not isinstance(ssa[i], str) and lat2[i] != lat2[i + 1] and lon2[i] <= -66.9 and lon2[i] >= -125 and lat2[i] >= 24.4 and lat2[i] <= 49.4:
            csv2.at[j, 'Field'] = sd[i]
            csv2.at[j, 'lat'] = lat2[i]
            csv2.at[j, 'lon'] = lon2[i]
            csv2.at[j, 'number'] = int(j + 1)
            j += 1
            print(j)

    # Index the corresponding location points in global data
    lat = csv2['lat']
    lon = csv2['lon']
    for i in range(j):
        lat1_index = abs(s1.coords['y'] - lat[i]).argmin()
        lon1_index = abs(s1.coords['x'] - lon[i]).argmin()
        lat2_index = abs(s2.coords['y'] - lat[i]).argmin()
        lon2_index = abs(s2.coords['x'] - lon[i]).argmin()
        lat3_index = abs(s3.coords['y'] - lat[i]).argmin()
        lon3_index = abs(s3.coords['x'] - lon[i]).argmin()
        lat4_index = abs(s4.coords['lat'] - lat[i]).argmin()
        lon4_index = abs(s4.coords['lon'] - lon[i]).argmin()
        lat5_index = abs(s5.coords['lat'] - lat[i]).argmin()
        lon5_index = abs(s5.coords['lon'] - lon[i]).argmin()

        a1_value = s1[0, lat1_index, lon1_index].values
        a2_value = s2[0, lat2_index, lon2_index].values
        a3_value = s3[0, lat3_index, lon3_index].values
        a4_value = s4['Band1'][lat4_index, lon4_index].values
        a5_value = s5['Band1'][lat5_index, lon5_index].values

        a1[i] = a1_value
        if a2_value >= 0:
            a2[i] = a2_value
        else:
            a2[i] = a3_value
        a3[i] = a4_value
        a4[i] = a5_value

    csv2['SoilGrids250m'] = a1
    csv2['gNATSGO'] = a2
    csv2['SoilGrids250m_rev'] = a3
    csv2['Pelletier'] = a4

    csv2.to_csv(csv_file2, index=False)

    print("the new DTB.csv is:")
    print(csv2)

# Collect the field Sbedrock from 3 different data
# (Field min/max,Ssoil,Sbedrock)
def count_fSb():
    file_path1 = f'{data_path}Ssoil.nc'
    file_path2 = f'{data_path}Sbedrock.nc'
    csv_file1 = f'{post_data_path}field/Sbedrock/new_literature_compilation.csv'
    csv_file2 = f'{data_path}Sbedrock.csv'

    s1 = xr.open_dataset(file_path1)
    s2 = xr.open_dataset(file_path2)
    csv1 = pd.read_csv(csv_file1, encoding='latin-1')

    lat2 = csv1['Latitude']
    lon2 = csv1['Longitude']
    min = csv1['Minimum']
    max = csv1['Maximum']
    ssa = csv1['Same Site As']
    nf =  csv1['Number_For_Plotting']

    # Set the Sbedrock.csv
    csv2 = {
        'number':[],
        'lat':[],
        'lon':[],
        'min':[],
        'max':[],
        'Ssoil':[],
        'Sbedrock':[]
    }
    csv2 = pd.DataFrame(csv2)

    a1 = csv2['Ssoil']
    a2 = csv2['Sbedrock']

    # Renew the csv data in field
    j = 0
    for i in range(len(lat2)):
        if isinstance(nf[i], str) and not isinstance(ssa[i], str):
            csv2.at[j, 'lat'] = lat2[i]
            csv2.at[j, 'lon'] = lon2[i]
            csv2.at[j, 'min'] = min[i]
            csv2.at[j, 'max'] = max[i]
            csv2.at[j, 'number'] = int(j + 1)
            j += 1
            print(j)

    # Index the corresponding location points in global data
    lat = csv2['lat']
    lon = csv2['lon']
    for i in range(j):
        lat1_index = abs(s1.coords['lat'] - lat[i]).argmin()
        lon1_index = abs(s1.coords['lon'] - lon[i]).argmin()
        lat2_index = abs(s2['lat'] - lat[i]).argmin()
        lon2_index = abs(s2['lon'] - lon[i]).argmin()

        a1_value = s1['Band1'][lat1_index, lon1_index].values
        a2_value = s2['Sr'][lat2_index, lon2_index].values

        a1[i] = a1_value
        a2[i] = a2_value
        print('the Ssoil is',a1[i])
        print('the Sbedrock is',a2[i])

    csv2['Ssoil'] = a1
    csv2['Sbedrock'] = a2

    csv2.to_csv(csv_file2, index=False)

    print("the new Sbedrock.csv is:")
    print(csv2)

@timer
def count_data():
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)
    
    count_G()
    count_US()
    count_site()
    count_fDTB()
    count_fSb()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

if __name__=='__main__':
    count_data()