import queue, copy,datetime, calendar, multiprocessing
from .data_provider.base import DataType
from . import utilities
from .session_config import SessionMode, SessionStaticVariable
from dateutil.relativedelta import relativedelta


#LiveSession is a websocket client

class LiveSession(object):
    def __init__(self, config):
        self.config = config

        self.data_queue = queue.Queue()
        self.orders_queue = queue.Queue()

        #use default class?
        #or it depends on exchange and trade product?

        if self.config.exchange == "hkex":
            from ..data_provider.IBHKEXDataProdiver import IBHKEXDataProdiver
            self.data_provider = IBHKEXDataProdiver(self)

            from ..portfolio.FutureIBHKEXPortfolio import FutureIBHKEXPortfolio
            self.portfolio = FutureIBHKEXPortfolio(self)

            from ..order_handler.IBHKEXOrderHandler import IBHKEXOrderHandler
            self.order_handler = IBHKEXOrderHandler(self)
        else:
            print("exchange " + self.config.exchange + " not support")
            quit()


        self.strategy = self.config.strategy_class()
        self.strategy.setup(self)

        #setup today data file path


        self.setup_ws_client()

    def setup_ws_client(self):
        print("setup_ws_client")
        pass

    def run(self):
        if self.config.mode == SessionMode.INTER_DAY_SINGLE_PROCESS or self.config.mode == SessionMode.INTRA_DAY_SINGLE_PROCESS or self.config.is_sub_process:
            self.data_provider.streaming()


    def on_in_period_data(self):
        self.strategy.in_period_data = True

    def on_data(self, data):
        if data is not None:
            if data.type == DataType.BAR:
                self.strategy.calculate_bar_data(data)
                self.portfolio.update_portfolio()
            elif data.type == DataType.TICK:
                self.strategy.calculate_tick_data(data)
                self.portfolio.update_portfolio()
            else:
                raise NotImplemented("Unsupported event.type '%s'" % event.type)

    def on_complete(self):
        self.save_report()

    def save_report(self):
        print("self.config.save")
        if not self.config.is_sub_process:
            self.config.save()

        print("self.config.portfolio")
        self.portfolio.save()
        print("self.config.strategy")
        self.strategy.save()

        if not self.config.is_sub_process:
            utilities.create_report_summary(self.config.report_directory)

    def merge_portfolio_json(self, obj_name):
        import json, os
        obj_list = []
        for i in range(1, self.config.num_sub_process + 1):
            json_filename = "//"+obj_name+"_" + str(i) + ".json"
            with open(self.config.report_directory + json_filename) as json_data:
                obj_list = obj_list + json.load(json_data)
            os.remove(self.config.report_directory + json_filename)

        obj_id = 1
        id_key = obj_name+'_id'
        id_key = id_key.replace("positions","position").replace("orders", "order")
        for obj in obj_list:
            obj[id_key] = obj_id
            obj_id += 1

        with open(self.config.report_directory + "//"+obj_name+".json", 'w') as fp:
            json.dump(obj_list, fp, cls=utilities.AntJSONEncoder)

    def merge_inter_ta_json(self, obj_name):
        import json, os
        obj_d = None
        for i in range(1, self.config.num_sub_process + 1):
            json_filename = "//"+obj_name+"_" + str(i) + ".json"
            with open(self.config.report_directory + json_filename) as json_data:
                new_come_obj_d = json.load(json_data)
                if obj_d is None:
                    obj_d = new_come_obj_d
                else:
                    for key in obj_d:
                        obj_d[key]["values"] = obj_d[key]["values"] +  new_come_obj_d[key]["values"]
                        obj_d[key]["calculated_values"] = obj_d[key]["calculated_values"] +  new_come_obj_d[key]["calculated_values"]
                        obj_d[key]["values_ts"] = obj_d[key]["values_ts"] +  new_come_obj_d[key]["values_ts"]
                        obj_d[key]["calculated_values_ts"] = obj_d[key]["calculated_values_ts"] +  new_come_obj_d[key]["calculated_values_ts"]
            os.remove(self.config.report_directory + json_filename)

        for key in obj_d:
            new_values = []
            new_calculated_values = []
            new_values_ts = []
            new_calculated_values_ts = []

            i = 0
            for ts_key in obj_d[key]["values_ts"]:
                if ts_key not in new_values_ts:
                    new_values_ts.append(ts_key)
                    new_values.append(obj_d[key]["values"][i])
                i += 1


            i = 0
            for ts_key in obj_d[key]["calculated_values_ts"]:
                if ts_key not in new_calculated_values_ts:
                    new_calculated_values_ts.append(ts_key)
                    new_calculated_values.append(obj_d[key]["calculated_values"][i])
                i += 1

            obj_d[key]["values"] = new_values
            obj_d[key]["values_ts"] = new_values_ts
            obj_d[key]["calculated_values"] = new_calculated_values
            obj_d[key]["calculated_values_ts"] = new_calculated_values_ts

        with open(self.config.report_directory + "//"+obj_name+".json", 'w') as fp:
            json.dump(obj_d, fp, cls=utilities.AntJSONEncoder)

    def merge_intra_ta_json(self, obj_name):
        import json, os
        obj_d = None

        new_values = {}
        new_calculated_values = {}
        new_values_ts = {}
        new_calculated_values_ts = {}

        for i in range(1, self.config.num_sub_process + 1):
            json_filename = "//"+obj_name+"_" + str(i) + ".json"
            with open(self.config.report_directory + json_filename) as json_data:
                new_come_obj_d = json.load(json_data)
                if obj_d is None:
                    obj_d = new_come_obj_d
                    for ta_key in new_come_obj_d:
                        new_values[ta_key] = new_come_obj_d[ta_key]["values"]
                        new_calculated_values[ta_key] = new_come_obj_d[ta_key]["calculated_values"]
                        new_values_ts[ta_key] = new_come_obj_d[ta_key]["values_ts"]
                        new_calculated_values_ts[ta_key] = new_come_obj_d[ta_key]["calculated_values_ts"]
                else:

                    for ta_key in new_come_obj_d:
                        for date_key in new_come_obj_d[ta_key]["values"]:
                            new_values[ta_key][date_key] = new_come_obj_d[ta_key]["values"][date_key]

                        for date_key in new_come_obj_d[ta_key]["calculated_values"]:
                            new_calculated_values[ta_key][date_key] = new_come_obj_d[ta_key]["calculated_values"][date_key]

                        for date_key in new_come_obj_d[ta_key]["values_ts"]:
                            new_values_ts[ta_key][date_key] = new_come_obj_d[ta_key]["values_ts"][date_key]

                        for date_key in new_come_obj_d[ta_key]["calculated_values_ts"]:
                            new_calculated_values_ts[ta_key][date_key] = new_come_obj_d[ta_key]["calculated_values_ts"][date_key]
            os.remove(self.config.report_directory + json_filename)

            for ta_key in new_values:
                obj_d[ta_key]["values"] = new_values[ta_key]

            for ta_key in new_values_ts:
                obj_d[ta_key]["values_ts"] = new_values_ts[ta_key]

            for ta_key in new_calculated_values:
                obj_d[ta_key]["calculated_values"] = new_calculated_values[ta_key]

            for ta_key in new_calculated_values_ts:
                obj_d[ta_key]["calculated_values_ts"] = new_calculated_values_ts[ta_key]

        with open(self.config.report_directory + "//"+obj_name+".json", 'w') as fp:
            json.dump(obj_d, fp, cls=utilities.AntJSONEncoder)

    def merge_report(self):
        self.config.save()
        self.merge_portfolio_json("positions")
        self.merge_portfolio_json("orders")

        self.merge_inter_ta_json("inter_day_ta")
        self.merge_inter_ta_json("inter_day_ta_separated")
        self.merge_intra_ta_json("intra_day_ta")
        self.merge_intra_ta_json("intra_day_ta_separated")

        utilities.create_report_summary(self.config.report_directory)

    def next_valid_order_id(self):
        self.order_id += 1
        return self.order_id


    def log(self, *args):
        '''
        message = ""
        for arg in args:
            message += " " + str(arg)
        self.on_log.fire(message)
        print(str(datetime.datetime.now()), message)
        #ToDo log to file
        '''