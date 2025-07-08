import os
import xarray as xr
import numpy as np
import netCDF4 as nc
import shutil
import subprocess
from math import radians, sin
from pyproj import Geod
from shapely.geometry import Point, LineString, Polygon
import glob
from joblib import Parallel, delayed
from tqdm import tqdm, trange
from myfunc import timer, run_command
import math

path = '/tera04/zhwei/xionghui/bedrock/'

"""
Calculate the mask procedure include: 
1. mask area without adequate water (sum ET>P from 2003 to 2020)
2. mask area without woody vegetation (IGBP=1~9)
3. mask area without shallow bedrock (DTB<150cm)
the mask procedure4 need to calculate after the Dbedrock calculation.
"""
def mask():
    def mask_adequatewater() -> None:
        diff_file = os.path.join(path, 'diff', 'diff.nc')
        dir_path = os.path.join(path, 'mask_all', 'mask_adequatewater')
        os.makedirs(dir_path, exist_ok=True)
        output_sum = os.path.join(dir_path, 'diff_sum.nc4')
        output_interp = os.path.join(dir_path, 'diff_sum_interp.nc4')
        mask_file = os.path.join(dir_path, 'mask_adequatewater.nc4')
        run_command(f"cdo -f nc4 -P 48 timsum {diff_file} {output_sum}")
        run_command(f"gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts 86400 43200 -overwrite {output_sum} {output_interp}")
        run_command(f"cdo -f nc4 -z zip -setrtoc2,0,inf,nan,1 {output_interp} {mask_file}")
        print("mask_adequatewater completed")

    def mask_woodyveg() -> None:
        dir_path = os.path.join(path, 'mask_all', 'mask_woodyveg')
        os.makedirs(dir_path, exist_ok=True)
        igbp_file = os.path.join(dir_path, 'global_igbp_15s_2020.nc')
        mask_file = os.path.join(dir_path, 'mask_woodyveg.nc4')
        run_command(f"cdo -f nc4 -z zip -setrtoc2,1,9,1,nan {igbp_file} {mask_file}")
        print("mask_woodyveg completed")

    def mask_shallowbedrock() -> None:
        dir_path = os.path.join(path, 'mask_all', 'mask_shallowbedrock')
        os.makedirs(dir_path, exist_ok=True)
        dtb_file = os.path.join(dir_path, 'average_soil_and_sedimentary-deposit_thickness_remap_cm.nc')
        output_interp = os.path.join(dir_path, 'dtb_interp.nc4')
        mask_file = os.path.join(dir_path, 'mask_shallowbedrock.nc4')
        run_command(f"gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts 86400 43200 -overwrite {dtb_file} {output_interp}")
        run_command(f"cdo -f nc4 -z zip -setrtoc2,0,150,1,nan {output_interp} {mask_file}")
        print("mask_shallowbedrock completed")
    
    mask_adequatewater()
    mask_woodyveg()
    mask_shallowbedrock()


"""
Calculate the Ssoil:
1. calculate the DTB stratification (0~5~15~30~60~100~150 cm) to align the SAWS stratification (0~5~15~30~60~100~200 cm)
2. use the vertical stratification (DTB and SAWS) to calculate the Ssoil
""" 
def Ssoil() -> None:
    layer = [0, 5, 15, 30, 60, 100, 150]
    dir_path = os.path.join(path, 'Ssoil')
    os.makedirs(dir_path, exist_ok=True)
    saws_path = os.path.join(dir_path, 'SAWS_Kosugi')
    ssoil_file = os.path.join(dir_path, f'Ssoil.nc4')

    def DTB_layer() -> None:
        dtb_file = os.path.join(dir_path, 'average_soil_and_sedimentary-deposit_thickness_remap_cm.nc')
        image = xr.open_dataset(dtb_file)
        s = image['Band1']
        for i in range(len(layer)-1):
            dtb_layer_file = os.path.join(dir_path, f'DTB_layer{i+1}.nc')
            delta_s = s - layer[i]
            delta_s = np.where(delta_s>(layer[i+1]-layer[i]), (layer[i+1]-layer[i]), delta_s)
            delta_s = np.where(delta_s<0, 0, delta_s)
            
            shutil.copyfile(f'{saws_path}/saws{i+1}.nc', dtb_layer_file)
            with nc.Dataset(dtb_layer_file, 'a') as file:
                s_var = file.variables['Band1']
                s_var[:,:] = delta_s      
        print("DTB_layer completed")

    DTB_layer()
    for i in range(len(layer)-1):
        dtb_layer_file = os.path.join(dir_path, f'DTB_layer{i+1}.nc')
        saws_layer_file = os.path.join(dir_path, f'saws{i+1}.nc')
        ssoil_layer_file = os.path.join(dir_path, f'Ssoil_layer{i+1}.nc4')
        run_command(f'ln -sf {saws_path}/saws{i+1}.nc {saws_layer_file}')
        run_command(f'cdo -f nc4 -z zip -mulc,10 -mul {saws_layer_file} {dtb_layer_file} {ssoil_layer_file}')
    filelist = [f'{dir_path}/Ssoil_layer{i+1}.nc4' for i in range(len(layer)-1)]
    filelistname = ' '.join(filelist)
    run_command(f'cdo -f nc4 -z zip -enssum {filelistname} {ssoil_file}')
    print("Ssoil completed")

"""
Calculate some other variables include:
1. SnowCover: convert the snowcover(%) to if snow(0 and 1)
2. IGBP: sel the time
3. Koppen: translate the tif to nc4, and remaplaf from 1km to 500m
4. area: calculate the area for 500m and 0p1
5. DTB: calculate some DTB for different sources
wrong!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
def other():
    def SnowCover():
        # py_file = os.path.join('/stu01/xuxh22/Bedrock/preprocess/', 'pre_SC.py')
        # run_command(f'python {py_file}')
        dir_path = os.path.join(path, 'SC')
        os.makedirs(dir_path, exist_ok=True)
        sc_0p05_file = os.path.join(dir_path, 'SnowCover_0p05.nc')
        sc_0p1_file = os.path.join(dir_path, 'SnowCover_0p1.nc4')
        sc_0p1_mask_file = os.path.join(dir_path, 'SnowCover_0p1_mask.nc4')
        # The snow cover fraction should be kept at the same resolution as diff_3.nc of Sr and Dr Data, from 0.05° to 0.1°
        run_command(f"gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts 3600 1800 -overwrite {sc_0p05_file} {sc_0p1_file}")
        run_command(f'cdo -f nc4 -z zip -setrtoc2,10,100,0,1 {sc_0p1_file} {sc_0p1_mask_file}')
        print("SnowCover completed")

    def IGBP():
        dir_path = os.path.join(path, 'IGBP')
        os.makedirs(dir_path, exist_ok=True)
        origin_file = os.path.join(dir_path, 'global_igbp_15s_2020.nc')
        igbp_file = os.path.join(dir_path, 'IGBP.nc4')
        run_command(f'cdo -f nc4 -z zip -seltimestep,1 {origin_file} {igbp_file}')
        print("IGBP completed")

    def Koppen():
        dir_path = os.path.join(path, 'Koppen')
        os.makedirs(dir_path, exist_ok=True)
        origin_tif_file = os.path.join(dir_path, 'Beck_KG_V1_present_0p0083.tif')
        origin_nc4_file = os.path.join(dir_path, 'Beck_KG_V1_present_0p0083.nc4')
        remap_file = os.path.join(path, '500.txt')
        koppen_file = os.path.join(dir_path, 'Koppen.nc4')
        run_command(f"gdal_translate -of netCDF -co FORMAT=NC4 -a_srs EPSG:4326 {origin_tif_file} {origin_nc4_file}")
        run_command(f"cdo -f nc4 -z zip -b I32 -P 48 --no_remap_weights remaplaf,{remap_file} {origin_nc4_file} {koppen_file}")
        print("Koppen completed")

    def area():
        dir_path = os.path.join(path, 'Area')
        os.makedirs(dir_path, exist_ok=True)
        data_file = os.path.join(path, 'diff', 'diff.nc')
        area_file = os.path.join(dir_path, 'Area.nc')
        # area_file = os.path.join(dir_path, 'Area_0p1.nc')

        def count_area(lat1,lat2):
            lat1,lat2 = map(radians,[lat1,lat2])
            r = 6.37122e6
            dlon = 0.00416666688397527
            # dlon = 0.1
            dlon_rad = math.radians(dlon)
            area = abs(r**2 * dlon_rad * (sin(lat2)-sin(lat1)))
            # print(area)
            return area

        data = xr.open_dataset(data_file)
        lat = data['lat']
        lon = data['lon']
        inc = 0.00416666688397527
        # inc = 0.1
        lat1 = lat-inc/2
        lat2 = lat+inc/2    
        grid1,grid2 = np.meshgrid(lon, lat)
        area = np.zeros_like(grid1)
        result = Parallel(n_jobs=12)(delayed(count_area)(lat1[i], lat2[i]) for i in range(len(lat)))
        for i in range(len(lat)):
            area[i, :] = result[i]
            print(area[i,0])
        print(f'The total area of the earth: {np.sum(area):.3f} $m^2$')
                
        output_ds = xr.Dataset({'area': (('lat', 'lon'), area)},
                            coords={'lat': data['lat'], 'lon': data['lon']})
        print(area)
        print(f'The total area of the earth: {np.sum(area)/1e12:.3f} million $km^2$')
        output_ds.to_netcdf(area_file)
        print("Area completed")

    def DTB():
        # Iowa measured data, the data is given by Shangguan et al.
        dir_path = os.path.join(path, 'DTB', 'DTB_Iowa')
        os.makedirs(dir_path, exist_ok=True)
        tif_file = os.path.join(dir_path, 'Iowa.tif')
        nc_file = os.path.join(dir_path, 'Iowa.nc4')
        run_command(f'gdal_translate -of netCDF -co FORMAT=NC4 -a_srs EPSG:4326 {tif_file} {nc_file}')
        
        # Send the processed Soilgrids data cp over
        dir_path = os.path.join(path, 'DTB', 'DTB_Shangguan')
        os.makedirs(dir_path, exist_ok=True)
        tif_file = os.path.join(dir_path, 'BDTICM_M_250m_ll.tif')
        nc_file = os.path.join(dir_path, 'DTB_Shangguan.nc4')
        run_command(f"gdalwarp -multi -wo NUM_THREADS=48 -ot Float32 -of netCDF -co FORMAT=NC4 -r bilinear -ts 86400 43200 -t_srs EPSG:4326 -te -180 -90 180 90 -overwrite {tif_file} {nc_file}")
        
        # gNATSGO bedrock data exported by GEE, 2 of which contains the Iowa region
        dir_path = os.path.join(path, 'DTB', 'DTB_gNATSGO')
        os.makedirs(dir_path, exist_ok=True)
        gNATSGO_file = os.path.join(dir_path, 'DTB_gNATSGO.nc4')
        for i in range(8):
            tif_file = os.path.join(dir_path, f'Bedrock_US_gNATSGO_90m-{i+1}.tif')
            nc_file = os.path.join(dir_path, f'Bedrock_US_gNATSGO_90m-{i+1}.nc4')
            run_command(f'gdal_translate -of netCDF -co FORMAT=NC4 -a_srs EPSG:4326 {tif_file} {nc_file}')
        filelist = [f'{dir_path}/Bedrock_US_gNATSGO_90m-{i}.nc4' for i in range(5, 9)] + [f'{dir_path}Bedrock_US_gNATSGO_90m-{i}.nc4' for i in range(1, 5)]
        filelistname = ' '.join(filelist)
        run_command(f'cdo -f nc4 -z zip -collgrid {filelistname} {gNATSGO_file}')

    SnowCover()
    IGBP()
    Koppen()
    area()
    DTB()

if __name__ =='__main__':
    # mask()
    # Ssoil()
    other()
