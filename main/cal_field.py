import rioxarray as rxr
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
import os

path = os.getcwd()+'/'
print("当前文件路径:", path)

def fDTB():
    file_path1 = '/tera11/zhwei/students/Xionghui/data/mask1/BDTICM_M_1km_ll.tif'
    file_path2 = '/tera11/zhwei/students/Xionghui/data/DTB/gNATSGO/Bedrock_US_gNATSGO_90m-1.tif'
    file_path3 = '/tera11/zhwei/students/Xionghui/data/DTB/gNATSGO/Bedrock_US_gNATSGO_90m-6.tif'
    file_path4 = '/tera11/zhwei/students/Xionghui/data/DTB/Soilgrids_Iowa/DTB_temp3.nc'
    csv_file1 = '/tera11/zhwei/students/Xionghui/data/field/DTB/new_literature_compilation.csv'
    csv_file2 = '/tera11/zhwei/students/Xionghui/data/field/DTB/DTB1.csv'
    csv_file3 = '/tera11/zhwei/students/Xionghui/data/field/DTB/DTB2.csv'

    s1 = rxr.open_rasterio(file_path1)
    s2 = rxr.open_rasterio(file_path2)
    s3 = rxr.open_rasterio(file_path3)
    s4 = xr.open_dataset(file_path4)
    csv1 = pd.read_csv(csv_file1, encoding='latin-1')
    csv2 = pd.read_csv(csv_file2, encoding='latin-1')

    lat2 = csv1['Latitude']
    lon2 = csv1['Longitude']
    sd = csv1['SoilDepth_Numberline_cm']
    ssa = csv1['Same Site As']
    fc2 = csv1['Full Citation']
    ci2 = csv1['Citation'] 
    nf2 = csv1['Number_For_Plotting']


    a1 = csv2['gNATSGO']
    a2 = csv2['SoilGrids250m']
    a3 = csv2['SoilGrids250m_rev']
    
    # 副本以免修改原始数据
    csv_copy = csv2.copy()

    j = 0
    for i in range(len()):
        if sd[i] > 0 and not isinstance(ssa[i], str) and lat2[i] != lat2[i + 1] and lon2[i] <= -66.9 and lon2[i] >= -125 and lat2[i] >= 24.4 and lat2[i] <= 49.4:
            # 更新副本中的数据
            csv_copy.at[j, 'SoilDepth_Numberline_cm'] = sd[i]
            csv_copy.at[j, 'lat'] = lat2[i]
            csv_copy.at[j, 'lon'] = lon2[i]
            csv_copy.at[j, 'Full Citation'] = fc2[i]
            csv_copy.at[j, 'Citation'] = ci2[i]
            csv_copy.at[j, 'Number_For_Plotting'] = j + 1
            j += 1

    lat = csv_copy['lat']
    lon = csv_copy['lon']

    for i in range(j):
        lat1_index = abs(s1.coords['y'] - lat[i]).argmin()
        lon1_index = abs(s1.coords['x'] - lon[i]).argmin()
        lat2_index = abs(s2.coords['y'] - lat[i]).argmin()
        lon2_index = abs(s2.coords['x'] - lon[i]).argmin()
        lat3_index = abs(s3.coords['y'] - lat[i]).argmin()
        lon3_index = abs(s3.coords['x'] - lon[i]).argmin()
        lat4_index = abs(s4.coords['lat'] - lat[i]).argmin()
        lon4_index = abs(s4.coords['lon'] - lon[i]).argmin()

        a1_value = s1[0, lat1_index, lon1_index].values
        a2_value = s2[0, lat2_index, lon2_index].values
        a3_value = s3[0, lat3_index, lon3_index].values
        a4_value = s4['Band1'][lat4_index, lon4_index].values


        a1[i] = a1_value
        if a2_value >= 0:
            a2[i] = a2_value
        else:
            a2[i] = a3_value
        a3[i] = a4_value
        
    csv_copy['SoilGrids250m'] = a1
    csv_copy['gNATSGO'] = a2
    csv_copy['SoilGrids250m_rev'] = a3

    csv_copy.to_csv(csv_file3, index=False)

    print("更新后的CSV文件:")
    print(csv_copy)

def fSb():
    file_path1 = 'Ssoil.nc'
    file_path2 = 'Sbedrock.nc'
    csv_file1 = '/tera11/zhwei/students/Xionghui/data/field/Sbedrock/literature_compilation.csv'
    csv_file2 = '/tera11/zhwei/students/Xionghui/data/field/Sbedrock/Sbedrock_new1.csv'
    csv_file3 = '/tera11/zhwei/students/Xionghui/data/field/Sbedrock/Sbedrock_new2.csv'

    s1 = xr.open_dataset(file_path1)
    s2 = xr.open_dataset(file_path2)
    csv1 = pd.read_csv(csv_file1, encoding='latin-1')
    csv2 = pd.read_csv(csv_file2, encoding='latin-1')

    lat2 = csv1['Latitude']
    lon2 = csv1['Longitude']
    min = csv1['Minimum']
    max = csv1['Maximum']
    ssa = csv1['Same Site As']
    fc2 = csv1['Full Citation']
    ci2 = csv1['Citation'] 
    nf2 = csv1['Number_For_Plotting']


    a1 = csv2['S_soil_mm']
    a2 = csv2['Sbedrock']
    # a3 = csv2['Minimum']
    # a4 = csv2['Maximum']
    
    # 副本以免修改原始数据
    csv_copy = csv2.copy()

    j = 0
    for i in range(80):
        if isinstance(nf2[i], str) and not isinstance(ssa[i], str):
            # 更新副本中的数据
            csv_copy.at[j, 'lat'] = lat2[i]
            csv_copy.at[j, 'lon'] = lon2[i]
            csv_copy.at[j, 'Full Citation'] = fc2[i]
            csv_copy.at[j, 'Citation'] = ci2[i]
            csv_copy.at[j, 'Minimum'] = min[i]
            csv_copy.at[j, 'Maximum'] = max[i]
            
            csv_copy.at[j, 'Number_For_Plotting'] = j + 1
            j += 1

    print(j)
    lat = csv_copy['lat']
    lon = csv_copy['lon']

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

    csv_copy['S_soil_mm'] = a1
    csv_copy['Sbedrock'] = a2

    csv_copy.to_csv(csv_file3, index=False)

    print("更新后的CSV文件:")
    print(csv_copy)
    
fDTB()
fSb()
