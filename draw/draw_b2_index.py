import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotnine import *
from pylab import rcParams
import matplotlib
from myfunc import timer
from myfunc import DirMan
from myfunc import load_and_flatten_data
import config
import os

resolution     = config.resolution
region         = config.region
data_path      = config.data_path
post_data_path = config.post_data_path
shp_path       = config.shp_path
fig_path       = config.fig_path

dir_man = DirMan(data_path)
dir_man.enter()

os.makedirs(f'{data_path}/csv', exist_ok=True)

pd.set_option('display.max_columns', None)
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
size1 = 30
size2 = 24

def read_csv():
    df = pd.read_csv('/tera11/zhwei/students/Xionghui/data/run/500/csv/Global_index.csv')

    df = df[df['Sbedrock'] > 0]

    print(df["P/Sbedrock_div_Sr"].mean())
    print(df["P/Sbedrock_div_ET_mean"].mean())
    print(df["P/Sbedrock_div_PR_mean"].mean())
    print(df["P/ET_mean_div_PR_mean"].mean())
    print(df["P/ET_mean_sub_Sbedrock_div_PR_mean"].mean())
    print(df["P/Q_mean_div_PR_mean"].mean())
    print(df["P/PET_div_PR_mean"].mean())

    df['Dbedrock_Frequency'] = df['Dbedrock_Frequency'].astype('int64')
    n1 = len(df[df['Dbedrock_Frequency']==1])
    n2 = len(df[df['Dbedrock_Frequency']==2])
    n3 = len(df[df['Dbedrock_Frequency']==3])
    print(n1,n2,n3)
    n = [n1,n2,n3]

    df['Dbedrock_Frequency'] = df['Dbedrock_Frequency'].astype(str)
    df = df[df['Dbedrock_Frequency'] != '4']

    # print(df['Dbedrock_Frequency'].describe())

    df['Dbedrock_Frequency'] = pd.Categorical(df['Dbedrock_Frequency'], categories=["1", "2", "3"], ordered=True)
    return n,df

def Sbedrock_div_Sr(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/Sbedrock_div_Sr", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("Percentage of root-zone water storage \ncapacity accomodated by bedrock \n($S_{bedrock}$/$S_{r}$)", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks = np.arange(0, 120, 20)
    plt.yticks(ticks=yticks, labels=yticks,fontsize=size1, fontweight='bold')

    fig.savefig(f'{fig_path}b2_Sbedrock_div_Sr.png')


def Sbedrock_div_ET_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/Sbedrock_div_ET_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("Proportion of annual ET sourced \n from $S_{bedrock}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')

    fig.savefig(f'{fig_path}b2_Sbedrock_div_ET_mean.png')


def Sbedrock_div_PR_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/Sbedrock_div_PR_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("$S_{bedrock}$ / $PR_{mean}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')
    fig.savefig(f'{fig_path}b2_Sbedrock_div_PR_mean.png')


def ET_mean_div_PR_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/ET_mean_div_PR_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.38, 88, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("$ET_{mean}$ / $PR_{mean}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')
    fig.savefig(f'{fig_path}b2_ET_mean_div_PR_mean.png')

def ET_mean_sub_Sbedrock_div_PR_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/ET_mean_sub_Sbedrock_div_PR_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("($ET_{mean}$ - $S_{bedrock}$) / $PR_{mean}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')
    fig.savefig(f'{fig_path}b2_ET_mean_sub_Sbedrock_div_PR_mean.png')


def Q_mean_div_PR_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/Q_mean_div_PR_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("$Q_{mean}$/$PR_{mean}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')
    fig.savefig(f'{fig_path}b2_Q_mean_div_PR_mean.png')


def PET_div_PR_mean(n,df):
    fig = plt.figure(figsize=(18, 8))
    sns.boxenplot(x="Dbedrock_Frequency", y="P/PET_div_PR_mean", data=df, linewidth=3,
                hue='Dbedrock_Frequency',palette=sns.husl_palette(4, s=0.90, l=0.65, h=0.0417))
                    
    ax = plt.gca()

    ax.tick_params(axis='x', which='major', length=10, width=2, direction='out')
    ax.tick_params(axis='y', which='major', length=10, width=2, direction='out')

    for spine in ax.spines.values():
        spine.set_edgecolor('black')  
        spine.set_linewidth(3)  

    for i, label in enumerate(ax.get_xticklabels()):
        x_pos = label.get_position()[0]
        ax.text(x_pos+0.3, 85, f'{n[i]}', ha='center', va='bottom', fontsize=size1, fontweight='bold', color='black')

    plt.ylim(0, 100)


    plt.xlabel('')  
    plt.ylabel("PET / $PR_{mean}$", fontsize=size1, fontweight='bold')  

    current_ticks = [0,1,2]

    new_labels = ['Bedrcok water \nwithdrawn every year \nfrom 2003 to 2020', 
                            'Bedrcok water \nwithdrawn some year(s) \nfrom 2003 to 2020', 
                            'Bedrcok water \nnot needed to explain ET \nover course of study']

    plt.xticks(ticks=current_ticks, labels=new_labels, fontsize=size1, fontweight='bold')

    yticks =np.linspace(0,100,6).astype('int64')
    plt.yticks(ticks=yticks,labels=yticks,fontsize=size1, fontweight='bold')
    fig.savefig(f'{fig_path}b2_PET_div_PR_mean.png')

if __name__=='__main__':
    n,df = read_csv()
    Sbedrock_div_Sr(n,df)
    Sbedrock_div_ET_mean(n,df)
    Sbedrock_div_PR_mean(n,df)
    ET_mean_div_PR_mean(n,df)
    ET_mean_sub_Sbedrock_div_PR_mean(n,df)
    Q_mean_div_PR_mean(n,df)
    PET_div_PR_mean(n,df)
