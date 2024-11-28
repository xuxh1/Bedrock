import os
import subprocess
import numpy as np
import xarray as xr
from myfunc import timer
from myfunc import DirMan
import config

from datetime import datetime, timedelta

def get_step_info():
    all_step = 828
    stt_y = np.zeros(all_step)
    stt_m = np.zeros(all_step)
    stt_d = np.zeros(all_step)
    stt_i = np.zeros(18*12)
    end_y = np.zeros(all_step)
    end_m = np.zeros(all_step)
    end_d = np.zeros(all_step)
    end_i = np.zeros(18*12)
    stt_last = np.zeros(all_step)
    end_last = np.zeros(all_step)
    cum_d = np.zeros(all_step)
    s = 0

    start_date = datetime(2003, 1, 1)
    current_date = start_date
    cumulative_days = 0

    # Iterate through each step to find the correct range
    for current_step in range(1, all_step + 1):
        # Determine the interval length
        if current_date.year % 4 == 0 and (current_date.year % 100 != 0 or current_date.year % 400 == 0):
            # Leap year
            if current_step % 46 == 0:
                interval_length = 6
            else:
                interval_length = 8
        else:
            # Non-leap year
            if current_step % 46 == 0:
                interval_length = 5
            else:
                interval_length = 8


        next_date = current_date + timedelta(days=interval_length)
        cumulative_days += interval_length

        start = current_date
        end = next_date - timedelta(days=1)
        end_temorrow = next_date
        stt_y[current_step-1],stt_m[current_step-1],stt_d[current_step-1] = start.year,start.month,start.day
        end_y[current_step-1],end_m[current_step-1],end_d[current_step-1] = end.year,end.month,end.day
        cum_d[current_step-1] = cumulative_days - interval_length + 1

        # print(f"Step {current_step}:")
        # print(f"  Start Date: {start.strftime('%Y-%m-%d')}")
        # print(f"  End Date: {end.strftime('%Y-%m-%d')}")
        # print(f"  Cumulative Days: {cumulative_days - interval_length + 1}")

        # Check if the step crosses a month boundary
        if start.month != end.month:
            start_month_days = (datetime(start.year, start.month + 1, 1) - start).days
            end_month_days = (end - datetime(end.year, end.month, 1)).days + 1

            # print("  Crosses Month:")
            # print(f"    {start.strftime('%Y-%m')} Days: {start_month_days}")
            # print(f"    {end.strftime('%Y-%m')} Days: {end_month_days}")
            stt_last[current_step-1] = start_month_days
            end_last[current_step-1] = end_month_days
            end_i[s] = current_step - 1
            s = s+1
            stt_i[s] = current_step - 1
        elif end.month != end_temorrow.month:
            end_i[s] = current_step - 1
            s = s+1
            if s != 216:
                stt_i[s] = current_step
            
        # else:
        #     print("  Does Not Cross Month")

        current_date = next_date

    #     if current_step in range(828):
    #         if start.month != end.month:
    #             print(f"Step {current_step}:")
    #             print(f"  Start Date: {start.strftime('%Y-%m-%d')}")
    #             print(f"  End Date: {end.strftime('%Y-%m-%d')}")
    #             print(f"  Cumulative Days: {cumulative_days - interval_length + 1}")
    #             print("  Crosses Month:")
    #             print(f"    {start.strftime('%Y-%m')} Days: {start_month_days}")
    #             print(f"    {end.strftime('%Y-%m')} Days: {end_month_days}")
    # print(stt_i)
    # print(end_i)
    return stt_i,end_i,stt_last,end_last

# Example Usage
stt_i,end_i,stt_last,end_last = get_step_info()

for j in range(18*12):
    print(f"year is {j//12+2003}")
    print(f" mon is {j%12+1}")
    for i in range(int(stt_i[j]),int(end_i[j])+1):
        print(f"  i is {i}")
        if i == int(stt_i[j]) and stt_i[j] == end_i[j-1]:
            print(f"    plus is {1 - stt_last[i]/8}")
        elif j!=215 and i == int(end_i[j]) and stt_i[j+1] == end_i[j]:
            print(f"    plus is {1 - end_last[i]/8}")
        else:
            print("    plus is 1")

        
exit(0)



# year = np.zeros(828, dtype=int)
# mon = np.zeros(828, dtype=int)
# day_stt = np.zeros(828, dtype=int)
# day_end = np.zeros(828, dtype=int)

# days_in_month_common = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# days_in_month_leap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# def is_leap_year(y):
#     return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

# for i in range(828):
#     year[i] = i // 46 + 2003
    
#     days_in_month = days_in_month_leap if is_leap_year(year[i]) else days_in_month_common

#     day_stt[i] = 8 * i + 1 - 3 * (i // 46) + ((i // 46) + 2) // 4
#     day_end[i] = 8 * (i + 1) + 1 - 3 * ((i + 1) // 46) + (((i + 1) // 46) + 2) // 4 - 1

#     cumulative_days = np.cumsum([0] + days_in_month) 
#     for month in range(1, 13):
#         if cumulative_days[month - 1] < day_stt[i] <= cumulative_days[month]:
#             mon[i] = month
#             break


# j = 47
# print(year[j])
# print(mon[j])
# print(day_stt[j])
# print(day_end[j])


np.set_printoptions(threshold=np.inf)
# 设置数组的形状
time_len = 115  # 时间长度
height = 20     # 数组的高度
width = 20     # 数组的宽度

# 创建一个随机的data_var和snowf数组
np.random.seed(0)  # 设置随机种子以获得可重复的结果
data_values = np.random.randint(-500, 500, size=(time_len, height, width))
data_var = xr.DataArray(data_values, dims=["time", "lat", "lon"])
# snowf = xr.DataArray(data_values, dims=["time", "lat", "lon"])

# 输出用于检查的数组
print("data_var:")
print(data_var.values)
# print("snowf:")
# print(snowf)

shape = data_var.isel(time=0).shape


deficit_pmax = np.zeros((time_len, *shape))
deficit_pmin = np.zeros((time_len, *shape))
deficit_diff = np.zeros((time_len, *shape))
deficit_Srv1 = np.zeros((time_len, *shape))
deficit_acc = np.zeros((time_len, *shape))
pmax = np.zeros(shape) 
pmin = np.zeros(shape)  
Srv1 = np.zeros(shape)
data_acc = np.zeros(shape)

p = np.zeros(shape)
n = np.zeros(shape)

data_pos_acc = np.zeros(shape)
max_data_pos_acc = np.zeros(shape)
for i in range(time_len):
    print(f'the time is {i+1}')
    current_data_mask = data_var.isel(time=i).values 

    # set the modified method - exp1
    if i < time_len - 1:
        next_data_mask = data_var.isel(time=i + 1).values 
    else:
        next_data_mask = current_data_mask

    print(current_data_mask[0,10])
    print(next_data_mask[0,10])
    if (current_data_mask[0,10]>0)&(next_data_mask[0,10]<0):
        print('p')
    elif (current_data_mask[0,10]<0)&(next_data_mask[0,10]>0):
        print('n')
    else:
        print('none')


    # if i > 0:
    #     last_data_mask = data_var.isel(time=i - 1).values 
    # else:
    #     last_data_mask = current_data_mask

    # sum the number of max, min points
    p = np.where((current_data_mask>0)&(next_data_mask<0),p+1,p)
    n = np.where((current_data_mask<0)&(next_data_mask>0),n+1,n)

    data_acc += current_data_mask

    # set pmax(the closest maximum point)
    pmax_last = pmax
    pmin_last = pmin
    pmax = np.where((current_data_mask>0)&(next_data_mask<0),data_acc,pmax)
    pmin = np.where((current_data_mask<0)&(next_data_mask>0),data_acc,pmin)

    # set the Continuous extreme value diff and the max diff
    diff_max = np.where(current_data_mask<0,pmax-pmin_last,data_acc-pmin_last)
    Srv1 = np.maximum(Srv1,diff_max)
    
    # write out the value change over time
    deficit_pmax[i, :, :] = pmax
    deficit_pmin[i, :, :] = pmin
    deficit_diff[i, :, :] = diff_max
    deficit_Srv1[i, :, :] = Srv1
    deficit_acc[i, :, :] = data_acc

    # set the original method - exp1
    data_pos_acc = np.where(current_data_mask>=0,data_pos_acc+current_data_mask,0)
    max_data_pos_acc = np.where(data_pos_acc>max_data_pos_acc,data_pos_acc,max_data_pos_acc)

    # print(pmax)
    # print(pmin)
    # print(Srv1)
    # print(max_data_pos_acc)
    print(f"p is {p[0,10]}")
    print(f"n is {n[0,10]}")
    diff1 = p -n 
    print(f"diff is {diff1[0,10]}")
