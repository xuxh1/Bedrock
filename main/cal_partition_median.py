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
    
def Proportion1():
    # Calculate Proportion1(Sbedrock/Sr)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc Sr_temp2.nc Proportion1_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion1_temp1.nc mask123.nc Proportion1_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 Proportion1_temp2.nc Proportion1.nc", shell=True, check=True)
    print(f'The Proportion1 has finished')

def Proportion2_median():
    # Calculate Proportion2_median(Sbedrock/ET_median)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock.nc ET_median.nc Proportion2_median_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion2_median_temp1.nc mask123.nc Proportion2_median_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo setrtomiss,-inf,0 Proportion2_median_temp2.nc Proportion2_median.nc", shell=True, check=True)
    print(f'The Proportion2_median has finished')

def Proportion3_median():
    # Calculate Proportion3_median(Q_median/PR_median)
    subprocess.run(f"cdo -mulc,100 -div Q_median.nc PR_median.nc Proportion3_median_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion3_median_temp1.nc mask123.nc Proportion3_median.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion3_temp1.nc Proportion3.nc", shell=True, check=True)
    print(f'The Proportion3_median has finished')

def Proportion4_median():
    # Calculate Proportion4_median(ET_median/PR_median)
    subprocess.run(f"cdo -mulc,100 -div ET_median.nc PR_median.nc Proportion4_median_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion4_median_temp1.nc mask123.nc Proportion4_median.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion4_temp1.nc Proportion4.nc", shell=True, check=True)
    print(f'The Proportion4_median has finished')

def Proportion5_median():
    # Calculate Proportion5_median(Sbedrock/PR_median)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc PR_median.nc Proportion5_median_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion5_median_temp1.nc mask123.nc Proportion5_median.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion5_temp1.nc Proportion5.nc", shell=True, check=True)
    print(f'The Proportion5_median has finished')

def Proportion6_median():
    # Calculate Proportion6_median((ET_median-Sbedrock)/PR_median)
    os.system('cdo -setrtoc2,-inf,0,0,1 Sbedrock_temp1.nc mask_sr.nc')
    os.system('cdo -setrtoc2,-inf,0,1,0 Sbedrock_temp1.nc mask_ssoil.nc')
    os.system('cdo sub Proportion4_median_temp1.nc Proportion5_median_temp1.nc Proportion6_median_sr_temp1.nc')
    os.system('cdo mul Proportion6_median_sr_temp1.nc mask_sr.nc Proportion6_median_sr.nc')
    os.system('cdo mul Proportion4_median_temp1.nc mask_ssoil.nc Proportion6_median_ssoil.nc')
    os.system('cdo add Proportion6_median_sr.nc Proportion6_median_ssoil.nc Proportion6_median_temp1.nc')
    subprocess.run(f"cdo mul Proportion6_median_temp1.nc mask123.nc Proportion6_median.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion6_temp1.nc Proportion6.nc", shell=True, check=True)
    print(f'The Proportion6_median has finished')

    # # Calculate Latent Heat(Ee=Sbedrock*1000*2257/(3600*24*365))
    # subprocess.run(f'cdo -expr,"Ee=Sr*1000*2257/(3600*24*365)" Sbedrock.nc LH.nc', shell=True, check=True)
    # print(f'The Latent Heat has finished')

def Proportion7_median():
    # Calculate Proportion7_median(PET/PR_median)
    subprocess.run(f"cdo -mulc,100 -div PET.nc PR_median.nc Proportion7_median_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion7_median_temp1.nc mask123.nc Proportion7_median.nc", shell=True, check=True)
    print(f'The Proportion7_median has finished')

# Execute all program
@timer
def cal_partition():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Sr()
    # Sbedrock()
    # Proportion1()
    # Proportion2_median()
    # Proportion3_median()
    # Proportion4_median()
    # Proportion5_median()
    # Proportion6_median()
    Proportion7_median()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_partition() 