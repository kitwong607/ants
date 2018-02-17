from abc import ABCMeta
from datetime import timedelta
from .. import utilities

class Order(object):
    __metaclass__ = ABCMeta

    def __init__(self, order_id, ticker, data_ticker, exchange, contract, trigger_price, action, stop_loss_threshold, label, quantity):
        self.order_id = order_id
        self.ticker = ticker
        self.data_ticker = data_ticker
        self.exchange = exchange
        self.contract = contract
        self.trigger_price = trigger_price
        self.action = action
        self.stop_loss_threshold = stop_loss_threshold
        self.quantity = quantity
        self.label = label
        self.type = None
        self.status = None
        self.filled_price = -1
        self.filled_timestamp = None
        self.slippage = None
        self.commission = 0

    def to_dict(self):
        time_offset = timedelta(minutes=utilities.EXCHANGE_TIME_ZONE[self.exchange])
        d = {}

        d['order_id'] = self.order_id
        d['ticker'] = self.ticker
        d['data_ticker'] = self.data_ticker
        d['exchange'] = self.exchange
        d['contract'] = self.contract
        d['price'] = self.filled_price
        d['trigger_price'] = self.trigger_price
        d['action'] = self.action
        d['stop_loss_threshold'] = self.stop_loss_threshold
        d['quantity'] = self.quantity
        d['label'] = self.label
        d['type'] = self.type
        d['status'] = self.status
        d['filled_price'] = self.filled_price
        d['date'] = utilities.dt_get_date_str(self.filled_timestamp)
        d['time'] = utilities.dt_get_time_str(self.filled_timestamp)
        d['timestamp'] = (self.filled_timestamp + time_offset).timestamp()
        d['commission'] = self.commission
        d['slippage'] = self.slippage

        return d

    def calculate_commission(self):
        print("calculate_commission")

class MktOrder(Order):
    def __init__(self, order_id, ticker, data_ticker, exchange, contract, trigger_pice, action, stop_loss_threshold, label, quantity):
        super().__init__(order_id, ticker, data_ticker, exchange, contract, trigger_pice, action, stop_loss_threshold, label, quantity)
        self.type = "MKT"