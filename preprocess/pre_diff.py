import os
import subprocess
from joblib import Parallel, delayed

def cdo_set(n1,n2):
    os.system(f'cdo -setrtoc,-inf,0,0 {n1} {n2}')

path = "/tera04/zhwei/xionghui/bedrock/"
print(path)
# def mv_ET():
#     filelist = subprocess.getoutput(f'ls {path}/ET/').split("\n")
#     for file in filelist:
#         filename = file[13:].split("_2003")[0]
#         print(file)
#         os.makedirs(f'./ET/{filename}', exist_ok=True)
#         os.system(f'mv {file} ./ET/{filename}/')

def nn_ln():
    filelist = subprocess.getoutput(f'ls {path}/ET/').split("\n")
    print(filelist)
    Parallel(n_jobs=5)(delayed(cdo_set)(f'{path}/ET/{file}/ET_{file}_2003_2020_8D_0p1_mm8d.nc', f"{path}/ET/{file}/ET_{file}_2003_2020_8D_0p1_mm8d_nn.nc") for file in filelist)
    for file in filelist:
        # os.system(f'cdo -setrtoc2,0,150,1,nan')
        os.system(f'ln -sf {path}/ET/{file}/ET_{file}_2003_2020_8D_0p1_mm8d_nn.nc {path}/diff/ET_{file}_2003_2020_8D_0p1_mm8d_nn.nc')
        
    filelist = subprocess.getoutput(f'ls {path}/PR/').split("\n")
    print(filelist)
    Parallel(n_jobs=5)(delayed(cdo_set)(f'{path}/PR/{file}/PR_{file}_2003_2020_8D_0p1_mm8d.nc', f"{path}/PR/{file}/PR_{file}_2003_2020_8D_0p1_mm8d_nn.nc") for file in filelist)
    for file in filelist:
        os.system(f'ln -sf {path}/PR/{file}/PR_{file}_2003_2020_8D_0p1_mm8d_nn.nc {path}/diff/PR_{file}_2003_2020_8D_0p1_mm8d_nn.nc')

def ensmean_sub():
    os.chdir(f'{path}/diff/')
    
    filelist = subprocess.getoutput(f'ls ET*').split("\n")
    filelistname = ' '.join(file for file in filelist)
    print(filelistname)
    os.system(f'cdo ensmean {filelistname} ET_2003_2020_8D_0p1_mm8d_nn.nc')
    
    filelist = subprocess.getoutput(f'ls PR*').split("\n")
    filelistname = ' '.join(file for file in filelist)
    print(filelistname)
    os.system(f'cdo ensmean {filelistname} PR_2003_2020_8D_0p1_mm8d_nn.nc')
    
    os.system('cdo sub ET_2003_2020_8D_0p1_mm8d_nn.nc PR_2003_2020_8D_0p1_mm8d_nn.nc diff.nc')
    
def year():
    os.chdir(f'{path}/diff/')
    
    os.system('cdo yearsum ET_2003_2020_8D_0p1_mm8d_nn.nc ET_2003_2020_yr_0p1_mmyr_nn.nc')
    os.system('cdo yearsum PR_2003_2020_8D_0p1_mm8d_nn.nc PR_2003_2020_yr_0p1_mmyr_nn.nc')
    
    os.system('cdo timmean ET_2003_2020_yr_0p1_mmyr_nn.nc ET_2003_2020_mean_0p1_mmyr_nn.nc')
    os.system('cdo timmean PR_2003_2020_yr_0p1_mmyr_nn.nc PR_2003_2020_mean_0p1_mmyr_nn.nc')
    
    os.system('cdo remapbil,../500.txt ET_2003_2020_mean_0p1_mmyr_nn.nc ET_2003_2020_mean_500_mmyr_nn.nc')
    os.system('cdo remapbil,../500.txt PR_2003_2020_mean_0p1_mmyr_nn.nc PR_2003_2020_mean_500_mmyr_nn.nc')


nn_ln()
ensmean_sub()
year()

