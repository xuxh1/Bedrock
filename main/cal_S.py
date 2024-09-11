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
def Sr():
    ds = xr.open_dataset('diff.nc')
    data_var = ds['et']

    ds2 = xr.open_dataset('SnowCover.nc')
    snowf = ds2['snowf']
    
    # 初始化一个数组来存储正值累加
    positive_accumulation = np.zeros_like(data_var.isel(time=0).values)

    # 初始化一个数组来存储正值累加最大值
    max_positive_accumulation = np.zeros_like(data_var.isel(time=0).values)

    for i in range(len(ds.time)):
        current_data = data_var.isel(time=i).values
        
        sc = snowf.isel(time=i).values
        
        current_data_mask = current_data*sc
        # 累加正值
        positive_accumulation = np.where((current_data_mask > 0), positive_accumulation + current_data, 0)
        
        # 更新最大正值累加
        max_positive_accumulation = np.maximum(max_positive_accumulation, positive_accumulation)

    output_ds = xr.Dataset({'Sr': (('lat', 'lon'), max_positive_accumulation)},
                    coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf('Sr_temp1.nc')
    ds.close()
    ds2.close()
    

# 对Sr进行筛选
@timer
def Sr_mask():
    subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,500.txt Sr_temp1.nc Sr_temp2.nc", shell=True, check=True)
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
 