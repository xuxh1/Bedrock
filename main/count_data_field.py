import os
import numpy as np
import xarray as xr
import pandas as pd
import netCDF4 as nc
import geopandas as gpd
import rioxarray as rxr
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

# Collect the global calculated data
def count_G():
    

# Reprocessing US statistical data(note:Save and reopen to remove zero values)
# from Sovereignt to state, based on the previous function
def count_US():
    df = pd.read_csv('US.csv')
    print(df)

    shp = gpd.read_file(shp_path+'US/USA_adm1.shp')

    print(shp)

    gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']), crs='EPSG:4326')
    result1 = gpd.sjoin(gdf_points, shp, how='left', predicate='within')

    df['State'] = result1['NAME_1']

    print(df)

    with open('US.csv','w') as f:
        df.to_csv(f)