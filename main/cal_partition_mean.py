import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
name = config.name
data_path = config.data_path
post_data_path = config.post_data_path

def Proportion2_mean():
    # Calculate Proportion2_mean(Sbedrock/ET_mean)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock.nc ET_mean.nc Proportion2_mean_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion2_mean_temp1.nc mask123.nc Proportion2_mean_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 Proportion2_mean_temp2.nc Proportion2_mean.nc", shell=True, check=True)
    print(f'The Proportion2_mean has finished')

def Proportion3_mean():
    # Calculate Proportion3_mean(Q_mean/PR_mean)
    subprocess.run(f"cdo -mulc,100 -div Q_mean.nc PR_mean.nc Proportion3_mean_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion3_mean_temp1.nc mask123.nc Proportion3_mean.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion3_temp1.nc Proportion3.nc", shell=True, check=True)
    print(f'The Proportion3_mean has finished')

def Proportion4_mean():
    # Calculate Proportion4_mean(ET_mean/PR_mean)
    subprocess.run(f"cdo -mulc,100 -div ET_mean.nc PR_mean.nc Proportion4_mean_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion4_mean_temp1.nc mask123.nc Proportion4_mean.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion4_temp1.nc Proportion4.nc", shell=True, check=True)
    print(f'The Proportion4_mean has finished')

def Proportion5_mean():
    # Calculate Proportion5_mean(Sbedrock/PR_mean)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc PR_mean.nc Proportion5_mean_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion5_mean_temp1.nc mask123.nc Proportion5_mean.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion5_temp1.nc Proportion5.nc", shell=True, check=True)
    print(f'The Proportion5_mean has finished')

def Proportion6_mean():
    # Calculate Proportion6_mean((ET_mean-Sbedrock)/PR_mean)
    # os.system('cdo -setrtoc2,-inf,0,0,1 Sbedrock_temp1.nc mask_sr.nc')
    # os.system('cdo -setrtoc2,-inf,0,1,0 Sbedrock_temp1.nc mask_ssoil.nc')
    os.system('cdo sub Proportion4_mean_temp1.nc Proportion5_mean_temp1.nc Proportion6_mean_sr_temp1.nc')
    os.system('cdo mul Proportion6_mean_sr_temp1.nc mask_sr.nc Proportion6_mean_sr.nc')
    os.system('cdo mul Proportion4_mean_temp1.nc mask_ssoil.nc Proportion6_mean_ssoil.nc')
    os.system('cdo add Proportion6_mean_sr.nc Proportion6_mean_ssoil.nc Proportion6_mean_temp1.nc')
    subprocess.run(f"cdo mul Proportion6_mean_temp1.nc mask123.nc Proportion6_mean.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion6_temp1.nc Proportion6.nc", shell=True, check=True)
    print(f'The Proportion6_mean has finished')

    # # Calculate Latent Heat(Ee=Sbedrock*1000*2257/(3600*24*365))
    # subprocess.run(f'cdo -expr,"Ee=Sr*1000*2257/(3600*24*365)" Sbedrock.nc LH.nc', shell=True, check=True)
    # print(f'The Latent Heat has finished')

def Proportion7_mean():
    # Calculate Proportion7_mean(PET/PR_mean)
    subprocess.run(f"cdo -mulc,100 -div PET.nc PR_mean.nc Proportion7_mean_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion7_mean_temp1.nc mask123.nc Proportion7_mean.nc", shell=True, check=True)
    print(f'The Proportion7_mean has finished')

def cal_partition():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Proportion2_mean()
    # Proportion3_mean()
    # Proportion4_mean()
    # Proportion5_mean()
    # Proportion6_mean()
    Proportion7_mean()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_partition() 