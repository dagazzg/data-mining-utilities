# Extracts the coordinates from the csv file. Compatible with the results of get_coordinates

import pandas as pd

filepath = "resale-flat-prices\mrtfaretime.csv"
df = pd.read_csv(filepath, encoding="unicode-escape")
stations = df.groupby("Station_start")

# I only need the coordinates of the stations, and the station name
stations = stations.first()

df2 = stations[['Longitude_Start','Latitude_Start']]
df2.to_csv("resale-flat-prices\mrt-coordinates.csv", encoding="latin1")

# Not sure if we want to use the given travel times from MRT to MRT, so KIV
# for station in stations.itertuples():
#     name = station['Station_start']
#     longitude = station['Longitude_Start']
#     latitude = station['Latitude_Start']


# In[ ]: