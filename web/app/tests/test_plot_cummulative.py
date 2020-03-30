import os
import pandas as pd
import unittest

from covid19.expogo.core import PlotCummulative


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(columns=["Province/State", "Country/Region", "Lat", "Long", "1/22/20", "1/23/20"],
                               data=[["Tokyo", "1.2", "2.2", "Japan", 5, 10]])
        self.base_df = PlotCummulative(self.df)

    def test_json_plot(self):
        self.assertIsNotNone(self.base_df.plot_by_country_json())
