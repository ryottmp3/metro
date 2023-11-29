# analyze temp data

import os 
import numpy
from matplotlib import pyplot as plt
import pandas as pd

csv_dir = "/home/ryott/Projects/metro/data"


dataframes = []


for filename in os.listdir(csv_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_dir, filename)
        df = pd.read_csv(file_path, delimiter=",",header=0,usecols=['timestamp','temperature','relative_humidity'])
        dataframes.append(df)


data = pd.concat(dataframes, ignore_index=True)

print(data)




plt.figure('Temperature Vs. Time')
plt.plot(
    (data['timestamp']/3600),
    data['temperature']
)
plt.xlabel("Hours")
plt.ylabel("Temp C")
plt.grid()
plt.show()

