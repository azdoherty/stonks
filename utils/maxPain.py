import pandas as pd
import numpy as np
import yfinance as yf


class MaxPain:
    dtypes = {
        'contractSymbol': str,
        'strike': np.float64,
        'lastPrice': np.float64,
        'change': np.float64,
        'openInterest': np.float64,
    }

    def __init__(self, ticker):
        self.tickerString = ticker
        self.ticker = yf.Ticker(ticker)
        self.chain = None
        self.max_pain = pd.DataFrame()

    def run(self, strike_date=None):
        self.chain = self.get_option_data(strike_date)
        self.max_pain = self.calculate_max_pain(self.chain)

    def get_option_data(self, strike_date=None):
        if not strike_date:
            strike_date = self.ticker.options[0]
        chain = self.ticker.option_chain(strike_date)
        return chain

    def calculate_max_pain(self, chain):
        calls = chain.calls.loc[:, self.dtypes.keys()]
        puts = chain.puts.loc[:, self.dtypes.keys()]
        calls_and_puts = calls.merge(puts, left_on='strike', right_on='strike', suffixes=('_c', '_p'))
        calls_and_puts['cash_c'] = None
        calls_and_puts['cash_p'] = None
        calls_and_puts['cash_total'] = None

        for idx, row in calls_and_puts.iterrows():
            p = row['strike']
            c_cash = (p - calls_and_puts['strike']) * calls_and_puts['openInterest_c'] * 100
            c_cash[c_cash < 0] = 0
            p_cash = (calls_and_puts['strike'] - p) * calls_and_puts['openInterest_p'] * 100
            p_cash[p_cash < 0] = 0
            c_cash_total = c_cash.sum()
            p_cash_total = p_cash.sum()
            calls_and_puts.loc[idx, 'cash_c'] = c_cash_total
            calls_and_puts.loc[idx, 'cash_p'] = p_cash_total
            calls_and_puts.loc[idx, 'cash_total'] = c_cash_total + p_cash_total
        return calls_and_puts
