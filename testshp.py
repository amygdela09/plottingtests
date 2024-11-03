import os
import pyart

# open radar data
filename = os.getcwd() + '/Data/data (5).gz'
# radar = pyart.io.read_nexrad_archive(filename, station='KTLX')

radar = pyart.io.read_nexrad_archive(filename)
gatefilter = pyart.filters.GateFilter(radar)
gatefilter.exclude_below('reflectivity', 0)
gatefilter.exclude_transition()
grid = pyart.map.grid_from_radars(
    radar,
    gatefilters=(gatefilter,),
    grid_shape=(1, 1600, 1600),
    # grid_shape=(1, 241, 241),
    grid_limits=(
        (2000, 2000,),
        (-123000.0, 123000.0),
        (-123000.0, 123000.0),
    ),
    # gridding_algo='map_gates_to_grid',
)
pyart.io.write_grid_geotiff(
    grid,
    'geotest',
    'reflectivity',
    rgb=True,
    warp=True,
    cmap='pyart_NWSRef',
)
