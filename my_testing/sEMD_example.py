


"""
Spiking ELementary Motion Detector (sEMD) example
See https://www.cit-ec.de/en/nbs/spiking-insect-vision for more details
"""

# imports
import spynnaker8 as p
# from spynnaker.pyNN.models.neuron.builds import IFCurrExpSEMD
import numpy
import matplotlib.pyplot as plt
# import matplotlib as mpl
from pyNN.utility.plotting import Figure, Panel


# variables
weights = 1
spike_time_facilitation = 4
spike_time_trigger = 20



# set up simulation
simulation_timestep = 1 # ms
simulation_runtime = 100 # ms
p.setup(timestep=simulation_timestep)




# neuron parameters
cell_params_semd = {'cm'        : 0.25,
                    'i_offset'  : 0,                        # offset current
                    'tau_m'     : 10,                       # membrane potential time constant
                    'tau_refrac': 1,                        # refractory period time constant
                    'tau_syn_E' : 20 ,                      # excitatory current time constant
                    'tau_syn_I' : 20 ,                      # inhibitory current time constant
                    'v_reset'   : -85,                      # reset potential
                    'v_rest'    : -60,                      # resting potential
                    'v_thresh'  : -50                       # spiking threshold
                              }





# neuron populations
sEMD = p.Population(1, p.extra_models.IF_curr_exp_sEMD, cell_params_semd, label = "sEMD") # (population size, neuron type, cell parameters, label)
input_facilitation = p.Population(1, p.SpikeSourceArray, {'spike_times': [[spike_time_facilitation]]}, label = "input_facilitation")
input_trigger = p.Population(1, p.SpikeSourceArray, {'spike_times': [[spike_time_trigger]]}, label = "input_trigger")

sEMD.initialize(v=-60.0)


# projections
p.Projection(input_facilitation,sEMD, p.OneToOneConnector(), p.StaticSynapse(weight= weights,delay=1), receptor_type= 'excitatory')
p.Projection(input_trigger,sEMD, p.OneToOneConnector(), p.StaticSynapse(weight=weights,delay=1), receptor_type= 'excitatory2')




# records
sEMD.record(['spikes','v','gsyn_exc','gsyn_inh'])

# run simulation
p.run(simulation_runtime)

# receive data from neurons
spikes = sEMD.get_data(['spikes'])
v = sEMD.get_data(['v'])
current_exc = sEMD.get_data(['gsyn_exc'])
current_inh = sEMD.get_data(['gsyn_inh'])




# plots
Figure(
    # raster plot of the neuron spike times
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=4, xlim=(0, simulation_runtime)),
    # membrane potential
    Panel(v.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[sEMD.label], yticks=True, xlim=(0, simulation_runtime)),
    # excitatory current
    Panel(current_exc.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[sEMD.label], yticks=True, xlim=(0, simulation_runtime)),
    # inhibitory current
    Panel(current_inh.segments[0].filter(name='gsyn_inh')[0],
          xlabel="Time (ms)", xticks=True,
          ylabel="gsyn inhibitory (mV)",
          data_labels=[sEMD.label], yticks=True, xlim=(0, simulation_runtime)),
    title="SEMD example",
    annotations="Simulated with {}".format(p.name())
)
# plt.show()
plt.savefig('results.png')



# end
p.end()


