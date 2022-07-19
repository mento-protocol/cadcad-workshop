from typing import TypedDict

class StateVariables(TypedDict):
    timestep: int
    dai_balance: int
    eth_balance: int
    lp_token_supply: int
    price_ratio: int

initial_state = StateVariables(
    dai_balance=0,
    eth_balance=0,
    lp_token_supply=0,
    price_ratio=0
)
    
# genesis_states = {
#     'DAI_balance': 5900000000000000000000,
#     'ETH_balance': 30000000000000000000,
#     'UNI_supply': 30000000000000000000,
#     'price_ratio': 0
# }