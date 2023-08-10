import sys
import json
import numpy as np

import folium
from PIL import Image

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
from rasterio.merge import merge

from pyproj import Transformer

from collections import defaultdict


# Dict to contain greenspace data
TRACT_GREENSPACE = defaultdict(lambda: 0)

# The area in square meters of a pixel in the orthodata
PIXEL_SQUARE_AREA = 0.02322576

IR_THRESHOLD = 45
GREEN_THRESHOLD = 0


tiles  = gpd.read_file('tract/orthotiles.json')
tracts = gpd.read_file('tract/tracts.json')


to_merge = []




def getFeatures(gdf):
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


def getGreenspaceImage(ds):
    r = ds.read(1).astype(np.int16)
    g = ds.read(2).astype(np.int16)
    b = ds.read(3).astype(np.int16)

    ir = ds.read(4).astype(np.int16)
    
    ir_filtered = np.clip((ir * 2) - (r + b), 0, 255)

    empty = np.zeros(ir_filtered.shape)


    binary = np.where((ir_filtered > IR_THRESHOLD), 255, 0)

    return np.array([empty.astype('uint8'), binary.astype('uint8'), empty.astype('uint8')])
    
    # binary = np.where((ir_filtered > IR_THRESHOLD), 255, 0).astype('uint8')

    # rgbmask = 
    
    # return np.array([np.zeros((5000,5000)).astype('uint8'), binary.astype('uint8'), np.zeros((5000,5000)).astype('uint8'), binary.astype('uint8')])
    


noFileCount = 0
sussyBakas = 0



greenspace_imgs = folium.FeatureGroup(name="greenspace_imgs")
tile_count = 0


# with rasterio.open("mergedDEM.tif") as img:
#     rasterio.plot.show([img.read(1), img.read(4), img.read(3)])

for tile_index, tile in tiles.iterrows():
    for x in range(75):
        print('*' * (75 - x), x, end='\x1b[1K\r')
    print(str(tile_index * 100 / len(tiles))[0:5] + "% orthotiles saved", end="\r")
    

    # Find and read the associated orthoimage
    ds = None
    image_path = str(tile['IMAGE'].zfill(6)) + '.jp2'


    try:
        crs = rasterio.crs.CRS({"init": "epsg:3857"})
        ds = rasterio.open(image_path)

        img = getGreenspaceImage(ds)

        # img_out = str(tile['IMAGE'].zfill(6)) + ".png"
        # mag = Image.fromarray(img, 'RGBA')
        # mag.save(img_out)


        with rasterio.open(
            'greenspace_ortho_tiles/' + tile['IMAGE'] + '.tif',
            'w',
            driver='GTiff',
            height=ds.shape[0],
            width=ds.shape[1],
            count=3,
            dtype='uint8',
            crs=ds.crs,
            transform=ds.transform,) as dst:
            dst.write(img)

        # rasterio.plot.show(img)

        tile_count += 1
        # if (tile_count > 5):
        #     break

    except Exception as e:
        print(e)
        noFileCount += 1