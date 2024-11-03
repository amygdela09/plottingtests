import os
import pyart

# open radar data
filename = os.getcwd() + '/Data/data (7).gz'
# radar = pyart.io.read_nexrad_archive(filename, station='KTLX')
radar = pyart.io.read_nexrad_archive(filename)
pyart.io.write_cfradial('testcfimage', radar, include_fields='reflectivity')
