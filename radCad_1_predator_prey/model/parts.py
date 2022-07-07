
import numpy as np

"""
    'grow_pokemon': grow_pokemon,
    'grow_trainers': grow_trainers,
    'eliminate_pokemon': eliminate_pokemon,
    'eliminate_trainers': eliminate_trainers,
    'pokemon_population': pokemon_population,
    'trainer_population': trainer_population            
"""

# Behaviors
def grow_pokemon(params, substep, state_history, prev_state):
    population_delta = (
        prev_state['pokemon_population'] *
        params['pokemon_reproduction_rate'] *
        params['dt']
    )
    return {'pokemon_population_delta': population_delta} 

def grow_trainers(params, substep, state_history, prev_state):
    population_delta = (
        prev_state['trainer_population'] *
        prev_state['pokemon_population'] *
        params['trainer_growth_rate'] *
        params['dt']
    )
    return {'trainer_population_delta': population_delta} 

def eliminate_pokemon(params, substep, state_history, prev_state):
    population_delta = -1 * (
        ( # natural elimination
            prev_state['pokemon_population'] *
            params['pokemon_death_rate']
        ) +
        ( # capture
            prev_state['pokemon_population'] *
            prev_state['trainer_population'] *
            params['pokemon_capture_rate']
        )
    ) * params['dt']
    return {'pokemon_population_delta': population_delta} 

def eliminate_trainers(params, substep, state_history, prev_state):
    population_delta = -1 * (
        prev_state['trainer_population'] *
        params['trainer_abandon_rate'] *
        params['dt']
    )
    return {'trainer_population_delta': population_delta} 



# Mechanisms
def pokemon_population(params, substep, state_history, prev_state, policy_input):
    updated_population = np.ceil(prev_state['pokemon_population'] + policy_input['pokemon_population_delta'])
    return ('pokemon_population', max(updated_population, 0))

def trainer_population(params, substep, state_history, prev_state, policy_input):
    updated_population = np.ceil(prev_state['trainer_population'] + policy_input['trainer_population_delta'])
    return ('trainer_population', max(updated_population, 0))