import numpy as np
from netCDF4 import Dataset

# 打开 NetCDF 文件
ncfile = Dataset('/tera11/zhwei/students/Xionghui/data/run/0p1_rawdata/mask123.nc4', 'r+')

# 获取变量
var = ncfile.variables['Band1']  # 根据实际情况替换

# 获取数据
data = var[:]

# 设置缺失值标记，假设原始缺失值为 -9999 和 1e20
data[data == -1] = np.nan
data[data == 9.96921e36] = np.nan

# 将 NaN 替换为你希望的值（例如 -9999）
data[np.isnan(data)] = 9.96921e36

# 写回数据
var[:] = data

# 关闭文件
ncfile.close()
