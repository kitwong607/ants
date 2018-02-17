from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel

class ThreeColRebounceStrategy(FutureAbstractStrategy):
    OPTIMIZATION_PARAMETER = {
        "fast_sma_window_size": {
            "name": "fast_sma_window_size",
            "value": 6,
            "min_value": 6,  # 3
            "max_value": 6,  # 3      3 is the best
            "step": 1
        },
        "slow_sma_window_size": {
            "name": "slow_sma_window_size",
            "value": 36,
            "min_value": 36,  # 3
            "max_value": 36,  # 3      3 is the best
            "step": 2
        },
        "column_size_1": {
            "name": "column_size_1",
            "value": 22,
            "min_value": 22,
            "max_value": 22,
            "step": 1
        },
        "column_size_2": {
            "name": "column_size_2",
            "value": 8,
            "min_value": 8,
            "max_value": 8,
            "step": 1
        },
        "column_size_3": {
            "name": "column_size_3",
            "value": 22,
            "min_value": 22,
            "max_value": 22,
            "step": 2
        },
        "fixed_stop_gain": {
            "name": "fixed_stop_gain",
            "value": 200,
            "min_value": 160,
            "max_value": 220,
            "step": 10
        },
        "fixed_stop_loss": {
            "name": "fixed_stop_loss",
            "value": 180,
            "min_value": 160,
            "max_value": 200,
            "step": 10
        },
        "step_up_ratio": {
            "name": "step_up_ratio",
            "value": 60,
            "min_value": 60,
            "max_value": 90,
            "step": 5
        },
        "trailing_stop_ratio": {
            "name": "trailing_stop_ratio",
            "value": 70,
            "min_value": 60,
            "max_value": 80,
            "step": 5
        }
    }

    STRATEGY_NAME = "3 Col Rebounce"
    STRATEGY_SLUG = "three_col_rebounce"
    VERSION = "0.1"
    LAST_UPDATE_DATE = "2017-12-19"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.slow_sma = SMA.SMA(self.session, int(self.parameter['fast_sma_window_size']['value']))
        self.fast_sma = SMA.SMA(self.session, int(self.parameter['slow_sma_window_size']['value']))

        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])

        #price channle TA
        self.column_size_1 = int(self.parameter['column_size_1']['value'])
        self.column_size_2 = int(self.parameter['column_size_2']['value'])
        self.column_size_3 = int(self.parameter['column_size_3']['value'])
        self.col_size = self.column_size_1 + self.column_size_2 + self.column_size_3
        self.price_channel = PriceChannel.PriceChannel(self.session, self.col_size, True)

        self.step_up_ratio = self.parameter['step_up_ratio']['value'] / 100
        self.trailing_stop_ratio = self.parameter['trailing_stop_ratio']['value'] / 100

        self.all_inter_ta.extend((self.slow_sma, self.fast_sma))
        self.inter_day_ta.append(self.slow_sma)
        self.inter_day_ta.append(self.fast_sma)
        self.all_intra_ta.append(self.price_channel)
        self.intra_day_ta.append(self.price_channel)

        self.today_action = "BUY"


    def on_end_date(self, data):
        for ta in self.all_inter_ta:
            ta.push_data(data)

    def on_new_date(self, data):
        slow_sma_val = self.slow_sma.calculate(data)
        fast_sma_val = self.fast_sma.calculate(data)

        if fast_sma_val > slow_sma_val:
            self.today_action = "BUY"
        elif fast_sma_val < slow_sma_val:
            self.today_action = "SELL"
        else:
            self.today_action = None

        #set interday ta
        for ta in self.all_intra_ta:
            ta.on_new_date(data.timestamp)

    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in all_intra_ta:
                ta.push_data(data)

    def calculate_entry_signals(self, data):
        if self.today_action is None:
            return

        if self.invested_count != 0:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        is_entry = False
        stop_loss_pips = self.fixed_stop_loss

        label = 'long entry (sl:' + str(stop_loss_pips) + ')'
        is_entry = True

        if (is_entry):
            print("entry", data.timestamp)
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
                print("exit", data.timestamp)
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