import os
import config
from myfunc import run_command

# resolution     = config.resolution
# region         = config.region
# data_path      = config.data_path
# raw_data_path = config.raw_data_path
# shp_path       = config.shp_path
# fig_path       = config.fig_path

def cp(resolution):
    raw_data_path = f'/tera04/zhwei/xionghui/bedrock/'
    path = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}_rawdata/'
    os.makedirs(path, exist_ok=True)
    
    def rsync_data(input_file, output_file='') -> None:
        run_command(f"rsync -avP {raw_data_path}{input_file} {path}{output_file}")

    rsync_data('mask_all/mask_adequatewater/mask_adequatewater.nc4')
    rsync_data('mask_all/mask_woodyveg/mask_woodyveg.nc4')
    rsync_data('mask_all/mask_shallowbedrock/mask_shallowbedrock.nc4')

    rsync_data('Ssoil/Ssoil.nc4')
    rsync_data('diff/diff.nc')
    rsync_data(f'diff/ET_2003_2020_mean_{resolution}_mmyr_nn.nc', 'ET_mean.nc')
    rsync_data(f'diff/PR_2003_2020_mean_{resolution}_mmyr_nn.nc', 'PR_mean.nc')
    rsync_data(f'diff/Q_2003_2020_mean_{resolution}_mmyr_nn.nc', 'Q_mean.nc')
    rsync_data(f'diff/ET_2003_2020_median_{resolution}_mmyr_nn.nc', 'ET_median.nc')
    rsync_data(f'diff/PR_2003_2020_median_{resolution}_mmyr_nn.nc', 'PR_median.nc')
    rsync_data(f'diff/Q_2003_2020_median_{resolution}_mmyr_nn.nc', 'Q_median.nc')
    rsync_data(f'PET/PET_{resolution}.nc', 'PET.nc')

    rsync_data('SC/SnowCover_0p1_mask.nc4', 'SnowCover.nc4')
    rsync_data('Koppen/Koppen.nc4')
    rsync_data('IGBP/IGBP.nc4')
    rsync_data('Area/Area.nc4')
    rsync_data('C_Density/aboveground_biomass_carbon_remap.nc4', 'Aboveground.nc4')
    rsync_data('C_Density/belowground_biomass_carbon_remap.nc4', 'Belowground.nc4')
    rsync_data('500.txt')
    rsync_data('0p1.txt')

def cp_0p1(resolution):
    raw_data_path = f'/tera04/zhwei/xionghui/bedrock/'
    path = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}_rawdata/'
    os.makedirs(path, exist_ok=True)
    
    def rsync_data(input_file, output_file='') -> None:
        run_command(f"rsync -avP {raw_data_path}{input_file} {path}{output_file}")

    # rsync_data(f'mask_all/mask_adequatewater/mask_adequatewater_{resolution}.nc4','mask_adequatewater.nc4')
    # rsync_data(f'mask_all/mask_woodyveg/mask_woodyveg_{resolution}.nc4','mask_woodyveg.nc4')
    # rsync_data(f'mask_all/mask_shallowbedrock/mask_shallowbedrock_{resolution}.nc4','mask_shallowbedrock.nc4')

    # rsync_data(f'Ssoil/Ssoil_{resolution}.nc4', 'Ssoil.nc4')
    # rsync_data('diff/diff.nc')
    # rsync_data(f'diff/ET_2003_2020_mean_{resolution}_mmyr_nn.nc', 'ET_mean.nc')
    # rsync_data(f'diff/PR_2003_2020_mean_{resolution}_mmyr_nn.nc', 'PR_mean.nc')
    # rsync_data(f'diff/Q_2003_2020_mean_{resolution}_mmyr_nn.nc', 'Q_mean.nc')
    # rsync_data(f'diff/ET_2003_2020_median_{resolution}_mmyr_nn.nc', 'ET_median.nc')
    # rsync_data(f'diff/PR_2003_2020_median_{resolution}_mmyr_nn.nc', 'PR_median.nc')
    # rsync_data(f'diff/Q_2003_2020_median_{resolution}_mmyr_nn.nc', 'Q_median.nc')
    # rsync_data(f'PET/PET_{resolution}.nc', 'PET.nc')

    # rsync_data('SC/SnowCover_0p1.nc4', 'SnowCover.nc4')
    # rsync_data(f'Koppen/Koppen_{resolution}.nc4', 'Koppen.nc4')
    # rsync_data(f'IGBP/IGBP_{resolution}.nc4', 'IGBP.nc4')
    # rsync_data(f'Area/Area_{resolution}.nc4', 'Area.nc4')
    rsync_data('C_Density/aboveground_biomass_carbon_remap_0p1.nc', 'Aboveground.nc')
    rsync_data('C_Density/belowground_biomass_carbon_remap_0p1.nc', 'Belowground.nc')
    rsync_data('500.txt')
    rsync_data('0p1.txt')

def ln():
    path1 = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}_rawdata/'
    path2 = f'/tera04/zhwei/xionghui/bedrock/run/{resolution}/'

    path_0p1 = f'/tera04/zhwei/xionghui/bedrock/run/0p1/'

    os.makedirs(path2, exist_ok=True)
    os.makedirs(fig_path, exist_ok=True)
    
    # -----------------------------------DTB-----------------------------------------
    os.system(f'ln -sf {path1}mask1.nc4 {path2}mask1.nc4')
    os.system(f'ln -sf {path1}DTB.nc4 {path2}DTB.nc4')

    os.system(f'ln -sf {path1}mask12.nc4 {path2}mask12.nc4')
    os.system(f'ln -sf {path1}mask123.nc4 {path2}mask123.nc4')
    
    os.system(f'ln -sf {path1}Ssoil.nc4 {path2}Ssoil.nc4')
    
    # -----------------------------------ET and PR-----------------------------------
    os.system(f'ln -sf {path1}diff.nc4 {path2}diff.nc4')
    os.system(f'ln -sf {path1}ET_mean.nc4 {path2}ET_mean.nc4')
    os.system(f'ln -sf {path1}PR_mean.nc4 {path2}PR_mean.nc4')
    os.system(f'ln -sf {path1}Q_mean.nc4 {path2}Q_mean.nc4')
    os.system(f'ln -sf {path1}ET_median.nc4 {path2}ET_median.nc4')
    os.system(f'ln -sf {path1}PR_median.nc4 {path2}PR_median.nc4')
    os.system(f'ln -sf {path1}Q_median.nc4 {path2}Q_median.nc4')

    os.system(f'ln -sf {path1}PET.nc4 {path2}PET.nc4')

    os.system(f'ln -sf {path1}SnowCover.nc4 {path2}SnowCover.nc4')
    os.system(f'ln -sf {path1}mask3.nc4 {path2}mask3.nc4')
    
    # -----------------------------------no change-----------------------------------
    os.system(f'ln -sf {path1}mask2.nc4 {path2}mask2.nc4')

    os.system(f'ln -sf {path1}Koppen.nc4 {path2}Koppen.nc4')
    os.system(f'ln -sf {path1}IGBP.nc4 {path2}IGBP.nc4')
    os.system(f'ln -sf {path1}Area.nc4 {path2}Area.nc4')
    os.system(f'ln -sf {path1}Aboveground.nc4 {path2}Aboveground.nc4')
    os.system(f'ln -sf {path1}Belowground.nc4 {path2}Belowground.nc4')
    os.system(f'ln -sf {path1}Aboveground_mask123.nc4 {path2}Aboveground_mask123.nc4')
    os.system(f'ln -sf {path1}Belowground_mask123.nc4 {path2}Belowground_mask123.nc4')

    os.system(f'cp {path1}500.txt {path2}')
    os.system(f'cp {path1}0p1.txt {path2}')

    # ----------------------------------data-----------------------------------------
    os.system(f'ln -sf {path_0p1}Sr_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}Sbedrock_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}S_FD_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}S_Duration_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}S_Period_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}Sr_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}Sr_tmp1.nc4 {path2}')
    os.system(f'ln -sf {path_0p1}Sr_tmp1.nc4 {path2}')
    
    for year in range(2003,2021):
        os.system(f'ln -sf {path_0p1}/D/Dr_{year}_tmp1.nc4 {path2}/D/')
        os.system(f'ln -sf {path_0p1}/D/Dbedrock_{year}_tmp1.nc4 {path2}/D/')
        os.system(f'ln -sf {path_0p1}/D/D_FD_{year}_tmp1.nc4 {path2}/D/')
        os.system(f'ln -sf {path_0p1}/D/D_Duration_{year}_tmp1.nc4 {path2}/D/')
    os.system(f'ln -sf {path_0p1}/D/D_Period_tmp1.nc4 {path2}/D/')



if __name__ == '__main__':
    # cp('500')
    cp_0p1('0p1')
    # ln()
