import glob
import os

path = '/stu01/xuxh22/Bedrock/fig/0p1_exp1/'
list = glob.glob(f'{path}g4_*', recursive=True)

for file in list:
    print(file)
    newfile = file.replace('g4_', 'g2_')
    os.system(f'mv {file} {newfile}')