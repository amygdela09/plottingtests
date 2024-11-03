import os
import matplotlib.pyplot as plt
import pyart

# open the file, create the displays and figure
filename = os.getcwd() + "/Data/data (9).gz"
radar = pyart.io.read_nexrad_archive(filename)
gatefilter = pyart.filters.GateFilter(radar)
gatefilter.exclude_below("reflectivity", 0)
gatefilter.exclude_transition()
display = pyart.graph.RadarDisplay(radar)
fig = plt.figure(figsize=(18, 10))

ax = fig.add_subplot(121)
display.plot_ppi(
    "reflectivity",
    sweep=0,
    vmin=-32,
    vmax=70,
    title='Reflectivity',
    cmap="pyart_NWSRef",
    gatefilter=gatefilter,
    ax=ax,
    colorbar_orient='horizontal',
    axislabels_flag=False,
)
display.set_limits((-100, 100), (-100, 100), ax=ax)

ax2 = fig.add_subplot(122)
display.plot_ppi(
    "velocity",
    sweep=1,
    vmin=-32,
    vmax=30,
    title="Velocity",
    cmap="pyart_NWSVel",
    gatefilter=gatefilter,
    ax=ax2,
    colorbar_orient='horizontal',
    axislabels_flag=False,
)
display.set_limits((-100, 100), (-100, 100), ax=ax2)
plt.show()
