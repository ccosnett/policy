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





import logging
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Optional

from policy import UniswapV3PoolWealthAgent
from dateutil import parser as dateparser
from policy import buy_bitcoins
#from policies. import PassiveConcentratedLP

from dojo.common.constants import Chain
from dojo.environments import UniswapV3Env
from dojo.runners import backtest_run




    # SNIPPET 1 START
pool0 = "USDC/WETH-0.05"
#pool1 = "USDC/WETH-0.3"
pool1 = "WBTC/WETH-0.05"
#pool1 = "USDC/WETH-0.3"
pools = ["USDC/WETH-0.05", "WBTC/WETH-0.05"]

run_length=timedelta(hours=0.05)    
start_time = dateparser.parse("2022-06-21 00:00:00 UTC")
end_time = start_time + run_length

agent1 = UniswapV3PoolWealthAgent(
     initial_portfolio= {"USDC": Decimal(50_000), "WETH": Decimal(25),"WBTC": Decimal(1)},
     name="bitcoin_buyer")


  
    # Simulation environment (Uniswap V3)
env = UniswapV3Env(
        chain=Chain.ETHEREUM,
        date_range=(start_time, end_time),
        agents=[agent1],
        pools=pools,
        backend_type="forked",
        market_impact="replay"
    )

    # Policies 
    #mvag_policy = MovingAveragePolicy(
    #   agent=agent1, pool="USDC/WETH-0.05", short_window=25, long_window=100
    #)

dashboard_server_port=2222
simulation_status_bar=True
auto_close=False
policy=buy_bitcoins(agent = agent1)

backtest_run(
        env,
        [policy],
        dashboard_server_port=dashboard_server_port,
        auto_close=auto_close,
        simulation_status_bar=simulation_status_bar,
    )
    # SNIPPET 1 END