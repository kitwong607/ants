from abc import ABCMeta, abstractmethod
from .. import utilities


class AbstractStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def GET_ALL_OPTIMIZATION_PARAMETER(parameter_list):
        raise NotImplementedError("Should implement GET_ALL_OPTIMIZATION_PARAMETER()")

    @abstractmethod
    def calculate_bar_event(self, event):
        raise NotImplementedError("Should implement calculate_bar_event()")

    @abstractmethod
    def calculate_tick_event(self, event):
        raise NotImplementedError("Should implement calculate_tick_event()")

    @abstractmethod
    def calculate_entry_signals(self, event):
        raise NotImplementedError("Should implement calculate_tick_event()")

    @abstractmethod
    def calculate_exit_signals(self, event):
        raise NotImplementedError("Should implement calculate_tick_event()")

    @abstractmethod
    def place_order(self, event):
        raise NotImplementedError("Should implement place_order()")

    @abstractmethod
    def on_order_timeout(self, event):
        raise NotImplementedError("Should implement on_order_timeout()")


    def get_strategy_settings(self):
        settings = {}
        settings['data_ticker'] = self.data_ticker
        settings['trade_ticker'] = self.trade_ticker
        settings['contract'] = self.contract
        settings['strategy_name'] = self.strategy_name
        settings['strategy_slug'] = self.strategy_slug
        settings['version'] = self.version
        settings['last_update'] = self.last_update

        settings['parameter'] = {}
        for key in self.parameter:
            settings['parameter'][key] = str(self.parameter[key]['value']) + " (min=" + str(
                self.parameter[key]['min_value']) + ", max=" + str(self.parameter[key]['max_value']) + ", step=" + str(
                self.parameter[key]['step']) + ")"
        return settings




class Strategies(AbstractStrategy):elf, *strategies):
    def __init__(s
        self._lst_strategies = strategies

    def calculate_signals(self, event):
        for strategy in self._lst_strategies:
            strategy.calculate_signals(event)
