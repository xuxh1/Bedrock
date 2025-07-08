# for i in range(828):
#     # print(f"Processing time index: {i}")
#     day_stt = 8*i+1-3*(i//46)+((i//46)+2)//4
#     day_end = 8*(i+1)+1-3*((i+1)//46)+(((i+1)//46)+2)//4-1
#     # print(f"the period {i+1:3} day from {day_stt:4} to {day_end:4}")
#     if (day_end-day_stt+1) != 8:
#         print(f"the period {i+1:3} day is {day_end-day_stt+1:1}")


for j in range(18):
    print(f"year is {j+2003}")
    for i in range(0+46*j,46+46*j):
        # print(f"Processing time index: {i}")
        day_stt = 8*(i-46*j)+1
        day_end = 8*(i-46*j)+1+\
            ((5 if ((j + 2003) % 4 == 0 and ((j + 2003) % 100 != 0 or (j + 2003) % 400 == 0)) else 4)\
            if (i+1) % 46 == 0 else 7)
        day_duration = day_end-day_stt+1
        
        if day_duration != 8:
            print(f"the period {i+1:3} day from {day_stt:4} to {day_end:4}")
            print(f"the period {i+1:3} day is {day_duration:1}")