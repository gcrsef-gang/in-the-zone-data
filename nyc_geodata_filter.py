import json

CODE_TO_COUNTY = {
    "005": "BX",
    "047": "BK",
    "061": "MN",
    "081": "QN",
    "085": "SI"
}

with open("ny_2010_census_tracts.json") as f:
        geodata = json.load(f)
# Add data row-by-row.
to_remove = []
for tract in geodata["features"]:
    if tract["properties"]["COUNTYFP10"] in CODE_TO_COUNTY.keys():
        tract["properties"]["ITZ_GEOID"] = CODE_TO_COUNTY[tract["properties"]["COUNTYFP10"]] + tract["properties"]["NAME10"]
    else:
        to_remove.append(tract)

to_remove.reverse()
for index in to_remove:
    geodata["features"].remove(index)
with open("nyc_2010_census_tracts.json", "w") as f:
    json.dump(geodata, f)