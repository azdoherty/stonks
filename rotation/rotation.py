import pandas as pd
import yfinance as yf


class RotationChart:

    NORMALIZED_CLOSE = 'Adj Close Normed'
    DEFAULT_WINDOW = 50

    def __init__(self, start_date='2020-01-01', end_date='2021-01-01', benchmark='SPY', tickers=None):
        self.start_date = start_date
        self.end_date = end_date
        self.yf = yf
        self.benchmark = benchmark
        self.tickers = ['IWM'] if not tickers else [t.upper() for t in tickers]
        self.data = pd.DataFrame()

    def download_starting_data(self):
        ticker_string = self.benchmark + ' ' + ' '.join(self.tickers)
        self.data = self.yf.download(ticker_string, start=self.start_date, end=self.end_date)

    def process(self):
        self.normalize()
        self.calculate_rs()

    def normalize(self):
        """
        normalize all prices to the starting price
        :return:
        """
        start = self.data.index[0]
        all_tickers = self.tickers + [self.benchmark]
        normed = self.data.loc[:, ('Adj Close', all_tickers)] / self.data.loc[start, ('Adj Close', all_tickers)]
        normed.columns = normed.columns.set_levels([self.NORMALIZED_CLOSE], level=0)
        self.data = self.data.join(normed)

    def calculate_rs(self, smooth_factor=10, momentum_offset=10):
        for ticker in self.tickers + [self.benchmark]:
            # make all prices relative to benchmark
            self.data['RS-Ratio', ticker] = 100 * (self.data.loc[:, (self.NORMALIZED_CLOSE, ticker)] /
                                                   self.data.loc[:, (self.NORMALIZED_CLOSE, self.benchmark)])
            # rolling mean and standard deviation of relative price
            self.data['RS-mean', ticker] = self.data['RS-Ratio', ticker].rolling(self.DEFAULT_WINDOW).mean()
            self.data['RS-stdev', ticker] = self.data['RS-Ratio', ticker].rolling(self.DEFAULT_WINDOW).std()
            # JDK RS ratio
            self.data['JDK RS-ratio', ticker] = \
                100 + (self.data['RS-Ratio', ticker] - self.data['RS-mean', ticker]) / self.data['RS-stdev', ticker]
            # momentum of RS ratio
            self.data['momentum', ticker] = self.data['RS-Ratio', ticker] - \
                                            self.data['RS-Ratio', ticker].shift(momentum_offset)
            # JSK RS Momentum
            self.data['JDK RS-Momentum', ticker] = \
                100 + (self.data['momentum', ticker] - self.data['momentum', ticker].rolling(self.DEFAULT_WINDOW).mean()) \
                / self.data['momentum', ticker].rolling(self.DEFAULT_WINDOW).std()

            # now smooth the ratio and momentum
            self.data['JDK RS-ratio', ticker] = self.data['JDK RS-ratio', ticker] .rolling(smooth_factor).mean()
            self.data['JDK RS-Momentum', ticker] = self.data['JDK RS-Momentum', ticker] .rolling(smooth_factor).mean()


