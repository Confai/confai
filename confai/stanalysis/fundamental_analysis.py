import yfinance as yf

class FundamentalAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.stock = yf.Ticker(self.symbol)
        self.basic_info = None
        self.financials = None
        self.balance_sheet = None
        self.cash_flow = None

    def fetch_data(self):
        self.basic_info = self.stock.info
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balancesheet
        self.cash_flow = self.stock.cashflow