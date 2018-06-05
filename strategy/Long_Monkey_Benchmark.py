from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel, SMASlope

class Long_Monkey_Benchmark(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = []


    FILTER_OPTIMIZATION_PARAMETER = {
    }

    OPTIMIZATION_PARAMETER = {
        #entry_testing
        "fixed_time_exit": {
            "name": "price_channel_window_size",
            "value": 600,
            "min_value": 600,            #72
            "max_value": 3600,           #108
            "step": 600
        },


        #stop loss / stop gain related.
        "fixed_stop_loss": {
            "name": "fixed_stop_loss",
            "value": 80,
            "min_value": 80,
            "max_value": 240,
            "step": 20
        }
    }

    STRATEGY_SLUG = "Long_Monkey_Benchmark"
    STRATEGY_NAME = "Long_Monkey_Benchmark"
    VERSION = "dev_long-entry-testing_fixed-time_exit"
    LAST_UPDATE_DATE = "2017-05-04"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.fixed_stop_gain = self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_time_exit = int(self.parameter['fixed_time_exit']['value'])

        #other varibles
        self.today_action = "BUY"
        self.status = self.STATUS_WAITING


    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in self.all_intra_ta:
                ta.push_data(data)


    def calculate_entry_signals(self, data):
        if self.today_action is None:
            return

        if self.invested_count != 0:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        if self.today_action == "BUY":

            if utilities.is_time_after(10, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
                label = 'dev: fixed time entry'

                self.set_inverted()
                self.entry(data, self.session.config.trade_ticker, data.close_price, self.today_action, label, self.base_quantity, self.fixed_stop_loss)


    def calculate_exit_signals(self, data):
        if self.invested and self.invested_count > 0:
            is_exit = False

            '''
            if utilities.second_between_two_datetime(data.timestamp, self.entry_time) > self.fixed_time_exit:
                label = "#dev: fixed time exit"
                is_exit = True
            '''

            if data.low_price < self.sl_price:
                label = "#dev: fixed SL exit"
                is_exit = True

            elif data.high_price > self.sp_price:
                label = "#dev: fixed SP exit"
                is_exit = True

            elif utilities.second_between_two_datetime(data.timestamp, self.td_close_time) < 900 and is_exit != True:
                is_exit = True
                label = "#dev: force exit"


            if is_exit:
                self.set_not_inverted()
                if (self.today_action == 'BUY'):
                    self.exit(data, self.session.config.trade_ticker, data.close_price, "SELL", label, self.base_quantity)
                elif (self.today_action == 'SELL'):
                    self.exit(data, self.session.config.trade_ticker, data.close_price, "BUY", label, self.base_quantity)


    def entry(self, data, ticker, trigger_price, action, label, quantity, stop_loss_threshold):
        self.sl_price = trigger_price - stop_loss_threshold
        self.sp_price = trigger_price + self.fixed_stop_gain
        self.entry_price = trigger_price
        self.entry_time = data.timestamp

        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, stop_loss_threshold, label,
        quantity)
        self.session.order_handler.place_order(order)


    def exit(self, data, ticker, trigger_price, action, label, quantity):
        self.exit_price = trigger_price
        self.exit_time = data.timestamp

        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, 0, label, quantity)
        self.session.order_handler.place_order(order)