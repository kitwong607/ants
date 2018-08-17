from .base import AbstractPortfolio
from ..position.future_position import FuturePosition
from .. import utilities
import json

class FutureIBHKEXPortfolio(AbstractPortfolio):
    NAME = "FutureIBHKEXPortfolio"

    def __init__(self, session):
        super().__init__()

        self.session 	        = session
        self.config 	        = session.config
        self.init_cash          = session.config.cash
        self.cur_cash           = session.config.cash
        self.equity             = 0
        self.positions 			= {}
        self.closed_positions 	= []
        self.realised_pnl 		= 0
        self.unrealised_pnl		= 0

        self.position_records  = []
        self.order_records      = []

    def update_portfolio(self):
        self.unrealised_pnl = 0
        self.equity = self.realised_pnl
        self.equity += self.init_cash

        for ticker in self.positions:
            position = self.positions[ticker]
            bid, ask = self.session.data_provider.get_last_bid_ask(position.data_ticker)
            position.update_market_value(self.session.data_provider.get_last_timestamp(position.data_ticker), bid, ask)
            self.unrealised_pnl += position.unrealised_pnl
            self.equity += (position.unrealised_pnl + position.realised_pnl)

    def _add_position(self, order):
        if self.config.trade_ticker not in self.positions:
            if self.session.data_provider.is_tick:
                bid, ask = self.session.data_provider.get_best_bid_ask(order.data_ticker)
            elif self.session.data_provider.is_bar:
                close_price = self.session.data_provider.get_last_close(order.data_ticker)
                bid = close_price
                ask = close_price
				
            position = FuturePosition(order)
            self.positions[order.ticker] = position
            self.update_portfolio()
        else:
            print(
                "Ticker %s is already in the positions list. "
                "Could not add a new position." % ticker
            )


    def _modify_position(self, order):
        if order.ticker in self.positions:
            timestamp = self.session.data_provider.get_last_timestamp(order.data_ticker)
            self.positions[order.ticker].transact_order(order)
            if self.session.data_provider.is_tick:
                bid, ask = self.config.data_provider.get_best_bid_ask(order.data_ticker)
            elif self.session.data_provider.is_bar:
                close_price = self.session.data_provider.get_last_close(order.data_ticker)
                bid = close_price
                ask = close_price
            else:
                print("Bar type not support.")
                return

            self.positions[order.ticker].update_market_value(timestamp, bid, ask)


            if self.positions[order.ticker].status == "CLOSED":
                closed_position = self.positions.pop(order.ticker)

                self._record_position(closed_position)
                self.realised_pnl += closed_position.realised_pnl
                self.closed_positions.append(closed_position)

            self.update_portfolio()
        else:
            print(
                "Ticker %s not in the current position list. "
                "Could not modify a current position." % ticker
            )


    def _record_position(self, position):
        record = position.to_dict()
        record['position_id'] = len(self.position_records) + 1
        self.position_records.append(record)


    def _record_order(self, order):
        record = order.to_dict()
        self.order_records.append(record)

    def save(self):
        json_filename = "//positions.json"
        if self.session.config.is_sub_process:
            json_filename = "//positions_" + str(self.session.config.process_no) + ".json"

        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(self.position_records, fp, cls=utilities.AntJSONEncoder)

        json_filename = "//orders.json"
        if self.session.config.is_sub_process:
            json_filename = "//orders_" + str(self.session.config.process_no) + ".json"
        with open(self.session.config.report_directory + json_filename, 'w') as fp:
            json.dump(self.order_records, fp, cls=utilities.AntJSONEncoder)

    def transact_order(self, order):
        if order.action == "BUY":
            self.cur_cash -= ((order.quantity * order.filled_price) + order.commission)
        elif order.action == "SELL":
            self.cur_cash += ((order.quantity * order.filled_price) - order.commission)

        if order.ticker not in self.positions:
            self._add_position(order)
        else:
            self._modify_position(order)

        self._record_order(order)