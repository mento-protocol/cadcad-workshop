"""
The default experiment with default model, Initial State,
System Parameters, and Simulation Configuration.

The defaults are defined in their respective modules:
* Initial State in `model/state_variables.py`
* System Parameters in `model/system_parameters.py`
* Simulation Configuration in `experiments/simulation_configuration.py`
"""

from radcad import Simulation, Experiment, Backend, Model
from .parts.uniswap_model import *
from .sim_params import *
from .state_variables import initial_state
from .system_parameters import params

model = Model(
    initial_state=initial_state,
    params=params,
    state_update_blocks=[
        {
            'policies': {
                'user_action': decode_action,
            },
            'variables': {
                'dai_balance': update_dai_balance,
                'eth_balance': update_eth_balance,
                'lp_token_supply': update_lp_token_supply,
                'price_ratio': update_price_ratio
            }
        }

    ]
)


# Create Model Simulation
simulation = Simulation(
    model=model,
    timesteps=SIMULATION_TIME_STEPS,
    runs=MONTE_CARLO_RUNS
)

# Create Experiment of single Simulation
experiment = Experiment([simulation])

# Configure Simulation & Experiment engine
# simulation.engine = experiment.engine
experiment.engine.backend = Backend.MULTIPROCESSING
experiment.engine.deepcopy = False
# experiment.engine.drop_substeps = True  # Do not store data for substeps
