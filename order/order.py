from .base import Order

class IBOrder(Order):
    IS_DISPLAY_IN_OPTION = False
    ORDER_TYPE = [  "auction",
                    "market", "market_if_touch", "market_on_close", "market_on_open",
                    "pegged_to_primary",
                    "limit_order", "limit_if_touched", "limit_on_close", "limit_on_open",
                    "market_to_limit", "market_with_protection",
                    "stop", "stop_limit", "stop_with_protection",
                    "trailing_stop", "trailing_stop_limit",
                    "combo_limit", "combo_market", "combo_limit_with_price_per_leg",
                    "relative_limit_combo", "relative_market_combo"]


    ORDER_ACTION = {"auction": "AUC",
                  "market": "MKT",
                  "market_if_touch": "MIT",
                  "market_on_close": "MOC",
                  "market_on_open": "MKT",
                  "pegged_to_primary": "REL",
                  "limit_order": "LMT",
                  "limit_if_touched": "LIT",
                  "limit_on_close": "LOC",
                  "limit_on_open": "LMT",
                  "market_to_limit": "MTL",
                  "market_with_protection": "MKT PRT",
                  "stop": "STP",
                  "stop_limit": "STP LMT",
                  "stop_with_protection": "STP PRT",
                  "trailing_stop": "TRAIL",
                  "trailing_stop_limit": "TRAIL LIMIT",
                  "combo_limit": "LMT",
                  "combo_market": "MKT",
                  "combo_limit_with_price_per_leg": "LMT",
                  "relative_limit_combo": "REL + LMT",
                  "relative_market_combo": "REL + MKT"
                  }

    def __init__(self, order_id, ticker, contact, order_type, action, stop_loss_threshold, label, quantity):
        super().init(order_id, ticker, contact, action, stop_loss_threshold, label, quantity)
        self.order_id = order_id
        self.ticker = ticker
        self.trade_contact = trade_contact
        self.data_ticker = ticker['data_ticker']
        self.trade_ticker = ticker['trade_ticker']
        self.action = action
        self.stop_loss_threshold = stop_loss_threshold
        self.quantity = quantity
        self.label = label

class IBMktOrder(IBOrder):
    IS_DISPLAY_IN_OPTION = False
    def __init__(self, order_id, ticker, contact, order_type, action, stop_loss_threshold=0, label="", quantity=0):
        super().init(order_id, ticker, contact, order_type, action, stop_loss_threshold, label, quantity)

class IBSimulatedOrder(IBOrder):
    IS_DISPLAY_IN_OPTION = False
    def __init__(self, order_id, ticker, contact, order_type, action, stop_loss_threshold=0, label="", quantity=0):
        super().init(order_id, ticker, contact, order_type, action, stop_loss_threshold, label, quantity)