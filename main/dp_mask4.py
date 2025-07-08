import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
data_path = config.data_path

dir_man = DirMan(data_path)
dir_man.enter()

def mask4():
    os.system(f"cdo mul Sbedrock_tmp2.nc4 mask1234.nc4 Sbedrock.nc4")
    os.system(f"cdo mul Sr_tmp2.nc4 mask1234.nc4 Sr.nc4")
    # os.system('cdo mul S_FD_tmp2.nc4 mask1234.nc4 S_FD.nc4')
    # os.system(f"cdo mul S_Frequency_mean_tmp2.nc4 mask1234.nc4 S_Frequency_mean.nc4")
    # os.system(f"cdo mul S_Frequency_max_tmp2.nc4 mask1234.nc4 S_Frequency_max.nc4")
    # os.system(f"cdo mul S_Frequency_max_sub_mean_tmp2.nc4 mask1234.nc4 S_Frequency_max_sub_mean.nc4")

    # os.system(f"cdo mul S_time_max_duration_tmp3.nc4 mask1234.nc4 S_time_max_duration.nc4")
    # os.system(f"cdo mul S_time_mean_duration_tmp3.nc4 mask1234.nc4 S_time_mean_duration.nc4")
    # os.system(f"cdo mul S_sum_Frequency_tmp3.nc4 mask1234.nc4 S_sum_Frequency.nc4")
    # os.system(f"cdo mul S_sum_duration_tmp3.nc4 mask1234.nc4 S_sum_duration.nc4")

    # os.system(f"cdo mul S_CY_tmp3.nc4 mask1234.nc4 S_CY.nc4")
    # os.system(f"cdo mul S_Duration_mean_tmp2.nc4 mask1234.nc4 S_Duration_mean.nc4")
    # os.system(f"cdo mul S_Duration_max_tmp2.nc4 mask1234.nc4 S_Duration_max.nc4")
    # os.system(f"cdo mul S_Duration_max_sub_mean_tmp2.nc4 mask1234.nc4 S_Duration_max_sub_mean.nc4")
    # os.system(f"cdo mul S_FD_mean_tmp2.nc4 mask1234.nc4 S_FD_mean.nc4")
    # os.system(f"cdo mul S_FD_max_tmp2.nc4 mask1234.nc4 S_FD_max.nc4")
    # os.system(f"cdo mul S_FD_max_sub_mean_tmp2.nc4 mask1234.nc4 S_FD_max_sub_mean.nc4")