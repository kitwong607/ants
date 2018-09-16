from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel, SMASlope

class VReverseBasic(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = []

    FILTER_OPTIMIZATION_PARAMETER = {
        "fast_sma_window_size": {
            "name": "fast_sma_window_size",
            "value": 8,
            "min_value": 2,
            "max_value": 18,
            "step": 1
        },
        "slow_sma_window_size": {
            "name": "slow_sma_window_size",
            "value": 30,
            "min_value": 20,
            "max_value": 80,
            "step": 2
        }
    }

    '''
        "fast_sma_window_size": {
            "name": "fast_sma_window_size",
            "value": 8,
            "min_value": 2,  # 3
            "max_value": 18,  # 3      3 is the best
            "step": 1
        },
        "slow_sma_window_size": {
            "name": "slow_sma_window_size",
            "value": 30,
            "min_value": 20,  # 3
            "max_value": 80,  # 3      3 is the best
            "step": 2
        },
        '''

    OPTIMIZATION_PARAMETER = {
        # more trades
        "price_channel_window_size": {
            "name": "price_channel_window_size",
            "value": 66,
            "min_value": 18,            #72
            "max_value": 240,           #108
            "step": 6
        },
        #will less trade

        #"price_channel_window_size": {
        #    "name": "price_channel_window_size",
        #    "value": 150,
        #    "min_value": 150,
        #    "max_value": 204,
        #    "step": 6
        #},

        "price_threshold": {
            "name": "price_threshold",
            "value": 80,
            "min_value": 0,             #0
            "max_value": 160,           #60
            "step": 10
        },
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

    STRATEGY_NAME = "V Reverse Basic"
    STRATEGY_SLUG = "v_reverse_basic"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2017-04-15"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])
        self.price_threshold = int(self.parameter['price_threshold']['value'])
        self.step_up_stop_gain_size = int(self.parameter['step_up_stop_gain_size']['value'])


        #price channle TA
        self.price_channel_window_size = int(self.parameter['price_channel_window_size']['value'])
        self.price_channel_look_back_window_size = 1
        self.price_channel = PriceChannel.PriceChannel(self.session, self.price_channel_window_size, self.price_channel_look_back_window_size, "1T", True)

        self.all_intra_ta.append(self.price_channel)
        self.intra_day_ta.append(self.price_channel)

        self.market_open_time_min = None
        self.today_action = "BUY"
        self.is_find_pattern = False


    def on_end_date(self, data):
        for ta in self.all_inter_ta:
            ta.push_data(data)


    def on_new_date(self, data):
        self.today_action = "BUY"
        self.today_action = "SELL"


        #set interday ta
        for ta in self.all_intra_ta:
            ta.on_new_date(data.timestamp)

    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in self.all_intra_ta:
                ta.push_data(data)

            #custom usage
            self.is_find_pattern = False
            #if self.price_channel.is_ready():
            if not utilities.get_total_minute_from_datetime(data.timestamp) - self.market_open_time_min < self.price_channel_window_size:
                col_size = int(self.price_channel_window_size / 3)
                if self.today_action == "BUY":
                    self.low2 = self.price_channel.get_low(col_size, col_size*2)
                    self.high1 = self.price_channel.get_high(0, col_size)

                    condition = (self.high1 - self.low2 > self.price_threshold)
                    if not condition:
                        return

                    self.is_find_pattern = True

                elif self.today_action == "SELL":
                    self.high2 = self.price_channel.get_high(col_size, col_size * 2)
                    self.low1 = self.price_channel.get_low(0, col_size)

                    condition = (self.high2 - self.low1 > self.price_threshold)
                    if not condition:
                        return

                    '''
                    low3 = self.price_channel.get_low(col_size * 2, self.price_channel_window_size)
                    condition = (low3 > low1)
                    if not condition:
                        return
                    '''
                    self.is_find_pattern = True

    def calculate_entry_signals(self, data):
        if self.today_action is None:
            return

        if self.invested_count != 0:
            return

        if not self.is_find_pattern:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return


        if utilities.is_time_before(10, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return


        #if data.close_price > (self.box_min + diff * 1):
        if self.today_action == "BUY":
            #if data.high_price > self.price_channel_low  + (self.price_channel_high-self.price_channel_low)*0.75:
            if data.high_price > self.high1:
                stop_loss_pips = self.fixed_stop_loss
                label = 'long entry (sl:' + str(stop_loss_pips) + ')'

                #print("entry", data.timestamp)
                self.set_inverted()
                self.entry(self.session.config.trade_ticker, data.close_price, self.today_action, label, self.base_quantity, stop_loss_pips)

        elif self.today_action == "SELL":
            #if data.close_price < self.price_channel_high  - (self.price_channel_high-self.price_channel_low)*0.75:
            if data.close_price < self.low1 and data.close_price > self.low1 - self.price_threshold/2:
                stop_loss_pips = self.fixed_stop_loss
                label = 'short entry (sl:' + str(stop_loss_pips) + ')'
                #print("entry", data.timestamp)
                self.set_inverted()
                self.entry(self.session.config.trade_ticker, data.close_price, self.today_action, label, self.base_quantity, stop_loss_pips)

    def calculate_exit_signals(self, data):
        if self.invested and self.invested_count > 0:
            is_exit = False

            position = self.session.portfolio.get_open_position_by_ticker(self.session.config.trade_ticker)
            if not position.is_set_stop_gain():
                position.set_stop_gain_pips(self.fixed_stop_gain)
            # 1. stop loss
            if not is_exit:
                if position.is_hit('stop_loss', data.close_price):
                    is_exit = True
                    if position.step_up_stop_loss_count == 0:
                        label = "#1 stop_loss(" + str(position.stop_loss_price) + ")"
                    else:
                        label = "#2 step_up_stop_loss(" + str(position.stop_loss_price) + ")"

            # 2. exit before 15 mins market close
            if utilities.second_between_two_datetime(data.timestamp, self.td_close_time) < 900 and is_exit != True:
                is_exit = True
                label = "#2 force exit"

            '''
            #3
            if position.is_hit('stop_gain', data.close_price):
                position.step_up_stop_loss_pips(self.step_up_stop_gain_size)
                position.step_up_stop_gain_pips(self.step_up_stop_gain_size)
            '''


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