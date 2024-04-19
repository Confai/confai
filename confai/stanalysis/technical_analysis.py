import datetime
import yfinance as yf
import talib as ta

class StockAnalyzer:
    def __init__(self, symbol, start, end=None):
        self.symbol = symbol
        self.start = start
        self.end = datetime.date.today() if end is None else end
        self.data = None

    def get_data(self):
        self.data = yf.download(self.symbol, self.start, self.end)

    def get_adj_close_ema_sma(self):
        df = self.data
        df['SMA'] = ta.SMA(df['Adj Close'].values, timeperiod = 20)
        df['EMA'] = ta.EMA(df['Adj Close'].values, timeperiod = 20)
        return df[['Adj Close', 'SMA', 'EMA']]

    def get_bollinger_bands(self):
        df = self.data
        df['upper_band'], df['middle_band'], df['lower_band'] = ta.BBANDS(df['Adj Close'], timeperiod =20)
        return df[['Adj Close', 'upper_band', 'middle_band', 'lower_band']]

    def get_macd(self):
        df = self.data
        df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        return df[['macd', 'macdsignal']]

    def get_rsi(self):
        df = self.data
        df['RSI'] = ta.RSI(df['Adj Close'], timeperiod=14)
        return df['RSI']

    def get_obv(self):
        df = self.data
        df['OBV'] = ta.OBV(df['Adj Close'], df['Volume'])/10**6
        return df['OBV']

    def big_three(self):
        df = self.data
        df['SMA_20'] = df['Adj Close'].rolling(20).mean()
        df['SMA_40'] = df['Adj Close'].rolling(40).mean()
        df['SMA_80'] = df['Adj Close'].rolling(80).mean()

        return df[['Adj Close', 'SMA_20', 'SMA_40', 'SMA_80']]

    def get_all(self):
        self.get_data()
        return {
            'adj_close_ema_sma': self.get_adj_close_ema_sma(),
            'bollinger_bands': self.get_bollinger_bands(),
            'macd': self.get_macd(),
            'rsi': self.get_rsi(),
            'obv': self.get_obv(),
            'big_three': self.big_three(),
        }