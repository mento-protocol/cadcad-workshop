from typing import List, TypedDict
import pandas as pd
# UNISWAP_EVENTS = pd.read_pickle('./data/uniswap_events.pickle').drop([0, 1]).reset_index()

UNISWAP_EVENTS = pd.read_pickle('./data/uniswap_events.pickle')

class Event(TypedDict):
    transactionHash: str
    transaction_index: int
    transaction_sender: str
    data: str
    topics: List[str]
    block_timestamp: pd.Timestamp
    blockNumber_dec: int
    contract: str
    event: str
    contract_event: str
    block_group: int
    agent: str
    eth_delta: int
    token_delta: int
    uni_delta: int
    eth_balance: int
    token_balance: int
    UNI_supply: int
    invariant: int