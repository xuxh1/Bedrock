import glob
import os

def changename():
    path = '/tera11/zhwei/students/Xionghui/wetland/cases/bedrock_1/tmp/'
    list = glob.glob(f'{path}ssoil_*', recursive=True)

    for file in list:
        print(file)
        newfile = file.replace('ssoil_', 'saws_')
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