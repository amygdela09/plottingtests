import os
import pyart
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import numpy as np
import pandas as pd

# open shapefiles
countyfile = os.getcwd() + '/shapefiles/counties/ne_10m_admin_2_counties.shp'
populationfile = os.getcwd() + '/shapefiles/populated_places/ne_10m_populated_places.shp'
roadsfile = os.getcwd() + '/shapefiles/roads/ne_10m_roads.shp'
# open radar data
filename = os.getcwd() + '/Data/data (9).gz'
radar = pyart.io.read_nexrad_archive(filename, station='KTLX')
# filter data
gatefilter = pyart.filters.GateFilter(radar)
gatefilter.exclude_below('reflectivity', 0)
gatefilter.exclude_transition()
# create figure and plot
fig = plt.figure(figsize=(18, 10))
ax = fig.add_subplot(projection=ccrs.PlateCarree())
# adjust subplot size
plt.subplots_adjust(0, 0, 1, 1)
# map and plot radar data
display = pyart.graph.RadarMapDisplay(radar)
display.plot_ppi_map(
    'reflectivity',
    sweep=0,
    vmin=-32,
    vmax=70,
    lat_0=radar.latitude['data'][0],
    lon_0=radar.longitude['data'][0],
    min_lon=radar.longitude['data'][0] - 1,
    max_lon=radar.longitude['data'][0] + 1,
    min_lat=radar.latitude['data'][0] - 1,
    max_lat=radar.latitude['data'][0] + 1,
    cmap='pyart_NWSRef',
    gatefilter=gatefilter,
    ax=ax,
    embellish=False,
    colorbar_flag=False,
    edges=False,
    add_grid_lines=False,
    title_flag=False,
    resolution='10m'
)
# load and draw counties shapefile
county_feature = ShapelyFeature(Reader(countyfile).geometries(),
                                ccrs.PlateCarree(), facecolor='none',
                                edgecolor='black', linewidth=0.2)
ax.add_feature(county_feature)
# load and draw roads shapefile
roads_feature = ShapelyFeature(Reader(roadsfile).geometries(),
                               ccrs.PlateCarree(), facecolor='none',
                               edgecolor='blue', linewidth=0.4)
ax.add_feature(roads_feature)
# get town locations
shp = Reader(populationfile)
xy = [pt.coords[0] for pt in shp.geometries()]
x, y = list(zip(*xy))
# get town names
towns = shp.records()
names_en = []
for town in towns:
    names = town.attributes['NAME_EN']
    names_en.append(names)
# create data frame and index by the region of the plot
all_towns = pd.DataFrame({'names_en': names_en, 'x': x, 'y': y})
region_towns = all_towns[(all_towns.y < np.max(radar.latitude['data'][0] + 1)) &
                         (all_towns.y > np.min(radar.latitude['data'][0] - 1)) &
                         (all_towns.x > np.min(radar.longitude['data'][0] - 1)) &
                         (all_towns.x < np.max(radar.longitude['data'][0] + 1))]
# plot the locations and labels of the towns in the region
ax.scatter(region_towns.x.values, region_towns.y.values,
           c='black', marker='.', s=20,
           transform=ccrs.PlateCarree(), zorder=3)
transform_mpl = ccrs.PlateCarree()._as_mpl_transform(ax)
for i, txt in enumerate(region_towns.names_en):
    ax.annotate(txt, (region_towns.x.values[i] - 0.005,
                      region_towns.y.values[i] + 0.007),
                xycoords=transform_mpl,
                c='black',
                size=6)

# plt.savefig('mappedradar.jpeg', format='jpeg', dpi=900)
plt.show()
