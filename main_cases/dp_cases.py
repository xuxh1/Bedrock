import os
import shutil
import subprocess
import numpy as np
import xarray as xr
import netCDF4 as nc
from tqdm import tqdm, trange
from joblib import Parallel, delayed
from myfunc import timer
from myfunc import DirMan
import config
import calendar

resolution = config.resolution
data_path = config.data_path

dir_man = DirMan(data_path)
dir_man.enter()


def dp_Sr_mean(path):
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'{path}/Sr_{year}_tmp1.nc4'
        name_list = name_list+' '+name
    output_file = f'{path}Sr_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}Sr_mean_tmp1.nc4 {path}Sr_mean_tmp2.nc4", shell=True, check=True)
    os.system(f"cdo mul {path}Sr_mean_tmp2.nc4 mask123.nc4 {path}Sr_mean.nc4")

# def dp_Sr_mean(path):
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'{path}/tmp/Sr_{year}_tmp2.nc4'
#         name_list = name_list+' '+name
#     output_file = f'{path}Sr_mean_tmp1.nc4'
#     print(name_list+' '+output_file)
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}Sr_mean_tmp1.nc4 {path}Sr_mean_tmp2.nc4", shell=True, check=True)
#     os.system(f"cdo mul {path}Sr_mean_tmp2.nc4 mask123.nc4 {path}Sr_mean.nc4")

# def dp_PSr_mean(path):
#     name_list = 'cdo -O -ensmean '
#     for year in range(2003,2021):
#         name = f'{path}/tmp/PSr_{year}_tmp2.nc4'
#         name_list = name_list+' '+name
#     output_file = f'{path}PSr_mean_tmp1.nc4'
#     print(name_list+' '+output_file)
#     os.system(name_list+' '+output_file)

#     subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}PSr_mean_tmp1.nc4 {path}PSr_mean_tmp2.nc4", shell=True, check=True)
#     os.system(f"cdo mul {path}PSr_mean_tmp2.nc4 mask123.nc4 {path}PSr_mean.nc4")

casename_list = ['bedrock_1','bedrock_2','bedrock_3']
for casename in casename_list[:2]:
    path = f'{data_path}/cases/{casename}/'
    os.makedirs(path+'/tmp', exist_ok=True)
    dp_Sr_mean(path)
    # dp_Sr_mean(path)
    # dp_PSr_mean(path)