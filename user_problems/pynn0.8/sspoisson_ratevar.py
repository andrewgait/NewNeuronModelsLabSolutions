import statistics
import spynnaker8 as sim

rates = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11,
0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.32, 0.64,
1.28, 2.56, 5.12, 10.24, 20.48, 40.96, 81.92, 163.84, 327.68, 655.36,
1310.72]

# rates = [2000, 3000]
n_neurons = 20 # number of neurons in each population
simtime = 10 * 1000

sim.setup(timestep=1.0, min_delay=1.0, max_delay=144.0)
# sim.setup(timestep=0.1, min_delay=0.1, max_delay=14.4)

inputs = {}
for rate in rates:
    params = {"rate": rate}
    input = sim.Population(
        n_neurons, sim.SpikeSourcePoisson, params, label='inputSpikes_1')
    input.record("spikes")
    inputs[rate] = input

sim.run(simtime)

means = {}
stdevs = {}
with open("spikes2.csv", "w") as spike_file:
    for rate in rates:
        neo = inputs[rate].get_data("spikes")
        spikes = neo.segments[0].spiketrains
        counts = []
        spike_file.write(str(rate))
        for a_spikes in spikes:
            spike_file.write(",")
            length = len(a_spikes)
            spike_file.write(str(length))
            counts.append(length)
        spike_file.write("\n")
        means[rate] = statistics.mean(counts)
        stdevs[rate] = statistics.stdev(counts, means[rate])

for rate in rates:
    print(rate, means[rate], stdevs[rate])

sim.end()