import pandas as pd
from plotnine import *
from pylab import rcParams
import matplotlib
import matplotlib.colors as colors
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path

print('python draw_h2_historgram.py')

font = {'family': 'Times New Roman'}
matplotlib.rc('font', **font)

params = {'backend': 'ps',
          'axes.labelsize': 25,
          'grid.linewidth': 0.2,
          'font.size': 25,
          'legend.fontsize': 18,
          'legend.frameon': False,
          'xtick.labelsize': 30,
          'xtick.direction': 'out',
          'ytick.labelsize': 30,
          'ytick.direction': 'out',
          'legend.handlelength': 1,
          'legend.handleheight': 1,
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          "mathtext.default":"regular",
          'text.usetex': False}
rcParams.update(params)

df = pd.read_csv(f'{data_path}/csv/Global.csv')
rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
cmap = colors.ListedColormap(rgb_list)

def plot_bar():
    df_area = df.copy()
    df1 = pd.DataFrame()
    df1['Sr'] = df_area.groupby('Continent')['Sr'].mean()
    df1['Sbedrock'] = df_area.groupby('Continent')['Sbedrock'].mean()
    df1['Ssoil'] = df_area.groupby('Continent')['Ssoil'].mean()
    df1['Continent'] = df1.index
    print(df1)
    df2 = df1.set_index('Continent').transpose()
    print(df2)
    df2['name'] = df2.index
    for column in [col for col in df2.columns if 'name' not in col]:
        print(column)
        print(df2[column])
        # exit(0)
        base_hist = (ggplot(df2, aes(x=df2['name'],y=df2[column], fill=df2['name'])) +
                    geom_col(stat="identity", position="dodge")+
                    # scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl') +
                    theme(
                        text=element_text(size=13, color="black"),
                        plot_title=element_text(size=15),
                        aspect_ratio=1.15,
                        figure_size=(5, 5)
                    )+
                    ylim(0, 400)+  
                    labs(x=None, y="mean value (mm)")+
                    guides(fill=False)+
                    scale_fill_manual(values=rgb_list)
                    # ggtitle(column)
                    )
        base_hist.save(f'{fig_path}/h2_{column}.png')

plot_bar()