import pandas as pd
import numpy as np
from difflib import get_close_matches

# Load the data from the provided Excel files
file_2017_2023_path = '/home/xuxh22/stu01/Bedrock/data/Streamflow/2017-2023.xlsx'
file_major_path = '/home/xuxh22/stu01/Bedrock/data/Streamflow/major_river_streamflow2.xlsx'
out = '/home/xuxh22/stu01/Bedrock/data/Streamflow/major_river_streamflow_out.xlsx'
# Read the sheets to check the structure
data1 = pd.read_excel(file_2017_2023_path, None)  # Reading all sheets
data2 = pd.read_excel(file_major_path, None)          # Reading all sheets

result = []

for year in range(2022,2024):
    mon = 12*(year-2022)
    for x in range(13):
        base_row = 17 * x 

        for i in range(13):
            name = data1[str(year)].iloc[base_row, 1 + 4 * i]

            if pd.isna(name):
                break

            month_data = []
            for j in range(12):
                month_data.append(data1[str(year)].iloc[base_row + 2 + j, 2 + 4 * i])
            
            result.append([name] + month_data)


    for row in result:
        print(row[0])

        for i in range(95):
            name2 = data2['all_stations'].iloc[i, 0]
            if row[0] in name2 or name2 in row[0]:
                for j in range(12):
                    data2['all_stations'].iloc[i, 244+mon+j] = row[j+1]
                    print(data2['all_stations'].iloc[i, 244+mon+j])
                break
            if i == 94:
                print(row[0])


with pd.ExcelWriter(out, engine='openpyxl') as writer:
    for sheet_name, df in data2.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)