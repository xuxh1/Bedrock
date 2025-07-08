import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

print('python draw_l1_change.py')

def plot_xG_rolling(team, ax, data, window = 5, color_for = "blue", color_ag = "orange", color_Sr="balck"):

    Y_for = df["et"].reset_index(drop = True)
    Y_ag = df["pr"].reset_index(drop = True)



    X_ = pd.Series(range(len(Y_for)))

    Y_for = Y_for.rolling(window = 2, min_periods = 0).mean() # min_periods is for partial avg.
    Y_ag = Y_ag.rolling(window = 2, min_periods = 0).mean()
    # Sr = Sr.rolling(window = 5, min_periods = 0).mean()

    d = Y_for-Y_ag
    pos = d
    pos[0] = 0
    for i in range(1,len(d)):
        current_data = d[i]
        
        pos[i] = np.where((current_data>0), pos[i-1]+current_data, 0)
    Sr = pd.Series(pos)
    
    # ---- Create auxiliary series for filling between curves

    X_aux = X_.copy()
    X_aux.index = X_aux.index * 10 # 9 aux points in between each match
    last_idx = X_aux.index[-1] + 1
    X_aux = X_aux.reindex(range(last_idx))
    X_aux = X_aux.interpolate()

    # --- Aux series for the xG created (Y_for)
    Y_for_aux = Y_for.copy()
    Y_for_aux.index = Y_for_aux.index * 10
    last_idx = Y_for_aux.index[-1] + 1
    Y_for_aux = Y_for_aux.reindex(range(last_idx))
    Y_for_aux = Y_for_aux.interpolate()

    # --- Aux series for the xG conceded (Y_ag)
    Y_ag_aux = Y_ag.copy()
    Y_ag_aux.index = Y_ag_aux.index * 10
    last_idx = Y_ag_aux.index[-1] + 1
    Y_ag_aux = Y_ag_aux.reindex(range(last_idx))
    Y_ag_aux = Y_ag_aux.interpolate()

    # --- Plotting our data

    # --- Remove spines and add gridlines

    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(ls = "--", lw = 0.25, color = "#4E616C")

    # --- The data

    for_ = ax.plot(X_, Y_for, mfc = "white", ms = 4, color = color_for)
    ag_ = ax.plot(X_, Y_ag, mfc = "white", ms = 4, color = color_ag)
    # ag_ = ax.plot(X_, Sr, mfc = "white", ms = 4, color = color_Sr)
    

    # --- Fill between

    for index in range(len(X_aux) - 1):
        # Choose color based on which line's on top
        if Y_for_aux.iloc[index + 1] > Y_ag_aux.iloc[index + 1]:
            color = for_[0].get_color()
        else:
            color = ag_[0].get_color()
        
        # Fill between the current point and the next point in pur extended series.
        ax.fill_between([X_aux[index], X_aux[index+1]], 
                        [Y_for_aux.iloc[index], Y_for_aux.iloc[index+1]], 
                        [Y_ag_aux.iloc[index], Y_ag_aux.iloc[index+1]], 
                        color=color, zorder = 2, alpha = 0.2, ec = None)
        

    # --- Ensure minimum value of Y-axis is zero
    ax.set_ylim(0)

    # --- Adjust tickers and spine to match the style of our grid

    ax.xaxis.set_major_locator(ticker.MultipleLocator(2)) # ticker every 2 matchdays
    #   xticks_ = ax.xaxis.set_ticklabels([x - 1 for x in range(0, len(X_) + 3, 2)])
    xticks = ['Jan', 'Feb', 'Apr', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
    ax.xaxis.set_ticks([x for x in range(0, len(X_) + 1, 2)])
    xticks_ = ax.xaxis.set_ticklabels([x for x in range(0, len(X_) + 1, 2)])

    ax.xaxis.set_tick_params(length = 2, color = "#4E616C", labelcolor = "#4E616C", labelsize = 6)
    ax.yaxis.set_tick_params(length = 2, color = "#4E616C", labelcolor = "#4E616C", labelsize = 6)

    ax.spines["bottom"].set_edgecolor("#4E616C")

    # --- Legend and team name

    Y_for_last = Y_for.iloc[-1]
    Y_ag_last = Y_ag.iloc[-1]
    Y_Sr_last = Sr.max()
    # -- Add the team's name
    team_ = ax.text(
            x = 0, y = ax.get_ylim()[1] + ax.get_ylim()[1]/20,
            s = f'{team}',
            color = "#4E616C",
            va = 'center',
            ha = 'left',
            size = 7
            )

    # -- Add the xG created label
    for_label_ = ax.text(
            x = X_.iloc[-1] + 0.75, y = Y_for_last,
            s = f'{Y_for_last:,.1f} Evapotranspiration',
            color = color_for,
            va = 'center',
            ha = 'left',
            size = 6.5
            )

    # -- Add the xG conceded label
    ag_label_ = ax.text(
            x = X_.iloc[-1] + 0.75, y = Y_ag_last,
            s = f'{Y_ag_last:,.1f} Precipitation',
            color = color_ag,
            va = 'center',
            ha = 'left',
            size = 6.5
            )
    
    # Sr_label_ = ax.text(
    #         x = X_.iloc[33] + 0.75, y = Y_Sr_last,
    #         s = f'Root-zone storage deficit is {Y_Sr_last:,.1f}',
    #         color = color_Sr,
    #         va = 'center',
    #         ha = 'left',
    #         size = 6.5
    #         )


et = xr.open_dataset(f'{post_data_path}diff/ET_2003_2020_8D_0p1_mm8d_nn.nc')
pr = xr.open_dataset(f'{post_data_path}diff/PR_2003_2020_8D_0p1_mm8d_nn.nc')
t = pd.Series(pd.to_datetime(et['time'])).dt.date

lon = -112
lat = 38
year = 2012
start = 46*(year-2003)
end = 46*(year-2003+1)+1

lon_min = lon - 5
lon_max = lon + 5
lat_min = lat - 5
lat_max = lat + 5

p1_et = et['et'].sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max)).mean(dim=['lon', 'lat'])
p1_pr = pr['tp'].sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max)).mean(dim=['lon', 'lat'])

# p1_et = et['et'].sel(lon=lon,lat=lat, method='nearest')
# p1_pr = pr['tp'].sel(lon=lon,lat=lat, method='nearest')

# df = pd.DataFrame()
# df['et'] = p1_et[start:end]
# df['pr'] = p1_pr[start:end]
# df['date'] = t[start:end]
# df['lat'] = [lat] * (end-start)
# df['lon'] = [lon] * (end-start)

df = pd.DataFrame()
# df['et'] = p1_et[start:end].values
# df['pr'] = p1_pr[start:end].values
print(len(p1_et[start:end].values))
# print(p1_pr[start:end].values)
et_set = [17, 18.0, 15.74, 17.48, 18.22, 19.96, 19.7, 22.44, 
          23.19, 21.93, 24.67, 23.41, 26.15, 24.89, 26.63, 
          25.37, 29.11, 27.85, 29.59, 31.33, 29.07, 29.81, 
          33.56, 31.3, 32.04, 33.78, 34.52, 36.26, 36.0, 
          35.0, 35.67, 35.33, 31.0, 32.67, 30.33, 30.0, 
          25.67, 24.33, 23.0, 24.67, 21.33, 20.0, 19.67, 
          18.33, 17.0, 16, 17]
pr_set = [2, 3.0, 21.5, 26.0, 46.5, 50.0, 69.5, 77.0, 96.5, 
          108.0, 115, 114, 112, 128.0, 88.67, 56.33, 29.0, 0, 
          0, 0, 0, 0, 1.0, 29.5, 52.0, 67.5, 92.0, 96, 93, 94, 
          93.0, 76.0, 58.0, 39.0, 23.0, 5.0, 0, 0, 0, 0, 0, 0, 
          0, 0.0, 34.0, 0, 4]
df['et'] = et_set
df['pr'] = pr_set
df['date'] = t[start:end].values
df['lat'] = [lat] * (end - start)
df['lon'] = [lon] * (end - start)


fig = plt.figure(figsize=(5, 2), dpi = 200)
ax = plt.subplot(111)

plot_xG_rolling("8-days Water Flux or Root-Zone Deficit (mm)", ax, data = df, color_for = "#fdcf41", color_ag = "#153aab", color_Sr="red")

plt.tight_layout()
plt.savefig(f"{fig_path}/l1_change.png",dpi=500, bbox_inches='tight')
# exit(0)
# fig, ax = plt.subplots(figsize=(12,6), dpi=2000)

# ax.plot(t[start:end], p1_et[start:end], linestyle = '-', lw=2, label='ET') 
# ax.plot(t[start:end], p1_pr[start:end], linestyle = '-', lw=2, label='P') 

# ax.set_xlim(t[start],t[end-1])
# ax.set_ylim(0,275)
# ax.xaxis.set_major_locator(mdates.MonthLocator())
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# # plt.xticks(rotation=45)
# # xticks = ['Jan', 'Feb', 'Apr', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
# # ax.set_xticks(xticks,rotation=45)

# # fig.autofmt_xdate()
# plt.legend(bbox_to_anchor=(1.20, 1), loc=1, borderaxespad=0)   #显示标签，并放在外侧
# plt.xlabel('time',fontsize=12) #设置x轴的标签
# plt.ylabel('8-days Water Flux or Root-Zone Deficit (mm)',fontsize=12) #设置y轴的标签
# plt.savefig("values.png",dpi=500, bbox_inches='tight') # 保存图片