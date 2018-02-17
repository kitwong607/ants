from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from collections import deque
import numpy as np
from ..ta import SMA

class BoscoStrategy(FutureAbstractStrategy):
    OPTIMIZATION_PARAMETER = {
        "stop_loss": {
            "name": "stop_loss",
            "value": 85,
            "min_value": 60,
            "max_value": 120,
            "step": 10
        },

        "sma_window_size": {
            "name": "sma_window_size",
            "value": 30,
            "min_value": 12,
            "max_value": 36,
            "step": 2
        },

        "avg_window_size": {
            "name": "avg_window_size",
            "value": 5,
            "min_value": 2,
            "max_value": 5,
            "step": 1
        }
    }

    STRATEGY_NAME = "Bosco Strategy"
    STRATEGY_SLUG = "bosco_strategy"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2017-12-15"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.sma = SMA.SMA(self.session, int(self.parameter['sma_window_size']['value']))

        self.previous_bar = deque(maxlen=self.parameter['avg_window_size']['value'])
        self.upper = deque(maxlen=self.parameter['avg_window_size']['value'])
        self.lower = deque(maxlen=self.parameter['avg_window_size']['value'])

        self.upper_avg = None
        self.lower_avg = None

        self.today_action = "BUY"


    def on_end_date(self, data):
        self.sma.push_data(data)

        self.previous_bar.append(data)
        self.upper.append(data.high_price - data.open_price)
        self.lower.append(data.low_price - data.open_price)

        if len(self.upper)==self.parameter['avg_window_size']['value']:
            self.upper_avg = float(np.mean(self.upper)) * 1
            self.lower_avg = float(np.mean(self.lower)) * 1




    def on_new_date(self, data):
        sma = self.sma.calculate(data)

        if data.open_price > sma:
            self.today_action = "BUY"
        else:
            self.today_action = "SELL"

    def calculate_intra_day_ta(self, data):
        pass

    def calculate_entry_signals(self, data):
        if self.invested_count != 0:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        if self.upper_avg is None:
            return

        is_entry = False
        stop_loss_pips = self.parameter['stop_loss']['value']

        if (data.close_price - self.td_open) > self.upper_avg and self.today_action == "SELL":
            #self.today_action = "SELL"
            return
            is_entry = True
            label = 'long entry ('+ str((data.close_price - self.td_open)) + ', '+str(self.upper_avg)+')'
        elif (data.close_price - self.td_open) < self.lower_avg and self.today_action == "BUY":
            #self.today_action = "BUY"
            is_entry = True
            label = 'short entry ('+ str((data.low_price - self.td_open)) + ', '+str(self.lower_avg)+')'
        else:
            return

        if (is_entry):
            self.set_inverted()
            self.entry(self.session.config.trade_ticker, data.close_price, self.today_action, label, self.base_quantity, stop_loss_pips)

    def calculate_exit_signals(self, data):
        if self.invested and self.invested_count > 0:
            is_exit = False

            position = self.session.portfolio.get_open_position_by_ticker(self.session.config.trade_ticker)

            # 1. stop loss
            if not is_exit:
                if position.is_hit('stop_loss', data.close_price):
                    is_exit = True
                    if position.step_up_stop_loss_count == 0:
                        label = "#1 stop_loss(" + str(position.stop_loss_price) + ")"
                    else:
                        label = "#2 step_up_stop_loss(" + str(position.stop_loss_price) + ")"

            if not is_exit:
                if position.step_up_stop_gain_count > 0 and position.current_profit_pips() <= position.max_profit_pip * (
                    1 - (self.trailing_stop_ratio / position.step_up_stop_gain_count)):
                    is_exit = True
                    label = "#3 trailing_stop(" + str(position.current_profit_pips()) + "/" + str(
                        position.max_profit_pip) + " " + str(
                        (1 - (self.trailing_stop_ratio / (position.step_up_stop_gain_count + 1)))) + " " + str(
                        position.step_up_stop_gain_count) + ")"

            # exit before 15 mins market close
            #print(data.timestamp, self.td_close_time, utilities.second_between_two_datetime(data.timestamp, self.td_close_time))
            if utilities.second_between_two_datetime(data.timestamp, self.td_close_time) < 900 and is_exit != True:
                is_exit = True
                label = "#4 force exit"

            if is_exit:
                print(data.timestamp, label)
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

