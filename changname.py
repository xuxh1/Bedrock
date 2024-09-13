import glob
import os

path = '/stu01/xuxh22/Bedrock/'
list = glob.glob(f'{path}*.txt', recursive=True)

for file in list:
    print(file)
    newfile = file.replace('.txt', '.md')
    os.system(f'mv {file} {newfile}')