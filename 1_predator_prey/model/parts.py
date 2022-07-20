
import numpy as np

# ΔPokemon / Δt = 𝛼 * Pokemon - 𝛽 * Pokemon * Trainers - 𝛾 * Pokemon
# ΔTrainers / Δt = 𝛿 * Pokemon * Trainers - ε * Trainers

# 𝛼 = pokemon reproduction rate
# 𝛽 = pokemon capture rate
# 𝛾 = pokemon death rate
# 𝛿 = trainer growth rate 
# ε  = trainer abandon rate


# ΔPokemon  = (𝛼 * Pokemon - 𝛽 * Pokemon * Trainers - 𝛾 * Pokemon) * Δt
# ΔTrainers = (𝛿 * Pokemon * Trainers - ε * Trainers) * Δt 

# Behaviors
def pokemon_natural_growth(params, substep, state_history, prev_state):
    # 𝛼 * Pokemon * Δt 
    population_delta = (
        prev_state['pokemon_population'] *
        params['pokemon_reproduction_rate'] *
        params['dt']
    )
    return {'pokemon_population_delta': population_delta} 

def pokemon_capture(params, substep, state_history, prev_state):
    # -(𝛽 * Pokemon * Trainers)
    population_delta = -1 * (
        prev_state['pokemon_population'] *
        prev_state['trainer_population'] *
        params['pokemon_capture_rate'] *
        params['dt']
    )
    return {'pokemon_population_delta': population_delta} 


def pokemon_natural_death(params, substep, state_history, prev_state):
    # -𝛾 * Pokemon * Δt
    population_delta = -1 * (
        prev_state['pokemon_population'] *
        params['pokemon_death_rate'] *
        params['dt']
    )
    return {'pokemon_population_delta': population_delta} 

def trainer_migration(params, substep, state_history, prev_state):
    #  𝛿 * Pokemon * Trainers * Δt 
    population_delta = (
        prev_state['trainer_population'] *
        prev_state['pokemon_population'] *
        params['trainer_growth_rate'] *
        params['dt']
    )
    return {'trainer_population_delta': population_delta} 

def trainer_abandon(params, substep, state_history, prev_state):
    # -ε * Trainers * Δt
    population_delta = -1 * (
        params['trainer_abandon_rate'] *
        prev_state['trainer_population'] *
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