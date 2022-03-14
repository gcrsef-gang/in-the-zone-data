"""Aggregates the lot data to census tracts.
"""

import pandas as pd

lot_df = pd.read_csv("all_lot_data.csv")
bbl_to_geoid = {}
for _, row in lot_df.iterrows():
    bbl_to_geoid[row["BBL"]] = row["ITZ_GEOID"]


geoid_distances = {}
for geoid in lot_df["ITZ_GEOID"].value_counts().index:
    geoid_distances[geoid] = []
tract_df = pd.DataFrame(index=geoid_distances.keys(), columns=["2010_distance_from_park","2014_distance_from_park","2018_distance_from_park"])

for year in ["2010","2014","2018"]:
    distance_df = pd.read_csv("park_distance_"+year+"_data.csv")
    distance_df = distance_df[distance_df["1"].notnull()]
    for _, row in distance_df.iterrows():
        geoid_distances[bbl_to_geoid[row["0"]]].append(row["1"])
    for geoid, distances in geoid_distances.items():
        if len(distances) == 0:
            tract_df.loc[geoid, year+"_distance_from_park"] = None
        else:
            tract_df.loc[geoid, year+"_distance_from_park"] = sum(distances)/len(distances)

tract_df["d_2010_2014_distance_from_park"] = tract_df["2014_distance_from_park"]-tract_df["2010_distance_from_park"]
tract_df["d_2014_2018_distance_from_park"] = tract_df["2018_distance_from_park"]-tract_df["2014_distance_from_park"]
tract_df["d_2010_2018_distance_from_park"] = tract_df["2018_distance_from_park"]-tract_df["2010_distance_from_park"]
tract_df.to_csv("tract_distance_from_park.csv")