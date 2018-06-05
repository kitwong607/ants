from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA

class SimpleDebugStrategy(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = []

    OPTIMIZATION_PARAMETER = {
        "stop_loss": {
            "name": "stop_loss",
            "value": 60,
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

        "intra_sma_window_size": {
            "name": "intra_sma_window_size",
            "value": 30,
            "min_value": 12,
            "max_value": 36,
            "step": 2
        }
    }

    STRATEGY_NAME = "Basic Strategy For Debug"
    STRATEGY_SLUG = "basic_strategy_for_debug"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2017-09-07"

    @staticmethod
    def GET_ALL_OPTIMIZATION_PARAMETER(parameter_list):
        parameter = BasicStrategyForDebug.OPTIMIZATION_PARAMETER
        for stop_loss in formula.drange(parameter['stop_loss']['min_value'],
                                        parameter['stop_loss']['max_value'] + 1,
                                        parameter['stop_loss']['step']):
            # This is the key to duplicate dict otherwise it get same address
            temp_parameter = copy.deepcopy(parameter)
            temp_parameter['stop_loss']['value'] = stop_loss

            parameter_list.append(temp_parameter)
        return parameter_list

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.sma = SMA.SMA(self.session, int(self.parameter['sma_window_size']['value']))
        self.intra_sma = SMA.SMA(self.session, int(self.parameter['intra_sma_window_size']['value']), True)
        self.intra_sma2 = SMA.SMA(self.session, int(self.parameter['intra_sma_window_size']['value']*2), True)
        self.today_action = "BUY"

        self.inter_day_ta.append(self.sma)
        self.inter_day_ta_separated.append(self.sma)
        self.intra_day_ta.append(self.intra_sma)
        self.intra_day_ta.append(self.intra_sma2)
        self.intra_day_ta_separated.append(self.intra_sma)
        self.intra_day_ta_separated.append(self.intra_sma2)



    def on_end_date(self, data):
        self.sma.push_data(data)

    def on_new_date(self, data):
        sma = self.sma.calculate(data)

        self.intra_sma.on_new_date(data.timestamp)
        self.intra_sma2.on_new_date(data.timestamp)

    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            self.intra_sma.push_data(data)
            self.intra_sma2.push_data(data)

    def calculate_entry_signals(self, data):
        if self.invested_count != 0:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        is_entry = False
        stop_loss_pips = self.parameter['stop_loss']['value']

        label = 'long entry (sl:' + str(stop_loss_pips) + ')'
        is_entry = True

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

