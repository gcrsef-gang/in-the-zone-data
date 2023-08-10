"""Outdated - it shouldn't be necessary to run this after generating integrated-itz-data. 
"""


import pandas as pd

data_df = pd.read_csv("integrated-itz-data.csv")

for index, row in data_df.iterrows():
    if row["orig_percent_public_transport_trips_under_45_min"] < 0 or row["orig_percent_public_transport_trips_under_45_min"] > 100:
        data_df.loc[index, "orig_percent_public_transport_trips_under_45_min"] = 0
        print("tripped!!", index, row["ITZ_GEOID"])
    if row["orig_percent_car_trips_under_45_min"] < 0 or row["orig_percent_car_trips_under_45_min"] > 100:
        data_df.loc[index, "orig_percent_car_trips_under_45_min"] = 0
    if row["d_2010_2018_percent_public_transport_trips_under_45_min"] < 0 or row["d_2010_2018_percent_public_transport_trips_under_45_min"] > 100:
        data_df.loc[index, "d_2010_2018_percent_public_transport_trips_under_45_min"] = 0
    if row["d_2010_2018_percent_car_trips_under_45_min"] < 0 or row["d_2010_2018_percent_car_trips_under_45_min"] > 100:
        data_df.loc[index, "d_2010_2018_percent_car_trips_under_45_min"] = 0

data_df.set_index("ITZ_GEOID", inplace=True)
data_df.to_csv("updated-itz-data.csv")