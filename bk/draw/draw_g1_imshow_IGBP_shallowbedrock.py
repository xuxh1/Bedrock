import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from matplotlib import patches
from mpl_toolkits.basemap import Basemap
import config

resolution     = config.resolution
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path


# 1. 读取数据
# 假设两个文件分别为 'igbp_data.nc' 和 'bedrock_depth.nc'
igbp_data = xr.open_dataset(f'{data_path}IGBP.nc4')
bedrock_data = xr.open_dataset(f'{data_path}DTB.nc4')

# 提取IGBP分类数据和基岩深度数据
igbp_classification = igbp_data['LC'][0,:,:].values
bedrock_depth = bedrock_data['Band1'].values

# 2. 设置IGBP分类的颜色
igbp_colors = [
    "#e1d9b6", "#b8e1bb", "#9bcb4f", "#3a9d23", "#d8e0e1", # 1-5
    "#a2a0a5", "#b18a68", "#6f452a", "#c1b7b1"  # 6-9
]

# 3. 创建绘图
fig, ax = plt.subplots(figsize=(10, 5))

# 使用Basemap进行地图投影和绘制
m = Basemap(projection='robin', resolution='c', lon_0=0, lat_0=0)

# 绘制海洋
m.drawmapboundary(fill_color='lightgray')
m.fillcontinents(color='lightgray', lake_color='lightblue')

# 4. 绘制IGBP分类数据
# 为每个类别填充颜色
for i, color in enumerate(igbp_colors, 1):
    mask = igbp_classification == i
    # 转换为地图坐标
    x, y = m(*np.meshgrid(np.arange(igbp_classification.shape[1]), np.arange(igbp_classification.shape[0])))
    ax.pcolormesh(x, y, mask, color=color, shading='auto')

# 5. 绘制基岩深度小于150cm的区域方格
bedrock_mask = bedrock_depth < 150
x, y = m(*np.meshgrid(np.arange(igbp_classification.shape[1]), np.arange(igbp_classification.shape[0])))
# 设置方格透明度
ax.pcolormesh(x, y, bedrock_mask, color='white', alpha=0.5, hatch='//', shading='auto')

# 6. 显示地图
plt.title('Global Woody Vegetation Coverage Map')
plt.show()
