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

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/csv', exist_ok=True)

def site():
    df = pd.read_csv(f'{post_data_path}/field/field_all.csv', encoding='latin-1')

    # dir_man = DirMan(data_path)
    # dir_man.enter()

    s1 = nc.Dataset('Sbedrock_tmp2.nc4', 'r')
    s2 = nc.Dataset('Ssoil.nc4', 'r')
    s3 = nc.Dataset('DTB.nc4', 'r')
    s4 = nc.Dataset('mask1.nc4', 'r')
    s5 = nc.Dataset('mask2.nc4', 'r')
    s6 = nc.Dataset('mask3.nc4', 'r')
    s7 = nc.Dataset('mask123.nc4', 'r')

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
            # print('-----------------------------------------------')
            
            lat1_index = np.argmin(np.abs(lat1 - lat[i]))
            lon1_index = np.argmin(np.abs(lon1 - lon[i]))
            lat1_target = lat1[lat1_index]
            lon1_target = lon1[lon1_index]
            # print(lat[i])
            # print(lon[i])
            # print('find ')
            # print(lat1_target)
            # print(lon1_target)
            # print('-----------------------------------------------')
            
            df2.loc[j, 'Measure'] = df.loc[i, 'Measurement or Estimate of RM Contribution to ET?']
            df2.loc[j, 'lat'] = lat[i]
            df2.loc[j, 'lon'] = lon[i]
            df2.loc[j, 'Sbedrock_field_min'] = df.loc[i, 'Minimum']
            df2.loc[j, 'Sbedrock_field_max'] = df.loc[i, 'Maximum']
            df2.loc[j, 'Sbedrock'] = s1['Sbedrock'][lat1_index,lon1_index]
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
    with open('csv/site.csv','w') as f:
        df3.to_csv(f)
        
    print(df3)

def DTB():
    file_path1 = f'{post_data_path}mask1/mask1_v1/BDTICM_M_1km_ll.tif'
    file_path2 = f'{post_data_path}DTB/gNATSGO/Bedrock_US_gNATSGO_90m-1.tif'
    file_path3 = f'{post_data_path}DTB/gNATSGO/Bedrock_US_gNATSGO_90m-6.tif'
    file_path4 = f'{post_data_path}mask1/mask1_v1/DTB_temp3.nc'
    file_path5 = f'{post_data_path}mask1/mask1_v3/DTB_temp1.nc'
    csv_file1 = f'{post_data_path}field/field_all.csv'
    csv_file2 = f'{data_path}csv/DTB.csv'

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

if __name__=='__main__':
    site()
    DTB()