# pip install colorama to run
########## ASSUMPTIONS #################################################
########################################################################
#
# add these lines to your "run.py" file
#
# pools = ["USDC/WETH-0.05", "WBTC/WETH-0.05"]
# 
# agent1 = UniswapV3PoolWealthAgent(
#     initial_portfolio= {"USDC": Decimal(50_000), "WETH": Decimal(25),"WBTC": Decimal(1)},
#     name="bitcoin_buyer",
#)
#
########################################################################
########################################################################
#
# START: 
from colorama import Fore, Style
from collections import deque
from decimal import Decimal
from typing import Any, List, Optional
import numpy as np
from dojo.actions.base_action import BaseAction
from dojo.actions.uniswapV3 import UniswapV3Trade
from dojo.agents import BaseAgent
from dojo.environments.uniswapV3 import UniswapV3Observation
from dojo.policies import BasePolicy
from dojo.agents import UniswapV3Agent
from decimal import Decimal
from typing import Optional
from dojo.agents import UniswapV3Agent
from dojo.environments.uniswapV3 import UniswapV3Observation

#######################################################################
# helper functions:
########################################################################
def echo(expr, label=None):
    """
    prints expr and returns expr
    """
    expr = str(expr)
    if label:
        print(f"{label} --> {expr}")
    else:
        print(expr)
    return expr

# this one needs a: "pip install colorama"
def echo_yellow(expr, label=None):
    """
    prints expr and returns expr
    """
    col = Fore.YELLOW
    expr = str(round(expr, 2))

    if label:
        print(col + f"{label} : $ {expr}" + Style.RESET_ALL)
    else:
        print(col + expr + Style.RESET_ALL)
    return expr

def echo_magenta(expr, label=None):
    """
    prints expr and returns expr
    """
    col = Fore.MAGENTA
    expr = str(round(expr, 2))

    if label:
        print(col + f"{label} : $ {expr}" + Style.RESET_ALL)
    else:
        print(col + expr + Style.RESET_ALL)
    return expr

def echo_cyan(expr, label=None):
    """
    prints expr and returns expr
    """
    col = Fore.CYAN
    expr = str(round(expr, 2))

    if label:
        print(col + f"{label} : {expr} %" + Style.RESET_ALL)
    else:
        print(col + expr + Style.RESET_ALL)
    return expr

def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


########################################################################
###### METRIC FUNCTIONS ###############################################
########################################################################

# need to be refactored as they aren't readable so don't read em

def total_wealth(portfolio, conversions):

    #echo(portfolio,'portfolio')
    # Compute USDC per WETH
    USDC_per_WETH = 1 / conversions['USDC/WETH-0.05']  # 1 / 0.000280
    # USDC_per_WETH = 3571.4285714285716

    # Compute USDC per WBTC
    WETH_per_WBTC = conversions['WBTC/WETH-0.05']  # 18.3
    USDC_per_WBTC = WETH_per_WBTC * USDC_per_WETH  # 18.3 * 3571.4285714285716

    # Now compute total wealth
    total_USDC = portfolio.get('USDC', 0)
    total_USDC += portfolio.get('WETH', 0) * USDC_per_WETH
    total_USDC += portfolio.get('WBTC', 0) * USDC_per_WBTC

    print("Total wealth in USDC:", total_USDC)


    #out1 = total_wealth(portfolio, conversions)
    return total_USDC

def portfol(agent):
    return agent.erc20_portfolio()


def conversions(obs):
    #pools =  obs.pools
    d = {}
    d["WBTC/WETH-0.05"] = obs.price('WBTC', 'WETH', "WBTC/WETH-0.05")
    d["USDC/WETH-0.05"] = obs.price('USDC', 'WETH', 'USDC/WETH-0.05')
    return d

def tw(obs, agent):
    portf = portfol(agent)
    convers = conversions(obs)
    return total_wealth(portf, convers)

def tw_p(obs, p):
    portf = p
    convers = conversions(obs)
    return total_wealth(portf, convers)


def initial_agent_wealth(obs, agent):
        if obs.block == 20129224:
            init_w = tw(obs, agent)
            
            global welt
            welt = init_w
            #echo_magenta(welt, "global welt set")
        else:
            init_w = welt 
            #echo_magenta(init_w, "global welt set")
        
        return init_w


def current_agent_wealth(obs, agent):
    return tw(obs, agent)
    
def HODL_agent_wealth(obs, agent):
    
    return tw_p(obs, agent.initial_portfolio)

def profit_n_loss(current_wealth, initial_wealth):
    out1 = current_wealth - initial_wealth
    out2 = out1
    return out2

def HODL_profit_n_loss(HODL_current_wealth, initial_wealth):
    out1 = HODL_current_wealth - initial_wealth
    out2 = out1
    return out2


def profit_n_loss_percentage(current_wealth, initial_wealth):
    out1 = 100*(current_wealth - initial_wealth)/initial_wealth
    return out1

def HODL_profit_n_loss_percentage(HODL_current_wealth, initial_wealth):
    out1 = 100*(HODL_current_wealth - initial_wealth)/initial_wealth
    return out1


def sig(sig, name, obs):
    obs.add_signal(name, sig)
    return None

def add_signals(obs, agent):

    init_w = initial_agent_wealth(obs, agent)
    echo_yellow(init_w, 'init_w')

    current_w_HODL = HODL_agent_wealth(obs, agent)
    echo_yellow(current_w_HODL, 'current_w_HODL')
        
    current_w = current_agent_wealth(obs, agent)
    echo_yellow(current_w,'current_w')

    PnL = profit_n_loss(current_w, init_w)
    PnL_HODL = HODL_profit_n_loss(current_w_HODL, init_w)
    PnLP = profit_n_loss_percentage(current_w, init_w)
    PnLP_HODL = HODL_profit_n_loss_percentage(current_w_HODL, init_w)


    echo(init_w,"initial_wealth")
    echo(current_w_HODL,"HODL_current_wealth")
    echo(current_w, "current_wealth")
    
    echo_magenta(PnL, "PnL")
    echo_magenta(PnL_HODL, "PnL HODL")
    echo_cyan(PnLP, "PnL %")
    echo_cyan(PnLP_HODL, "PnL_HODL %")

    sig(PnL, "PnL", obs)
    sig(PnLP, "PnL Percentage", obs)
    sig(init_w,"initial_wealth",obs)
    sig(PnLP_HODL,"PnL Percentage HODL",obs)
    sig(PnL_HODL,"PnL HODL",obs)
    #port = agent.erc20_portfolio()
    #echo_yellow(port,'port')
    #echo_yellow(agent,'self')
    



########################################################################
########################################################################

#       THE POLICY       ###############################################

########################################################################
########################################################################

class buy_bitcoins(BasePolicy):  # type: ignore
    """A policy that executes a single action: buying bitcoins.
    """

    def __init__(self, agent: BaseAgent):
        """Initialize the policy.

        :param agent: The agent which is using this policy.
        :param action: The action to execute.
        """
        super().__init__(agent)
        # rate of dumping
        self.dump_rate = Decimal(0.5)

    
    def dump_dollars(self, agent):

        amount_of_dollars = self.agent.erc20_portfolio()['USDC']
        echo(amount_of_dollars,"amount_of_dollars")

        if amount_of_dollars * self.dump_rate + Decimal(0.01) > Decimal(1):

            # amount to sell
            amount = amount_of_dollars * self.dump_rate
            action = UniswapV3Trade(agent=agent,
                              pool = "USDC/WETH-0.05",
                              quantities=(amount, Decimal(0))
                              )
            return action
        
        else:
            return []

        

    
    
    def buy_bitcoin(self, agent):

        amount_of_WETH = Decimal(0.01)* self.agent.erc20_portfolio()['WETH']
        echo(amount_of_WETH,"amount_of_WETH")

        if amount_of_WETH * self.dump_rate > Decimal(0.0005):

            # amount to sell
            amount = amount_of_WETH * self.dump_rate
            action = UniswapV3Trade(agent=agent,
                              pool = "WBTC/WETH-0.05",
                              quantities=(Decimal(0), amount)
                              )
            return action

        else:
            return []
        

        

    def predict(self, obs):
        echo(self.agent.erc20_portfolio()['WBTC'],'self.agent.erc20_portfolio()[\'WBTC\']')

        action_sequence = [
                self.dump_dollars(self.agent),
                self.buy_bitcoin(self.agent)
                ] 
        
        add_signals(obs = obs, agent=self.agent)
        
        return flatten(action_sequence)


        

    #def predict(self, obs):
#        return 1



########################################################################
########## Agent to be used:
########################################################################

class UniswapV3PoolWealthAgent(UniswapV3Agent):
    """This agent implements a pool wealth reward function for a single UniswapV3 pool.

    The agent should not be given any tokens that are not in the UniswapV3Env pool.
    """

    def __init__(
        self, initial_portfolio: dict[str, Decimal], name: Optional[str] = None
    ):
        """Initialize the agent."""
        super().__init__(name=name, initial_portfolio=initial_portfolio)

    def reward(self, obs: UniswapV3Observation) -> float:  # type: ignore
        """The agent wealth in units of asset y according to the UniswapV3 pool."""
        # define your PnL here, I'm happy to supply my own if asked.

        return Decimal(1_000_000_000)
