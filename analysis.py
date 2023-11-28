# analyze temp data

import numpy
from matplotlib import pyplot as plt
import pandas as pd

num = int(input("Enter run number: "))
df = pd.read_csv(f'data/data_{num}.csv',delimiter=",",header=0,usecols=['timestamp','temperature','relative_humidity'])

print(df)




plt.figure('Temperature Vs. Time')
plt.plot(
    df['timestamp'],
    df['temperature']
)
plt.grid()
plt.show()

