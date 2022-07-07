"""
The default experiment with default model, Initial State,
System Parameters, and Simulation Configuration.

The defaults are defined in their respective modules:
* Initial State in `model/state_variables.py`
* System Parameters in `model/system_parameters.py`
* Simulation Configuration in `experiments/simulation_configuration.py`
"""

from radcad import Simulation, Experiment, Backend, Model
from .parts import *

# from model import model


model = Model(
    params={
        'pokemon_reproduction_rate': [0.3],
        'pokemon_capture_rate': [0.001],
        'pokemon_death_rate': [0.01],
        'trainer_abandon_rate': [0.2],
        'trainer_growth_rate': [0.0001],
        'dt': [0.1]
    },
    initial_state={
        'pokemon_population': 100,
        'trainer_population': 3000
    },
    state_update_blocks=[
        {
            # lotka_volterra.py
            'policies': {
                'grow_pokemon': grow_pokemon,
                'grow_trainers': grow_trainers,
                'eliminate_pokemon': eliminate_pokemon,
                'eliminate_trainers': eliminate_trainers,
            },
            'variables': {
                'pokemon_population': pokemon_population,
                'trainer_population': trainer_population            
            }
        }
    ]
)


# Create Model Simulation
simulation = Simulation(
    model=model,
    timesteps=3000,
    runs=1
)

# Create Experiment of single Simulation
experiment = Experiment([simulation])

# Configure Simulation & Experiment engine
# simulation.engine = experiment.engine
experiment.engine.backend = Backend.SINGLE_PROCESS
experiment.engine.deepcopy = False
experiment.engine.drop_substeps = True  # Do not store data for substeps
