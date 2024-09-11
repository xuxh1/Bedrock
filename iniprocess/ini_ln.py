import os

def ln(resolution,name):
    path1 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}/'
    path2 = f'/tera11/zhwei/students/Xionghui/data/run/{resolution}_{name}/'
    os.makedirs(path2, exist_ok=True)
    
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
    ln('0p1','exp1')