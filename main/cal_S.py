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


# Calculate Sr(the Culmulate Water Deficit - CWD) version2
@timer
def Sr():
    ds = xr.open_dataset('diff.nc')
    data_var = ds['et']
    ds2 = xr.open_dataset('SnowCover.nc')
    snowf = ds2['snowf']
    
    # Initialize matrices
    shape = data_var.isel(time=0).shape
    pos_acc = np.zeros(shape)
    neg_acc = np.zeros(shape)
    last_max_pos_acc = np.zeros(shape)
    max_pos_acc = np.zeros(shape)
    min_neg_acc = np.zeros(shape)
    all_max_pos_acc = np.zeros(shape)
    net_pos_acc = np.zeros(shape)
    last_data_mask = np.zeros(shape)

    for i in range(len(ds.time)):
        current_data = data_var.isel(time=i).values
        sc = snowf.isel(time=i).values
        current_data_mask = current_data * sc

        # Accumulate positive and negative values
        pos_acc = np.where(current_data_mask > 0, pos_acc + current_data_mask, 0)
        neg_acc = np.where(current_data_mask < 0, neg_acc + current_data_mask, 0)

        # Update last max positive accumulation
        last_max_pos_acc = np.where((last_data_mask < 0) & (current_data_mask > 0), max_pos_acc, last_max_pos_acc)
        max_pos_acc = np.where(current_data_mask > 0, pos_acc, max_pos_acc)
        min_neg_acc = np.where(current_data_mask < 0, neg_acc, min_neg_acc)

        # Update net positive accumulation
        net_pos_acc = np.where((net_pos_acc + last_max_pos_acc + min_neg_acc > 0) & (last_data_mask > 0) & (current_data_mask < 0), net_pos_acc + last_max_pos_acc + min_neg_acc, 0)

        # Update all time maximum positive accumulation
        all_max_pos_acc = np.maximum(all_max_pos_acc, max_pos_acc + net_pos_acc)
        
        last_data_mask = current_data_mask

    # Save the results to a new NetCDF file
    output_ds = xr.Dataset({'Sr': (('lat', 'lon'), all_max_pos_acc)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf('Sr_temp1.nc')
    
    # Close datasets
    ds.close()
    ds2.close()


# Mask Sr
@timer
def Sr_mask():
    subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,0p1.txt Sr_temp1.nc Sr_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sr_temp2.nc mask123.nc Sr.nc", shell=True, check=True)
    print(f'The Sr has finished')    
    

# Calculate Sbedrock(rock moisture) and Proportion1(Sbedrock/Sr)
@timer
def Sb_P1_P2_P3_LH():
    # Calculate Sbedrock(rock moisture)
    subprocess.run(f"cdo sub Sr_temp2.nc Ssoil.nc Sbedrock_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sbedrock_temp1.nc mask123.nc Sbedrock.nc", shell=True, check=True)
    print(f'The Sbedrock has finished')
    
    # Calculate Proportion1(Sbedrock/Sr)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc Sr_temp2.nc Proportion1_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion1_temp1.nc mask123.nc Proportion1.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion1_temp1.nc Proportion1.nc", shell=True, check=True)
    print(f'The Proportion1 has finished')

    # Calculate Proportion2(Sbedrock/ET)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc ET.nc Proportion2_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion2_temp1.nc mask123.nc Proportion2.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion2_temp1.nc Proportion2.nc", shell=True, check=True)
    print(f'The Proportion2 has finished')

    # Calculate Proportion3(Q/PR)
    subprocess.run(f"cdo -mulc,100 -div Q.nc PR.nc Proportion3_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Proportion3_temp1.nc mask123.nc Proportion3.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Proportion3_temp1.nc Proportion3.nc", shell=True, check=True)
    print(f'The Proportion3 has finished')

    # Calculate Latent Heat(Ee=Sbedrock*1000*2257/(3600*24*365))
    subprocess.run(f'cdo -expr,"Ee=Sr*1000*2257/(3600*24*365)" Sbedrock.nc LH.nc', shell=True, check=True)
    print(f'The Latent Heat has finished')

# Delete the intermediate data to save memory
@timer
def delete():
    os.system('rm -rf Sr_temp1.nc')
    os.system('rm -rf Sr_temp2.nc')
    os.system('rm -rf Sbedrock_temp1.nc')
    os.system('rm -rf Proportion1_temp1.nc')    


# Execute all program
@timer
def cal_S():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    Sr()
    Sr_mask()
    Sb_P1_P2_P3_LH()
    # delete()

    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_S() 