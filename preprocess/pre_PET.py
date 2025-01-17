from netCDF4 import Dataset
import netCDF4 as nc
import subprocess
import xarray as xr
import numpy as np
import os
from tqdm import tqdm
import config

resolution = config.resolution

path1 = '/tera11/zhwei/students/Xionghui/data/'
os.chdir(path1)

dir_path = path1+'PET/'
os.chdir(dir_path)
os.system(f'cdo -setrtoc,10000,inf,nan et0_v3_yr.nc PET_{resolution}_temp1.nc')
os.system(f'cdo -b F32 -P 12 --no_remap_weights -remapbil,{path1}{resolution}.txt PET_{resolution}_temp1.nc PET_{resolution}.nc')