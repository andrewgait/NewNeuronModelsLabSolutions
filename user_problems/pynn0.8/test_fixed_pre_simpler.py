import spynnaker8 as sim
from pyNN.utility.plotting import Figure, Panel
import matplotlib.pyplot as plt

sim.setup(timestep=1.0)

n_pre_neurons = 5
n_post_neurons = 5
runtime = 100

input_pop = sim.Population(n_pre_neurons, sim.SpikeSourceArray([0]), label="input")
pop = sim.Population(n_post_neurons, sim.IF_curr_exp(), label="pop")

n_pre = 2
weights = 3.0
delays = 5

c2 = sim.Projection(input_pop, pop, sim.FixedNumberPreConnector(n_pre),
                    sim.StaticSynapse(weight=weights, delay=delays))

pop.record(['v', 'spikes'])

sim.run(runtime)

weights_delays = sorted(c2.get(['weight', 'delay'], 'list'),
                        key = lambda x: x[1])

print(weights_delays)
print(len(weights_delays))


# get data (could be done as one, but can be done bit by bit as well)
spikes = pop.get_data('spikes')
v = pop.get_data('v')

Figure(
    # membrane potential of the postsynaptic neuron
    Panel(v.segments[0].filter(name='v')[0],
          ylabel="Membrane potential (mV)",
          data_labels=[pop.label], yticks=True, xlim=(0, runtime)),
    # raster plot of the presynaptic neuron spike times
    Panel(spikes.segments[0].spiketrains,
          xlabel="Time (ms)", xticks=True,
          yticks=True, markersize=0.5, xlim=(0, runtime)),
    title="one-to-one connector, varying delays",
    annotations="Simulated with {}".format(sim.name())
)

plt.show()

sim.end()
