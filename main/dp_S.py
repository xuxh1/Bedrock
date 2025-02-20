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

def dp_Sbedrock_mask123():
    os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Sbedrock_tmp1.nc4 Sbedrock_tmp2.nc4')
    # os.system(f'cdo setrtoc2,-inf,0,-1,1 Sbedrock_tmp2.nc4 mask4.nc4')
    # os.system(f'cdo mul mask123.nc4 mask4.nc4 mask1234.nc4')
    os.system(f"cdo mul Sbedrock_tmp2.nc4 mask123.nc4 Sbedrock.nc4")
    print(f'The Sbedrock has finished')  

def dp_Sr():
    os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Sr_tmp1.nc4 Sr_tmp2.nc4')
    os.system(f"cdo mul Sr_tmp2.nc4 mask123.nc4 Sr.nc4")
    print(f'The Sr has finished')    

def dp_FD2FY():
    os.system('cdo -b F32 -P 48 --no_remap_weights remapbil,mask1.nc4 S_FD_tmp1.nc4 S_FD_tmp2.nc4')
    os.system('cdo mul S_FD_tmp2.nc4 mask123.nc4 S_FD.nc4')

    days_in_year = [366 if (i % 4 == 0 and (i % 100 != 0 or i % 400 == 0)) else 365 for i in range(2003,2021)]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_year):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list

    command = f'cdo {command_list}-setrtoc,-1,0,0 S_FD_tmp2.nc4 S_FY_tmp1.nc4'
    print(f"Executing: {command}")  
    os.system(command)
    os.system('cdo mul S_FY_tmp1.nc4 mask123.nc4 S_FY.nc4')

def dp_S_Duration():
    os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt S_Duration_tmp1.nc4 S_Duration_tmp2.nc4')
    os.system(f"cdo mul S_Duration_tmp2.nc4 mask123.nc4 S_Duration.nc4")
    print(f'The S_Duration has finished')  

def dp_S_Drought():
    # os.system('cdo yearmax Drought_Period_tmp1.nc4 Drought_Period_yearmax_tmp1.nc4')
    # os.system('cdo timmean Drought_Period_yearmax_tmp1.nc4 Drought_Period_yearmax_timmean_tmp1.nc4')
    # os.system('cdo timmax Drought_Period_tmp1.nc4 Drought_Period_timmax_tmp1.nc4')

    os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_yearmax_timmean_tmp1.nc4 Drought_Period_yearmax_timmean_tmp2.nc4')
    os.system('cdo mul Drought_Period_yearmax_timmean_tmp2.nc4 mask123.nc4 Drought_Period_yearmax_timmean.nc4')

    os.system(f'cdo -b F32 -P 48 --no_remap_weights remapbil,{resolution}.txt Drought_Period_timmax_tmp1.nc4 Drought_Period_timmax_tmp2.nc4')
    os.system('cdo mul Drought_Period_timmax_tmp2.nc4 mask123.nc4 Drought_Period_timmax.nc4')

    os.system('cdo sub Drought_Period_timmax.nc4 Drought_Period_yearmax_timmean.nc4 Drought_Period_sub.nc4')


if __name__=='__main__':
    # dp_Sbedrock_mask123()
    # dp_Sr()
    # dp_FD2FY()
    # dp_S_Duration()
    dp_S_Drought()