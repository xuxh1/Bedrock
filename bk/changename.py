import glob
import os

def changename():
    path = '/tera04/zhwei/xionghui/bedrock/run/'
    list = glob.glob(f'{path}**/*', recursive=True)

    for file in list:
        print(file)
        newfile = file.replace('D_max_duration_per_use', 'D_duration_per_use_max')
        os.system(f'mv {file} {newfile}')

def nc2nc4():
    path = '/tera11/zhwei/students/Xionghui/data/run/500_rawdata/'
    list = glob.glob(f'{path}*.nc', recursive=True)

    for file in list:
        print(file)
        newfile = file.replace('.nc', '.nc4')
        os.system(f'cdo -f nc4 copy {file} {newfile}')

# nc2nc4()
changename()