# ASSUMPTIONS:
# add these lines to your "run.py" file
#
# pools = ["USDC/WETH-0.05", "WBTC/WETH-0.05"]
# 
# agent1 = UniswapV3PoolWealthAgent(
#     initial_portfolio= {"USDC": Decimal(50_000), "WETH": Decimal(25),"WBTC": Decimal(1)},
#     name="bitcoin_buyer",
#)
#
#


from collections import deque
from decimal import Decimal
from typing import Any, List

import numpy as np

from dojo.actions.base_action import BaseAction
from dojo.actions.uniswapV3 import UniswapV3Trade
from dojo.agents import BaseAgent
from dojo.environments.uniswapV3 import UniswapV3Observation
from dojo.policies import BasePolicy


#pools = ["USDC/WETH-0.05", "WBTC/WETH-0.05"]

class buy_bitcoins(BasePolicy):  # type: ignore
    """A policy that executes a single action: buying bitcoins.
    """

    def __init__(self, agent):
        """Initialize the policy.

        :param agent: The agent which is using this policy.
        :param action: The action to execute.
        """
        super().__init__(agent)

    
    def dump_dollars(agent):

        amount_of_dollars = 

        return UniswapV3Trade(agent=agent,
                              pool = "USDC/WETH-0.05"
                              quantities=()
                              )

        

        
        self.dump_your_dollars = act.buy(agent, "USDC/WETH-0.05", Decimal(100))
        self.buy_bitcoin = act.sell(agent, "USDC/WETH-0.05", Decimal(100))


    def predict(self, obs):
        #p = self.agent.portfolio()
        #echo_red(self.agent.initial_portfolio,"init_p")
        #echo_red(p,"p")
        #echo_red(current_wealth(obs, p),"c_weal")
        #sig(initial_agent_wealth(obs,))

        
        

        buy = self.buy
        sell = self.sell
        x = self.last_price
        y = pric(obs)

        sig(x,'x',obs)
        sig(y,'y',obs)


        if x - y > Decimal(0.1):
            echo_yellow("price has dropped: buy!!!")
            self.last_price = y
            return []
        elif x - y < Decimal(0.1):
            #echo_yellow("price hasn't changed much: do nothing!!!")
            self.last_price = y
            return []
        else:
            echo_yellow("price has risen: sell!!!")
            self.last_price = y
            return [] 
        


        

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
        pool = obs.pools[0]
        pool_tokens = obs.pool_tokens(pool=pool)

        token_ids = self.get_liquidity_ownership_tokens()
        lp_portfolio = obs.lp_portfolio(token_ids)
        wallet_portfolio = self.erc20_portfolio()

        # wealth expressed as token0 of the pool
        wealth = Decimal(0)
        for token, quantity in lp_portfolio.items():
            wealth += quantity * obs.price(token=token, unit=pool_tokens[0], pool=pool)
        for token, quantity in wallet_portfolio.items():
            wealth += quantity * obs.price(token=token, unit=pool_tokens[0], pool=pool)
        return float(wealth)
