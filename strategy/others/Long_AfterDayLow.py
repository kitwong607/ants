from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel, SMASlope

#   Entry Rule
#1. Entry

class Long_AfterDayLow(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = []

    FILTER_OPTIMIZATION_PARAMETER = {
    }

    OPTIMIZATION_PARAMETER = {
        #depth / width related
        "bounceback_threshold": {
            "name": "bounceback_threshold",
            "value": 50,
            "min_value": 30,  # 72
            "max_value": 100,  # 108
            "step": 10
        },
        "action": {
            "name": "action",
            "value": 1,
            "min_value": -1,  # 72
            "max_value": 1,  # 108
            "step": 2
        },

        #stop loss / stop gain related.
        "fixed_stop_gain": {
            "name": "fixed_stop_gain",
            "value": 160,
            "min_value": 80,
            "max_value": 240,
            "step": 20
        },
        "step_up_stop_gain_size": {
            "name": "step_up_stop_gain_size",
            "value": 80,
            "min_value": 20,
            "max_value": 140,
            "step": 10
        },
        "fixed_stop_loss": {
            "name": "fixed_stop_loss",
            "value": 80,
            "min_value": 80,
            "max_value": 80,
            "step": 10
        }
    }

    STRATEGY_NAME = "Long After Day Low"
    STRATEGY_SLUG = "long_after_day_low"
    VERSION = "dev"
    LAST_UPDATE_DATE = "2017-05-02"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.bounceback_threshold = int(self.parameter['bounceback_threshold']['value'])

        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])
        self.step_up_stop_gain_size = int(self.parameter['step_up_stop_gain_size']['value'])

        #other varibles
        self.today_action = None
        if (int(self.parameter['action']['value']) == 1):
            self.today_action = "BUY"
        elif(int(self.parameter['action']['value'])==-1):
            self.today_action = "SELL"

        self.is_find_pattern = False
        self.market_open_time_min = None

        self.sl_price = 0
        self.sp_price = 0
        self.entry_price = 0

        self.status = self.STATUS_WAITING


    def calculate_intra_day_ta(self, data):
        pass


    def calculate_entry_signals(self, data):
        if self.today_action is None:
            return

        if self.invested_count != 0:
            return

        '''
        if self.today_action == "BUY":
            #current price must higher than open
            if not data.close_price > self.td_open:
                return
            # day high must higher than day open
            if not self.td_high > self.td_open:
                return
        elif self.today_action == "SELL":
            # current price must lower than open
            if not data.close_price < self.td_open:
                return
            # day low must lower than day open
            if not self.td_low < self.td_open:
                return
        '''

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return


        if utilities.is_time_before(10, 30, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        is_entry = False
        threshold = self.bounceback_threshold * (self.td_high-self.td_low)
        threshold = self.bounceback_threshold
        if self.today_action == "BUY":
            if data.close_price - self.td_low >= threshold:
                stop_loss_pips = self.fixed_stop_loss
                self.sl_price = data.close_price - self.fixed_stop_loss
                label = 'long entry (sl:' + str(stop_loss_pips) + ')'
                is_entry = True
        if self.today_action == "SELL":
            if self.td_high - data.close_price >= threshold:
                stop_loss_pips = self.fixed_stop_loss
                self.sl_price = data.close_price + self.fixed_stop_loss
                label = 'short entry (sl:' + str(stop_loss_pips) + ')'
                is_entry = True

        if is_entry:
            print('entry', data.timestamp)
            self.entry_time = data.timestamp
            self.entry_price = data.close_price
            self.status = self.STATUS_ENTERED
            self.set_inverted()
            self.entry(self.session.config.trade_ticker, data.close_price, self.today_action, label, self.base_quantity, stop_loss_pips)


    def calculate_exit_signals(self, data):
        if self.invested and self.invested_count > 0:
            is_exit = False

            '''
            # 2. exit before 15 mins market close
            if utilities.second_between_two_datetime(data.timestamp, self.td_close_time) < 900 and is_exit != True:
                is_exit = True
                label = "#1 force exit"

            if self.today_action == "BUY":
                if data.low_price <= self.sl_price and not is_exit:
                    label = "#2 stop_loss(" + str(self.sl_price) + ")"
                    is_exit = True

                if data.low_price <= self.td_low and not is_exit:
                    label = "#3 break daylow exit"
                    is_exit = True

                if utilities.second_between_two_datetime(data.timestamp,
                                                         self.entry_time) > 3600 and data.close_price < self.entry_price:
                    label = "#4 breakout fail"
                    is_exit = True

            elif self.today_action == "SELL":
                if data.high_price >= self.sl_price and not is_exit:
                    label = "#2 stop_loss(" + str(self.sl_price) + ")"
                    is_exit = True

                if data.high_price >= self.td_high and not is_exit:
                    label = "#3 break dayhigh exit"
                    is_exit = True

                if utilities.second_between_two_datetime(data.timestamp, self.entry_time) > 3600 and data.close_price > self.entry_price:
                    label = "#4 breakout fail"
                    is_exit = True
            '''
            if utilities.second_between_two_datetime(data.timestamp, self.entry_time) > 3600:
                label = "#dev: fixed time exit"
                is_exit = True

            if is_exit:
                print('exit', data.timestamp)
                self.set_not_inverted()
                if (self.today_action == 'BUY'):
                    self.exit(self.session.config.trade_ticker, data.close_price, "SELL", label, self.base_quantity)
                elif (self.today_action == 'SELL'):
                    self.exit(self.session.config.trade_ticker, data.close_price, "BUY", label, self.base_quantity)


    def entry(self, ticker, trigger_price, action, label, quantity, stop_loss_threshold):
        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, stop_loss_threshold, label,
        quantity)
        self.session.order_handler.place_order(order)


    def exit(self, ticker, trigger_price, action, label, quantity):
        # for backtest it use process directly
        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, 0, label, quantity)
        self.session.order_handler.place_order(order)