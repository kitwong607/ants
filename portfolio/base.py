from abc import ABCMeta

class AbstractPortfolio(object):
	__metaclass__ = ABCMeta

	def get_open_position(self):
		return self.positions

	def get_open_position_by_ticker(self, ticker):
		if ticker in self.positions:
			return self.positions[ticker]
		return False

	def get_last_update_timestamp():
		return self.last_update_timestamp


	def get_equity():
		return self.equity()