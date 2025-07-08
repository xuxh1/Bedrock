import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from myfunc import timer
from myfunc import DirMan
import config

resolution     = config.resolution
name           = config.name
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

print('python draw_h1_field.py')

pd.set_option('display.max_columns', None)

def fDTB():
    roots = pd.read_csv(f'{data_path}DTB.csv', encoding='latin-1')
    print(roots)

    barplot = pd.DataFrame()
    barplot = roots[['number','Field','gNATSGO','SoilGrids250m','SoilGrids250m_rev','Pelletier']].copy()
    #barplot = barplot.dropna()
    barplot['Name'] = (barplot['number']).astype(str) # make name column string

    # barplot = barplot[0:20]
    barplot = barplot.sort_values(by = 'number')
    barplot = barplot.dropna()
    print(barplot)

    # Make labels for X-axis to have accurate Ssoil and Dbedrock meanings
    # soillabels = list(np.arange(150, -50, step=-50))
    dlabels = list(np.arange(0, 1600, step=200))
    # labels = soillabels + dlabels
    labels = dlabels

    # Plot figure
    plt.figure(figsize = (3, 2.5), dpi=300)
    #plt.barh(barplot['Name'],barplot['Mean_D_bedrock_mm'], xerr = barplot['Stdev_D_bedrock_mm'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['SoilGrids250m'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['Pelletier'], color = '#91755a',alpha=0.5)

    plt.plot(barplot['Field'],barplot['Name'], 'o', ms=5, markerfacecolor="black", markeredgecolor='black', markeredgewidth=0.5)
    plt.plot(barplot['gNATSGO'],barplot['Name'],'o', ms=5, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.5)

    # plt.xticks(np.arange(-150, 2050, step=50), labels = labels)
    plt.xticks(np.arange(0, 1600, step=200), labels = labels)

    # plt.xlim(-150, 2000)
    plt.xlim(0, 1400)
    plt.gca().invert_yaxis()
    plt.xticks(rotation=90)
    plt.tight_layout()

    ## Uncomment for downloading fig
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig(f"{fig_path}/h1_fDTB.pdf", transparent=True)
    # files.download("doublebar.pdf")
      
def fSb():
    ## Extract Columns for Barplot (NOTE: Must exclude first header row manually)
    roots = pd.read_csv(f'{data_path}site.csv', encoding='latin-1')
    print(roots)
    roots = roots[roots['Sbedrock_field_min'] > 0]
    roots = roots.sort_values(by=['lon', 'lat']).reset_index(drop=True)
    barplot = pd.DataFrame()
    barplot = roots.copy()
    print(barplot)

    #barplot = barplot.dropna()
    barplot['Ssoil'] = barplot['Ssoil'] * -1
    barplot['Name'] = np.arange(1,9,1)

    barplot = barplot[0:20]
    # barplot = barplot.sort_values(by = 'Number_For_Plotting')
    print(barplot)

    # Make labels for X-axis to have accurate Ssoil and Dbedrock meanings
    soillabels = list(np.arange(300, -100, step=-100))
    dlabels = list(np.arange(100, 600, step=100))
    labels = soillabels + dlabels

    # Plot figure
    plt.figure(figsize = (3, 2.5), dpi=300)
    #plt.barh(barplot['Name'],barplot['Mean_D_bedrock_mm'], xerr = barplot['Stdev_D_bedrock_mm'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['Ssoil'], alpha=0.5, ecolor='black', capsize=3)
    plt.barh(barplot['Name'],barplot['Sbedrock'], color = '#91755a',alpha=0.5)

    plt.plot(barplot['Sbedrock_field_min'],barplot['Name'], 'o', ms=5, markerfacecolor="black", markeredgecolor='black', markeredgewidth=0.5)
    plt.plot(barplot['Sbedrock_field_max'],barplot['Name'],'o', ms=5, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.5)

    # plt.xticks(np.arange(-150, 2050, step=50), labels = labels)
    # plt.xticks(np.arange(0, 1600, step=200), labels = labels)
    yticks = ['1','$2^{{Δ}}$','3','$4^{{*}}$','$5^{{*}}$','$6^{{Δ}}$','7','8']
    plt.ylim(0, 9)
    plt.yticks(np.arange(1, 9, 1), labels = yticks)
    plt.xticks(np.arange(-300, 600, step=100), labels = labels)
    plt.xlim(-300, 500)
    plt.gca().invert_yaxis()
    plt.xticks(rotation=90)
    ax = plt.gca()
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    # ax.spines['left'].set_color('none')
    
    ## Uncomment for downloading fig
    plt.tight_layout()
    plt.rcParams['pdf.fonttype'] = 42
    plt.savefig(f"{fig_path}/h1_fSb.pdf", transparent=True)

fDTB()
fSb()
