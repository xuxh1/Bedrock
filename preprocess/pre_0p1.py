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
from myfunc import timer, run_command
import math

path = '/tera04/zhwei/xionghui/bedrock/'

def remap_data(input_file,output_file):
    run_command(f'gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts 3600 1800 -overwrite {input_file} {output_file}')

input_file = os.path.join(path, 'mask_all', 'mask_adequatewater', 'mask_adequatewater.nc4')
output_file = os.path.join(path, 'mask_all', 'mask_adequatewater', 'mask_adequatewater_0p1.nc4')
remap_data(input_file,output_file)

input_file = os.path.join(path, 'mask_all', 'mask_woodyveg', 'mask_woodyveg.nc4')
output_file = os.path.join(path, 'mask_all', 'mask_woodyveg', 'mask_woodyveg_0p1.nc4')
remap_data(input_file,output_file)

input_file = os.path.join(path, 'mask_all', 'mask_shallowbedrock', 'mask_shallowbedrock.nc4')
output_file = os.path.join(path, 'mask_all', 'mask_shallowbedrock', 'mask_shallowbedrock_0p1.nc4')
remap_data(input_file,output_file)

input_file = os.path.join(path, 'Ssoil', 'Ssoil.nc4')
output_file = os.path.join(path, 'Ssoil', 'Ssoil_0p1.nc4')
remap_data(input_file,output_file)