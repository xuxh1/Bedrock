import os
import config

resolution = config.resolution
data_path = config.data_path
fig_path = config.fig_path
path = config.path

os.chdir('../')

def ini():
    os.system(f'python {path}run/ini_ln.py')

def main():
    os.system(f'python {path}main/cal_S.py')
    os.system(f'python {path}main/cal_D.py')
    os.system(f'python {path}main/dp_S.py')
    os.system(f'python {path}main/dp_D.py')
    os.system(f'python {path}main/dp_index.py')
    os.system(f'python {path}main/cmp_G.py')
    os.system(f'python {path}main/cmp_field.py')
    os.system(f'python {path}main/cmp_class.py')

    os.system(f'python {path}main_cases/cal_cases.py')
    os.system(f'python {path}main_cases/dp_cases.py')
    os.system(f'python {path}main_cases/cmp_cases.py')


def draw():
    # os.system(f'python {path}draw/draw_g2_scatter_DF.py')
    # os.system(f'python {path}draw/draw_g2_scatter_FDFMFY.py')
    # os.system(f'python {path}draw/draw_g2_scatter_Duration.py')
    # os.system(f'python {path}draw/draw_g2_scatter_S.py')
    os.system(f'python {path}draw/draw_v1_class.py')
    # os.system(f'python {path}draw/draw_g2_scatter_Db.py')
    # os.system(f'python {path}draw/draw_g2_scatter_statistics.py')
    # os.system(f'python {path}draw/draw_g2_scatter_index.py')
    # os.system(f'python {path}draw/draw_g2_scatter_DTB.py')
    # os.system(f'python {path}draw/draw_b1_box.py')
    # os.system(f'python {path}draw/draw_b2_index.py')

    # os.system(f'python {path}draw/draw_c1_DTB.py')

    # os.system(f'python {path}draw_cases/draw_g2_scatter_cases.py')
    # os.system(f'python {path}draw_cases/draw_g2_scatter_cases_diff.py')





if __name__=='__main__':
    # ini()
    # main()
    draw()