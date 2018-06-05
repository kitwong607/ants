from .future_strategy import FutureAbstractStrategy
from ..order.ib_order import IBMktOrder
from .. import utilities
from ..ta import SMA, PriceChannel, SMASlope

class Long_Breakout_FirstXMinute(FutureAbstractStrategy):
    OPTIMIZATION_PAIR = [["fixed_stop_loss","fixed_stop_gain"],["dump_to_exit","dump_to_exit_threshold"],["price_channel_window_size"]]

    FILTER_OPTIMIZATION_PARAMETER = {
    }

    OPTIMIZATION_PARAMETER = {
        #depth / width related
        "price_channel_window_size": {
            "name": "price_channel_window_size",
            "value": 115,
            "min_value": 15,            #72
            "max_value": 180,           #108
            "step": 5
        },


        #stop loss / stop gain related.
        "dump_to_exit": {
            "name": "dump_to_exit",
            "value": 90,
            "min_value": 30,
            "max_value": 100,
            "step": 10
        },
        "dump_to_exit_threshold": {
            "name": "dump_to_exit_threshold",
            "value": 265,
            "min_value": 100,
            "max_value": 310,
            "step": 15
        },
        "fixed_stop_loss": {
            "name": "fixed_stop_loss",
            "value": 80,
            "min_value": 20,
            "max_value": 240,
            "step": 10
        },
        "fixed_stop_gain": {
            "name": "fixed_stop_gain",
            "value": 160,   #120,160 from backtest result
            "min_value": 80,
            "max_value": 240,
            "step": 20
        }
    }

    STRATEGY_SLUG = "long_breakout_firstxminute"
    STRATEGY_NAME = "Long Breakout First X Minute"
    VERSION = "dev_long-exit-testing"
    LAST_UPDATE_DATE = "2017-05-09"

    def __init__(self):
        pass

    def setup(self, session):
        super().setup(session)
        self.price_channel_window_size = int(self.parameter['price_channel_window_size']['value'])

        self.fixed_stop_loss = int(self.parameter['fixed_stop_loss']['value'])
        self.fixed_stop_gain = int(self.parameter['fixed_stop_gain']['value'])
        self.dump_to_exit = int(self.parameter['dump_to_exit']['value'])
        self.dump_to_exit_threshold = int(self.parameter['dump_to_exit_threshold']['value'])

        #price channle TA
        self.price_channel_window_size = int(self.price_channel_window_size)
        self.price_channel_look_back_window_size = 1
        self.price_channel = PriceChannel.PriceChannel(self.session, self.price_channel_window_size, self.price_channel_look_back_window_size, "1T", True)

        self.all_intra_ta.append(self.price_channel)
        self.intra_day_ta.append(self.price_channel)

        #other varibles
        self.today_action = "BUY"
        self.num_minutes = 0;
        self.range_high = self.range_low = None
        self.status = self.STATUS_WAITING

        self.step_up_sl_price = 0
        self.step_up_sl_count = 0

        self.step_up_sp_price = 0
        self.step_up_sp_count = 0

        self.last_trade_result = None
        self.quantity = self.base_quantity
        self.profit = 0
        self.max_profit = None
        self.min_profit = None



    def on_end_date(self, data):
        self.num_minutes = 0
        self.range_high = 0
        self.range_low = 0
        self.step_up_sl_price = 0
        self.step_up_sl_count = 0
        self.step_up_sp_price = 0
        self.step_up_sp_count = 0
        self.profit = 0
        self.max_profit = self.min_profit = None
        super(Long_Breakout_FirstXMinute, self).on_end_date(data)


    def calculate_intra_day_ta(self, data):
        if data.resolution == "1T":
            for ta in self.all_intra_ta:
                ta.push_data(data)

            #custom usage
            self.num_minutes += 1
            if self.num_minutes == self.price_channel_window_size:
                self.range_high = self.price_channel.get_high()
                self.range_low = self.price_channel.get_low()


    def calculate_entry_signals(self, data):
        if data.resolution=="1T":
            return

        if self.today_action is None:
            return

        if self.invested:
            return

        if self.invested_count !=0:
            return

        if utilities.is_time_after(16, 0, 0, data.timestamp.hour, data.timestamp.minute, data.timestamp.second):
            return

        if self.num_minutes < self.price_channel_window_size:
            return

        if self.today_action == "BUY":
            if data.high_price > self.range_high:
                self.delay_num_minutes = 0
                self.step_up_sl_price = data.close_price + self.fixed_stop_loss
                self.step_up_sp_price = data.close_price + self.fixed_stop_gain
                stop_loss_pips = self.fixed_stop_loss
                label = 'long entry (sl:' + str(stop_loss_pips) + ')'

                '''
                print("last_trade_result", self.last_trade_result)
                if self.last_trade_result != "SL":
                    self.quantity = 2
                else:
                    self.quantity = 1
                '''

                self.entry(data, self.session.config.trade_ticker, data.close_price, self.today_action, label,
                           self.quantity, stop_loss_pips)



    def calculate_exit_signals(self, data):
        if data.resolution=="1T":
            return

        if self.invested:
            is_exit = False

            #step up rules
            if self.today_action == "BUY":
                self.profit = data.close_price - self.entry_price
                if self.max_profit is None or self.profit > self.max_profit:
                    self.max_profit = self.profit

                if self.min_profit is None or self.profit < self.min_profit:
                    self.min_profit = self.profit


                if data.high_price >= self.step_up_sl_price and self.step_up_sl_count < 2:
                    self.step_up_sl_count += 1
                    self.step_up_sl_price += self.fixed_stop_loss
                    self.sl_price += self.fixed_stop_loss

                if data.high_price >= self.step_up_sp_price and self.step_up_sp_count < 3:
                    self.step_up_sp_count += 1
                    self.step_up_sp_price += self.fixed_stop_gain
                    self.sp_price += self.fixed_stop_gain

            #Exit rules
            if data.low_price < self.sl_price:
                label = "#1: SL exit("+str(self.step_up_sl_count)+")"
                self.last_trade_result = "SL"
                is_exit = True

            elif data.high_price > self.sp_price:
                label = "#2: SP exit("+str(self.step_up_sp_count)+")"
                self.last_trade_result = "SP"
                is_exit = True

            elif self.max_profit > 0 and self.profit < self.max_profit - self.dump_to_exit and self.max_profit>=self.dump_to_exit_threshold and self.step_up_sp_count != 0:
                label = "#3: SP dump to exit("+str(self.step_up_sp_count)+")"
                self.last_trade_result = "SP_DUMP"
                is_exit = True

            elif utilities.second_between_two_datetime(data.timestamp, self.td_close_time) < 900 and is_exit != True:
                is_exit = True
                self.last_trade_result = "MKT_CLOSE"
                label = "#4: exit b4 close mkt"


            if is_exit:
                self.set_not_inverted()
                if (self.today_action == 'BUY'):
                    self.exit(data, self.session.config.trade_ticker, data.close_price, "SELL", label, self.quantity)
                elif (self.today_action == 'SELL'):
                    self.exit(data, self.session.config.trade_ticker, data.close_price, "BUY", label, self.quantity)


    def entry(self, data, ticker, trigger_price, action, label, quantity, stop_loss_threshold):
        print("entry", data.timestamp)
        self.set_inverted()

        self.sl_price = trigger_price - stop_loss_threshold
        self.sp_price = trigger_price + self.fixed_stop_gain
        self.entry_price = trigger_price
        self.entry_time = data.timestamp

        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, stop_loss_threshold, label, quantity, data.adjusted_date, data.adjusted_time)
        self.session.order_handler.place_order(order)


    def exit(self, data, ticker, trigger_price, action, label, quantity):
        print("exit", data.timestamp)
        self.set_not_inverted()

        self.exit_price = trigger_price
        self.exit_time = data.timestamp

        order = IBMktOrder(self.session.next_valid_order_id(), ticker, self.session.config.data_ticker, self.session.config.exchange,
                           self.contact, trigger_price, action, 0, label, quantity, data.adjusted_date, data.adjusted_time)
        self.session.order_handler.place_order(order)