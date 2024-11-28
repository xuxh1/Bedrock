import netCDF4 as nc
import numpy as np

# 读取原始 NetCDF 文件
input_file = '/home/xuxh22/stu01/data/mask1/mask1_v3/mask1_0p1.nc'  # 请替换为你的输入文件路径
output_file = '/home/xuxh22/stu01/data/mask1/mask1_v3/mask1_0p1_set0_correct.nc'  # 输出文件路径

# 打开输入文件
with nc.Dataset(input_file, 'r') as src:
    # 获取原始的纬度和经度
    lon = src.variables['lon'][:]
    lat = src.variables['lat'][::-1]
    band1 = src.variables['Band1'][::-1,:]

    # 检查是否存在 _FillValue 或 missing_value
    fill_value = src.variables['Band1']._FillValue if '_FillValue' in src.variables['Band1'].ncattrs() else np.nan
    missing_value = src.variables['Band1'].missing_value if 'missing_value' in src.variables['Band1'].ncattrs() else np.nan

    # 将缺失值（NaN 或 fill_value 或 missing_value）设置为 0
    band1 = np.where(np.isnan(band1), 0, band1)  # 替换 NaN 为 0
    band1 = np.where(band1 == fill_value, 0, band1)  # 替换 _FillValue 为 0
    band1 = np.where(band1 == missing_value, 0, band1)  # 替换 missing_value 为 0

# 创建新的 NetCDF 文件
with nc.Dataset(output_file, 'w', format='NETCDF4') as dst:
    # 创建维度
    dst.createDimension('lat', len(lat))
    dst.createDimension('lon', len(lon))

    # 创建新的变量
    lon_w = dst.createVariable('lon_w', 'd', ('lon',), zlib=True, chunksizes=(3600,))
    lon_e = dst.createVariable('lon_e', 'd', ('lon',), zlib=True, chunksizes=(3600,))
    lat_s = dst.createVariable('lat_s', 'd', ('lat',), zlib=True, chunksizes=(1800,))
    lat_n = dst.createVariable('lat_n', 'd', ('lat',), zlib=True, chunksizes=(1800,))
    landmask = dst.createVariable('landmask', 'b', ('lat', 'lon'), zlib=True, chunksizes=(1800, 3600))


    # 填充 landmask 数据
    landmask[:, :] = band1.astype(np.byte)

    # 填充经纬度数据
    lon_w[:] = lon-0.05
    lon_e[:] = lon+0.05
    lat_s[:] = lat-0.05
    lat_n[:] = lat+0.05

    # 添加全局属性
    dst.description = "Processed landmask file with missing values set to 0"
    dst.history = "Created by Python script"
    dst.source = "Original file: " + input_file

print("NetCDF 文件已成功创建: ", output_file)