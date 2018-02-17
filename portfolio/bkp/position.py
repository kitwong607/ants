from numpy import sign
import pandas as pd
from .base import AbstractPosition
from datetime import timedelta

class Position(AbstractPosition):
    def __init__(self, order):
        self.last_update_time = self.entry_time = order.filled_timestamp
        self.init_price = order.filled_price
        self.entry_label = order.label
        self.marker = None
        self.action = order.action
        self.ticker = order.ticker
        self.data_ticker = order.data_ticker

        self.pips_value = 1
        if(self.ticker=='MHI' or self.ticker=='MCH'):
            self.pips_value = 10
        else:
            self.pips_value = 50

        self.max_net = self.quantity = order.quantity
        self.commission = order.commission
        self.realised_pnl = -self.commission
        self.unrealised_pnl = -self.commission

        self.trade_log = {}
        self._update_trade_log(order)

        self.buys = 0
        self.sells = 0
        self.avg_bot = 0
        self.avg_sld = 0
        self.total_bot = 0
        self.total_sld = 0
        self.total_commission = order.commission

        self.max_profit_pip = -10000.0
        self.max_profit_time = order.filled_timestamp

        self.stop_gain_price = None
        self.stop_gain_pips = None
        self.step_up_stop_gain_price = None
        self.step_up_stop_gain_count = 0

        if self.action =="BUY":
            self.stop_loss_price = self.init_stop_loss_price = order.filled_price - order.stop_loss_threshold
        elif self.action =="SELL":
            self.stop_loss_price = self.init_stop_loss_price = order.filled_price + order.stop_loss_threshold
        self.stop_loss_pips = self.init_stop_loss
        self.step_up_stop_loss_price = None
        self.step_up_stop_loss_count = 0

        self._calculate_initial_value()
        self.update_market_value(order.filled_timestamp, order.filled_price, order.filled_price)

    def _update_trade_log(self, order):
        self.trade_log[order.filled_timestamp] = {'action': order.action, 'price': order.filled_price, 'quantity': order.quantity,
                                     'commission': order.commission, 'stop_loss_threshold': order.stop_loss_threshold, 'contract_value': self.pips_value}

    def _update_max_net(self):
        if self.action == "BUY":
            self.max_net = max(self.max_net, self.buys)
        elif self.action == "SELL":
            self.max_net = min(self.max_net, self.sells)

    def _calculate_initial_value(self):
        if self.action == "BUY":
            self.buys = self.quantity
            self.avg_bot = self.init_price
            self.total_bot = self.buys * self.avg_bot
            self.avg_price = (self.init_price * self.quantity + (self.commission/self.contract_value)) // self.quantity
            self.cost_basis = self.quantity * self.avg_price
        else:  # action == "SELL"
            self.sells = self.quantity
            self.avg_sld = self.init_price
            self.total_sld = self.sells * self.avg_sld
            self.avg_price = (self.init_price * self.quantity - (self.commission/self.contract_value)) // self.quantity
            self.cost_basis = -self.quantity * self.avg_price
        self.net = self.buys - self.sells
        self.net_total = self.total_sld - self.total_bot
        self.net_incl_comm = self.net_total - self.commission

    def current_profit_in_pips(self):
        return self.unrealised_pnl/self.contract_value

    def update_market_value(self):
        bid, ask = self.session.data_provider.get_last_bid_ask(self.data_ticker)
        timestamp = self.session.data_provider.get_last_timestamp(self.data_ticker)

        self.last_update_time = timestamp
        midpoint = (bid + ask) // 2
        self.market_value = self.quantity * midpoint * sign(self.net)
        self.unrealised_pnl = (self.market_value - self.cost_basis) * self.contract_value

        current_profit_pips = self.current_profit_pips()
        if self.max_profit_pip < current_profit_pips:
            self.max_profit_pip = current_profit_pips
            self.max_profit_time = timestamp





        self.pips_high_time = None


    def transact_order(self, order):
        timestamp = order.filled_timestamp
        action = order.action
        quantity = order.quantity
        price = order.filled_price
        commission = order.commission
        label = order.label

        self._update_trade_log(timestamp, action, price, quantity, commission, self.contract_value)
        self.total_commission += commission
        self.last_update_time = timestamp

        # Adjust total bought and sold
        if action == "BUY":
            self.avg_bot = (
                self.avg_bot * self.buys + price * quantity
            ) // (self.buys + quantity)
            if self.action != "SELL":  # Increasing long position
                self.avg_price = (
                    self.avg_price * self.buys +
                    price * quantity + (commission/ self.contract_value)
                ) // (self.buys + quantity)
            elif self.action == "SELL":  # Closed partial positions out
                self.realised_pnl += quantity * (
                    self.avg_price - price
                ) * self.contract_value - commission  # Adjust realised PNL
            self.buys += quantity
            self.total_bot = self.buys * self.avg_bot

        # action == "SELL"
        else:
            self.avg_sld = (
                self.avg_sld * self.sells + price * quantity
            ) // (self.sells + quantity)
            if self.action != "BUY":  # Increasing short position
                self.avg_price = (
                    self.avg_price * self.sells +
                    price * quantity - (commission/ self.contract_value)
                ) // (self.sells + quantity)
                self.unrealised_pnl -= commission
            elif self.action == "BUY":  # Closed partial positions out
                self.realised_pnl += quantity * (
                    price - self.avg_price
                ) * self.contract_value - commission
            self.sells += quantity
            self.total_sld = self.sells * self.avg_sld

        # Adjust net values, including commissions
        self.net = self.buys - self.sells
        self.quantity = self.net
        self.net_total = self.total_sld - self.total_bot
        self.net_incl_comm = self.net_total - self.total_commission

        # Adjust average price and cost basis
        self.cost_basis = self.quantity * self.avg_price

        self.exit_time = timestamp
        self.exit_label = label

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
        return formula.second_between_two_datetime(self.entry_time, self.last_update_time)

    def close_position(self):
        trade_log_df = pd.DataFrame.from_dict(self.trade_log, orient='index').sort_index()
        self.profit = self.realised_pnl
        self.profit_pip = self.net_total
        if(self.profit>0):
            self.result = 'WIN'
        else:
            self.result = 'LOSS'
        self.commission = self.total_commission
        self.entry_price = trade_log_df[(trade_log_df.action == self.action)]
        self.exit_price = trade_log_df[(trade_log_df.action != self.action)]

        if(self.action=='BOT'):
            self.avg_entry_price = self.avg_bot
            self.avg_exit_price = self.avg_sld
        else:
            self.avg_entry_price = self.avg_sld
            self.avg_exit_price = self.avg_bot

        self.dd_s, self.max_dd = perf.create_unrealised_pnl_drawdown(self.unrealised_pnl_s)
        self.run_up_s, self.max_run_up = perf.create_unrealised_pnl_runup(self.unrealised_pnl_s)
