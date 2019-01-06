from abc import ABCMeta
from .base import AbstractOrderHandler

class IBHKEXOrderHandler(AbstractOrderHandler):
    NAME = "IBHKEXOrderHandler"

    def __init__(self, session):
        self.session = session
        self.filled_order = []
        self.unfilled_order = []

    def place_order(self, order):
        if order.action is None:
            raise Exception('Order has no action')

        #todo make filled_order and unfilled_order to a dict with date key.
        self.unfilled_order.append(order)

        #This will get from broker if in live trade
        filled_timestamp = self.session.data_provider.get_last_timestamp(order.data_ticker)

        if order.action == "BUY":
            self.fill_order(order.order_id, self.session.data_provider.get_last_close(
                order.data_ticker) + self.session.config.slippage_pips, filled_timestamp, self.session.config.commission)
        elif order.action == "SELL":
            self.fill_order(order.order_id, self.session.data_provider.get_last_close(
                order.data_ticker) - self.session.config.slippage_pips, filled_timestamp, self.session.config.commission)


    def fill_order(self, order_id, filled_price, filled_timestamp, comission):
        for order in self.unfilled_order:
            if order.order_id == order_id:
                order.status = "filled"
                order.filled_price = filled_price
                order.filled_timestamp = filled_timestamp
                order.commission = comission * order.quantity

                if(order.action == "BUY"):
                    order.slippage = filled_price - order.trigger_price
                else:
                    order.slippage = order.trigger_price - filled_price

                self.filled_order.append(self.unfilled_order.pop(self.unfilled_order.index(order)))
                self.session.portfolio.transact_order(order)
                break
