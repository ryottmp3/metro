# analyze temp data

import os 
import numpy
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime


run = int(input("Enter Run Number: "))
csv_dir = f"/home/ryott/Projects/metro/data/run_{run}"



dataframes = []


for filename in os.listdir(csv_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(file_path, delimiter=",",header=0,usecols=['timestamp','temperature','relative_humidity'])
        dataframes.append(df)


data = pd.concat(dataframes, ignore_index=True)

print(data)




plt.figure(f'Temperature Vs. Time, Test Run {run}')
plt.title(f'Temperature Vs. Time, Test Run {run}')
plt.plot(
    (data['timestamp']/3600),
    data['temperature']
)
plt.xlabel("Hours")
plt.ylabel("Temp C")
plt.grid()
plt.savefig(f'/home/ryott/Projects/metro/analysis/temp_vs_time_test_run_{run}.png')

plt.figure(f'RH Vs. Time, Test Run {run}')
plt.title(f'RH Vs. Time, Test Run {run}')
plt.plot(
    (data['timestamp']/3600),
    data['relative_humidity']
)
plt.xlabel("Hours")
plt.ylabel("Relative Humidity %")
plt.grid()
plt.savefig(f'/home/ryott/Projects/metro/analysis/rh_vs_time_test_run_{run}.png')
plt.show()

