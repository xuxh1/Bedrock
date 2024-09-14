import os
import config

resolution = config.resolution
name = config.name
data_path = config.data_path
fig_path = config.fig_path

os.chdir('../')

def ini():
    os.system('python iniprocess/ini_ln.py')

def main():
    os.system('python main/cal_S.py')
    os.system('python main/cal_D.py')
    os.system('python main/cal_area.py')


def draw():
    os.system('python draw/draw_S_G.py')
    os.system('python draw/draw_D_G.py')
    os.system('python draw/c_plot_DFG.py')
    os.system('python draw/c_plot_mask.py')


if __name__=='__main__':
    # ini()
    # main()
    draw()