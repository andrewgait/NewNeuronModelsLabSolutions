import spynnaker8 as sim

sim.setup(timestep=1.0)

model = sim.IF_curr_exp

cell_params_input = {'cm': 0.25,
                     'i_offset': 1.0,
                     'tau_m': 20.0,
                     'tau_refrac': 2.0,
                     'tau_syn_E': 5.0,
                     'tau_syn_I': 5.0,
                     'v_reset': -70.0,
                     'v_rest': -65.0,
                     'v_thresh': -50.0
                     }

cell_params_output = {'cm': 0.25,
                      'i_offset': 0.0,
                      'tau_m': 20.0,
                      'tau_refrac': 2.0,
                      'tau_syn_E': 5.0,
                      'tau_syn_I': 5.0,
                      'v_reset': -70.0,
                      'v_rest': -65.0,
                      'v_thresh': -50.0
                      }

pre_size = 2
post_size = 3
simtime = 200

pre_pop = sim.Population(pre_size, model(**cell_params_input))
post_pop = sim.Population(post_size, model(**cell_params_output))

wiring = sim.AllToAllConnector()
static_synapse = sim.StaticSynapse(weight=2.5, delay=100.0)
proj = sim.Projection(pre_pop, post_pop, wiring, receptor_type='excitatory',
                      synapse_type=static_synapse)

# record post-pop spikes to check activation
post_pop.record(['spikes'])

# run simulation
sim.run(simtime)

# get data
neo_post_spikes = post_pop.get_data(['spikes'])
weightsdelays = proj.get(["weight", "delay"], "list")

# end simulation
sim.end()

# Check there are spikes
length = len(neo_post_spikes.segments[0].spiketrains[0])
print(neo_post_spikes.segments[0].spiketrains[0])
print("length: ", length)
print(weightsdelays)
assert(length > 0)