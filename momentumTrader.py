# -*- coding: utf-8 -*-
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series
import json


@with_series('close')
def momentum(series):
    return series - series.shift()  # Change to previous day


class MomentumStrategy(AbstractStrategy):
    def setUniverse(self, universe):
        self.universe=universe
    def initialize(self):
        #self.setUniverse(['GOOGL','TSLA', 'MSFT', 'NVDA', 'AMD', 'INTC' ])
        self.skip_days=1  # Automate this
        self.indicators={ 'MOMENTUM': momentum }
        self.netWorth = []

    def handle_data(self, data, indicators=None):
        sec_weight = 1 / len(self.universe)

        for sec in self.universe:
            if indicators[sec]['MOMENTUM'][-1] > 0.0:
                # Buy at next price, if security closed with an uptick
                self.environment.order_target_percent(sec, sec_weight)
            else:
                # Sell at next price, if security closed with a downtick
                self.environment.order_target_percent(sec, 0.0)
        networth = self.environment.portfolio.total_value(self.environment._next_prices())
        self.netWorth.append(networth)
    def jsonifyNetworth(self):
       print (type(self.netWorth))
       return self.netWorth

#strategy = MomentumStrategy()
#strategy.setUniverse(['GOOGL','TSLA', 'MSFT', 'NVDA', 'AMD', 'INTC' ])
#strategy.run()
#strategy.jsonifyNetworth()
