from model.system_parameters import SystemParameters

from .policy_aux import *
from .suf_aux import *
from .actions import *

def p_actionDecoder(params: SystemParameters, substep, sH, s):
    action = {
        'eth_sold': 0,
        'tokens_sold': 0,
        'eth_deposit': 0,
        'UNI_burn': 0, 
        'UNI_pct': 0,
        'fee': 0,
        'conv_tol': 0,
        'price_ratio': 0
    }

    #Event variables
    event = uniswap_events['event'][t]
    action['action_id'] = event

    if event in ['TokenPurchase', 'EthPurchase']:
        I_t, O_t, I_t1, O_t1, delta_I, delta_O, action_key = get_parameters(uniswap_events, event, s, t)
        if params['retail_precision'] == -1:
            action[action_key] = delta_I
        elif classifier(delta_I, delta_O, params['retail_precision']) == "Conv":            #Convenience trader case
            calculated_delta_O = int(get_output_amount(delta_I, I_t, O_t, params))
            if calculated_delta_O >= delta_O * (1-params['retail_tolerance']):
                action[action_key] = delta_I
            else:
                action[action_key] = 0
            action['price_ratio'] =  delta_O / calculated_delta_O
        else:            #Arbitrary trader case
            P = I_t1 / O_t1
            actual_P = I_t / O_t
            if(actual_P > P):
                I_t, O_t, I_t1, O_t1, delta_I, delta_O, action_key = get_parameters(uniswap_events, reverse_event(event), s, t)
                P = I_t1 / O_t1
                actual_P = I_t / O_t
                delta_I = get_delta_I(P, I_t, O_t, params)
                delta_O = get_output_amount(delta_I, I_t, O_t, params)
                if(unprofitable_transaction(I_t, O_t, delta_I, delta_O, action_key, params)):
                    delta_I = 0
                action[action_key] = delta_I
            else:
                delta_I = get_delta_I(P, I_t, O_t, params)
                delta_O = get_output_amount(delta_I, I_t, O_t, params)
                if(unprofitable_transaction(I_t, O_t, delta_I, delta_O, action_key, params)):
                    delta_I = 0
                action[action_key] = delta_I
    elif event == 'AddLiquidity':
        delta_I = uniswap_events['eth_delta'][t]
        action['eth_deposit'] = delta_I
    elif event == 'Transfer':
        UNI_delta = uniswap_events['uni_delta'][t]
        UNI_supply = uniswap_events['UNI_supply'][t-1]
        if UNI_delta < 0:
            action['UNI_burn'] = -UNI_delta
            action['UNI_pct'] = -UNI_delta / UNI_supply
    del uniswap_events
    return action
