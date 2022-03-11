"""Given NYC orthographic census tract json data, adds a ITZ_GEOID property.
"""

import json

with open("nyct2010.json", "r") as f:
    tract_json = json.load(f)

COUNTY_TO_CODE = {
    "Bronx": "BX",
    "Brooklyn": "MK",
    "Manhattan": "MN",
    "Queens": "QN",
    "Staten Island": "SI"
}

for tract in tract_json["features"]:
    tract["properties"]["ITZ_GEOID"] = COUNTY_TO_CODE[tract["properties"]["BoroName"]] + tract["properties"]["CTLabel"]

with open("new-nyct2010.json", "w") as f:
    json.dump(tract_json, f)

