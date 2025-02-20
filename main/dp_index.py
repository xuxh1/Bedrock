import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
data_path = config.data_path
post_data_path = config.post_data_path

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/P', exist_ok=True)

def Sbedrock_div_Sr():
    # Calculate Sbedrock/Sr
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_tmp2.nc4 Sr_tmp2.nc4 P/Sbedrock_div_Sr_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/Sbedrock_div_Sr_tmp1.nc4 mask123.nc4 P/Sbedrock_div_Sr_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/Sbedrock_div_Sr_tmp2.nc4 P/Sbedrock_div_Sr.nc4", shell=True, check=True)
    print(f'The Sbedrock/Sr has finished')  

def Sbedrock_div_ET_mean():
    # Calculate Sbedrock/ET_mean
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_tmp2.nc4 ET_mean.nc4 P/Sbedrock_div_ET_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/Sbedrock_div_ET_mean_tmp1.nc4 mask123.nc4 P/Sbedrock_div_ET_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/Sbedrock_div_ET_mean_tmp2.nc4 P/Sbedrock_div_ET_mean.nc4", shell=True, check=True)
    print(f'The Sbedrock/ET_mean has finished') 

def Sbedrock_div_PR_mean():
    # Calculate Sbedrock/PR_mean
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_tmp2.nc4 PR_mean.nc4 P/Sbedrock_div_PR_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/Sbedrock_div_PR_mean_tmp1.nc4 mask123.nc4 P/Sbedrock_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/Sbedrock_div_PR_mean_tmp2.nc4 P/Sbedrock_div_PR_mean.nc4", shell=True, check=True)
    print(f'The Sbedrock/PR_mean has finished') 

def ET_mean_div_PR_mean():
    # Calculate ET_mean/PR_mean
    subprocess.run(f"cdo -mulc,100 -div ET_mean.nc4 PR_mean.nc4 P/ET_mean_div_PR_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/ET_mean_div_PR_mean_tmp1.nc4 mask123.nc4 P/ET_mean_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/ET_mean_div_PR_mean_tmp2.nc4 P/ET_mean_div_PR_mean.nc4", shell=True, check=True)
    print(f'The ET_mean/PR_mean has finished') 

def ET_mean_sub_Sbedrock_div_PR_mean():
    # Calculate (ET_mean-Sbedrock)/PR_mean
    os.system('cdo -setrtoc,-inf,0,0 P/Sbedrock_div_PR_mean_tmp1.nc4 P/Sbedrock_div_PR_mean_tmp1_mask.nc4')
    os.system('cdo sub P/ET_mean_div_PR_mean_tmp1.nc4 P/Sbedrock_div_PR_mean_tmp1_mask.nc4 P/ET_mean_sub_Sbedrock_div_PR_mean_tmp1.nc4')
    subprocess.run(f"cdo mul P/ET_mean_sub_Sbedrock_div_PR_mean_tmp1.nc4 mask123.nc4 P/ET_mean_sub_Sbedrock_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/ET_mean_sub_Sbedrock_div_PR_mean_tmp2.nc4 P/ET_mean_sub_Sbedrock_div_PR_mean.nc4", shell=True, check=True)
    print(f'The (ET_mean-Sbedrock)/PR_mean has finished')

def Q_mean_div_PR_mean():
    # Calculate Q_mean/PR_mean
    subprocess.run(f"cdo -mulc,100 -div Q_mean.nc4 PR_mean.nc4 P/Q_mean_div_PR_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/Q_mean_div_PR_mean_tmp1.nc4 mask123.nc4 P/Q_mean_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/Q_mean_div_PR_mean_tmp2.nc4 P/Q_mean_div_PR_mean.nc4", shell=True, check=True)
    print(f'The Q_mean/PR_mean has finished') 

def PET_div_PR_mean():
    # Calculate PET/PR_mean
    subprocess.run(f"cdo -mulc,100 -div PET.nc4 PR_mean.nc4 P/PET_div_PR_mean_tmp1.nc4", shell=True, check=True)
    subprocess.run(f"cdo mul P/PET_div_PR_mean_tmp1.nc4 mask123.nc4 P/PET_div_PR_mean_tmp2.nc4", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 P/PET_div_PR_mean_tmp2.nc4 P/PET_div_PR_mean.nc4", shell=True, check=True)
    print(f'The PET/PR_mean has finished') 

if __name__=='__main__':
    Sbedrock_div_Sr()
    Sbedrock_div_ET_mean()
    Sbedrock_div_PR_mean()
    ET_mean_div_PR_mean()
    ET_mean_sub_Sbedrock_div_PR_mean()
    Q_mean_div_PR_mean()
    PET_div_PR_mean()