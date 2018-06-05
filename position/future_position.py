from numpy import sign
from .base import Position
from .. import utilities
from datetime import timedelta
import pandas as pd

#avg_sld_price, avg_bot_price include commission

class FuturePosition():
    def __init__(self, order):
        self.last_update_time = self.entry_time = order.filled_timestamp
        self.init_price = order.filled_price
        self.entry_label = order.label
        self.entry_price = order.filled_price
        self.action = order.action
        self.ticker = order.ticker
        self.exchange = order.exchange
        self.data_ticker = order.data_ticker

        if(self.ticker=='MHI' or self.ticker=='MCH'):
            self.contract_value = 10
        else:
            self.contract_value = 50

        self.orders = [order]
        self.market_value = self.entry_price
        self.max_net = self.quantity = order.quantity
        self.total_commission = order.commission
        self.init_stop_loss = order.stop_loss_threshold

        self.adjusted_date = order.adjusted_date
        self.adjusted_time = order.adjusted_time

        self.realised_pnl = 0
        self.unrealised_pnl = -order.commission

        self.num_bot = 0
        self.num_sld = 0
        self.avg_bot_price = 0
        self.avg_sld_price = 0


        self.stop_gain_price = None
        self.stop_gain_pips = None
        self.step_up_stop_gain_size = None
        self.step_up_stop_gain_price = None
        self.step_up_stop_gain_count = 0

        if self.action =="BUY":
            self.num_bot = order.quantity
            self.avg_bot_price = self.init_price + (order.commission/ order.quantity / self.contract_value)
            self.stop_loss_price = self.init_stop_loss_price = order.filled_price - order.stop_loss_threshold
            self.cost_basis = (self.avg_bot_price * self.num_bot) * self.contract_value + self.total_commission


        elif self.action =="SELL":
            self.num_sld = order.quantity
            self.stop_loss_price = self.init_stop_loss_price = order.filled_price + order.stop_loss_threshold
            self.avg_sld_price = self.init_price - (order.commission/ order.quantity / self.contract_value)
            self.cost_basis = (self.avg_sld_price * self.num_sld) * self.contract_value

        self.net = abs(self.num_bot - self.num_sld)
        self.max_count = 0

        self.stop_loss_pips = self.init_stop_loss
        self.step_up_stop_loss_price = None
        self.step_up_stop_loss_count = 0

        self._update_max_net()
        self.update_market_value(order.filled_timestamp, order.filled_price, order.filled_price)

        self.status = "OPEN"

    def _update_max_net(self):
        if self.action == "BUY":
            self.max_count = max(self.max_net, self.num_bot)
        elif self.action == "SELL":
            self.max_count = max(self.max_net, self.num_sld)

    def unrealised_pnl_pips(self):
        return self.unrealised_pnl/self.contract_value

    def realised_pnl_pips(self):
        return self.realised_pnl/self.contract_value

    def update_market_value(self, timestamp, bid, ask):
        self.last_update_time = timestamp
        midpoint = (bid + ask) / 2

        self.market_value = self.quantity * midpoint  * self.contract_value
        if self.action == "BUY":
            self.unrealised_pnl = self.market_value - self.cost_basis
        elif self.action == "SELL":
            self.unrealised_pnl = self.cost_basis - self.market_value


    def transact_order(self, order):
        timestamp = order.filled_timestamp
        action = order.action
        ticker = order.ticker
        quantity = order.quantity
        price = order.filled_price
        commission = order.commission
        commission_pre_contract_in_pips = (order.commission / order.quantity) / self.contract_value
        label = order.label

        self.total_commission += commission
        self.last_update_time = timestamp

        # Adjust total bought and sold
        if self.action == "BUY":
            if action == "BUY":  # Increasing long position
                self.avg_bot_price = ((self.avg_bot_price * self.num_bot) +
                                      (price + commission_pre_contract_in_pips) * quantity ) / (self.num_bot + quantity)
                self.num_bot += quantity
            elif action == "SELL":  # Closed partial positions out
                self.exit_price = price
                self.exit_time = timestamp
                self.exit_label = label
                self.realised_pnl += ((((price - commission_pre_contract_in_pips) * quantity) - (self.avg_bot_price * self.num_bot))) * self.contract_value

                self.avg_sld_price = ((self.avg_sld_price * self.num_sld) +
                                      ((price - commission_pre_contract_in_pips) * quantity ))/(self.num_sld + quantity)
                self.num_sld += quantity

            self.cost_basis = ((self.avg_bot_price * self.num_bot) - (
            self.avg_sld_price * self.num_sld))*self.contract_value

        # action == "SELL"
        else:
            if action == "SELL":  # Increasing short position
                self.avg_sld_price = ((self.avg_sld_price * self.num_sld) +
                                      ((price - commission_pre_contract_in_pips) * quantity ))/(self.num_sld + quantity)
                self.num_sld += quantity
            elif action == "BUY":  # Closed partial positions out
                self.exit_price = price
                self.exit_time = timestamp
                self.exit_label = label

                self.realised_pnl += ((
                ((self.avg_sld_price * self.num_sld) - (price + commission_pre_contract_in_pips) * quantity))) * self.contract_value
                self.avg_bot_price = ((self.avg_bot_price * self.num_bot) +
                                      (price + commission_pre_contract_in_pips) * quantity ) / (self.num_bot + quantity)

                self.num_bot += quantity

            self.cost_basis = ((self.avg_sld_price * self.num_sld) - (
                self.avg_bot_price * self.num_bot)) * self.contract_value

        # Adjust net values, including commissions

        self.net = abs(self.num_bot - self.num_sld)

        self.quantity = self.net
        self.orders.append(order)

        if self.quantity == 0:
            self._close_position()

    def is_hit(self, target_to_hit, current_price):
        if target_to_hit=='stop_loss':
            if self.stop_loss_price is None: return False
            if (self.action == "BUY"):
                if (current_price <= self.stop_loss_price):
                    return True
            elif (self.action == "SELL"):
                if (current_price >= self.stop_loss_price):
                    return True
            return False
        elif target_to_hit=='stop_gain':
            if self.stop_gain_price is None: return False
            if (self.action == "BUY"):
                if (current_price >= self.stop_gain_price):
                    return True
            elif (self.action == "SELL"):
                if (current_price <= self.stop_gain_price):
                    return True
            return False
        elif target_to_hit=='step_up_stop_loss':
            if self.step_up_stop_loss_price is None: return False
            if (self.action == "BUY"):
                if (current_price >= self.step_up_stop_loss_price):
                    return True
            elif (self.action == "SELL"):
                if (current_price <= self.step_up_stop_loss_price):
                    return True
            return False
        elif target_to_hit=='step_up_stop_gain':
            if self.step_up_stop_gain_price is None: return False
            if (self.action == "BUY"):
                if (current_price >= self.step_up_stop_gain_price):
                    return True
            elif (self.action == "SELL"):
                if (current_price <= self.step_up_stop_gain_price):
                    return True
            return False

    '''
    def set_step_up_stop_loss_pips(self, step_up_stop_loss_pips):
        if self.step_up_stop_loss_price is None:
            if (self.action == "BUY"):
                self.step_up_stop_loss_price = self.init_price + step_up_stop_loss_pips

            elif (self.action == "SELL"):
                self.step_up_stop_loss_price = self.init_price - step_up_stop_loss_pips

    def set_step_up_stop_gain_pips(self, step_up_stop_gain_pips):
        if self.step_up_stop_loss_price is None:
            if (self.action == "BUY"):
                self.step_up_stop_gain_price = self.init_price + step_up_stop_gain_pips
            elif (self.action == "SELL"):
                self.step_up_stop_gain_price = self.init_price - step_up_stop_gain_pips
    '''

    def is_set_stop_gain(self):
        if self.stop_gain_price is None:
            return False
        return True

    def set_stop_gain_pips(self, stop_gain_pips):
        if self.stop_gain_price is None:
            self.force_set_stop_gain_pips(stop_gain_pips)

    def force_set_stop_gain_pips(self, stop_gain_pips):
        self.stop_gain_pips = stop_gain_pips
        if (self.action == "BUY"):
            self.stop_gain_price = self.init_price + self.stop_gain_pips
        elif (self.action == "SELL"):
            self.stop_gain_price = self.init_price - self.stop_gain_pips
        self.stop_gain_pips = stop_gain_pips

    def step_up_stop_gain_pips(self, stop_gain_pips):
        self.stop_gain_pips += stop_gain_pips
        if (self.action == "BUY"):
            self.stop_gain_price = self.init_price + self.stop_gain_pips
        elif (self.action == "SELL"):
            self.stop_gain_price = self.init_price - self.stop_gain_pips
        self.step_up_stop_gain_count += 1

    def set_stop_loss_price(self, value, is_compare=False):
        if is_compare:
            if (self.action == "BUY"):
                self.stop_loss_price = max(self.stop_loss_price, value)
            elif (self.action == "SELL"):
                self.stop_loss_price = min(self.stop_loss_price, value)
        else:
            if(self.action == "BUY"):
                self.stop_loss_price = value
            elif(self.action == "SELL"):
                self.stop_loss_price = value

    def step_up_stop_loss_pips(self, stop_loss_pips):
        self.stop_loss_pips -= stop_loss_pips
        if(self.action == "BUY"):
            self.stop_loss_price = self.init_price - self.stop_loss_pips
        elif(self.action == "SELL"):
            self.stop_loss_price = self.init_price + self.stop_loss_pips
        self.step_up_stop_loss_count += 1

    def step_up_stop_loss_by_percent(self, percent):
        if(self.action == "BUY"):
            self.stop_loss_price = self.init_price - (self.init_stop_loss*percent)
        elif(self.action == "SELL"):
            self.stop_loss_price = self.init_price + (self.init_stop_loss * percent)

    def is_percent_trailing(self, amount_in_pips, percent):
        try:
            percent_trailing = self.percent_trailing
        except AttributeError:
            percent_trailing = {}
            percent_trailing['amount_in_pips'] = amount_in_pips
            percent_trailing['percent'] = percent
            percent_trailing['is_reached_threshold'] = False
            self.percent_trailing = percent_trailing

        self.percent_trailing['amount_in_pips'] = amount_in_pips
        self.percent_trailing['percent'] = percent

        if(self.max_profit_pip >= self.percent_trailing['amount_in_pips']):
            self.percent_trailing['is_reached_threshold'] = True

        if self.percent_trailing['is_reached_threshold']:
            if self.max_profit_pip - self.current_profit_pips() >= self.percent_trailing['amount_in_pips'] * self.percent_trailing['percent']:
                return True

        return False

    def lifetime_in_second(self):
        return utilities.second_between_two_datetime(self.entry_time, self.last_update_time)

    def _close_position(self):
        self.status = "CLOSED"
        self.unrealised_pnl = 0
        self.profit = self.realised_pnl
        self.profit_pip = self.realised_pnl / self.contract_value
        if(self.profit>0):
            self.result = 'WIN'
        else:
            self.result = 'LOSS'

        self.entry_price_s = []
        self.exit_price_s = []
        self.slippage = 0
        for order in self.orders:
            self.slippage += order.slippage * order.quantity
            if order.action == self.action:
                self.entry_price_s.append(order.filled_price)
            else:
                self.exit_price_s.append(order.filled_price)

        if(self.action=='BOT'):
            self.avg_entry_price = self.avg_bot_price
            self.avg_exit_price = self.avg_sld_price
        else:
            self.avg_entry_price = self.avg_sld_price
            self.avg_exit_price = self.avg_bot_price




    def to_dict(self):
        time_offset = timedelta(minutes=utilities.EXCHANGE_TIME_ZONE[self.exchange])
        d = {}
        d['position_id'] = None
        d['date'] = utilities.dt_get_date_str(self.entry_time)
        d['date_ts'] = (self.entry_time + time_offset).timestamp()
        d['ticker'] = self.ticker
        d['data_ticker'] = self.data_ticker
        d['action'] = self.action

        d['entry_time'] = utilities.dt_get_time_str(self.entry_time)
        d['exit_time'] = utilities.dt_get_time_str(self.exit_time)
        d['entry_time_ts'] = (self.entry_time + time_offset).timestamp()
        d['exit_time_ts'] = (self.exit_time + time_offset).timestamp()

        d['entry_label'] = self.entry_label
        d['exit_label'] = self.exit_label

        d['adjusted_date'] = self.adjusted_date
        d['adjusted_time'] = self.adjusted_time

        d['entry_price'] = self.entry_price
        d['exit_price'] = self.exit_price

        d['avg_entry_price'] = self.avg_entry_price
        d['avg_exit_price'] = self.avg_exit_price

        d['qty'] = self.max_count
        d['pnl'] = self.realised_pnl
        d['net_pips'] = self.realised_pnl / self.contract_value
        d['net_pips_pre_contract'] = self.realised_pnl / self.contract_value / self.max_count
        d['slippage'] = self.slippage
        d['slippage_pre_contract'] = self.slippage / (self.num_sld + self.num_bot)


        d['max_net'] = self.max_net
        d['init_price'] = self.init_price
        d['commission'] = self.total_commission
        d['realised_pnl'] = self.realised_pnl
        d['unrealised_pnl'] = self.unrealised_pnl

        d['num_bot'] = self.num_bot
        d['num_sld'] = self.num_sld
        d['avg_bot_price'] = self.avg_bot_price
        d['avg_sld_price'] = self.avg_sld_price
        d['result'] = self.result

        return d