import os
import pyart
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# open radar data
filename = os.getcwd() + '/Data/data (5).gz'
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
    # cmap='viridis',
    gatefilter=gatefilter,
    ax=ax,
    embellish=False,
    colorbar_flag=False,
    edges=False,
    add_grid_lines=False,
    title_flag=False,
    resolution='10m',
)
plt.show()
