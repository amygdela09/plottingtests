import glob
import matplotlib.pyplot as plt
from matplotlib import animation
import pyart
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import os

files = sorted(glob.glob('./Data/*'))
countyfile = os.getcwd() + '/shapefiles/counties/ne_10m_admin_2_counties.shp'
roadsfile = os.getcwd() + '/shapefiles/roads/ne_10m_roads.shp'

fig = plt.figure(figsize=(18, 10))
plt.subplots_adjust(0, 0, 1, 1)
# load and draw counties shapefile
county_feature = ShapelyFeature(Reader(countyfile).geometries(),
                                ccrs.PlateCarree(), facecolor='none',
                                edgecolor='black', linewidth=1)
# load and draw roads shapefile
roads_feature = ShapelyFeature(Reader(roadsfile).geometries(),
                               ccrs.PlateCarree(), facecolor='none',
                               edgecolor='blue', linewidth=1)


def animate(nframe):
    plt.clf()
    ax = plt.axes(projection=ccrs.PlateCarree())
    radar = pyart.io.read_nexrad_archive(files[nframe], station='KTLX')
    # filter data
    gatefilter = pyart.filters.GateFilter(radar)
    gatefilter.exclude_below('reflectivity', 0)
    gatefilter.exclude_transition()
    # graph radar for animation
    display = pyart.graph.RadarMapDisplay(radar)
    display.plot_ppi_map(
        'reflectivity',
        sweep=0,
        vmin=-32,
        vmax=70,
        ax=ax,
        cmap='pyart_NWSRef',
        colorbar_flag=False,
        # lat_0=radar.latitude['data'][0],
        # lon_0=radar.longitude['data'][0],
        min_lon=radar.longitude['data'][0] - 1,
        max_lon=radar.longitude['data'][0] + 1,
        min_lat=radar.latitude['data'][0] - 1,
        max_lat=radar.latitude['data'][0] + 1,
        add_grid_lines=False,
        edges=False,
        embellish=False,
    )
    ax.add_feature(county_feature)
    ax.add_feature(roads_feature)


anim = animation.FuncAnimation(fig, animate, frames=len(files))

anim.save('tdwr_animation.gif', fps=3)
# plt.show()
print('Done.')
