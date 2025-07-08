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

def et():
    et_path = "/tera04/zhwei/xionghui/bedrock/diff/"
    ds = xr.open_dataset(f'{et_path}ET_2003_2020_yr_{resolution}_mmyr_nn.nc')
    et = ds['et'].load()

    et_year_median = np.median(et, axis=0)

    print(et_year_median)

    output_ds = xr.Dataset({'et': (('lat', 'lon'), et_year_median)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{et_path}ET_2003_2020_median_{resolution}_mmyr_nn.nc')

    os.system('cdo -b F32 -P 12 --no_remap_weights -remapbil,../500.txt ET_2003_2020_median_0p1_mmyr_nn.nc ET_2003_2020_median_500_mmyr_nn.nc')


def pr():
    pr_path = "/tera04/zhwei/xionghui/bedrock/diff/"
    ds = xr.open_dataset(f'{pr_path}PR_2003_2020_yr_{resolution}_mmyr_nn.nc')
    pr = ds['tp'].load()

    pr_year_median = np.median(pr, axis=0)

    print(pr_year_median)

    output_ds = xr.Dataset({'tp': (('lat', 'lon'), pr_year_median)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{pr_path}PR_2003_2020_median_{resolution}_mmyr_nn.nc')

    os.system('cdo -b F32 -P 12 --no_remap_weights -remapbil,../500.txt PR_2003_2020_median_0p1_mmyr_nn.nc PR_2003_2020_median_500_mmyr_nn.nc')


def q():
    q_path = "/tera04/zhwei/xionghui/bedrock/diff/"
    ds = xr.open_dataset(f'{q_path}Q_2003_2020_yr_{resolution}_mmyr_nn.nc')
    q = ds['tp'].load()

    q_year_median = np.median(q, axis=0)

    print(q_year_median)

    output_ds = xr.Dataset({'tp': (('lat', 'lon'), q_year_median)},
                           coords={'lat': ds['lat'], 'lon': ds['lon']})
    output_ds.to_netcdf(f'{q_path}Q_2003_2020_median_{resolution}_mmyr_nn.nc')

    os.system('cdo -b F32 -P 12 --no_remap_weights -remapbil,../500.txt Q_2003_2020_median_0p1_mmyr_nn.nc Q_2003_2020_median_500_mmyr_nn.nc')
    
et()
pr()
q()