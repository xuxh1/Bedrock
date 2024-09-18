import os
import config

resolution     = config.resolution
name           = config.name
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

def cp_500():
    path = f'/tera11/zhwei/students/Xionghui/data/run/500/'
    os.makedirs(path, exist_ok=True)
    os.makedirs(fig_path, exist_ok=True)
    
    # -----------------------------------DTB-----------------------------------------
    os.system(f'cp {post_data_path}mask1/mask1_v3/mask1.nc {path}mask1.nc')
    os.system(f'cp {post_data_path}mask1/mask1_v3/DTB_temp1.nc {path}DTB.nc')

    os.system(f'cp {post_data_path}mask/mask_v3/mask12.nc {path}mask12.nc')
    os.system(f'cp {post_data_path}mask/mask_v3/mask123.nc {path}mask123.nc')
    
    os.system(f'cp {post_data_path}Ssoil/Ssoil_v3/Ssoil.nc {path}Ssoil.nc')
    
    # -----------------------------------ET and PR-----------------------------------
    os.system(f'cp {post_data_path}diff/diff.nc {path}diff.nc')
    os.system(f'cp {post_data_path}diff/ET_2003_2020_mean_500_mmyr_nn.nc {path}ET.nc')
    os.system(f'cp {post_data_path}diff/PR_2003_2020_mean_500_mmyr_nn.nc {path}PR.nc')
    os.system(f'cp {post_data_path}diff/Q_2003_2020_mean_500_mmyr_nn.nc {path}Q.nc')

    os.system(f'cp {post_data_path}SC/SnowCover_0p1.nc {path}SnowCover.nc')
    os.system(f'cp {post_data_path}mask3/mask3.nc {path}mask3.nc')
    
    # -----------------------------------no change-----------------------------------
    os.system(f'cp {post_data_path}mask2/mask2.nc {path}mask2.nc')

    os.system(f'cp {post_data_path}Koppen/Koppen.nc {path}Koppen.nc')
    os.system(f'cp {post_data_path}IGBP/IGBP.nc {path}IGBP.nc')
    os.system(f'cp {post_data_path}Area/Area.nc {path}Area.nc')
    os.system(f'cp {post_data_path}C_Density/aboveground_biomass_carbon_remap.nc {path}Aboveground.nc')
    os.system(f'cp {post_data_path}C_Density/belowground_biomass_carbon_remap.nc {path}Belowground.nc')

    os.system(f'cp {post_data_path}500.txt {path}')
    os.system(f'cp {post_data_path}0p1.txt {path}')

def ln():
    path1 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}_{name}/'
    os.makedirs(path2, exist_ok=True)
    os.makedirs(fig_path, exist_ok=True)
    
    # -----------------------------------DTB-----------------------------------------
    os.system(f'ln -sf {path1}mask1.nc {path2}mask1.nc')
    os.system(f'ln -sf {path1}DTB.nc {path2}DTB.nc')

    os.system(f'ln -sf {path1}mask12.nc {path2}mask12.nc')
    os.system(f'ln -sf {path1}mask123.nc {path2}mask123.nc')
    
    os.system(f'ln -sf {path1}Ssoil.nc {path2}Ssoil.nc')
    
    # -----------------------------------ET and PR-----------------------------------
    os.system(f'ln -sf {path1}diff.nc {path2}diff.nc')
    os.system(f'ln -sf {path1}ET.nc {path2}ET.nc')
    os.system(f'ln -sf {path1}PR.nc {path2}PR.nc')
    os.system(f'ln -sf {path1}Q.nc {path2}Q.nc')

    os.system(f'ln -sf {path1}SnowCover.nc {path2}SnowCover.nc')
    os.system(f'ln -sf {path1}mask3.nc {path2}mask3.nc')
    
    # -----------------------------------no change-----------------------------------
    os.system(f'ln -sf {path1}mask2.nc {path2}mask2.nc')

    os.system(f'ln -sf {path1}Koppen.nc {path2}Koppen.nc')
    os.system(f'ln -sf {path1}IGBP.nc {path2}IGBP.nc')
    os.system(f'ln -sf {path1}Area.nc {path2}Area.nc')
    os.system(f'ln -sf {path1}Aboveground.nc {path2}Aboveground.nc')
    os.system(f'ln -sf {path1}Belowground.nc {path2}Belowground.nc')

    os.system(f'cp {path1}500.txt {path2}')
    os.system(f'cp {path1}0p1.txt {path2}')

if __name__ == '__main__':
    # cp_500()
    ln()
