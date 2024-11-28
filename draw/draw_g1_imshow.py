import os
import cmaps
import salem
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from pylab import rcParams
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from myfunc import timer
from myfunc import DirMan
import config

resolution = config.resolution
name       = config.name
region     = config.region
data_path  = config.data_path
shp_path   = config.shp_path
fig_path   = config.fig_path

print('python draw_g1_imshow.py')

shp = gpd.GeoDataFrame.from_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

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

@timer
def data_process(name):
    image = xr.open_dataset(f'{data_path}/{name[0]}.nc').sel(lon=slice(region[0],region[1]),lat=slice(region[2],region[3]))
    s = image[f'{name[1]}']
    s = s.salem.roi(shape=shp)
    print(image)
    print(s.min(),s.max())

    image.close()

    if ((name[1]=='LC') or (name[1]=='tp') or (name[1]=='et')):
        s = s[0,:,:]

    if (name[2]=='Sb') or (name[2]=='Sp') or (name[1]=='FD') or (name[1]=='Dr'):
        s = np.where(s<=0, np.nan, s)   
    s = np.where(s==0, np.nan, s)    
    s = np.ma.masked_where(np.isnan(s), s)  

    df_s = pd.read_csv(f'{data_path}site.csv')
    df2 = df_s.copy()

    return s,df2

@timer
def set_fig():
    fig = plt.figure(figsize=(12, 6), dpi=500)

    fig.subplots_adjust(left=0.05, right=0.98, 
                    bottom=0.14, top=0.95, hspace=0.25) 
        
    #Create a subgraph grid with 2 rows and 3 columns
    gs = GridSpec(2, 6)
    ax = fig.add_subplot(gs[:, :], projection=ccrs.PlateCarree())
    return fig,ax

@timer
def set_ax(ax,s,df2,cmap,level):
    if name[2] == 'Sb':
        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors="#153aab", label='Report of roots \npenetrating bedrock, unmask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'Y')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="#153aab", facecolors='none', label='Report of roots \npenetrating bedrock, mask', zorder=2)

        df3 = df2[(df2['mask'] == 1) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors="red", label='Report of bedrock water contribution \nto ET from unsaturated zone, unmask', zorder=2)
        
        df3 = df2[(df2['mask'] != 0) & (df2['Measure'] == 'N')]
        print(df3)
        ax.scatter(df3['lon'], df3['lat'], marker='o',
                        s=20, linewidths=1, edgecolors="red", facecolors='none', label='Report of bedrock water contribution \nto ET from unsaturated zone, mask', zorder=2)
        
        ax.legend(fontsize=12 ,bbox_to_anchor=(0.29, 0.379))

    # Set drawing mode(note:extent's lat from positive to negative)
    img = ax.imshow(s, cmap=cmap,
                    extent=[region[0], region[1], region[3], region[2]],
                    vmin=level[0], vmax=level[-1])
    
    ax.set_xlim(region[0], region[1])
    ax.set_ylim(region[2], region[3])
    # arr_x = np.arange(region[0],region[1]+1,60)
    # arr_y = np.arange(region[2],region[3]+1,30)
    
    # ax.set_title(f'Sbedrock', fontsize=16, pad=10)
    # ax.set_xticks(arr_x)
    # ax.set_xticklabels(arr_x,fontsize=12)
    # ax.set_yticks(arr_y)
    # ax.set_yticklabels(arr_y,fontsize=12)
    
    ax.add_feature(cfeature.COASTLINE)
    # ax.add_feature(cfeature.BORDERS, linestyle=':')
    # ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    # ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')

    ax.set_extent(region)
    # ax.set_global()
    
    # ax.gridlines(draw_labels=True)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    return img

@timer
def set_colorbar(name,img,level,fig):
    # From the bottom left corner x, y, width, height
    cbar_ax = fig.add_axes([0.1, 0.1, 0.8, 0.04], frameon = False) 
    cb = fig.colorbar(img, 
                    drawedges=False,
                    ticks=level, 
                    cax=cbar_ax, 
                    orientation='horizontal',
                    spacing='uniform')
    cb.ax.tick_params(labelsize=12)
    cb.set_label(f'{name[3]}', fontsize=30, fontweight='bold')

def set_legend(fig,name):
    if name[2]=='IGBP':
        RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
                '#009900','#c6b044', '#dcd159', '#dade48',  
                '#fbff13','#b6ff05', '#27ff87', '#c24f44', 
                '#a5a5a5', '#ff6d4c','#69fff8', '#f9ffa4', 
                '#1c0dff', 'white', 'white', 'white']
        labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
                 'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
                'Savannas', 'Grasslands', 'Permanent Wetlands', 'Croplands',
                 'Urban and Built-up Lands', 'Cropland/Natural Vegetation Mosaics','Permanent Snow and Ice', 'Barren',
                 'Water Bodies', '', '', '']
        # RGBs = ['#05450a', '#086a10', '#54a708', '#78d203', 
        #         '#009900','#c6b044', '#dcd159', '#dade48',  
        #         '#fbff13']
        # labels = ['Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests', 'Deciduous Needleleaf Forests, Open Space','Deciduous Broadleaf Forests',
        #          'Mixed Forests','Closed Shrublands', 'Open Shrublands', 'Woody Savannas', 
        #         'Savannas']
        # From the bottom left corner x, y, width, height
        legend_ax = fig.add_axes([0, 0.03, 1, 0.06], frameon=False)
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(RGBs, labels)]

        legend = legend_ax.legend(handles=legend_patches, loc='center', fontsize=12, frameon=False, ncol=5, edgecolor='black', columnspacing=1.5)
    elif name[2]=='Koppen':
        RGBs = ['#0000FF', '#0078FF', '#46AAFA', 'white', '#FF0000', '#FF9696', '#F5A500', '#FFDC64', '#FFFF00', '#C8C800', '#969600', 'white', '#96FF96',
                '#64C864', '#329632', 'white', '#C8FF50', '#64FF32', '#32C800', 'white', '#FF00FF', '#C800C8', '#963296', '#966496', '#AAAFFF', '#5A78DC',
                '#4B50B4', '#320087', '#00FFFF', '#37C8FF', '#007D7D', '#00465F', '#B3B3B3', '#666666', 'white', 'white']
        labels = ['Af', 'Am', 'Aw', '', 'BWh', 'BWk', 'BSh', 'BSk', 'Csa', 'Csb', 'Csc', '', 'Cwa', 'Cwb', 'Cwc', '', 'Cfa', 'Cfb', 'Cfc', '', 'Dsa', 
                  'Dsb', 'Dsc', 'Dsd', 'Dwa', 'Dwb', 'Dwc', 'Dwd', 'Dfa', 'Dfb', 'Dfc', 'Dfd', 'ET', 'EF', '', '', ]
        # From the bottom left corner x, y, width, height
        legend_ax = fig.add_axes([0, 0.02, 1, 0.06], frameon=False)
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(RGBs, labels)]

        legend = legend_ax.legend(handles=legend_patches, loc='center', fontsize=16, frameon=False, ncol=9, edgecolor='black', columnspacing=2)

    legend_ax.set_xticks([])
    legend_ax.set_yticks([])
    legend_ax.set_xticklabels([])
    legend_ax.set_yticklabels([])

@timer
def draw(name,level,cmap):
    legend_list1 = ['IGBP', 'Koppen']
    legend_list2 = ['mask1', 'mask2', 'mask3', 'mask12', 'mask123']

    df1,df2 = data_process(name)
    fig,ax = set_fig()
    img = set_ax(ax,df1,df2,cmap,level)
    if name[2] in legend_list1:
        set_legend(fig,name)
    elif name[2] in legend_list2:
        print('no use colorbar')
    else:
        set_colorbar(name,img,level,fig)

    plt.savefig(f"{fig_path}/g1_{name[2]}.png")
    plt.close(fig)

level1 = np.arange(0,500,50)
level2 = np.arange(-300,350,50)
level3 = np.arange(0,120,20)
level4 = np.arange(-100,125,25)
level5 = np.arange(0,300,50)

rgb_list = ['#606060','#8ec0cb','#00CC66','#66CC00',
                                '#69aa4c','#CCCC00','#ebc874','#99004C','#FF6666']
cmap1 = colors.ListedColormap(rgb_list)
cmap2 = 'BrBG'
rgb_list = ['#403990','#80a6e2','#fbdd85', '#f46f43', '#cf3d3e']
cmap3 = colors.ListedColormap(rgb_list)
cmap4 = "bwr"

def Sb():
    name = ['Sbedrock', 'Sr', 'Sb', '$S_{{bedrock}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    name = ['Sbedrock', 'Sr', 'Sb_n2p', '$S_{{bedrock}}$ (mm)']
    level = level2
    cmap = cmap2
    draw(name,level,cmap)
    name = ['Sbedrock_temp1', 'Sr', 'Sb_n2p_nm', '$S_{{bedrock}}$ (mm)']
    level = level2
    cmap = cmap2
    draw(name,level,cmap)

def Sr():
    name = ['Sr', 'Sr', 'Sr', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    name = ['Sr_temp1', 'Sr', 'Sr_nm', '$S_{{r}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)
    
def Ss():
    name = ['Ssoil', 'Band1', 'Ss', '$S_{{soil}}$ (mm)']
    level = level1
    cmap = cmap1
    draw(name,level,cmap)

def PR_ET_Q_LH():
    name = ['PR', 'tp', 'PR', 'Precipitation (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['ET', 'et', 'ET', 'Evapotranspiration (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['Q', 'tp', 'Q', 'Streamflow (mm)']
    level = np.arange(0,1600,400)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['LH', 'Ee', 'LH', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,100,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)
    name = ['LH_temp1', 'Ee', 'LH_nm', 'Latent Heat (W/$m^{{2}}$)']
    level = np.arange(0,100,10)
    cmap = cmaps.WhiteBlue
    draw(name,level,cmap)

def P1():
    name = ['Proportion1', 'Sr', 'P1', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    name = ['Proportion1', 'Sr', 'P1_n2p', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
    name = ['Proportion1_temp1', 'Sr', 'P1_n2p_nm', '$S_{{bedrock}}$/$S_{{r}}$']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
        
def P2():
    name = ['Proportion2', 'Sr', 'P2', '$S_{{bedrock}}$/ET']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    name = ['Proportion2', 'Sr', 'P2_n2p', '$S_{{bedrock}}$/ET']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
    name = ['Proportion2_temp1', 'Sr', 'P2_n2p_nm', '$S_{{bedrock}}$/ET']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)

def P3():
    name = ['Proportion3', 'tp', 'P3', 'Q/PR']
    level = level3
    cmap = cmap3
    draw(name,level,cmap)
    name = ['Proportion3', 'tp', 'P3_n2p', 'Q/PR']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
    name = ['Proportion3_temp1', 'tp', 'P3_n2p_nm', 'Q/PR']
    level = level4
    cmap = cmap4
    draw(name,level,cmap)
    
def FD():
    name = ['FD', 'FD', 'FD', 'First Day']
    level = np.arange(0,900,150)
    cmap = cmaps.StepSeq25_r
    draw(name,level,cmap)
    name = ['FD_mean', 'FD', 'FD_mean', 'First Day']
    level = level5
    cmap = cmaps.StepSeq25_r
    draw(name,level,cmap)

def DTB():
    name = ['DTB', 'Band1', 'DTB', 'DTB (cm)']
    level = np.arange(0,300,25)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.CBR_drywet
    draw(name,level,cmap)
    name = ['DTB_mask2', 'Band1', 'DTB_mask2', 'DTB (cm)']
    level = np.arange(0,300,25)
    # rgb_list = ['#ed4a69', '#6c7bbc', '#65677e']
    # cmap = colors.ListedColormap(rgb_list)
    cmap = cmaps.CBR_drywet
    draw(name,level,cmap)

def Biomass():
    name = ['Aboveground', 'Band1', 'Ag_nm', 'Aboveground Carbon Density (MgC/ha)']
    level = np.arange(0,1600,400)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    name = ['Aboveground_mask123', 'Band1', 'Ag', 'Aboveground Carbon Density (MgC/ha)']
    level = np.arange(0,1600,400)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    name = ['Belowground', 'Band1', 'Bg_nm', 'Belowground Carbon Density (MgC/ha)']
    level = np.arange(0,400,100)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    name = ['Belowground_mask123', 'Band1', 'Bg', 'Belowground Carbon Density (MgC/ha)']
    level = np.arange(0,400,100)
    cmap = cmaps.cmocean_speed[:200]
    draw(name,level,cmap)
    
def IGBP():
    name = ['IGBP', 'LC', 'IGBP', 'IGBP']
    level = np.arange(0.5,18.5,1)
    rgb_list = ['#05450a', '#086a10', '#54a708', '#78d203', '#009900', '#c6b044', '#dcd159', '#dade48', '#fbff13', '#b6ff05', '#27ff87',
            '#c24f44', '#a5a5a5', '#ff6d4c', '#69fff8', '#f9ffa4', '#1c0dff']
    cmap = colors.ListedColormap(rgb_list)
    draw(name,level,cmap)
    
def Koppen():
    name = ['Koppen', 'Band1', 'Koppen', 'Koppen']
    level = np.arange(0,31,1)
    rgb_list = ['#ffffff','#0000FE','#0077FF','#46A9FA','#FE0000',
                '#FE9695','#F5A301','#FFDB63','#FDFD45','#C6C700',
                '#96FF96','#63C764','#329633','#C6FF4E','#66FF33',
                '#33C701','#FF00FE','#C600C7','#963295','#966495',
                '#ABB1FF','#5A77DB','#4C51B5','#320087','#18DCDC',
                '#38C7FF','#007E7D','#00455E','#B2B2B2','#686868']
    cmap = colors.ListedColormap(rgb_list)
    draw(name,level,cmap)
    
def mask():
    name = ['mask1', 'Band1', 'mask1', 'mask1']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['mask12','Band1','mask12','mask12']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['mask123','Band1','mask123','mask123']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['mask2','LC','mask2','mask2']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,level,cmap)
    name = ['mask3','et','mask3','mask3']
    level = np.arange(0,2,1)
    cmap = cmap1
    draw(name,level,cmap)

def Db():
    # for year in range(2003,2021):
    #     print(f'draw {year} Dr')
    #     name = [f'Dr_{year}', 'Dr', f'Dr_{year}', f'Dr {year} (mm)']
    #     level = level1
    #     cmap = cmap1
    #     draw(name, level, cmap)
    for year in range(2003,2021):
        print(f'draw {year} Dbedrock')
        name = [f'Dbedrock_{year}', 'Dr', f'Db_{year}', f'$D_{{bedrock}}$ {year} (mm)']
        level = level1
        cmap = cmap1
        draw(name, level, cmap)

def LH():
    for year in range(2003,2021):
        for mon in range(1,13):
            name = [f'LH_{year}_{mon}_temp1', 'Ee', f'LH_{year}_{mon}', 'Latent Heat (W/$m^{{2}}$)']
            level = np.arange(0,50,5)
            cmap = cmaps.WhiteBlue
            draw(name,level,cmap)

@timer
def draw_G():
    path = os.getcwd()+'/'
    print("Current file path: ", path)

    # Sb()
    # Sr()
    # Ss()
    # PR_ET_Q_LH()
    # P1()
    # P2()
    # P3()
    # FD()
    # DTB()
    # Biomass()
    # IGBP()
    # Koppen()
    # mask()
    # Db()
    LH()

if __name__=='__main__':
    draw_G()