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

def cdo_1(filename1, filename2, filename3):
    subprocess.run(f"cdo -timmean -selname,{filename1} {filename2} {filename3}", shell=True, check=True)

def saws(casename):
    path = f'/tera11/zhwei/students/Xionghui/wetland/cases/{casename}/history/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/cases/{casename}/tmp/'
    # os.makedirs(path2, exist_ok=True)
    os.chdir(path2)
    for year in range(2003,2021):
        print(f'saws data process year is {year}')
        Parallel(n_jobs=12)(delayed(cdo_1)(f"f_h2osoi", f"{path}{casename}_hist_{year}-{mon:02}.nc", f"{path2}saws_{year}-{mon:02}_tmp1.nc4") for mon in range(1,13))
        name = ''
        name += ' '.join(f'{path2}saws_{year}-{mon:02}_tmp1.nc4' for mon in range(1, 13))
        os.system(f'cdo mergetime {name} {path2}saws_{year}_tmp1.nc4')
        os.system(f'cdo timmean {path2}saws_{year}_tmp1.nc4 {path2}saws_{year}.nc4')

def DTB_saws_to_Ssoil(casename):
    path1 = f'/tera11/zhwei/students/Xionghui/data/run/0p1/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/cases/{casename}/'
    # os.makedirs(path2, exist_ok=True)

    ds = xr.open_dataset(f'{path1}DTB.nc4')
    dtb = ds['Band1'].load()
    dtb = np.where(dtb>150,0,dtb)
    shape = dtb.shape
    for year in range(2003,2021):
        print(f'Ssoil data process year is {year}')
        ssoil = np.zeros(shape)
        ds2 = xr.open_dataset(f'{path2}tmp/saws_{year}.nc4')
        saws = ds2['f_h2osoi'].load()
        saws = saws[0,::-1,:,:]
        # soil_layer = [0, 1.75, 4.51, 9.06, 16.55, 28.91, 49.29, 82.89, 138.28, 229.61, 343.31]
        soil_layer = [0, 1.75, 4.51, 9.06, 16.55, 28.91, 49.29, 82.89, 138.28, 150]
        for i in range(9):
            ssoil = np.where((dtb>=soil_layer[i])&(dtb<=soil_layer[i+1]),ssoil+(dtb-soil_layer[i])*saws[:,:,i],np.where(dtb>=soil_layer[i+1],ssoil+(soil_layer[i+1]-soil_layer[i])*saws[:,:,i],ssoil))
        ssoil = ssoil*10

        output_ds = xr.Dataset({'Sr': (('lat', 'lon'), ssoil)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'{path2}Ssoil_{year}_tmp1.nc4')

def saws_to_Sr(casename):
    path1 = f'/tera11/zhwei/students/Xionghui/data/run/0p1/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/cases/{casename}/'
    ds = xr.open_dataset(f'{path1}DTB.nc4')
    dtb = ds['Band1'].load()
    shape = dtb.shape
    for year in range(2003,2021):
        print(f'Sr data process year is {year}')
        sr = np.zeros(shape)
        ds2 = xr.open_dataset(f'{path2}tmp/saws_{year}.nc4')
        saws = ds2['f_h2osoi'].load()
        saws = saws[0,::-1,:,:]
        soil_layer = [0, 1.75, 4.51, 9.06, 16.55, 28.91, 49.29, 82.89, 138.28, 150]
        for i in range(9):
            sr = sr+(soil_layer[i+1]-soil_layer[i])*saws[:,:,i]
        sr = sr*10

        output_ds = xr.Dataset({'Sr': (('lat', 'lon'), sr.data)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'{path2}Sr_{year}_tmp1.nc4')

def cdo_2(num1, filename1, filename2, filename3):
    subprocess.run(f"cdo -O -setmisstoc,0 -setrtoc,-inf,0,0 -mulc,86400 -mulc,{num1} -timmean -selname,{filename1} {filename2} {filename3}", shell=True, check=True)

#total runoff
def rnof(casename):
    path = f'/tera11/zhwei/students/Xionghui/wetland/cases/{casename}/history/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/cases/{casename}/tmp/'
    # os.makedirs(path2, exist_ok=True)
    os.chdir(path2)
    for year in range(2003,2021):
        print(f'total runoff data process year is {year}')
        monday = [31,28,31,30,31,30,31,31,30,31,30,31]
        if year%4==0:
            monday[1] = 29
        Parallel(n_jobs=12)(delayed(cdo_2)(monday[mon-1],f"f_rnof", f"{path}{casename}_hist_{year}-{mon:02}.nc", f"{path2}rnof_{year}-{mon:02}_tmp1.nc4") for mon in range(1,13))
        name = ''
        name += ' '.join(f'{path2}rnof_{year}-{mon:02}_tmp1.nc4' for mon in range(1, 13))
        os.system(f'cdo -O mergetime {name} {path2}rnof_{year}_tmp1.nc4')
        os.system(f'cdo -O -timsum {path2}rnof_{year}_tmp1.nc4 {path2}rnof_{year}.nc4')

#evapotranspiration
def fevpa(casename):
    path = f'/tera11/zhwei/students/Xionghui/wetland/cases/{casename}/history/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/cases/{casename}/tmp/'
    # os.makedirs(path2, exist_ok=True)
    os.chdir(path2)
    for year in range(2003,2021):
        print(f'fevpa data process year is {year}')
        monday = [31,28,31,30,31,30,31,31,30,31,30,31]
        if year%4==0:
            monday[1] = 29
        Parallel(n_jobs=12)(delayed(cdo_2)(monday[mon-1],f"f_fevpa", f"{path}{casename}_hist_{year}-{mon:02}.nc", f"{path2}fevpa_{year}-{mon:02}_tmp1.nc4") for mon in range(1,13))
        name = ''
        name += ' '.join(f'{path2}fevpa_{year}-{mon:02}_tmp1.nc4' for mon in range(1, 13))
        os.system(f'cdo -O mergetime {name} {path2}fevpa_{year}_tmp1.nc4')
        os.system(f'cdo -O -timsum {path2}fevpa_{year}_tmp1.nc4 {path2}fevpa_{year}.nc4')

# def cdo_2(num1, filename1, filename2, filename3):
#     subprocess.run(f"cdo -setmisstoc,0 -setrtoc,-inf,0,0 -mulc,86400 -mulc,{num1} -timmean -selname,{filename1} {filename2} {filename3}", shell=True, check=True)

# def Sr(casename):
#     path = f'/tera11/zhwei/students/Xionghui/wetland/cases/{casename}/history/'
#     path2 = f'/tera11/zhwei/students/Xionghui/data/run/0p1/cases/{casename}/tmp/'
#     os.chdir(path2)
#     for year in range(2003,2021):
#         print(f'Sr data process year is {year}')
#         monday = [31,28,31,30,31,30,31,31,30,31,30,31]
#         if year%4==0:
#             monday[1] = 29
#         Parallel(n_jobs=12)(delayed(cdo_2)(monday[mon-1],"f_rootr", f"{path}{casename}_hist_{year}-{mon:02}.nc", f"{path2}Sr_{year}-{mon:02}_tmp1.nc4") for mon in range(1,13))
#         name = ''
#         name += ' '.join(f'{path2}Sr_{year}-{mon:02}_tmp1.nc4' for mon in range(1, 13))
#         os.system(f'cdo mergetime {name} {path2}Sr_{year}_tmp1.nc4')
#         os.system(f'cdo -vertsum -timsum {path2}Sr_{year}_tmp1.nc4 {path2}Sr_{year}_tmp2.nc4')

# def cdo_3(filename1, filename2, filename3):
#     subprocess.run(f"cdo -timmean -selname,{filename1} {filename2} {filename3}", shell=True, check=True)

# def PSr(casename):
#     path = f'/tera11/zhwei/students/Xionghui/wetland/cases/{casename}/history/'
#     path2 = f'/tera11/zhwei/students/Xionghui/data/run/0p1/cases/{casename}/tmp/'
#     os.chdir(path2)
#     for year in range(2003,2021):
#         print(f'PSr data process year is {year}')
#         Parallel(n_jobs=12)(delayed(cdo_3)("f_vegwp", f"{path}{casename}_hist_{year}-{mon:02}.nc", f"{path2}PSr_{year}-{mon:02}_tmp1.nc4") for mon in range(1,13))
#         name = ''
#         name += ' '.join(f'{path2}PSr_{year}-{mon:02}_tmp1.nc4' for mon in range(1, 13))
#         print(name)
#         os.system(f'cdo mergetime {name} {path2}PSr_{year}_tmp1.nc4')
#         os.system(f'cdo -vertsum -timmean {path2}PSr_{year}_tmp1.nc4 {path2}PSr_{year}_tmp2.nc4')


casename_list = ['bedrock_1','bedrock_2','bedrock_3']
for casename in casename_list:
    os.makedirs(f'{data_path}/cases/{casename}/tmp', exist_ok=True)
    # saws(casename)
    DTB_saws_to_Ssoil(casename)
    saws_to_Sr(casename)
    rnof(casename)
    fevpa(casename)
    # Sr(casename)
    # PSr(casename)