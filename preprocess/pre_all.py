import os
import xarray as xr
import numpy as np
import netCDF4 as nc
import shutil
import subprocess
from math import radians, sin
from pyproj import Geod
from shapely.geometry import Point, LineString, Polygon
import glob
from joblib import Parallel, delayed
from tqdm import tqdm, trange
import sys
sys.path.append('/home/xuxh22/anaconda3/lib/mylib/')
from myfunc import timer
import math

path1 = '/tera11/zhwei/students/Xionghui/data/'
os.chdir(path1)

# ---------------------------------------------------------------------------------- Calculate mask1,2,3,all -------------------------------------------------------------------------------------------------
# -------------------------------- mask1 ------------------------------------------------
def mask1():
    dir_path = path1+'mask1/mask1_v3/'
    os.chdir(dir_path)
    os.system(f'cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}500.txt average_soil_and_sedimentary-deposit_thickness_remap_cm.nc DTB_temp1.nc')
    os.system(f'cdo -setrtoc2,0,150,1,nan DTB_temp1.nc mask1.nc')
    print("mask1_v2已完成")
# -------------------------------- mask1 ------------------------------------------------


# -------------------------------- mask2 ------------------------------------------------
def mask2():
    dir_path = path1+'mask2/'
    os.chdir(dir_path)
    os.system(f'cp /stu01/linwy20/LCdata/MODIS/global_igbp_15s_2020.nc {dir_path}/global_igbp_15s_2020.nc')
    os.system('cdo -invertlat global_igbp_15s_2020.nc mask2_temp1.nc')
    # setrtoc2无法正确修改数据
    os.system('cdo -setrtoc2,1,9,1,nan mask2_temp1.nc mask2.nc')
    print("mask2已完成")
# -------------------------------- mask2 ------------------------------------------------


# -------------------------------- mask3 ------------------------------------------------
def mask3():
    dir_path = path1+'mask3/'
    os.chdir(dir_path)
    os.system(f"cdo timsum {path1}diff.nc reduce.nc")
    os.system(f'cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}500.txt reduce.nc mask3_temp1.nc')
    os.system(f"cdo -setrtoc2,-inf,0,1,nan mask3_temp1.nc mask3.nc")
    print("mask3已完成")
# -------------------------------- mask3 ------------------------------------------------


# -------------------------------- mask all ------------------------------------------------
def mask():
    dir_path = path1+'mask/mask_v3/'
    mask1_path = path1+'mask1/mask1_v3/'
    mask2_path = path1+'mask2/'
    mask3_path = path1+'mask3/'
    os.chdir(dir_path)
    subprocess.run(f"cdo mul {mask1_path}mask1.nc {mask2_path}mask2.nc mask12.nc", shell=True, check=True)
    subprocess.run(f"cdo mul mask12.nc {mask3_path}mask3.nc mask123_temp1.nc", shell=True, check=True)
    os.system(f"cdo -setrtoc2,1,1,1,nan mask123_temp1.nc mask123.nc")
    os.system('rm mask123_temp1.nc')
# -------------------------------- mask all ------------------------------------------------
# ---------------------------------------------------------------------------------- Calculate mask1,2,3,all -------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------- Calculate Ssoil -------------------------------------------------------------------------------------------------
# -------------------------------- DTB layer ------------------------------------------------
def DTB_layer():
    dir_path = path1+'mask1/mask1_v3/'
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)
    image = xr.open_dataset(f'DTB_temp1.nc')
    s = image['Band1']
    print(s.min(),s.max())
    
    layer = [0, 5, 15, 30, 60, 100, 150, float('inf')]
    for i in range(7):
        s1 = np.where((s>layer[i]) & (s<=layer[i+1]), (s-layer[i])*10, 0)
        print(s1.min(),s1.max())
        
        shutil.copyfile('DTB_temp1.nc', f'DTB_{layer[i]}_{layer[i+1]}.nc')
        with nc.Dataset(f'DTB_{layer[i]}_{layer[i+1]}.nc', 'a') as file:
            s_var = file.variables['Band1']
            new_s_data = s1 
            s_var[:,:] = new_s_data
            
        s1 = np.where((s>layer[i]) & (s<=layer[i+1]), 1, 0)
        print(s1.min(),s1.max())
        
        shutil.copyfile('DTB_temp1.nc', f'DTB_{layer[i]}_{layer[i+1]}_mask.nc')
        with nc.Dataset(f'DTB_{layer[i]}_{layer[i+1]}_mask.nc', 'a') as file:
            s_var = file.variables['Band1']
            new_s_data = s1 
            s_var[:,:] = new_s_data
            
    return dir_path
# -------------------------------- DTB layer ------------------------------------------------


# -------------------------------- calculate Ssoil ------------------------------------------------
def Ssoil():
    dir_path2 = DTB_layer()
    dir_path = path1+'Ssoil/Ssoil_v3/'
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)

    layer = [0, 5, 15, 30, 60, 100, 150, float('inf')]
    layer_depth_mm = [50, 100, 150, 300, 400, 500]

    for i in range(6):
        os.system(f'ln -sf {dir_path}../pawl{i}_500.nc {dir_path}pawl{i}_500.nc')
        os.system(f"cdo -mulc,{layer_depth_mm[i]} pawl{i}_500.nc pawl{i}_500_mm.nc")
        
        filelistname = ' '.join(f'pawl{j}_500_mm.nc' for j in range(i+1))
        os.system(f'cdo enssum {filelistname} pawl{i}_500_mm_sum.nc')

        # 将500m分辨率的每层数据乘于该层的基岩深度，基岩深度属于该层留下，不属于该层基岩则替换为0
        os.system(f"cdo -mul pawl{i}_500.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}.nc pawl{i}_500_mm_mask.nc")
    
    
    for i in range(1,6):    
        # mask每层（除本层外）的累计土壤水数据,第一层为他本身,最后一层只有累计值，基岩深度属于该层留下，其余则替换为0，这里mask为下一层的分布范围
        os.system(f"cdo -mul pawl{i-1}_500_mm_sum.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}_mask.nc pawl{i}_500_mm_sum_mask.nc")
        
        os.system(f"cdo -add pawl{i}_500_mm_mask.nc pawl{i}_500_mm_sum_mask.nc pawl{i}_all_mask.nc")
        
    os.system(f"cdo -mul pawl{6-1}_500_mm_sum.nc {dir_path2}DTB_{layer[6]}_{layer[6+1]}_mask.nc pawl{6}_500_mm_sum_mask.nc")
    os.system(f'cp pawl{0}_500_mm_mask.nc pawl{0}_500_mm_sum_mask.nc')

    filelistname = ' '.join(f'pawl{i}_500_mm_sum_mask.nc' for i in range(7))
    os.system(f'cdo enssum {filelistname} Ssoil.nc')
    
    print("Ssoil_v3.nc已完成")
# -------------------------------- calculate Ssoil ------------------------------------------------
# ---------------------------------------------------------------------------------- Calculate Ssoil -------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------- Snow Cover -------------------------------------------------------------------------------------------------
def SnowCover():
    os.system('python a_pre_SC.py')
    dir_path = path1+'SC/'
    os.chdir(dir_path)
    # 积雪分数应保持和计算Sr、Dr的数据diff_3.nc相同分辨率，从0.05°为0.1°
    os.system(f'cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}0p1.txt SnowCover_0p05.nc SnowCover_0p1.nc')
    os.system('cdo -setmisstoc,1 -setrtoc2,10,100,0,1 SnowCover_0p1.nc SnowCover_0p1_mask.nc')
    print("SnowCover已完成")
# ---------------------------------------------------------------------------------- Snow Cover -------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------- IGBP Koppen Area -------------------------------------------------------------------------------------------------
def IGBP_Koppen():
    dir_path = path1+'IGBP/'
    os.chdir(dir_path)
    os.system(f'cp /stu01/linwy20/LCdata/MODIS/global_igbp_15s_2020.nc {dir_path}/global_igbp_15s_2020.nc')
    os.system(f"cdo -b I32 -P 12 --no_remap_weights remaplaf,{path1}500.txt global_igbp_15s_2020.nc IGBP.nc")
    print("IGBP已完成")

    dir_path = path1+'Koppen/'
    os.chdir(dir_path)
    os.system("gdal_translate -of netCDF -a_srs EPSG:4326 Beck_KG_V1_present_0p0083.tif Koppen_1km.nc")
    os.system(f"cdo -b I32 -P 12 --no_remap_weights remaplaf,{path1}500.txt Koppen_1km.nc Koppen.nc")
    print("Koppen已完成")

def count_area(lat1,lat2):
    lat1,lat2 = map(radians,[lat1,lat2])
    r = 6.37122e6
    # dlon = 0.00416666688397527
    dlon = 0.1
    dlon_rad = math.radians(dlon)
    area = abs(r**2 * dlon_rad * (sin(lat2)-sin(lat1)))
    # print(area)
    return area

def area():
    dir_path = path1+'Area/'
    os.chdir(dir_path)
    # data = xr.open_dataset(f'{path1}mask1/mask1_v3/mask1.nc')
    data = xr.open_dataset(f'{path1}diff/diff.nc')
    
    lat = data['lat']
    lon = data['lon']
    # inc = 0.00416666688397527
    inc = 0.1
    lat1 = lat-inc/2
    lat2 = lat+inc/2    
    grid1,grid2 = np.meshgrid(lon, lat)
    area = np.zeros_like(grid1)
    result = Parallel(n_jobs=3)(delayed(count_area)(lat1[i], lat2[i]) for i in range(len(lat)))
    for i in range(len(lat)):
        area[i, :] = result[i]
        print(area[i,0])
    print(f'地球总面积为：{np.sum(area):.3f} $m^2$')
            
    output_ds = xr.Dataset({'area': (('lat', 'lon'), area)},
                        coords={'lat': data['lat'], 'lon': data['lon']})
    output_ds.to_netcdf('Area_0p1.nc')
    print(area)
    print(f'地球总面积为：{np.sum(area)/1e12:.3f} 百万$km^2$')
    # output_ds.to_netcdf('Area.nc')
    print("Area已完成")
# ---------------------------------------------------------------------------------- IGBP Koppen Area -------------------------------------------------------------------------------------------------

def DTB():
    #Iowa实测数据，该数据由上官老师给出
    dir_path = path1+'/DTB/Iowa/'
    os.chdir(dir_path)
    os.system('gdal_translate -of netCDF -a_srs EPSG:4326 Iowa.tif Iowa.nc')
    
    #将处理好的Soilgrids数据cp过来
    dir_path = path1+'/DTB/Soilgrids/'
    os.chdir(dir_path)
    os.system(f'ln -sf {dir_path}../../mask1/DTB_temp2.nc {dir_path}DTB_temp2.nc')
    
    #将处理好的Soilgrids根据Iowa实测修正的数据cp过来
    dir_path = path1+'/DTB/Soilgrids_Iowa/'
    os.chdir(dir_path)
    os.system(f'ln -sf {dir_path}../../mask1/DTB_temp3.nc {dir_path}DTB_temp3.nc')
    
    #由GEE输出的gNATSGO基岩数据，其中2包含Iowa地区
    dir_path = path1+'/DTB/gNATSGO/'
    os.chdir(dir_path)
    for i in range(8):
        os.system(f'gdal_translate -of netCDF -a_srs EPSG:4326 Bedrock_US_gNATSGO_90m-{i+1}.tif Bedrock_US_gNATSGO_90m-{i+1}.nc')
    
if __name__ =='__main__':
    # mask1()
    # mask2()
    # mask3()
    # mask()
    
    # Ssoil()
    # SnowCover()
    
    # IGBP_Koppen()
    area()
    
    # DTB()