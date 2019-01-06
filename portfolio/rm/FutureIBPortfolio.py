from .base import AbstractPortfolio
from ..position.future_position import FuturePosition
from .. import utilities
import json

class FuturePortfolio(AbstractPortfolio):
    NAME = "FutureIBPortfolio"

    def __init__(self, session):
        super().__init__(session)


    def TransactOrder(self, order):
        if order.ticker not in self.positions:
            self.AddPosition(order)
        else:
            self.ModifyPosition(order)
        self.RecordOrder(order)


    def AddPosition(self, order):
        self.positions[order.ticker] = FuturePosition(order)


    def ModifyPosition(self, order):
        self.positions[order.ticker].TransactOrder(order)
        if self.positions[order.ticker].status == "CLOSED":
            closedPosition = self.positions.pop(order.ticker)

            self.recordPosition(closedPosition)
            self.closedPositions.append(closedPosition)


    def RecordPosition(self, position):
        record = position.to_dict()
        record['positionId'] = len(self.positionRecords) + 1
        self.position_records.append(record)


    def RecordOrder(self, order):
        record = order.to_dict()
        self.order_records.append(record)


    def Save(self):
        json_filename = "//positions.json"
        with open(self.session.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(self.positionRecords, fp, cls=utilities.AntJSONEncoder)

        json_filename = "//orders.json"
        with open(self.session.config.reportDirectory + jsonFilename, 'w') as fp:
            json.dump(self.orderRecords, fp, cls=utilities.AntJSONEncoder)