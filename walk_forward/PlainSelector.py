from .base import ParameterSelector
from ..session_config import SessionStaticVariable

import json, numpy as np

class PlainSelector(ParameterSelector):
    def __init__(self, *args, **kwargs):
        super(PlainSelector, self).__init__(*args, **kwargs)
        if len(self.optimization_parameter)>2:
            raise Exception('PlainSelector: input optimization parameter more than two')

        self.grid_offset1 = [-2,-1,1,2]

        self.grid_offset2 = [               [0,-2],
                                   [-1,-1],[0,-1],[1,-1],
                            [-2,0],[-1,0] ,       [1,0] , [2,0],
                                   [-1,1] ,[0,1] ,[1,1] ,
                                           [0,2]
                            ]

    def get_selected_parameter(self):
        parameter_value = {}
        score_table = []
        keys = []
        len_parameter = []
        profit_factor_array = []

        score_array = []

        for key in self.optimization_parameter:
            keys.append(key)
            len_parameter.append(0)

            parameter = self.optimization_parameter[key]
            parameter['range'] = []
            for j in range(parameter['min_value'], parameter['max_value']+1, parameter['step']):
                parameter['range'].append(j)
            len_parameter[len(len_parameter)-1] = len(parameter['range'])

        if len(keys)==2:
            for i in range(0, len_parameter[0]):
                profit_factor_array.append([])
                score_array.append([])

                for j in range(0, len_parameter[1]):
                    profit_factor_array[i].append(0)
                    score_array[i].append(0)
        else:
            '''
            for i in range(0, len_parameter[0]):
                profit_factor_array.append([])
                score_array.append([])
            '''

            for i in range(0, len_parameter[0]):
                profit_factor_array.append(0)
                score_array.append(0)


        optimization_report = None

        for backtest in self.backtest_batch:
            optimization_report_path = SessionStaticVariable.base_report_directory + backtest['report_folder_name'] + "\\optimization.json"

            if optimization_report is None:
                with open(optimization_report_path) as f:
                    optimization_report = json.load(f)
                    #print(json.dumps(optimization_report, indent=2))
                    break

        for backtest in optimization_report['backtest']:
            if len(keys)==2:
                val1 = backtest['parameter'][keys[0]]
                val2 = backtest['parameter'][keys[1]]

                x = self.optimization_parameter[keys[0]]['range'].index(val1)
                y = self.optimization_parameter[keys[1]]['range'].index(val2)

                profit_factor_array[x][y] = backtest['performance']['profit_factor']

            else:
                val1 = backtest['parameter'][keys[0]]
                x = self.optimization_parameter[keys[0]]['range'].index(val1)
                profit_factor_array[x] = backtest['performance']['profit_factor']

        max_value = -100
        max_value_x = -1
        max_value_y = -1


        if len(keys) == 2:

            for x in range(0, len_parameter[0]):
                for y in range(0, len_parameter[1]):
                    value = []
                    for offset in self.grid_offset2:
                        new_x = x + offset[0]
                        new_y = y + offset[1]
                        if(new_x >= 0 and new_x < len_parameter[0] and new_y >= 0 and new_y < len_parameter[1]):
                            #print(x, y, "append:", new_x, new_y)
                            value.append(profit_factor_array[new_x][new_y])
                    score_array[x][y] = float(format(np.mean(value), '.4f'))
                    if(score_array[x][y] > max_value):
                        max_value = score_array[x][y]
                        max_value_x = x
                        max_value_y = y

            val2 = self.optimization_parameter[keys[1]]['range'][max_value_y]

            returnValue = {}
            returnValue[keys[0]] = self.optimization_parameter[keys[0]]['range'][max_value_x]
            returnValue[keys[1]] = self.optimization_parameter[keys[1]]['range'][max_value_y]

            return returnValue
        else:

            for x in range(0, len_parameter[0]):
                value = []
                for offset in self.grid_offset1:
                    new_x = x + offset
                    if(new_x >= 0 and new_x < len_parameter[0]):
                        value.append(profit_factor_array[new_x])
                score_array[x] = float(format(np.mean(value), '.4f'))
                if(score_array[x] > max_value):
                    max_value = score_array[x]
                    max_value_x = x

            returnValue = {}
            returnValue[keys[0]] = self.optimization_parameter[keys[0]]['range'][max_value_x]

            return returnValue