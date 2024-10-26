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
#from colorama import Fore, Style
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

def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


########################################################################

#pools = ["USDC/WETH-0.05", "WBTC/WETH-0.05"]

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

        if amount_of_WETH * self.dump_rate * Decimal(0.01) > Decimal(0.0005):

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
        
        return flatten(action_sequence)


        

    #def predict(self, obs):
#        return 1




########## Agent to be used:

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
