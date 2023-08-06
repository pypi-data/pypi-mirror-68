from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Unit import *

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

spice_library = SpiceLibrary('.')

####################################################################################################

circuit = Circuit('DCBench')
Vgs = circuit.V('gs', 'gate', circuit.gnd, 1.8@u_V)
Vbs = circuit.V('bs', 'base', circuit.gnd, 0@u_V)
Vds = circuit.V('ds', 'drain', circuit.gnd, 1.8@u_V)

circuit.include(spice_library['TSMC180nmN'])

M0 = circuit.MOSFET('0', 'drain', 'gate', circuit.gnd, 'base',
                  model='TSMC180nmN', length=200@u_nm, width=200@u_nm)
print(circuit)

TempC = 27
simulator = circuit.simulator(temperature=TempC, nominal_temperature=TempC)
simulator.save_internal_parameters('@M0[gm]', '@M0[id]')
analysis = simulator.dc(Vgs=slice(0, 5, .01))

print(analysis['@M0[gm]'].str_data()[:100])
print(analysis['@M0[id]'].str_data()[:100])
