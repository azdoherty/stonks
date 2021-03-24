from unittest import TestCase
import pandas as pd
from datetime import datetime, timedelta
from rotation import RotationChart


class RotationCharTest(TestCase):

    def test_process(self):
        test_size = 500
        data = pd.DataFrame(
            [
                {
                    'SPY': (i + 1) * 100,
                    'IWM': (i + 1)**2 * 200
                } for i in range(test_size)
            ]
        )
        date_list = [datetime(2020, 1, 1) + timedelta(days=i) for i in range(test_size)]
        index = pd.DatetimeIndex(date_list)
        data.index = index
        acIdx = pd.MultiIndex.from_arrays([['Adj Close', 'Adj Close'], ['SPY', 'IWM']])
        data.columns = acIdx

        r = RotationChart()
        r.data = data
        r.normalize()
        self.assertEqual(
            r.data.loc[date_list[0], ('Adj Close Normed', 'SPY')], 1
        )
        self.assertEqual(
            r.data.loc[date_list[1], ('Adj Close Normed', 'SPY')], 2
        )
        self.assertEqual(
            r.data.loc[date_list[-1], ('Adj Close Normed', 'SPY')], 500
        )
        self.assertEqual(
            r.data.loc[date_list[0], ('Adj Close Normed', 'IWM')], 1
        )
        self.assertEqual(
            r.data.loc[date_list[1], ('Adj Close Normed', 'IWM')], 4
        )
        self.assertEqual(
            r.data.loc[date_list[-1], ('Adj Close Normed', 'IWM')], 250000
        )
        r.calculate_rs()
        self.assertEqual(
            r.data.loc[date_list[0], ('RS-Ratio', 'IWM')], 100
        )
