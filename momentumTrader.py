# -*- coding: utf-8 -*-
from pytrading.entities import AbstractStrategy
from pytrading.indicators import with_series
import json
import random


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
    def getNetworth(self):
       return self.netWorth

class randomStrategy(AbstractStrategy):
    def setUniverse(self, universe):
        self.universe=universe
    def initialize(self):
        #self.setUniverse(['GOOGL','TSLA', 'MSFT', 'NVDA', 'AMD', 'INTC' ])
        self.indicators={'MOMENTUM':momentum}
        self.netWorth = []

    def handle_data(self, data, indicators=None):
        weights = []
        weight_sum = 0
        for i in range(len(self.universe)):
            number = random.randint(0,100)
            weights.append(number)
            weight_sum += number
        weights = list(map(lambda x: x/weight_sum, weights))
        for sec, sec_weight in zip(self.universe, weights):
            self.environment.order_target_percent(sec, sec_weight)
        networth = self.environment.portfolio.total_value(self.environment._next_prices())
        self.netWorth.append(networth)
    def getNetworth(self):
       return self.netWorth

testUn = ['BABA','ATHN','BLUE','DXCM','ESLT', 'SKX','TSLA','TUBE']
def testMomentum():
    strategy = MomentumStrategy(100000)
    strategy.setUniverse(testUn)
    strategy.run()
    print(strategy.getNetworth())
def testRandom():
    strategy = randomStrategy(100000)
    strategy.setUniverse(testUn)
    strategy.run()
    print(strategy.getNetworth())
