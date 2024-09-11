import glob
import os

path = '/stu01/xuxh22/Bedrock/preprocess/'
list = glob.glob(f'{path}a_pre_*.py', recursive=True)

for file in list:
    print(file)
    newfile = file.replace('a_pre_', 'pre_')
    os.system(f'mv {file} {newfile}')