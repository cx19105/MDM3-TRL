import matplotlib.pyplot as plt
from matplotlib.path import Path
import json
from LoadLocationData import LoadLocationData
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import pandas as pd
import numpy as np

def getTrafficGates():
    df = pd.read_json("dim-journey-links.json")

    data = json.load(open("dim-journey-links.json"))
    data = data[0]
    coordinates = np.array(data['fields']['geo_shape']['coordinates'])
    new_coordinates = []
    for pair in coordinates:
        new_coordinates.append([pair[1], pair[0]])
    return new_coordinates

def main(coordinates):
    imagery = OSM()
    lats = list(map(float, coordinates[:, 1]))
    longs = list(map(float, coordinates[:,0]))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=imagery.crs)
    ax.set_extent([coordinates[:,0].min(), coordinates[:,0].max(), coordinates[:,1].min(), coordinates[:,1].max()], ccrs.PlateCarree())
    ax.add_image(imagery, 14)

    theta = np.linspace(0, 2*np.pi, 100)
    circle_verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = Path.make_compound_path(Path(circle_verts[::-1]), Path(circle_verts*0.1))

    ax.plot(longs, lats, transform=ccrs.PlateCarree(), marker=circle, color='red', markersize=10, linestyle='', alpha=0.5)
    plt.show()



if __name__ == '__main__':
    coordinates = getTrafficGates()