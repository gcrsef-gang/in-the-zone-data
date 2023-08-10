import cv2
import sys
import json
import numpy as np

import geopandas as gpd
import os

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap
import matplotlib.image as mpimg

import math

os.environ['PROJ_LIB'] = '/usr/share/proj/'

import rasterio
from rasterio.plot import show
from rasterio.mask import mask

from collections import defaultdict


# Dict to contain greenspace data
TRACT_GREENSPACE = defaultdict(lambda: 0)

# The area in square meters of a pixel in the orthodata
PIXEL_SQUARE_AREA = 0.02322576

IR_THRESHOLD = 45
GREEN_THRESHOLD = 0


tiles  = gpd.read_file('tract/Tile_Grid_2010.json')
tracts = gpd.read_file('tract/tracts.json')



def getFeatures(gdf):
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


def getGreenSpaceCount(ds, geometry):
    out_img, __ = rasterio.mask.mask(ds, getFeatures(geometry), filled=True, crop=True)

    r = out_img[0].astype(np.int16)
    b = out_img[2].astype(np.int16)
    ir = out_img[3].astype(np.int16)

    ir_filtered = np.clip((ir * 2) - (r + b), 0, 255)

    binary = np.where((ir_filtered > IR_THRESHOLD), PIXEL_SQUARE_AREA, 0)
    return np.sum(binary)


def visualize(path, tracts, tiles):
    fig, ax = plt.subplots(1,1)
    plt.axis('equal')

    GREENSPACE = {}
    with open(path) as file:
        lines = file.readlines()
        for line in lines[2:]:
            GREENSPACE[line.split(",")[0][1:-1]] = math.log(float(line.split(",")[1]))

    for index, tract in tracts.iterrows():
        tracts.at[index, 'greenspace'] = GREENSPACE[tracts.at[index, 'ITZ_GEOID']]


    tracts.plot(ax=ax, column='greenspace', cmap='gray', zorder=2, legend=True)
    tiles.plot(ax=ax, alpha=.75, color="black", edgecolor="black", zorder=1)
    plt.show()


#visualize("2010-greenspace-orthoimagery.csv", tracts, tiles)

no_file_count = 0
missing_images = 0


for tile_index, tile in tiles.iterrows():
    for x in range(75):
        print('*' * (75 - x), x, end='\x1b[1K\r')
    print(str(tile_index * 100 / len(tiles))[0:5] + "% orthotiles analyzed, " + str(no_file_count) + " images missing, " + str(missing_images) + " sussy bakas", end="\r")
    
    # Get a list of the tracts at least partly contained by the tile
    coords = np.dstack(tile['geometry'].boundary.coords.xy).tolist()
    tracts_in_tile = tracts.cx[coords[0][1][0]:coords[0][3][0],coords[0][1][1]:coords[0][3][1]]

    # Find and read the associated orthoimage
    ds = None
    image_path = str(tile['IMAGE'].zfill(6)) + '.jp2'

    try:
        ds = rasterio.open(image_path)
    except Exception:
        no_file_count += 1

    if not tracts_in_tile.empty:
        for tract_index, tract in tracts_in_tile.iterrows():
            clipped_tract = tract['geometry'].intersection(tile['geometry'])            
            tract_df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(clipped_tract))

            if ds != None:
                cnt = getGreenSpaceCount(ds, tract_df)
                TRACT_GREENSPACE[tract['ITZ_GEOID']] += cnt
            else:
                missing_images += 1


with open("2010-greenspace-orthoimagery.csv", "a") as f:
    for key, value in TRACT_GREENSPACE.items():
        f.write('"' + key + "\"," + str(value) + "\n")
