import glob
import subprocess
import xarray as xr
import numpy as np
import os
import sys
sys.path.append('/home/xuxh22/anaconda3/lib/mylib/')
from myfunc import timer

path = os.getcwd()+'/'
print("当前文件路径:", path)

# 计算CWD(累计水分亏缺)为Sr值
@timer
# def Sr():
#     ds = xr.open_dataset('diff.nc')
#     data_var = ds['et']

#     ds2 = xr.open_dataset('SnowCover.nc')
#     snowf = ds2['snowf']
    
#     # set matrix: accumulation, positive accumulation, max positive accumulation
#     pos_acc = np.zeros_like(data_var.isel(time=0).values)
#     neg_acc = np.zeros_like(data_var.isel(time=0).values)
#     last_max_pos_acc = np.zeros_like(data_var.isel(time=0).values)
#     max_pos_acc = np.zeros_like(data_var.isel(time=0).values)
#     min_neg_acc = np.zeros_like(data_var.isel(time=0).values)
#     all_max_pos_acc = np.zeros_like(data_var.isel(time=0).values)
#     # all_min_neg_acc = np.zeros_like(data_var.isel(time=0).values)
#     time_acc = np.zeros_like(data_var.isel(time=0).values)
#     last_data_mask = np.zeros_like(data_var.isel(time=0).values)
#     for i in range(len(ds.time)):
#         current_data = data_var.isel(time=i).values
        
#         sc = snowf.isel(time=i).values
        
#         current_data_mask = current_data*sc

#         # accumulate
#         pos_acc = np.where((current_data_mask > 0), pos_acc + current_data, 0)
#         neg_acc = np.where((current_data_mask < 0), neg_acc + current_data, 0)

#         # this time maxmin
#         last_max_pos_acc = np.where((last_data_mask < 0) & (current_data_mask > 0), max_pos_acc, last_max_pos_acc)
#         max_pos_acc = np.where((current_data_mask > 0), pos_acc, max_pos_acc)
#         min_neg_acc = np.where((current_data_mask < 0), neg_acc, min_neg_acc)

#         # time accumulate
#         time_acc = np.where((time_acc + last_max_pos_acc + min_neg_acc > 0), time_acc + last_max_pos_acc + min_neg_acc, 0)

#         # all time maxmin
#         all_max_pos_acc = np.maximum(all_max_pos_acc, pos_acc + time_acc)
#         # all_min_neg_acc = np.minimum(all_min_neg_acc, neg_acc)
        
#         last_data_mask = current_data_mask

#     output_ds = xr.Dataset({'Sr': (('lat', 'lon'), all_max_pos_acc)},
#                     coords={'lat': ds['lat'], 'lon': ds['lon']})
#     output_ds.to_netcdf('Sr_temp1.nc')
#     ds.close()
#     ds2.close()
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


# 对Sr进行筛选
@timer
def Sr_mask():
    subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,0p1.txt Sr_temp1.nc Sr_temp2.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sr_temp2.nc mask123.nc Sr.nc", shell=True, check=True)
    print(f'The Sr has finished')    
    
# 计算Ssoil和Sbedrock
@timer
def Sb_Sp():
    # 计算Sbedrock(基岩水)
    subprocess.run(f"cdo sub Sr_temp2.nc Ssoil.nc Sbedrock_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sbedrock_temp1.nc mask123.nc Sbedrock.nc", shell=True, check=True)
    print(f'The Sbedrock has finished')
    
    # 计算Sproportion(基岩水/根系水)
    subprocess.run(f"cdo -mulc,100 -div Sbedrock_temp1.nc Sr_temp2.nc Sproportion_temp1.nc", shell=True, check=True)
    subprocess.run(f"cdo mul Sproportion_temp1.nc mask123.nc Sproportion.nc", shell=True, check=True)
    # subprocess.run(f"cdo setrtomiss,-inf,0 Sproportion_temp1.nc Sproportion.nc", shell=True, check=True)
    print(f'The Sproportion has finished')

@timer
def delete():
    os.system('rm -rf Sr_temp1.nc')
    os.system('rm -rf Sr_temp2.nc')
    os.system('rm -rf Sbedrock_temp1.nc')
    os.system('rm -rf Sproportion_temp1.nc')    
        
    
if __name__=='__main__':
    Sr()
    Sr_mask()
    Sb_Sp()
    # delete()
 