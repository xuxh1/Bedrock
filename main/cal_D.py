import glob
import subprocess
import xarray as xr
import numpy as np
import os
from joblib import Parallel, delayed
from tqdm import tqdm, trange
import sys
sys.path.append('/home/xuxh22/anaconda3/lib/mylib/')
from myfunc import timer
import netCDF4 as nc
import shutil

path = os.getcwd()+'/'
print("当前文件路径:", path)

# 计算CWD(累计水分亏缺)为Dr值
@timer
def Dr():
    ds = xr.open_dataset('diff.nc')
    data_var = ds['et']

    ds2 = xr.open_dataset('SnowCover.nc')
    snowf = ds2['snowf']
    
    # 遍历每个时间步
    for j in range(18):
        print(j)
        
        # 初始化一个数组来存储正值累加
        positive_accumulation = np.zeros_like(data_var.isel(time=0+46*j).values)

        # 初始化一个数组来存储正值累加最大值
        max_positive_accumulation = np.zeros_like(data_var.isel(time=0+46*j).values)
        
        for i in range(0+46*j,46+46*j):
            print(i)
            current_data = data_var.isel(time=i).values
            
            sc = snowf.isel(time=i).values
            
            current_data_mask = current_data*sc
            # 累加正值
            positive_accumulation = np.where((current_data_mask > 0), positive_accumulation + current_data, 0)
            
            # 更新最大正值累加
            max_positive_accumulation = np.maximum(max_positive_accumulation, positive_accumulation)

        output_ds = xr.Dataset({'Dr': (('lat', 'lon'), max_positive_accumulation)},
                            coords={'lat': ds['lat'], 'lon': ds['lon']})
        output_ds.to_netcdf(f'Dr_{2003+j}_temp1.nc')
    ds.close()
    
def cdo_mul(filename1, filename2, filename3):
    subprocess.run(f"cdo mul {filename1} {filename2} {filename3}", shell=True, check=True)
    
def cdo_sub(filename1, filename2, filename3):
    subprocess.run(f"cdo sub {filename1} {filename2} {filename3}", shell=True, check=True)
    
# 对Dr进行筛选
@timer
def Dr_mask():
    # 将0.1°分辨率重投影到500m上
    for j in range(18):
        print(j+2003)
        subprocess.run(f"cdo -b F32 -P 12 --no_remap_weights remapbil,mask1.nc Dr_{2003+j}_temp1.nc Dr_{2003+j}_temp2.nc", shell=True, check=True)
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"Dr_{2003+j}_temp2.nc", "mask123.nc", f"Dr_{2003+j}.nc") for j in tqdm(range(18)))
    
# 计算Ssoil和Sbedrock
@timer
def Ssoil_Dbedrock():
    Parallel(n_jobs=5)(delayed(cdo_sub)(f"Dr_{2003+j}.nc", "Ssoil.nc", f"Dbedrock_{2003+j}_temp1.nc") for j in tqdm(range(18)))
    
    Parallel(n_jobs=5)(delayed(cdo_mul)(f"Dbedrock_{2003+j}_temp1.nc", "mask123.nc", f"Dbedrock_{2003+j}.nc") for j in tqdm(range(18)))

    
def delete():
    os.system('rm -rf Dr_*_temp1.nc')
    os.system('rm -rf Dr_*_temp2.nc')
    os.system('rm -rf Dbedrock_*_temp1.nc')    
    
# calculate Dbedrock Frequency
def cal_DbF():
    s1 = 0
    # i =2
    for year in range(2003,2021):
        file = f'Dbedrock_{year}.nc'
        image = xr.open_dataset(file)
        # print(dtb)
        s = image['Dr']
        print(f'年份: {year}, 最小值: {s.min().values}, 最大值: {s.max().values}')
        
        s = np.where(s > 0, 2, np.where(s < 0, 1, 0))
        print(f'年份: {year}, 最小值: {s.min()}, 最大值: {s.max()}')
        
        print(s.min(),s.max())
        
        if year == 2003:
            s1 = s
        else:
            s1 = s*s1
        
        s_nonan = np.where((s1<0), 0, s1)
        print(s1.min(),s1.max(),np.mean(s_nonan))
        image.close()
    print('end do')

    s1 = np.where((s1 >=2) & (s1 < 262144), 2, s1)
    s1 = np.where((s1 == 1), 3, s1)
    s1 = np.where(s1==262144, 1, s1)

    file_mask = f'mask12.nc'
    mask = xr.open_dataset(file_mask)
    s2 = mask['Band1']
    print(s1.min(),s1.max())

    s1 = np.where((s1==0) & (s2 == 1), 4, s1)
    # s1 = np.where((s1==0), np.nan, s1)

    print(s1.min(),s1.max())
    shutil.copyfile('Dbedrock_2003.nc', 'Dbedrock_Frequency.nc')

    with nc.Dataset('Dbedrock_Frequency.nc', 'a') as file:
        # 获取 's' 变量
        s_var = file.variables['Dr']

        # 修改 's' 数据
        new_s_data = s1 

        # 将修改后的数据写回 's' 变量
        s_var[:,:] = new_s_data



if __name__=='__main__':
    Dr()
    Dr_mask()
    Ssoil_Dbedrock()
    delete()
    cal_DbF()