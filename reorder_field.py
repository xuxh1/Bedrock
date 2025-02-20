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

def count_field():
    df = pd.read_csv(f'{post_data_path}/field/new_literature_compilation.csv', encoding='latin-1')
    print(df)
    print(df.columns)
    df1 = df[['Full Citation', 'Citation',
       'Measurement or Estimate of RM Contribution to ET?', 'Same Site As',
       'Latitude','Longitude', 
       'Minimum', 'Maximum','Root_Depth_NumberLine_m','Maximum root depth (m)',
       'Soil Depth (cm)','SoilDepth_Numberline_cm',
       'Masked',  
       'US_RockMoisture_Validation_Site',
       'Reported Amount of Rock Moisture Use by Vegetation',
        'location',
       'Grouped location', 'observation site', 
       'Elevation (m)', 'Mean annual precipitation (MAP) (mm)',
       'MAP_Numberline_mm', 'Precipitation Delivery',
       'Mean Annual Temperature (C)', 'Stated Climate', 'Koppen Climate',
       'Species', 'Common Name',
       'Phenology (evergreen = 1, deciduous = 0, sub-deciduous = 3)',
       'All Methods',
       'Primary Method', 'Secondary Method',
       'Authors mention root mats? (1=yes; 0=no; blank = check)',
       'Authors mention mycorrhizal fungi? (1=yes, 0=no)', 'Soil Texture/Type',
       'Simplified Soil Texture/Type', 
        'Dominant Lithology', 'Grouped Lithology',
       'Is bedrock weathered?', 'Karst = 1;', 'Rock type', 'Age', 'Formation',
       'Slope (%)', 'Slope_Numberline_Percent', 'Slope aspect direction?',
       'Where on veg is slope?', 'Water table depth (m)',
       'Do authors mention possibility of tapping groundwtr? (yes = 1)',
       'Disturbance?', 'Plantation? (Y/N)']]
    
    print(df1)

    df1.to_csv(f"{post_data_path}/field/field.csv",index=False)

count_field()