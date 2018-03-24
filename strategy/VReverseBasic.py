from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel

class VReverseBasic(FutureAbstractStrategy):
    OPTIMIZATION_PARAMETER = {
        "fast_sma_window_size": {
            "name": "fast_sma_window_size",
            "value": 4,
            "min_value": 2,  # 3
            "max_value": 8,  # 3      3 is the best
            "step": 1
        },
        "slow_sma_window_size": {
            "name": "slow_sma_window_size",
            "value": 12,
            "min_value": 10,  # 3
            "max_value": 30,  # 3      3 is the best
            "step": 2
        },
        "box_size": {
            "name": "box_size",
            "value": 49,
            "min_value": 49,
            "max_value": 140,
            "step": 7
        },
        "fixed_stop_gain": {
            "name": "fixed_stop_gain",
            "value": 160,
            "min_value": 120,
            "max_value": 240,
            "step": 20
        },
        "fixed_stop_loss": {
            "name": "fixed_stop_loss",
            "value": 80,
            "min_value": 80,
            "max_value": 80,
            "step": 10
        }
    }

    STRATEGY_NAME = "V Reverse Basic"
    STRATEGY_SLUG = "v_reverse_basic"
    VERSION = "0.1"
    LAST_UPDATE_DATE = "2017-03-20"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.fast_sma = SMA.SMA(self.session, int(self.parameter['fast_sma_window_size']['value']))
        self.slow_sma = SMA.SMA(self.session, int(self.parameter['slow_sma_window_size']['value']))

        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])

        #price channle TA
        self.box_size = int(self.parameter['box_size']['value'])
        self.price_channel = PriceChannel.PriceChannel(self.session, self.box_size, True)

        self.first_part = self.box_size / 7 + 1
        self.middle_part_start = self.box_size / 7 * 3
        self.middle_part_end = self.middle_part_start + self.box_size / 7 + 1

        self.all_inter_ta.extend((self.slow_sma, self.fast_sma))
        self.inter_day_ta.append(self.slow_sma)
        self.inter_day_ta.append(self.fast_sma)
        self.all_intra_ta.append(self.price_channel)
        self.intra_day_ta.append(self.price_channel)

        self.today_action = "BUY"
        self.is_find_pattern = False


    def on_end_date(self, data):
        for ta in self.all_inter_ta:
            ta.push_data(data)


    def on_new_date(self, data):
        slow_sma_val = self.slow_sma.calculate(data)
        fast_sma_val = self.fast_sma.calculate(data)

        print(data.timestamp, fast_sma_val, slow_sma_val)

        if fast_sma_val > slow_sma_val:
            self.today_action = "BUY"
            '''
            elif fast_sma_val < slow_sma_val:
                #self.today_action = "SELL"
                self.today_action = None
            '''
        else:
            self.today_action = None

        #print("self.today_action", self.today_action)

        #set interday ta
        for ta in self.all_intra_ta:
            ta.on_new_date(data.timestamp)

    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in self.all_intra_ta:
                ta.push_data(data)

            #custom usage
            self.is_find_pattern = False
            if self.today_action == "BUY":
                min_idx = self.price_channel.get_low_idx()
                condition_1 = min_idx > self.middle_part_start and min_idx < self.middle_part_end
                if not condition_1:
                    return

                max_idx = self.price_channel.get_high_idx()
                condition_2 = max_idx < self.first_part
                if not condition_2:
                    return

                self.box_max = self.price_channel.get_high()
                self.box_min = self.price_channel.get_low()
                self.is_find_pattern = True


    def calculate_entry_signals(self, data):
        if self.today_action is None:
            return

        if self.invested_count != 0:
            return

        if not self.is_find_pattern:
            return

        '''
        if data.close_price < self.td_open * 0.99:
            return
        '''

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        if utilities.is_time_before(10, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        '''
        diff = self.box_max - self.box_min
        if(diff<0):
            return
        '''

        #if data.close_price > (self.box_min + diff * 1):
        if data.close_price > self.box_max:
            stop_loss_pips = self.fixed_stop_loss
            label = 'long entry (sl:' + str(stop_loss_pips) + ')'

            #print("entry", data.timestamp)
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