#!/usr/bin/env python
# coding: utf-8
# Search and pull coordinates from onemap
import pandas as pd
import time
import requests


def get_coordinates(input_file):
    filename = input_file.split("\\")[1]
    filename = filename[:-4] + "_Geo.csv"
    df = pd.read_csv(input_file)
    no_of_records = len(df)
    count = 0
    print("Number of records to pull: " + str(no_of_records))

    api_query = "https://developers.onemap.sg/commonapi/search"
    
    latitudes = []
    longitudes = []
    for addr in df.itertuples():
        street_name = addr[2]
        block = addr[3]
        results = requests.get(api_query,params={'searchVal':str(street_name)+ " " + str(block), 'returnGeom':'Y', 'getAddrDetails':'N'})
        results = results.json()
        coordinates = results['results']
        
        # Index out of range error will occur if no results can be found
        try:
            longitude = coordinates[0]['LONGITUDE']
            latitude = coordinates[0]['LATITUDE']
            latitudes.append(latitude)
            longitudes.append(longitude)
        except:
            print(addr)
            latitudes.append(0.0)
            longitudes.append(0.0)
            count += 1
            pass

        count += 1
        if count % 245 == 0:
            # prevent API rate limiting
            print(str(count) + " rows done, sleeping for 1 min")
            time.sleep(59)

    df['latitude'] = pd.Series(latitudes)
    df['longitude'] = pd.Series(longitudes)

    df.to_csv("resale-flat-prices\\" + filename)
    
get_coordinates("resale-flat-prices\Addresses.csv")
print("Done")