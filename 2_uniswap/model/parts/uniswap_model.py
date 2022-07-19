from signal import signal
from typing import Any, Dict, List, Tuple, TypedDict

from pandas import DataFrame

from model.data import Event
from model.system_parameters import SystemParameters
from model.state_variables import StateVariables

from .actions import *

def n(v: int) -> float:
    return (float(v) / 1e18)

class SignalInput(TypedDict):
    dai_delta: int
    eth_delta: int
    lp_token_delta: int
    price_ratio: float

def __event_at_t_as_dict__(events: DataFrame, t: int) -> Event:
    return events[t:t+1].to_dict(orient='index')[t]

def decode_action(
    params: SystemParameters, 
    _substep: int, 
    _state_history: List[StateVariables], 
    state: StateVariables
) -> Dict[str, Any]:
    action = Action.from_event(
        __event_at_t_as_dict__(
            params['uniswap_events'],
            state['timestep']
        )
    )
    deltas = { 
        'dai_delta': action.dai_delta(state, params),
        'eth_delta': action.eth_delta(state, params),
        'lp_token_delta': action.lp_token_delta(state, params)
    }
    if params['debug']:
        print("[%d] %s" % (state['timestep'], action))
        print("[%d]    ⍙Dai = %f (%d)" % (state['timestep'], n(deltas['dai_delta']), deltas['dai_delta']))
        print("[%d]    ⍙Eth = %f (%d)" % (state['timestep'], n(deltas['eth_delta']), deltas['eth_delta']))
        print("[%d]    ⍙LP = %f (%d)" % (state['timestep'], n(deltas['lp_token_delta']), deltas['lp_token_delta']))

    return deltas

def update_dai_balance(
    params: SystemParameters, 
    _substep: int, 
    _state_history: List[StateVariables], 
    state: StateVariables,
    input: SignalInput
) -> Tuple[str, int]:
    next_dai_balance = (
        state['dai_balance'] + 
        input['dai_delta']
    )
    if params['debug']:
        print("[%d] DAI %f -> %f" % (state['timestep'], n(state['dai_balance']), n(next_dai_balance)))
    return('dai_balance', next_dai_balance)
    
def update_eth_balance(
    params: SystemParameters, 
    _substep: int, 
    _state_history: List[StateVariables], 
    state: StateVariables,
    input: SignalInput
) -> Tuple[str, int]:
    next_eth_balance = (
        state['eth_balance'] +
        input['eth_delta']
    )
    if params['debug']:
        print("[%d] ETH %f -> %f" % (state['timestep'], n(state['eth_balance']), n(next_eth_balance)))
    return('eth_balance', next_eth_balance)

def update_lp_token_supply(
    params: SystemParameters, 
    _substep: int, 
    _state_history: List[StateVariables], 
    state: StateVariables,
    input: SignalInput
) -> Tuple[str, int]:
    next_lp_token_supply = (
        state['lp_token_supply'] +
        input['lp_token_delta']
    )
    if params['debug']:
        print("[%d] LP %f -> %f" % (state['timestep'], n(state['lp_token_supply']), n(next_lp_token_supply)))
    return('lp_token_supply', next_lp_token_supply)

def update_price_ratio(
    params: SystemParameters, 
    _substep: int, 
    _state_history: List[StateVariables], 
    state: StateVariables,
    input: SignalInput
) -> Tuple[str, float]:
    return('price_ratio', input.get('price_ratio', 0))