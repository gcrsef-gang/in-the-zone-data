"""
Given processed data, creates metric of nearest park for all lots for 2011, 2016, and 2019. 

usage: metric_constructor.py
"""
import pandas as pd
import numpy as np

# with open("all_lot_data.csv", "r") as f:
lot_data = pd.read_csv("all_lot_data.csv")
lot_data.set_index("BBL", inplace=True)

for year in ["2010","2014","2018"]:
    print("Year: ", year)
    park_data = pd.read_csv("lot_park_"+year+"_data.csv")[["x_coord","y_coord"]]
    # park_data = park_data.head(30)
    # park_coords = [np.array(row) for row in park_data[["x_coord", "y_coord"]]]
    distance_data = []
    i = 0
    for index, row in lot_data.iterrows():
        print(f"\r {i} out of {len(lot_data)}", flush=True, end=None)
        lot_coords = row[["x_coord", "y_coord"]]
        if index == 1000160190:
            print(pd.isna(lot_coords["x_coord"]))
        if pd.isna(lot_coords["x_coord"]):
            distance_data.append([index, None])
            continue
        # min_distance = 1e9
        park_dist_coords = park_data.sub(lot_coords, axis="columns")
        park_dist_coords = park_dist_coords[~park_dist_coords["x_coord"].isnull()]

        squared = pd.Series(np.square(park_dist_coords["x_coord"])+np.square(park_dist_coords["y_coord"]))
        dist = squared.pow(1/2)
        # print(dist)
        # print(index)
        distance_data.append([index,min(dist)])
        i += 1
    distance_data = pd.DataFrame(distance_data)
    distance_data.rename(columns={"0":"BBL","1":"park_distance"}, inplace=True)
    distance_data.to_csv("park_distance_"+year+"_data.csv")
        
