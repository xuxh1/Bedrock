import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

resolution     = config.resolution
name           = config.name
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

# Load datasets
ds = xr.open_dataset(f'{data_path}diff.nc')
data_var = ds['et']
ds2 = xr.open_dataset(f'{data_path}SnowCover.nc')
snowf = ds2['snowf']

# Choose a specific grid point for visualization, e.g., (lat, lon) at index (50, 50)
lat_index, lon_index = 50, 50

# Extract the data at the selected grid point
et_values = data_var[:, lat_index, lon_index].values
snow_cover_values = snowf[:, lat_index, lon_index].values

# Initialize matrices to accumulate positive and negative values
time_len = len(ds.time)
pos_acc = np.zeros(time_len)
neg_acc = np.zeros(time_len)

for i in range(time_len):
    current_data = data_var.isel(time=i).values[lat_index, lon_index]
    sc = snowf.isel(time=i).values[lat_index, lon_index]
    current_data_mask = current_data * sc
    
    # Accumulate positive and negative values
    if current_data_mask > 0:
        pos_acc[i] = pos_acc[i - 1] + current_data_mask
    else:
        pos_acc[i] = 0
        
    if current_data_mask < 0:
        neg_acc[i] = neg_acc[i - 1] + current_data_mask
    else:
        neg_acc[i] = 0

# Create time series plots
time = ds['time'].values

plt.figure(figsize=(12, 8))

# Plot ET-PR values over time
plt.subplot(2, 1, 1)
plt.plot(time, et_values, label='ET-PR', color='b')
plt.title('ET-PR over time at a specific grid point')
plt.ylabel('ET-PR')
plt.grid(True)

# Plot accumulated positive and negative values over time
plt.subplot(2, 1, 2)
plt.plot(time, pos_acc, label='Positive Accumulation', color='r')
plt.plot(time, neg_acc, label='Negative Accumulation', color='k')
plt.title('Accumulated Positive/Negative Values over time')
plt.ylabel('Accumulated Values')
plt.grid(True)

plt.tight_layout()
plt.savefig(f"{fig_path}l3_test.png")
