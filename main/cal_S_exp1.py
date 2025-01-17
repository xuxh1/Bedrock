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


# Calculate Sr(the Culmulate Water Deficit - CWD) version2
@timer
def Sr():
    ds = xr.open_dataset(f'{data_path}diff.nc')
    data_var = ds['et'].load()
    ds2 = xr.open_dataset(f'{data_path}SnowCover.nc')
    snowf = ds2['snowf'].load()
    ds3 = xr.open_dataset(f'{data_path}../0p1/Ssoil.nc')
    ssoil = ds3['Band1'].load()

    shape = data_var.isel(time=0).shape
    time_len = len(ds.time)

    deficit_pmax = np.zeros((time_len, *shape))
    deficit_pmin = np.zeros((time_len, *shape))
    deficit_diff = np.zeros((time_len, *shape))
    deficit_Srv1 = np.zeros((time_len, *shape))
    deficit_acc = np.zeros((time_len, *shape))
    pmax = np.zeros(shape) 
    pmin = np.zeros(shape)  
    Srv1 = np.zeros(shape)
    data_acc = np.zeros(shape)
    first_day = np.full_like(data_var.isel(time=0).values, -1, dtype=int)

    p = np.zeros(shape)
    n = np.zeros(shape)

    data_pos_acc = np.zeros(shape)
    max_data_pos_acc = np.zeros(shape)
    for i in range(time_len):
        print(i)
        current_data_mask = data_var.isel(time=i).values * snowf.isel(time=i).values

        # set the modified method - exp1
        if i < time_len - 1:
            next_data_mask = data_var.isel(time=i + 1).values * snowf.isel(time=i + 1).values
        else:
            next_data_mask = current_data_mask

        # if i > 0:
        #     last_data_mask = data_var.isel(time=i - 1).values * snowf.isel(time=i - 1).values
        # else:
        #     last_data_mask = current_data_mask

        # sum the number of max, min points
        p = np.where((current_data_mask>0)&(next_data_mask<0),p+1,p)
        n = np.where((current_data_mask<0)&(next_data_mask>0),n+1,n)

        data_acc += current_data_mask

        # set pmax(the closest maximum point)
        pmin_last = pmin
        pmax = np.where((current_data_mask>0)&(next_data_mask<0),data_acc,pmax)
        pmin = np.where((current_data_mask<0)&(next_data_mask>0),data_acc,pmin)

        # set the Continuous extreme value diff and the max diff
        diff_max = np.where(current_data_mask<0,pmax-pmin_last,data_acc-pmin_last)
        Srv1 = np.maximum(Srv1,diff_max)
        
        # write out the value change over time
        deficit_pmax[i, :, :] = pmax
        deficit_pmin[i, :, :] = pmin
        deficit_diff[i, :, :] = diff_max
        deficit_Srv1[i, :, :] = Srv1
        deficit_acc[i, :, :] = data_acc

        # set the original method - exp1
        data_pos_acc = np.where(current_data_mask>0,data_pos_acc+current_data_mask,0)
        max_data_pos_acc = np.where(data_pos_acc>max_data_pos_acc,data_pos_acc,max_data_pos_acc)

        # When first use the bedrock water?
        first_occurrence = ((data_acc-pmin) > ssoil.values) & (first_day == -1)
        
        day_stt = 8*i+1-3*(i//46)+((i//46)+2)//4
        day_end = 8*(i+1)+1-3*((i+1)//46)+(((i+1)//46)+2)//4-1
        first_day[first_occurrence] = day_stt
        print(day_stt)
        print(day_end)
        
    output_ds = xr.Dataset({'Sr': (('lat', 'lon'), Srv1)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{data_path}Sr_temp1.nc')
    
    output_ds = xr.Dataset({'Sr': (('lat', 'lon'), max_data_pos_acc)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{data_path}Sr_temp1_test.nc')

    output_ds1 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_acc)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds1.to_netcdf(f'{data_path}Deficit_S.nc')

    output_ds2 = xr.Dataset({'nmax': (('lat', 'lon'), p)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds2.to_netcdf(f'{data_path}nmax.nc')

    output_ds3 = xr.Dataset({'nmin': (('lat', 'lon'), n)},
                        coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds3.to_netcdf(f'{data_path}nmin.nc')

    output_ds4 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_pmax)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds4.to_netcdf(f'{data_path}Deficit_pmax.nc')

    output_ds5 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_pmin)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds5.to_netcdf(f'{data_path}Deficit_pmin.nc')

    output_ds6 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_diff)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds6.to_netcdf(f'{data_path}Deficit_diff.nc')

    output_ds7 = xr.Dataset({'Deficit': (('time', 'lat', 'lon'), deficit_Srv1)},
                        coords={'time': ds['time'], 'lat': ds['lat'], 'lon': ds['lon']})
    output_ds7.to_netcdf(f'{data_path}Deficit_Srv1.nc')

    output_ds = xr.Dataset({'FD': (('lat', 'lon'), first_day)},
                coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'FD_temp1.nc')

    ds.close()
    ds2.close()

# Calculate Sbedrock(rock moisture) and Proportion1(Sbedrock/Sr)
def cal_Sr_Sb():
    # Calculate Sr(root moisture)
    subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,{resolution}.txt Sr_temp1.nc Sr_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sr_temp2.nc mask123.nc Sr.nc", shell=True, check=True)
    print(f'The Sr has finished')    

    # Calculate Sbedrock(rock moisture)
    subprocess.run(f"cdo sub Sr_temp2.nc Ssoil.nc Sbedrock_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sbedrock_temp1.nc mask123.nc Sbedrock.nc", shell=True, check=True)
    print(f'The Sbedrock has finished') 


def cal_FY():
    os.system('cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc FD_temp1.nc FD_temp2.nc')
    os.system('cdo mul FD_temp2.nc mask123.nc FD.nc')

    days_in_year = [365, 366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366]
    sumday = 0
    command_list = ''
    for i, day in enumerate(days_in_year):
        sumday += day  
        command_name = f"-setrtoc,{sumday-day},{sumday},{i+1} "
        command_list = command_name + command_list

    command = f'cdo {command_list}-setrtoc,-1,0,0 FD.nc FY_temp1.nc'
    print(f"Executing: {command}")  
    os.system(command)
    os.system('cdo mul FY_temp1.nc mask123.nc FY.nc')

# Delete the intermediate data to save memory
# @timer
# def delete():
#     os.system('rm -rf Sr_temp1.nc')
#     os.system('rm -rf Sr_temp2.nc')
#     os.system('rm -rf Sbedrock_temp1.nc')
#     os.system('rm -rf Proportion1_temp1.nc')    

# Execute all program
@timer
def cal_S():        
    # Transfer the current path to the calculation path
    dir_man = DirMan(data_path)
    dir_man.enter()
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Sr()
    cal_Sr_Sb()
    cal_FY()


    # Transfer from the calculation path to the later path 
    dir_man.exit()
    path = os.getcwd()+'/'
    print("Current file path: ", path)


if __name__=='__main__':
    cal_S() 