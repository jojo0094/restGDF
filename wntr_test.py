import numpy as np
from scipy.stats import lognorm
import networkx as nx
import geopandas as gpd
import matplotlib.pylab as plt
import warnings
import wntr

# Create a WaterNetworkModel from an EPANET INP file
wn = wntr.network.WaterNetworkModel('data/test1.inp')
wn.nodes
print(wn.nodes)

print(wn.options)
#change duraiton 2 hr
wn.options.time.duration = 2 * 3600  # 2 hours in seconds

sim = wntr.sim.EpanetSimulator(wn)
results_EPANET = sim.run_sim()
print(results_EPANET.node['demand'].head())
#flow
print(results_EPANET.link['flowrate'].head())

#check demand form node
print(wn.nodes['J1'].demand_timeseries_list)


#save .inp file
wntr.network.io.write_inpfile(wn, 'data/test1_modified2.inp')

