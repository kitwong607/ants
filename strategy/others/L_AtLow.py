from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel, SMASlope

class L_AtLow(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = []

    FILTER_OPTIMIZATION_PARAMETER = {
    }

    OPTIMIZATION_PARAMETER = {
        #depth / width related
        "below_high_threshold": {
            "name": "below_high_threshold",
            "value": 150,
            "min_value": 60,  # 72
            "max_value": 400,  # 108
            "step": 10
        },
        "price_channel_height_threshold": {
            "name": "price_channel_height_threshold",
            "value": 30,
            "min_value": 40,             #0
            "max_value": 160,           #60
            "step": 10
        },
        "price_channel_window_size": {
            "name": "price_channel_window_size",
            "value": 66,
            "min_value": 18,            #72
            "max_value": 240,           #108
            "step": 6
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

    STRATEGY_NAME = "Long At Low"
    STRATEGY_SLUG = "long_AtLow"
    VERSION = "1.0"
    LAST_UPDATE_DATE = "2017-05-02"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.below_high_threshold = int(self.parameter['below_high_threshold']['value'])
        self.price_channel_height_threshold = int(self.parameter['price_channel_height_threshold']['value'])
        self.price_channel_window_size = int(self.parameter['price_channel_window_size']['value'])

        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])
        self.step_up_stop_gain_size = int(self.parameter['step_up_stop_gain_size']['value'])

        #price channle TA
        self.price_channel_window_size = int(self.price_channel_window_size)
        self.price_channel_look_back_window_size = 1
        self.price_channel = PriceChannel.PriceChannel(self.session, self.price_channel_window_size, self.price_channel_look_back_window_size, "1T", True)

        self.all_intra_ta.append(self.price_channel)
        self.intra_day_ta.append(self.price_channel)

        #other varibles
        self.today_action = "BUY"
        self.is_find_pattern = False
        self.market_open_time_min = None

        self.status = self.STATUS_WAITING


    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in self.all_intra_ta:
                ta.push_data(data)

            #custom usage
            self.is_find_pattern = False
            #if self.price_channel.is_ready():
            if not utilities.get_total_minute_from_datetime(data.timestamp) - self.market_open_time_min < self.price_channel_window_size:

                low = self.price_channel.get_low()
                condition = self.td_high - low > self.below_high_threshold
                if not condition:
                    return

                '''
                high_idx = self.price_channel.get_high_idx()
                low_idx = self.price_channel.get_low_idx()
                condition = high_idx < low_idx
                if not condition:
                    return
                '''

                '''
                condition = low == self.td_low
                if not condition:
                    return
                '''


                self.price_channel_high = self.price_channel.get_high()
                condition = self.price_channel_high - low > self.price_channel_height_threshold
                if not condition:
                    return


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


        if utilities.is_time_before(10, 30, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return


        #if data.close_price > (self.box_min + diff * 1):
        if self.today_action == "BUY":
            if data.high_price > self.price_channel_high:
                stop_loss_pips = self.fixed_stop_loss
                label = 'long entry (sl:' + str(stop_loss_pips) + ')'

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