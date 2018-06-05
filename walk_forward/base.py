from abc import ABCMeta
from collections import deque
from .. import utilities

class ParameterSelector(object):
    __metaclass__ = ABCMeta

    def __init__(self, backtest_batch, optimization_parameter, strategy_class):
        self.backtest_batch = backtest_batch
        self.optimization_parameter = optimization_parameter
        self.strategy_class = strategy_class
        self.optimization_parameter_set = self.strategy_class.OPTIMIZATION_PARAMETER