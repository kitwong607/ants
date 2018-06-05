import queue, copy,datetime, calendar, multiprocessing
from .data_provider.base import DataType
from . import utilities
from .session_config import SessionMode, SessionStaticVariable
from dateutil.relativedelta import relativedelta


class Session(object):
    def __init__(self, config):
        self.config = config
        if (self.config.mode == SessionMode.INTER_DAY_MULTI_PROCESS or self.config.mode == SessionMode.INTRA_DAY_MULTI_PROCESS) and (not self.config.is_sub_process):
            return

        self.data_queue = queue.Queue()
        self.orders_queue = queue.Queue()
        self.data_provider = self.config.data_provider_class(self)
        self.portfolio = self.config.portfolio_class(self)
        self.order_handler = self.config.order_handler_class(self)
        self.strategy = self.config.strategy_class()
        self.strategy.setup(self)

        self.order_id = 0

    def setup(self):
        #Todo forget why we have this function may be use for connect IB gateway py controller
        pass

    def run(self):
        if self.config.mode == SessionMode.INTER_DAY_SINGLE_PROCESS or self.config.mode == SessionMode.INTRA_DAY_SINGLE_PROCESS or self.config.is_sub_process:
            self.data_provider.streaming()
        elif self.config.mode == SessionMode.INTER_DAY_MULTI_PROCESS or self.config.mode == SessionMode.INTRA_DAY_MULTI_PROCESS:
            data_period = utilities.get_months_between_two_datetime(self.config.start_date, self.config.end_date)
            diff = self.config.start_date - self.config.data_start_date

            result_list = []
            pool = multiprocessing.Pool()
            process_no = 1
            for month_str in data_period:
                last_date_of_month = calendar.monthrange(int(month_str[0:4]), int(month_str[4:6]))[1]
                start_date = datetime.datetime(int(month_str[0:4]), int(month_str[4:6]), 1, 0, 0, 1)
                end_date = datetime.datetime(int(month_str[0:4]), int(month_str[4:6]), last_date_of_month, 23, 59, 59)
                data_start_date = start_date - diff

                self.config.num_sub_process = len(data_period)

                new_config = copy.deepcopy(self.config)
                new_config.start_date = start_date
                new_config.end_date = end_date
                new_config.data_start_date = data_start_date
                new_config.is_sub_process = True
                new_config.process_no = process_no

                new_config.prepare_data_period()

                result = pool.apply_async(self.start_sub_process, (new_config,))
                if (self.config.is_debug):
                    result.get()
                result_list.append(result)

                process_no += 1
            pool.close()
            pool.join()

            while len(result_list) != process_no-1:
                time.sleep(3)

            self.merge_report()

    def start_sub_process(self, new_config):
        session = Session(new_config)
        session.setup()
        session.run()

    def start(self):
        #Todo forget why we have this function may be use for connect IB gateway py controller
        pass

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
        '''
        if self.config.mode == "BT":
            #Todo connect center server for next order id
            return 1
        else:
            #Todo connect IB Gateway for next order id
            return 1
            '''

    def log(self, *args):
        '''
        message = ""
        for arg in args:
            message += " " + str(arg)
        self.on_log.fire(message)
        print(str(datetime.datetime.now()), message)
        #ToDo log to file
        '''