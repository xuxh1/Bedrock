import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from shapely.geometry import box
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.gridspec import GridSpec
import matplotlib.colors as colors
from math import radians, sin
import matplotlib
from pylab import rcParams
import pandas as pd
import netCDF4 as nc
import os

df = pd.read_csv('US.csv')
print(df)

shp_path   =  '/home/xuxh22/stu01/Bedrock/data/Shp/US/'
shp = gpd.read_file(shp_path+'USA_adm1.shp')

print(shp)

gdf_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']), crs='EPSG:4326')
result1 = gpd.sjoin(gdf_points, shp, how='left', predicate='within')

df['State'] = result1['NAME_1']

print(df)

with open('US.csv','w') as f:
    df.to_csv(f)