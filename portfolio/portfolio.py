from .base import AbstractPortfolio
from .position import FuturePosition, PositionStatus
from .. import utilities
import json

class FuturePortfolio(AbstractPortfolio):
    IS_DISPLAY_IN_OPTION = True
    NAME = "FuturePortfolio"


    def __init__(self, session):
        super().__init__(session)


    def AddPosition(self, order):
        self.positions[order.ticker] = FuturePosition(order)