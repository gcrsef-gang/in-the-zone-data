"""Filters PLUTO data in order to retrieve X and Y coordinates necessary for parks. 

usage: python3 datafilter.py
"""

import pandas as pd
import sys
import os

from itz.data import LOT_TRACT_DATA_STARTING_YEAR

print(os.path.abspath(__file__))
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(parent)

PLUTO_PATH = parent+"/zoning-data/mergedPLUTO-%s.csv"
PLUTO_TEXT_PATH = parent+"/zoning-data/mergedPLUTO-%s.txt"

LOT_TRACT_DATA_STARTING_YEAR = 2002

def filter_data():
    starting_pluto = pd.read_table(PLUTO_TEXT_PATH % 2010, header=0, sep=",", dtype=str, usecols=["BBL", "Borough", "LotArea"])
    next_pluto = pd.read_table(PLUTO_TEXT_PATH % 2012, header=0, sep=",", dtype=str, usecols=["BBL", "CT2010"])
    print("next pluto created")
    next_pluto.set_index("BBL", inplace=True)
    print("starting pluto created")

    starting_pluto.set_index("BBL", inplace=True)
    starting_pluto.sort_index()
    # print(starting_pluto)

    # Create ITZ_GEOID column in lot_df
    if LOT_TRACT_DATA_STARTING_YEAR < 2012:
        # print(next_pluto)
        starting_pluto = starting_pluto.join(next_pluto, on="BBL")
        del next_pluto
        # print(starting_pluto)
        # print(starting_pluto.columns)
        starting_pluto["ITZ_GEOID"] = starting_pluto["Borough"] + starting_pluto["CT2010"].str.strip()
    else: 
        starting_pluto["ITZ_GEOID"] = starting_pluto["Borough"] + starting_pluto["CT2010"]

    # Filter starting_pluto for valid ITZ_GEOIDs
    starting_pluto = starting_pluto[starting_pluto['ITZ_GEOID'].map(lambda x: len(str(x)) != 2)]
    starting_pluto = starting_pluto[starting_pluto["ITZ_GEOID"].notnull()]
    print("ITZ geoids created!")
    # Copy the index of BBLs in starting_pluto
    lot_bbl = starting_pluto.index

    lot_data = pd.DataFrame(index=lot_bbl)
    # Copy the ITZ_GEOIDs from starting_pluto. 
    lot_data["ITZ_GEOID"] = starting_pluto["ITZ_GEOID"]
    # LotArea doesn't change, and starting_pluto uses the same indexing as lot_df, so the column can simply be copied over.
    # lot_df["lot_area"] = starting_pluto["LotArea"].astype(float)  

    del starting_pluto


    for year in ["2010", "2014", "2018"]:
        print("Beginning: ", year)
        try:
            pluto_data = pd.read_csv(PLUTO_PATH % year, dtype=str)
        except:
            pluto_data = pd.read_table(PLUTO_TEXT_PATH % year, sep=",", dtype=str)
        # Set the index and sort by BBL in order to maintain consistency
        print(pluto_data)
        try:
            pluto_data.set_index('BBL', inplace=True)
        except:
            pluto_data.set_index('bbl', inplace=True)
        pluto_data.sort_index()
        pluto_data = pluto_data.loc[lot_data.index.intersection(pluto_data.index)]

        try:
            lot_data["land_use"+year] = pluto_data["LandUse"]
            lot_data["x_coord"] = pluto_data["XCoord"]
            lot_data["y_coord"] = pluto_data["YCoord"]
        except:
            lot_data["land_use"+year] = pluto_data["landuse"]
            lot_data["x_coord"] = pluto_data["xcoord"]
            lot_data["y_coord"] = pluto_data["ycoord"]
    # raise Exception('WAHT')
    lot_data.to_csv("all_lot_data.csv")
    lot_data[(lot_data["land_use"+"2010"] == "9") | (lot_data["land_use"+"2010"] == "09")].to_csv("lot_park_2010_data.csv") 
    lot_data[(lot_data["land_use"+"2014"] == "9") | (lot_data["land_use"+"2014"] == "09")].to_csv("lot_park_2014_data.csv") 
    lot_data[(lot_data["land_use"+"2018"] == "9") | (lot_data["land_use"+"2018"] == "09")].to_csv("lot_park_2018_data.csv") 

if __name__ == "__main__":
    filter_data()