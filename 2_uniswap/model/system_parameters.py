from typing import List, TypedDict
import pandas as pd
from model.data import UNISWAP_EVENTS

class SystemParametersConfig(TypedDict):
    debug: List[bool]
    fee_numerator: List[int]
    fee_denominator: List[int]
    uniswap_events: List[pd.DataFrame]
    # fix_cost: List[int] # -1 to deactivate
    # retail_precision: List[int]
    # retail_tolerance: List[float]

class SystemParameters(TypedDict):
    debug: bool
    fee_numerator: int
    fee_denominator: int
    uniswap_events: pd.DataFrame
    # fix_cost
    

params = SystemParametersConfig(
    debug=[False],
    fee_numerator=[997, 995, 990],
    fee_denominator=[1000],
    uniswap_events=[UNISWAP_EVENTS]
)

# sys_params = {
#     'fee_numerator': [997, 997, 997, 997,
#                         995, 995, 995, 995],
#     'fee_denominator': [1000],
#     'uniswap_events': [UNISWAP_EVENTS],
#     'fix_cost': [-1], # -1 to deactivate
#     'retail_precision': [3,3,15,15,
#                 3,3,15,15],
#     'retail_tolerance': [0.0005, 0.025, 0.0005, 0.025,
#                         0.0005, 0.025, 0.0005, 0.025]
# }