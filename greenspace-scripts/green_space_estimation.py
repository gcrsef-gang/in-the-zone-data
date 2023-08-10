import cv2
import sys
import json
import numpy as np

import geopandas as gpd
import os

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import ListedColormap, BoundaryNorm
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


tiles  = gpd.read_file('tract/orthotiles.json')
tracts = gpd.read_file('tract/tracts.json')



def getFeatures(gdf):
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


def getGreenSpaceCount(ds, geometry):
    cmap = ListedColormap(['white'])
    bounds = [0,255]
    norm = BoundaryNorm(bounds, cmap.N)


    # geometry = geometry.to_crs(crs=ds.crs.data)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.axis('equal')
    ax.set_axis_off()
    
    out_img, out_transform = rasterio.mask.mask(ds, getFeatures(geometry), filled=True, crop=True)
    # # out_meta = ds.meta.copy()
    # rasterio.plot.show(out_img, ax=ax, cmap="gray")

    r = out_img[0].astype(np.int16)
    g = out_img[1].astype(np.int16)
    b = out_img[2].astype(np.int16)
    ir = out_img[3].astype(np.int16)

    ir_filtered = np.clip((ir * 2) - (r + b), 0, 255)

    binary = np.where((ir_filtered > IR_THRESHOLD), PIXEL_SQUARE_AREA, 0)
    
    
    rm = np.ma.masked_where((ir_filtered > IR_THRESHOLD), r)#[[0] * len(r[0])] * len(r))
    gm = np.ma.masked_where((ir_filtered > IR_THRESHOLD), g)
    bm = np.ma.masked_where((ir_filtered > IR_THRESHOLD), b)#[[0] * len(r[0])] * len(r))
    
    # img = np.array([
    #     # [[0] * len(r[0])] * len(r),
    #     # r,
    #     np.ma.filled(rm, fill_value=0),
    #     np.ma.filled(gm, fill_value=255),
    #     # [[0] * len(r[0])] * len(r)
    #     np.ma.filled(bm, fill_value=0),
    # ])

    # rasterio.plot.show(binary, cmap='gray', ax=ax)
    # rasterio.plot.show([[0] * len(ds.read(1))] * len(ds.read(1)), cmap='gray', transform=ds.transform, ax=ax,  zorder=0)
    rasterio.plot.show([ds.read(1), ds.read(2), ds.read(3)], transform=ds.transform, ax=ax, zorder=0)
    geometry.plot(ax=ax, alpha=.5, facecolor="red", edgecolor="black", linewidth=3, zorder=0)

    plt.show()

    return np.sum(binary)


def visualize(path, tracts, tiles):
    # for index, tract in tracts.iterrows():
    #     tracts.loc[tract['ITZ_GEOID'], 'greenspace'] = 0
        
    fig, ax = plt.subplots(1,1)
    plt.axis('equal')

    GREENSPACE = {}
    with open(path) as file:
        lines = file.readlines()
        
        for line in lines[2:]:
            GREENSPACE[line.split(",")[0][1:-1]] = math.log(float(line.split(",")[1]))

    for index, tract in tracts.iterrows():
        print(tract)
        print("index:" + str(index))
        tracts.at[index, 'greenspace'] = GREENSPACE[tracts.at[index, 'ITZ_GEOID']]


    print(tracts)
    tracts.plot(ax=ax, column='greenspace', cmap='gray', zorder=2, legend=True)
    tiles.plot(ax=ax, alpha=.75, color="black", edgecolor="black", zorder=1)
    plt.show()


# visualize("2010-greenspace-orthoimagery.csv", tracts, tiles)

# fig, ax = plt.subplots(1,1)
# plt.axis('equal')


noFileCount = 0
sussyBakas = 0


for tile_index, tile in tiles.iterrows():
    for x in range(75):
        print('*' * (75 - x), x, end='\x1b[1K\r')
    print(str(tile_index * 100 / len(tiles))[0:5] + "% orthotiles analyzed, " + str(noFileCount) + " images missing, " + str(sussyBakas) + " sussy bakas, id: " + tile['IMAGE'] , end="\r")
    
    # Get a list of the tracts at least partly contained by the tile
    coords = np.dstack(tile['geometry'].boundary.coords.xy).tolist()
    tracts_in_tile = tracts.cx[coords[0][1][0]:coords[0][3][0],coords[0][1][1]:coords[0][3][1]]

    # Find and read the associated orthoimage
    ds = None
    image_path = str(tile['IMAGE'].zfill(6)) + '.jp2'

    try:
        ds = rasterio.open(image_path)
    except Exception:
        noFileCount += 1

    if not tracts_in_tile.empty:
        for tract_index, tract in tracts_in_tile.iterrows():
                clipped_tract = tract['geometry'].intersection(tile['geometry'])            
                tract_df = gpd.GeoDataFrame(geometry=gpd.GeoSeries(clipped_tract))

                if ds != None:
                    cnt = getGreenSpaceCount(ds, tract_df)
                    TRACT_GREENSPACE[tract['ITZ_GEOID']] += cnt
                else:
                    sussyBakas += 1


# with open("2010-greenspace-orthoimagery.csv", "a") as f:
#     for key, value in TRACT_GREENSPACE.items():
#         f.write('"' + key + "\"," + str(value) + "\n")


# gpd.GeoDataFrame([tile]).plot(ax=ax, color="white", edgecolor="black", zorder=1)     
# 



