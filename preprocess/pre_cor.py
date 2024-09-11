# --------------------------------------------------------------------------------------------cor1
import numpy as np
from scipy.stats import pearsonr
from scipy.spatial import KDTree
from scipy.stats import ttest_ind
from scipy.optimize import curve_fit
import xarray as xr
import matplotlib.pyplot as plt
import salem
import geopandas as gpd
from math import sqrt
import pandas as pd
import seaborn as sns
import matplotlib
from pylab import rcParams

# matplotlib.use('QT5Agg')
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
print('_______________Iowa Calculate________________________________________________________________')

def data():
    path1 = '/tera11/zhwei/students/Xionghui/data/DTB/Soilgrids/'
    path2 = '/tera11/zhwei/students/Xionghui/data/DTB/Iowa/'

    data1 = xr.open_dataset(f'{path1}DTB_Soilgrids_Iowa_remap.nc')
    data2 = xr.open_dataset(f'{path2}Iowa.nc')

    # print(data1)
    print('__________________________________________')
    s1 = data1['Band1'].astype('float32')
    s2 = data2['Band1'].astype('float32')
    # print(s1,s2)

    # s1_mask0 = np.where((s1<=np.e) | (s2<=np.e), np.nan, s1)
    # s2_mask0 = np.where((s1<=np.e) | (s2<=np.e), np.nan, s2)

    s1_mask0 = np.where((s1<=0) | (s2<=0), np.nan, s1)
    s2_mask0 = np.where((s1<=0) | (s2<=0), np.nan, s2)
    print('__________________________________________')
    # print(s1_mask0.min())
    

    # flat_data1 = s1_mask0.flatten()
    # flat_data2 = s2_mask0.flatten()
    flat_data1 = s1.values.flatten()
    flat_data2 = s2.values.flatten()
    # flat_data1 = s1_mask0.flatten()
    # flat_data2 = s2_mask0.flatten()

    # print(len(flat_data1))
    # print(len(flat_data2))
    # 过滤掉包含 NaN 或无穷大值的数据点
    valid_data_mask = np.isfinite(flat_data1) & np.isfinite(flat_data2)
    
    
    x = flat_data1[valid_data_mask]
    y = flat_data2[valid_data_mask]
    
    # print(len(x))
    # print(len(y))
    
    # exit(0)
    # 检查过滤后的数据是否为空
    if len(flat_data1) == 0:
        raise ValueError("过滤后的数据为空")
    return x,y

def cor(x, y, z):
    print(f"_____________________________________________________")
    if y is None or z is None:
        raise ValueError("y 或 z 为 None, 请处理后再进行迭代操作. ")
    if None in y or None in z:
        raise ValueError("y 或 z 中包含 None 值, 请处理后再进行运算. ")

    res = ttest_ind(x,y)
    print(res)

    
    res_y  = np.array(y) - np.array(z)
    ss_res     = np.sum(res_y**2)
    ss_tot     = np.sum((y - np.mean(y))**2)
    mse = ss_res/len(y)
    rmse = sqrt(mse)
    mae = np.sum(np.absolute(res_y))/len(y)
    r2 = 1-mse/np.var(y)
    r_squared  = 1 - (ss_res /ss_tot)
    correlation, _ = pearsonr(x, y)
    correlation_rev, _ = pearsonr(x, z)

    print(f'原数值pearson相关系数为:{correlation}')
    print(f'拟合后数值pearson相关系数为:{correlation_rev}')
    print(" mae:      ", mae)
    print(" mse:      ", mse) 
    print(" rmse:     ", rmse) 
    print(" r2:       ", r2)
    print("r_squared  ", r_squared)


def func1(x, a, b):
    return a*(x**b)

def curve1(x,y):
    popt, pcov  = curve_fit(func1, x, y)
    a, b= popt
    z = [func1(i, a, b) for i in x]
    print(f"y={a}*x^{b}")
    return z


def poly1(x,y):
    z1 = np.polyfit(x, y, 3)
    # print(z1)
    p1 = np.poly1d(z1)
    z = p1(x)
    print(p1) 
    return z


def func2(x, a, b, c, d):
    return a*(x**3)+b*(x**2)+c*x+d

def curve2(x,y):
    popt, pcov  = curve_fit(func2, x, y)
    a, b, c, d = popt
    # print(pcov) 
    z = [func2(i, a, b, c, d) for i in x]
    print(f"y={a}*x^3 + {b}*x^2 + {c}*x + {d}")
    return z


def func3(x, a, b):
    return a*np.exp(b*x)

def curve3(x,y):
    popt, pcov  = curve_fit(func3, x/1000, y)
    a, b = popt
    z = [func3(i, a, b) for i in (x/1000)]
    print(f"y={a} * e^({b/1000}*x)")
    return z


def func5(x, log_a, b):
    return log_a + b * x

def curve5(x,y):
    log_y = np.log(y)
    popt, pcov  = curve_fit(func5, x, log_y)
    log_a, b = popt
    log_z = [func5(i, log_a, b) for i in x]
    z = np.exp(log_z)
    print(f"y={np.exp(log_a)} * e ^ ({b}*x)")
    return z
    
def poly2(x,y):
    fit = np.polyfit(x, np.log(y), 1)
    # p1 = np.poly1d(fit)
    # log_z = p1(x)
    # z = np.exp(log_z)

    a, b = fit
    log_z = a*x +b
    z = np.exp(log_z)
    print(f"y={np.exp(b)} * e ^ ({a} *x)")
    return z
    

def func6(x, a):
    return a * np.log( x - 322.9)

def curve6(x,y):
    popt, pcov  = curve_fit(func6, x, y)
    a= popt
    z = [func6(i, a) for i in x]
    print(f"y={a} * ln( x - 322.9)")
    return z


def func7(x, a, b):
    return a * np.log(x) + b

def curve7(x,y):
    popt, pcov  = curve_fit(func7, x, y)
    a, b= popt
    z = [func7(i, a, b) for i in x]
    print(f"y={a} * ln( x ) + {b}")
    return z


def poly3(x,y):
    log_x = np.log(x)
    a, b = np.polyfit(log_x, y, 1)  
    # p1 = np.poly1d([a, b])
    # z = p1(x)
    z = a * log_x + b
    print(f"y={a}*ln(x)+{b}")
    return z



x,y = data()
z= curve1(x,y)
# z= poly3(x,y)

cor(x,y,z)

exit()
data = pd.DataFrame({'x':x,'y':y})
sns_hex = sns.jointplot(x='x', y='y',
                        data = data,
                        kind = 'hex',
                        height=12,
                        ratio=8,
                        color='#D31A8A',
                        linewidth = 0.2,
                        space = 0,
                        xlim=(0,7000),
                        ylim=(0,700),
                        joint_kws=dict(gridsize =100,edgecolor='w'),
                        marginal_kws=dict(bins=100, color='#D31A8A', hist_kws={'edgecolor':'k','alpha':1}),
                        )
sns_hex.set_axis_labels(xlabel='Soilgrids250m', ylabel='Iowa')

x= np.arange(0,7000,1)

y1 = 0.01627438893950506 * x ** 1.09779480659567
y2 = 3.519526106323941e-11*x**3 - 2.10128258249571e-06*x**2 + 0.06195601241193225*x - 63.72122549923073
y3_100 = -2.052942504603917e-16 * np.exp(0.009999999997653448 * x)
y3_1000 = 65.27155810253497 * np.exp(0.00018783029463345974 * x)
y5 = 25.761473590735086 * np.exp(0.00033273606477479044*x)
y6 = 19.891871134589287 * np.log(x - 322.9)
y7 = 176.26198578361357 * np.log( x )  -1293.8040300281714

f1 = 3.52e-11 * x **3 - 2.101e-06 * x ** 2  + 0.06196 * x - 63.72
f2 = 25.761473591261254 * np.exp(0.0003327360647705603 *x)



g = plt.plot(x,y1,alpha=1, color = 'black',linewidth=5, label='acc')
g = plt.plot(x,y2,alpha=1, color = 'orange',linewidth=5, label='acc')
g = plt.plot(x,y3_100,alpha=1, color = 'red',linewidth=5, label='acc')
g = plt.plot(x,y3_1000,alpha=1, color = 'grey',linewidth=5, label='acc')
g = plt.plot(x,y5,alpha=1, color = 'pink',linewidth=5, label='acc')
g = plt.plot(x,y6,alpha=1, color = 'yellow',linewidth=5, label='acc')
g = plt.plot(x,y7,alpha=1, color = 'green',linewidth=5, label='acc')


# g = plt.plot(x,f1,alpha=1, color = 'purple',linewidth=5, label='acc')
# g = plt.plot(x,f2,alpha=1, color = 'brown',linewidth=5, label='acc')

plt.legend(labels=['y = a*$x^{{b}}$', 'y = a*$x^{{3}}$+b*$x^{{2}}$+c*x+d', 'y = a*$e^{{b*x/100}}$', 
                   'y = a*$e^{{b*x/1000}}$', 'lny = lna+b*x', 'y = a*ln(x-322.9)', 'y = a*ln(x)+b'])

plt.savefig(f"p_cor_t1.png")

exit()
data = {'Soilgrids250m':x,
        'Iowa':y,
        'Soilgrids250m_rev':z}

df = pd.DataFrame(data)
df.to_csv(f'revision4_aebxln.csv', mode='w', index=False, header=True)