import spynnaker8 as sim
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

# UNFINISHED TEST AS VariableSpikeSourcePoisson isn't in master yet

sources = 1
destinations = 1

sim.setup(1.0)
# sim.set_number_of_neurons_per_core(sim.SpikeSourceArray, 5)
# sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 5)

pop1 = sim.Population(sources, sim.VariableSpikeSourcePoisson,
                      label="input")
pop2 = sim.Population(destinations, sim.IF_curr_exp(),
                      label="pop2")
synapse_type = sim.StaticSynapse(weight=1.5, delay=2)

pop1view = pop1[1:4]
pop2view = pop2[1:4]

pop2view.set(i_offset=3.0)

connector = sim.OneToOneConnector()
# connector = sim.AllToAllConnector()
# connector = sim.FromListConnector([(1, 2), (0, 1)])
# projection = sim.Projection(pop1, pop2, connector,
#                             synapse_type=synapse_type)
projection = sim.Projection(pop1view, pop2view, connector,
                            synapse_type=synapse_type)
#projection = sim.Projection(pop1, pop2, sim.FromListConnector([[0,0]]),
#                            synapse_type=synapse_type)
# sim.run(0)

pop2.record('all')

before_pro = projection.get(["weight", "delay"], "list")
print('projection.get was called before run')
runtime=100
sim.run(runtime)
after_pro = projection.get(["weight", "delay"], "list")

ioffset2 = pop2.get('i_offset')

print(ioffset2)

print(before_pro)
print(len(before_pro))
print(after_pro)
print(len(after_pro))

v = pop2.get_data('v')
gsyn_exc = pop2.get_data('gsyn_exc')
gsyn_inh = pop2.get_data('gsyn_inh')
spikes = pop2.get_data('spikes')

Figure(
    # raster plot of the presynaptic neuron spike times
    Panel(spikes.segments[0].spiketrains,
          yticks=True, markersize=0.2, xlim=(0, runtime)),
    # membrane potential of the postsynaptic neuron
    Panel(v.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop2.label], yticks=True, xlim=(0, runtime)),
    Panel(gsyn_exc.segments[0].filter(name='gsyn_exc')[0],
          ylabel="gsyn excitatory (mV)",
          data_labels=[pop2.label], yticks=True, xlim=(0, runtime)),
    Panel(gsyn_inh.segments[0].filter(name='gsyn_inh')[0],
          ylabel="gsyn inhibitory (mV)",
          data_labels=[pop2.label], yticks=True, xlim=(0, runtime)),
    title="Simple synfire chain example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()

sim.end()