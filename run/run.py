import os
import config

resolution = config.resolution
name = config.name
data_path = config.data_path
fig_path = config.fig_path
path = config.path

os.chdir('../')

def ini():
    os.system(f'python {path}iniprocess/ini_ln.py')

def main():
    os.system(f'python {path}main/cal_S_exp1.py')
    os.system(f'python {path}main/cal_D_exp1.py')
    os.system(f'python {path}main/cal_D_mon.py')
    os.system(f'python {path}main/count_data_G.py')
    os.system(f'python {path}main/count_data_Db.py')
    os.system(f'python {path}main/count_data_US.py')
    os.system(f'python {path}main/count_data_field.py')


def draw():
    os.system(f'python {path}draw/draw_b1_box.py')
    os.system(f'python {path}draw/draw_c1_DTB.py')
    os.system(f'python {path}draw/draw_g1_imshow.py')
    os.system(f'python {path}draw/draw_g1r1_DF.py')
    os.system(f'python {path}draw/draw_g2_scatter.py')
    os.system(f'python {path}draw/draw_h1_field.py')
    os.system(f'python {path}draw/draw_h2_histogram.py')
    os.system(f'python {path}draw/draw_l1_change.py')
    os.system(f'python {path}draw/draw_l2_latlon.py')
    os.system(f'python {path}draw/draw_r1_imshow.py')
    os.system(f'python {path}draw/draw_v1_class.py')

if __name__=='__main__':
    ini()
    main()
    # draw()