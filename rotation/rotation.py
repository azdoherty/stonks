import pandas as pd
import yfinance as yf


class RotationChart:

    NORMALIZED_CLOSE = 'Adj Close Normed'

    def __init__(self, start_date='2020-01-01', end_date='2021-01-01', benchmark='SPY', tickers=None):
        self.start_date = start_date
        self.end_date = end_date
        self.yf = yf
        self.benchmark = benchmark
        self.tickers = ['IWM'] if not tickers else [t.upper for t in tickers]
        self.data = pd.DataFrame()

    def download_starting_data(self):
        ticker_string = self.benchmark + ' ' + ' '.join(self.tickers)
        self.data = self.yf.download(ticker_string, start=self.start_date, end=self.end_date)

    def process(self):
        self.normalize()
        self.calculate_rs()

    def normalize(self):
        start = self.data.index[0]
        all_tickers = self.tickers + [self.benchmark]
        normed = self.data.loc[:, ('Adj Close', all_tickers)] / self.data.loc[start, ('Adj Close', all_tickers)]
        normed.columns = normed.columns.set_levels([self.NORMALIZED_CLOSE], level=0)
        self.data = self.data.join(normed)

    def calculate_rs(self):
        """
        calculate the relative strength to the benchmark
        :return:
        """
        for ticker in self.tickers:
            rs = 100 * (self.data.loc[:, (self.NORMALIZED_CLOSE, ticker)] /
                        self.data.loc[:, (self.NORMALIZED_CLOSE, self.benchmark)])
            self.data['RS-Ratio', ticker] = rs
