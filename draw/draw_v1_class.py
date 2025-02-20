import os
import numpy as np
import pandas as pd
import geopandas as gpd
from plotnine import *
from pylab import rcParams
import matplotlib
from myfunc import timer
from myfunc import DirMan
import config

resolution     = config.resolution
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

print('python draw_v1_class.py')

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

df = pd.read_csv(f'{data_path}csv/Global.csv')
shp = gpd.read_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

@timer
def plot_Con():
   df = pd.read_csv(f'{data_path}csv/Global.csv')
   shp = gpd.read_file(shp_path+'World_CN/ne_10m_admin_0_countries_chn.shp')

   # Group by Continent and calculate sum of Area
   df['Continent_Together'] = df['Continent'].replace(to_replace=['South America', 'North America'], value=['South \nAmerica', 'North \nAmerica'])
   continent_area = df.groupby('Continent_Together')['Area'].sum().div(1e9)

   # Filter continents with sufficient area
   continent_area = continent_area[continent_area > 300].sort_values(ascending=False)

   # Map the calculated areas back to the dataframe and sort it
   df['Continent_area'] = df['Continent_Together'].map(continent_area)
   df = df[df['Continent_Together'].isin(continent_area.index)]

   # Ensure Continent_Together is an ordered category for proper sorting
   df['Continent_Together'] = pd.Categorical(df['Continent_Together'], categories=continent_area.index, ordered=True)

   # Create the violin plot
   violin_plot = (ggplot(df, aes(x='Continent_Together', y="Sbedrock", fill="Continent_Together"))
      + geom_violin(show_legend=False)
      + geom_boxplot(fill="white", width=0.1, show_legend=False, outlier_alpha=0, outlier_size=1, outlier_color='#f6f2f4')
      + scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl')
      + theme_matplotlib()
      + ggtitle("Continent")
      + theme(
         text=element_text(size=20, colour="black"),
         axis_text_x=element_text(angle=90, hjust=0.5),
         axis_title_x=element_text(vjust=1),
         plot_title=element_text(vjust=1, hjust=0.5),
         aspect_ratio=0.8,
         dpi=400,
         figure_size=(16, 8))
      + labs(x='', y="$S_{{bedrock}}$ (mm)"))

   # Save the plot
   violin_plot.save(f'{fig_path}v1_con.png')


@timer
def plot_Sub():
   df2 = df.copy()

   list1 = ['South America','Australia and New Zealand','Southern Africa','Eastern Africa' ,'Melanesia', 
            'Western Europe', 'Polynesia', 'Middle Africa','South-Eastern Asia', 'Western Africa', 
            'Southern Asia', 'Central America','Northern Africa', 'Caribbean', 'Western Asia', 
            'Eastern Asia','Northern America', 'Southern Europe', 'Central Asia', 'Eastern Europe',
            'Northern Europe']
   list2 = ['South \nAmerica','Australia and \nNew Zealand','Southern \nAfrica','Eastern \nAfrica' ,'Melanesia', 
            'Western \nEurope', 'Polynesia', 'Middle \nAfrica','South-Eastern \nAsia', 'Western \nAfrica', 
            'Southern \nAsia', 'Central \nAmerica','Northern \nAfrica', 'Caribbean', 'Western \nAsia', 
            'Eastern \nAsia','Northern \nAmerica', 'Southern \nEurope', 'Central \nAsia', 'Eastern \nEurope',
            'Northern \nEurope']
   mapping = dict(zip(list1, list2))
   df2['Subregion_Together'] = df2['Subregion'].map(mapping).fillna(df2['Subregion'])
   
   df3 = pd.DataFrame()
   df3['Subregion_area'] = df2.groupby('Subregion_Together')['Area'].sum().div(1e9)
   df3 = df3[df3['Subregion_area'] > 300]
   df3 = df3.sort_values(by=['Subregion_area'], ascending=False).reset_index(drop=False)
   print(df3)
   
   list1 = df3.loc[:,'Subregion_Together']
   list2 = df3.loc[:,'Subregion_area']
   mapping = dict(zip(list1, list2))
   
   df2 = df2[df2.Subregion_Together.isin(list1)]
   df2 = df2[df2['Subregion_Together'].notna()]
   df2['Subregion_area'] = df2['Subregion_Together'].map(mapping)
   df2 = df2.sort_values(by=['Subregion_area'], ascending=False).reset_index(drop=True)
   order = df2['Subregion_Together'].unique()
   df2['Subregion_Together'] = pd.Categorical(df2['Subregion_Together'], categories=order, ordered=True)
   print(df2)
      
   violin_plot = (ggplot(df2, aes(x='Subregion_Together', y="Sbedrock", fill="Subregion_Together"))
            + geom_violin(show_legend=False)
            + geom_boxplot(fill="white", width=0.1, show_legend=False, outlier_alpha=0, outlier_size=1, outlier_color='#f6f2f4')
            + scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl')
         #    + coord_flip()
            + theme_matplotlib()
            + ggtitle("Subregion")
            
            + theme(  # legend_position='none',
   text=element_text(size=20, colour="black"),
   axis_text_x=element_text(angle=90, hjust=0.5),
   axis_title_x=element_text(vjust=1),
   plot_title=element_text(vjust=1, hjust = 0.5),
   aspect_ratio=0.8,
   dpi=400,
   figure_size=(16, 8))
            + labs(x='', y="$S_{{bedrock}}$ (mm)"))
   # violin_plot.save(f'{fig_path}v1_sub.pdf', transparent=True, bbox_inches='tight')
   violin_plot.save(f'{fig_path}v1_sub.png')
        
def plot_Sov():
   df2 = df.copy()
   
   list1 = ['United States of America','Democratic Republic of the Congo','Central African Republic']
   list2 = ['United States of \nAmerica','Democratic Republic of \nthe Congo','Central \nAfrican Republic']
   mapping = dict(zip(list1, list2))
   df2['Sovereignt_Together'] = df2['Sovereignt'].map(mapping).fillna(df2['Sovereignt'])
   
   df3 = pd.DataFrame()
   df3['Sovereignt_area'] = df2.groupby('Sovereignt_Together')['Area'].sum().div(1e9)
   df3 = df3[df3['Sovereignt_area'] > 300]
   df3 = df3.sort_values(by=['Sovereignt_area'], ascending=False).reset_index(drop=False)
   print(df3)
   
   list1 = df3.loc[:,'Sovereignt_Together']
   list2 = df3.loc[:,'Sovereignt_area']
   mapping = dict(zip(list1, list2))
   
   df2 = df2[df2.Sovereignt_Together.isin(list1)]
   df2 = df2[df2['Sovereignt_Together'].notna()]
   df2['Sovereignt_area'] = df2['Sovereignt_Together'].map(mapping)
   df2 = df2.sort_values(by=['Sovereignt_area'], ascending=False).reset_index(drop=True)
   order = df2['Sovereignt_Together'].unique()
   df2['Sovereignt_Together'] = pd.Categorical(df2['Sovereignt_Together'], categories=order, ordered=True)
   print(df2)
   
   violin_plot = (ggplot(df2, aes(x='Sovereignt_Together', y="Sbedrock", fill="Sovereignt_Together"))
            + geom_violin(show_legend=False)
            + geom_boxplot(fill="white", width=0.1, show_legend=False, outlier_alpha=0, outlier_size=1, outlier_color='#f6f2f4')
            + scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl')
         #    + coord_flip()
            + theme_matplotlib()
         #    + ggtitle("\n\nSovereignt")
            
            + theme(  # legend_position='none',
   text=element_text(size=20, colour="black"),
   axis_text_x=element_text(angle=90, hjust=0.5),
   axis_title_x=element_text(vjust=1),
   plot_title=element_text(vjust=1, hjust = 0.5),
   aspect_ratio=0.8,
   dpi=400,
   figure_size=(16, 8))
            + labs(x='', y="$S_{{bedrock}}$ (mm)", title='Sovereignt'))
   # violin_plot.save(f'{fig_path}v1_sov.pdf', transparent=True, bbox_inches='tight')
   violin_plot.save(f'{fig_path}v1_sov.png')
    
    
def plot_Koppen():
   df2 = df.copy()
   # exclude ocean (koppen = 0)
   df2 = df2[df2['Koppen'] != 0]
   df2['Koppen_Together'] = df2['Koppen'].replace(to_replace=[5, 7, 9, 10, 12, 13, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28], value=[4, 6, 8, 8, 11, 11, 14, 14, 17, 17, 17, 21, 21, 21, 25, 25, 25]) 
   list1 = np.arange(1,31,1)
   list2 = ['Tropical Rainforest (Af)','Tropical Monsoon (Am)','Tropical Savanna (Aw)','Desert & Arid (BW)',
            'Arid (BWk)','Semi Arid (BS)','Semi Arid (BSk)','Mediterranean (Cs)','Mediterranean (Csb)',
            'Mediterranean (Csc)','Humid Subtropical &\nOceanic (Cw)','Oceanic (Cwb)','Ocanic (Cwc)',
            'Humid Subtropical &\nOceanic (Cf)','Oceanic (Cfb)','Oceanic (Cfc)','Humid Continental &\nSubarctic (Ds)',
            'Humid Continental (Dsb)','Subarctic (Dsc)','Subarctic (Dsd)','Humid Continental &\nSubarctic (Dw)',
            'Humid Continental (Dw)','Subarctic (Dwc)','Subarctic (Dwd)','Humid Continental &\nSubarctic (Df)',
            'Humid Continental (Dfb)','Subarctic (Dfc)','Subarctic (Dfd)','Tundra (ET)', 'Frost (EF)']
   mapping = dict(zip(list1, list2))
   df2['Koppen_short'] = df2['Koppen_Together'].map(mapping).fillna(df2['Koppen_Together'])
   
   df3 = pd.DataFrame()
   df3['Koppen_area'] = df2.groupby('Koppen_short')['Area'].sum().div(1e9)
   # df3 = df3[df3['Koppen_Together'] > 200]
   df3 = df3.sort_values(by=['Koppen_area'], ascending=False).reset_index(drop=False)
   print(df3)
   
   list1 = df3.loc[:,'Koppen_short']
   list2 = df3.loc[:,'Koppen_area']
   mapping = dict(zip(list1, list2))
   
   df2 = df2[df2.Koppen_short.isin(list1)]
   df2 = df2[df2['Koppen_short'].notna()]
   df2['Koppen_area'] = df2['Koppen_short'].map(mapping)
   df2 = df2.sort_values(by=['Koppen_area'], ascending=False).reset_index(drop=True)
   order = df2['Koppen_short'].unique()
   df2['Koppen_short'] = pd.Categorical(df2['Koppen_short'], categories=order, ordered=True)
   print(df2)
   
   violin_plot = (ggplot(df2, aes(x='Koppen_short', y="Sbedrock", fill='Koppen_short'))
            + geom_violin(show_legend=False)
            + geom_boxplot(fill="white", width=0.1, show_legend=False, outlier_alpha=0, outlier_size=1, outlier_color='#f6f2f4')
            + scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl')
         #    + coord_flip()
            + theme_matplotlib()
            + ggtitle("Koppen Climate Type")
            
            + theme(  # legend_position='none',
   text=element_text(size=20, colour="black"),
   axis_text_x=element_text(angle=90, hjust=0.5),
   axis_title_x=element_text(vjust=1),
   plot_title=element_text(vjust=1, hjust = 0.5),
   aspect_ratio=0.8,
   dpi=400,
   figure_size=(16, 8))
            + labs(x="", y="$S_{{bedrock}}$ (mm)"))
   # violin_plot.save(f'{fig_path}v1_koppen.pdf', transparent=True, bbox_inches='tight')
   violin_plot.save(f'{fig_path}v1_koppen.png')
   
def plot_IGBP():
   df2 = df.copy()
   
   list1 = np.arange(1,18,1)
   list2 = ['Evergreen Needleleaf\nForests', 'Evergreen Broadleaf\nForests', 'Deciduous Needleleaf\nForests',
            'Deciduous Broadleaf\nForests', 'Mixed Forests', 'Closed Shrublands', 'Open Shrublands', 
            'Woody Savannas', 'Savannas', 'Grasslands', 'Permanent Wetlands', 'Croplands', 
            'Urban and Built-up Lands', 'Cropland/Natural Vegetation Mosaics', 'Permanent Snow and Ice', 
            'Barren', 'Water Bodies']
   mapping = dict(zip(list1, list2))
   df2['IGBP_short'] = df2['IGBP'].map(mapping).fillna(df2['IGBP'])
   
   df3 = pd.DataFrame()
   df3['IGBP_area'] = df2.groupby('IGBP_short')['Area'].sum().div(1e9)
   # df3 = df3[df3['IGBP_Together'] > 300]
   df3 = df3.sort_values(by=['IGBP_area'], ascending=False).reset_index(drop=False)
   print(df3)
   list1 = df3.loc[:,'IGBP_short']
   list2 = df3.loc[:,'IGBP_area']
   mapping = dict(zip(list1, list2))
   
   
   df2 = df2[df2.IGBP_short.isin(list1)]
   df2 = df2[df2['IGBP_short'].notna()]
   df2['IGBP_area'] = df2['IGBP_short'].map(mapping)
   df2 = df2.sort_values(by=['IGBP_area'], ascending=False).reset_index(drop=True)
   order = df2['IGBP_short'].unique()
   df2['IGBP_short'] = pd.Categorical(df2['IGBP_short'], categories=order, ordered=True)
   print(df2)
   
   # exit(0)
   violin_plot = (ggplot(df2, aes(x='IGBP_short', y="Sbedrock", fill='IGBP_short'))
            + geom_violin(show_legend=False)
            + geom_boxplot(fill="white", width=0.1, show_legend=False, outlier_alpha=0, outlier_size=1, outlier_color='#f6f2f4')
            + scale_fill_hue(s=0.90, l=0.65, h=0.0417, color_space='husl')
         #    + coord_flip()
            + theme_matplotlib()
            + ggtitle("IGBP")
            
            + theme(  # legend_position='none',
   text=element_text(size=20, colour="black"),
   axis_text_x=element_text(angle=90, hjust=0.5),
   axis_title_x=element_text(vjust=1),
   plot_title=element_text(vjust=1, hjust = 0.5),
   aspect_ratio=0.8,
   dpi=400,
   figure_size=(16, 8))
            + labs(x="", y="$S_{{bedrock}}$ (mm)"))
   # violin_plot.save(f'{fig_path}v1_IGBP.pdf', transparent=True, bbox_inches='tight')
   violin_plot.save(f'{fig_path}v1_IGBP.png')
   
def draw_violin():
   # Transfer the current path to the calculation path
   dir_man = DirMan(data_path)
   dir_man.enter()
   path = os.getcwd()+'/'
   print("Current file path: ", path)

   plot_Con()
   #  plot_Sub()
   #  plot_Sov()
   #  plot_Koppen()
   #  plot_IGBP()

if __name__=='__main__':
   draw_violin()