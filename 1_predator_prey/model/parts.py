
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
    population_delta = 0 # 𝛼 * Pokemon * Δt 
    return {'pokemon_population_delta': population_delta} 

def pokemon_capture(params, substep, state_history, prev_state):
    population_delta = 0 # -(𝛽 * Pokemon * Trainers)
    return {'pokemon_population_delta': population_delta} 


def pokemon_natural_death(params, substep, state_history, prev_state):
    population_delta = 0 # -𝛾 * Pokemon * Δt
    return {'pokemon_population_delta': population_delta} 

def trainer_migration(params, substep, state_history, prev_state):
    population_delta = 0 #  𝛿 * Pokemon * Trainers * Δt 
    return {'trainer_population_delta': population_delta} 

def trainer_abandon(params, substep, state_history, prev_state):
    population_delta = 0 # -ε * Trainers * Δt
    return {'trainer_population_delta': population_delta} 

# Mechanisms
def pokemon_population(params, substep, state_history, prev_state, policy_input):
    updated_population = np.ceil(prev_state['pokemon_population'] + policy_input['pokemon_population_delta'])
    return ('pokemon_population', max(updated_population, 0))

def trainer_population(params, substep, state_history, prev_state, policy_input):
    updated_population = np.ceil(prev_state['trainer_population'] + policy_input['trainer_population_delta'])
    return ('trainer_population', max(updated_population, 0))