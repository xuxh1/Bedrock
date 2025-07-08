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

path = os.getcwd()+'/'
print("当前文件路径:", path)

path1 = '/tera11/zhwei/students/Xionghui/data/'
os.chdir(path1)

# ---------------------------------------------------------------------------------- Calculate mask1,2,3,all -------------------------------------------------------------------------------------------------
# -------------------------------- mask1 ------------------------------------------------
def mask1():
    dir_path = path1+' mask1/mask1_v2/'
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)
    # os.system(f'ln -sf {dir_path}Pelletier/upland_hillslope_soil_remap_cm.nc {dir_path}upland_hillslope_soil_remap_cm.nc')
    os.system(f'cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}500.txt upland_hillslope_soil_remap_cm.nc DTB_temp1.nc')
    os.system(f'cdo -setrtoc2,0,150,1,nan DTB_temp1.nc mask1.nc')
    print("mask1_v3已完成")
# -------------------------------- mask1 ------------------------------------------------

# -------------------------------- mask all ------------------------------------------------
def mask():
    dir_path = path1+' mask/mask_v2/'
    mask1_path = path1+' mask1/mask1_v2/'
    mask2_path = path1+' mask2/'
    mask3_path = path1+' mask3/'
    os.makedirs(dir_path, exist_ok=True)
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
    dir_path = path1+' mask1/mask1_v2/'
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)
    image = xr.open_dataset(f'DTB_temp1.nc')
    s = image['Band1']
    print(s.min(),s.max())
    
    layer = [0, 5, 15, 30, 60, 100, 150]
    for i in range(6):
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
    # dir_path2 = path1+' mask1/mask1_v2/'
    dir_path = path1+' Ssoil/Ssoil_v2/'
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)

    layer = [0, 5, 15, 30, 60, 100, 150]
    layer_depth_mm = [50, 100, 150, 300, 400, 500]
    # for i in range(1,7):
    #     os.system(f"cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}500.txt pawl{i+1}.nc pawl{i+1}_500.nc")
    #     os.system(f"cdo -mulc,{layer_depth_mm[i]} pawl{i+1}_500.nc pawl{i+1}_mul.nc")
        
    # for i in range(1,6):
    #     if i==1:
    #         os.system(f'cdo add pawl{i}_mul.nc pawl{i+1}_mul.nc pawl{i+1}_mulp.nc')
    #     else:
    #         os.system(f'cdo add pawl{i+1}_mul.nc pawl{i}_mulp.nc pawl{i+1}_mulp.nc')
    
    for i in range(1,7):
        os.system(f'ln -sf {dir_path}../pawl{i}_500.nc {dir_path}pawl{i}_500.nc')
        if i != 6:
            os.system(f'ln -sf {dir_path}../pawl{i}_mulp.nc {dir_path}pawl{i}_mulp.nc')
       
    for i in range(6):
        # 将500m分辨率的每层数据乘于该层的基岩深度，基岩深度属于该层留下，不属于该层基岩则替换为0
        print(f"cdo -mul pawl{i+1}_500.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}.nc pawl{i+1}_mul_mask.nc")
        os.system(f"cdo -mul pawl{i+1}_500.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}.nc pawl{i+1}_mul_mask.nc")
        
    for i in range(1,6):    
        # mask每层（除本层外）的累计土壤水数据,第一层为他本身，基岩深度属于该层留下，其余则替换为0
        print(f"cdo -mul pawl{i}_mulp.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}_mask.nc pawl{i+1}_mulp_mask.nc")
        os.system(f"cdo -mul pawl{i}_mulp.nc {dir_path2}DTB_{layer[i]}_{layer[i+1]}_mask.nc pawl{i+1}_mulp_mask.nc")
        
        print(f"cdo -add pawl{i+1}_mul_mask.nc pawl{i+1}_mulp_mask.nc pawl{i+1}_mulpp_mask.nc")
        os.system(f"cdo -add pawl{i+1}_mul_mask.nc pawl{i+1}_mulp_mask.nc pawl{i+1}_mulpp_mask.nc")
        
    for i in range(1,6):
        if i==1:
            os.system(f'cdo add pawl{i}_mul_mask.nc pawl{i+1}_mulpp_mask.nc pawl{i+1}_mulpp.nc')
        else:
            os.system(f'cdo add pawl{i}_mulpp.nc pawl{i+1}_mulpp_mask.nc pawl{i+1}_mulpp.nc')
            
    os.system(f'cp pawl6_mulpp.nc Ssoil.nc')
    print("Ssoil.nc已完成")
# -------------------------------- calculate Ssoil ------------------------------------------------
# ---------------------------------------------------------------------------------- Calculate Ssoil -------------------------------------------------------------------------------------------------
    
def change_DTB():
    # mask1()
    # mask()
    Ssoil()
    
if __name__ =='__main__':
    change_DTB()
