
import numpy as np

# ΔPokemon / Δt = 𝛼 * Pokemon - 𝛽 * Pokemon * Trainers - ε * Pokemon
# ΔTrainers / Δt = 𝛿 * Pokemon * Trainers - 𝛾 * Trainers

# 𝛼 = pokemon reproduction rate
# 𝛽 = pokemon capture rate
# ε = pokemon death rate
# 𝛿 = trainer growth rate 
# 𝛾 = trainer abandon rate

# ΔPokemon  = (𝛼 * Pokemon - 𝛽 * Pokemon * Trainers - ε * Pokemon) * Δt
# ΔTrainers = (𝛿 * Pokemon * Trainers - 𝛾 * Trainers) * Δt 

# Behaviors
def grow_pokemon(params, substep, state_history, prev_state):
    # ΔPokemon = 𝛼 * Pokemon * Δt 
    population_delta = (
        prev_state['pokemon_population'] *
        params['pokemon_reproduction_rate'] *
        params['dt']
    )
    return {'pokemon_population_delta': 1} 

def eliminate_pokemon(params, substep, state_history, prev_state):
    # ΔPokemon = - (𝛽 * Pokemon * Trainers + ε * Pokemon) * Δt  
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

def grow_trainers(params, substep, state_history, prev_state):
    # ΔTrainers = 𝛿 * Pokemon * Trainers * Δt 
    population_delta = (
        prev_state['trainer_population'] *
        prev_state['pokemon_population'] *
        params['trainer_growth_rate'] *
        params['dt']
    )
    return {'trainer_population_delta': population_delta} 

def eliminate_trainers(params, substep, state_history, prev_state):
    # ΔTrainers = - ( 𝛾 * Trainers) * Δt 
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