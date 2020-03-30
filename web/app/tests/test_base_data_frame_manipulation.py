import os
import pandas as pd
import unittest

from covid19.expogo.core import BaseDataFrameManipulation

"""
We can stil add test to each method if we want to test specific conditions
"""


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(columns=["Province/State", "Country/Region", "Lat", "Long", "1/22/20", "1/23/20"],
                               data=[["Tokyo", "1.2", "2.2", "Japan", 5, 10]])

    def test_drop_fields(self):
        self.assertIsNotNone(BaseDataFrameManipulation(self.df))
