from abc import ABCMeta
from enum import IntEnum, Enum
from datetime import timedelta
from .. import utilities


# region Class: OrderAction
class OrderAction(Enum):
    IS_DISPLAY_IN_OPTION = False
    BUY = "BUY"
    SELL = "SELL"
# endregion

# region Class: OrderActionStr

# endregion

# region Class: OrderType
class OrderType(IntEnum):
    IS_DISPLAY_IN_OPTION = False
    MARKET = 0
    LIMIT = 1
# endregion



class Order(object):
    IS_DISPLAY_IN_OPTION = False

    __metaclass__ = ABCMeta

    def __init__(self, order_id, ticker, data_ticker, exchange, contract, trigger_price, action, stop_loss_threshold, label, quantity, adjusted_date, adjusted_time):
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
        self.adjusted_date = adjusted_date
        self.adjusted_time = adjusted_time
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
        d['adjusted_date'] = self.adjusted_date
        d['adjusted_time'] = self.adjusted_time
        d['date'] = utilities.dt_get_date_str(self.filled_timestamp)
        d['time'] = utilities.dt_get_time_str(self.filled_timestamp)
        d['timestamp'] = (self.filled_timestamp + time_offset).timestamp()
        d['commission'] = self.commission
        d['slippage'] = self.slippage

        return d

    def calculate_commission(self):
        print("calculate_commission")

class MktOrder(Order):
    IS_DISPLAY_IN_OPTION = False

    def __init__(self, order_id, ticker, data_ticker, exchange, contract, trigger_pice, action, stop_loss_threshold, label, quantity, adjusted_time, adjusted_date):
        super().__init__(order_id, ticker, data_ticker, exchange, contract, trigger_pice, action, stop_loss_threshold, label, quantity, adjusted_time, adjusted_date)
        self.type = "MKT"