from signal import default_int_handler
from tkinter import W
from typing import NamedTuple

from model.data import Event
from model.state_variables import StateVariables
from model.system_parameters import SystemParameters


class Action():
    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        raise NotImplemented

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        raise NotImplemented

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        raise NotImplemented
    
    @staticmethod
    def from_event(event: Event) -> "Action":
        if event['event'] == 'TokenPurchase':
            return SellEth(eth=abs(event['eth_delta']))
        elif event['event'] == 'EthPurchase':
            return SellToken(tokens=abs(event['token_delta']))
        elif event['event'] == 'AddLiquidity':
            return Deposit(eth=abs(event['eth_delta']), tokens=abs(event['token_delta']))
        elif event['event'] == 'RemoveLiquidity':
            return Withdraw(eth=abs(event['eth_delta']), tokens=abs(event['token_delta']))
        elif event['event'] == 'Transfer':
            if event['uni_delta'] > 0:
                return LPTokenMint(
                    tokens=abs(event['uni_delta']),
                    percentage= event['uni_delta'] / event['UNI_supply']
                )
            elif event['uni_delta'] < 0:
                return LPTokenBurn(
                    tokens=abs(event['uni_delta']),
                    percentage=event['uni_delta'] / event['UNI_supply']
                )
        return Noop()

class Noop(Action):
    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

class SellEth(Action, NamedTuple):
    eth: int

    def __str__(self) -> str:
        return "SellEth(eth=%f)" % (self.eth / 1e18)

    def dai_delta(self, state: StateVariables, params: SystemParameters) -> int:
        if self.eth == 0:
            return 0
        

        # ETH_after_fee = ETH * (1 - fee)
        # ΔDai = ETH_after_fee * Price
        # Price = B_Dai / (B_Eth + Eth_after_fee)
        # ΔDai = ETH_after_fee * B_Dai / (B_Eth+ Eth_after_fee)

        # with fee = 0.3% = 3 / 1000 
        # 1 - fee = 997 / 1000
        # fee_numerator = 997
        # fee_denominator = 1000
        # ΔDai = Eth * 997/1000 * B_Dai / (B_Eth + Eth * 997/1000)
        # ΔDai = (Eth * 997 * B_Dai) / (B_Eth + Eth * 997/1000) * 1000
        # ΔDai = (Eth * 997 * B_Dai) / B_Eth * 1000 + Eth * 997
        # ΔDai = (Eth * fee_numerator * B_Dai) / B_Eth * fee_denominator + Eth * fee_numerator
        
        sold_with_fee = self.eth * params['fee_numerator']
        numerator = sold_with_fee * state['dai_balance']
        denominator = (
            state['eth_balance'] * params['fee_denominator'] + 
            sold_with_fee
        )
        delta = -1 * int(numerator // denominator)                      
        return delta
    
    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return self.eth

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

class SellToken(Action, NamedTuple):
    tokens: int

    def __str__(self) -> str:
        return "SellToken(tokens=%f)" % (self.tokens / 1e18)

    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return self.tokens

    def eth_delta(self, state: StateVariables, params: SystemParameters) -> int:
        if self.tokens == 0:
            return 0
        sold_with_fee = self.tokens * params['fee_numerator']
        numerator = sold_with_fee * state['eth_balance']
        denominator = (
            state['dai_balance'] * params['fee_denominator'] + 
            sold_with_fee
        )
        delta = -1 * int(numerator // denominator)
        return delta

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0
        

class Deposit(Action, NamedTuple):
    eth: int
    tokens: int

    def __str__(self) -> str:
        return "Deposit(eth=%f, tokens=%f)" % (self.eth / 1e18, self.tokens / 1e18)

    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return self.tokens

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return self.eth

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

class Withdraw(Action, NamedTuple):
    eth: int
    tokens: int

    def __str__(self) -> str:
        return "Withdraw(eth=%f, tokens=%f)" % (self.eth / 1e18, self.tokens / 1e18)

    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return -1 * self.tokens

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return -1 * self.eth

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

class LPTokenMint(Action, NamedTuple):
    tokens: int
    percentage: float

    def __str__(self) -> str:
        return "LPTokenMint(tokens=%f, percentage=%f)" % (self.tokens / 1e18, self.percentage)

    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return self.tokens

class LPTokenBurn(Action, NamedTuple):
    tokens: int
    percentage: float

    def __str__(self) -> str:
        return "LPTokenBurn(tokens=%f, percentage=%f)" % (self.tokens / 1e18, self.percentage)

    def dai_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def eth_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return 0

    def lp_token_delta(self, _state: StateVariables, _params: SystemParameters) -> int:
        return -1 * self.tokens