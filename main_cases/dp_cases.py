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

def dp_Ssoil_mean(path):
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'{path}/Ssoil_{year}_tmp1.nc4'
        name_list = name_list+' '+name
    output_file = f'{path}Ssoil_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}Ssoil_mean_tmp1.nc4 {path}Ssoil_mean_tmp2.nc4", shell=True, check=True)
    os.system(f"cdo mul {path}Ssoil_mean_tmp2.nc4 mask123.nc4 {path}Ssoil_mean.nc4")

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

def cdo_1(filename1, filename2, filename3):
    subprocess.run(f"cdo sub {filename1} {filename2} {filename3}", shell=True, check=True)

def dp_Sbedrock(path):
    Parallel(n_jobs=18)(delayed(cdo_1)(f"{path}Sr_{year}_tmp1.nc4", f"{path}Ssoil_{year}_tmp1.nc4", f"{path}Sbedrock_{year}_tmp1.nc4") for year in range(2003,2021))

    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'{path}/Sbedrock_{year}_tmp1.nc4'
        name_list = name_list+' '+name
    output_file = f'{path}Sbedrock_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}Sbedrock_mean_tmp1.nc4 {path}Sbedrock_mean_tmp2.nc4", shell=True, check=True)
    os.system(f"cdo mul {path}Sbedrock_mean_tmp2.nc4 mask123.nc4 {path}Sbedrock_mean.nc4")

def dp_rnof_mean(path):
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'{path}/tmp/rnof_{year}.nc4'
        name_list = name_list+' '+name
    output_file = f'{path}rnof_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -O -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}rnof_mean_tmp1.nc4 {path}rnof_mean_tmp2.nc4", shell=True, check=True)
    os.system(f"cdo -O -mul {path}rnof_mean_tmp2.nc4 mask123.nc4 {path}rnof_mean.nc4")

def dp_fevpa_mean(path):
    name_list = 'cdo -O -ensmean '
    for year in range(2003,2021):
        name = f'{path}/tmp/fevpa_{year}.nc4'
        name_list = name_list+' '+name
    output_file = f'{path}fevpa_mean_tmp1.nc4'
    print(name_list+' '+output_file)
    os.system(name_list+' '+output_file)

    subprocess.run(f"cdo -O -b F32 -P 48 --no_remap_weights remapbil,{data_path}mask1.nc4 {path}fevpa_mean_tmp1.nc4 {path}fevpa_mean_tmp2.nc4", shell=True, check=True)
    os.system(f"cdo -O -mul {path}fevpa_mean_tmp2.nc4 mask123.nc4 {path}fevpa_mean.nc4")

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
for casename in casename_list[:]:
    path = f'{data_path}/cases/{casename}/'
    os.makedirs(path+'/tmp', exist_ok=True)
    dp_Sr_mean(path)
    dp_Ssoil_mean(path)
    dp_Sbedrock(path)
    # dp_rnof_mean(path)
    # dp_fevpa_mean(path)
    # dp_Sr_mean(path)
    # dp_PSr_mean(path)