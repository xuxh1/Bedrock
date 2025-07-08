import os
import subprocess

path = '/tera11/zhwei/students/Xionghui/data/Ssoil/'
output = subprocess.getoutput(f'ls {path}*_mulp.nc').split('\n')

for i,name in enumerate(output):
    print(i,name)
    namenew = name.replace(f'pawl{i}',f'pawl{i+1}')
    print(namenew)
    os.system(f'mv {name} {namenew}')

