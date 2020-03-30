import pandas as pd
import json

from datetime import datetime, timedelta

import plotly.graph_objs as go


class BaseDataFrameManipulation(object):
    def __init__(self, df):
        self.df = self.transform_date(
            self.transpose_and_remove_index(self.drop_fields(df)))
    # drop information that arent important for the first plots

    def drop_fields(self, df):
        return df.drop(['Province/State', 'Lat', 'Long', 'Country/Region'], axis=1)

    def transpose_and_remove_index(self, df):
        return df.transpose().reset_index()

    # the date row must be transformed from string to date
    def transform_date(self, df):
        df.columns = ['date', 'cases']
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
        return df


class PlotCummulative(BaseDataFrameManipulation):
    def plot_by_country_json(self):
        return [go.Scatter(x=self.df['date'], y=self.df['cases'])]


class ExponentialGrowth(BaseDataFrameManipulation):
    def table_json(self):
        growth_table = self.generate_table(self.exponential_growth(self.df))
        return growth_table.to_json(orient='records', date_format='iso')

    # df must be the the result of transponse_and_remove_index
    def exponential_growth(self, df):
        df.columns = ['date', 'cases']
        days = df['date'].map(lambda x: (x - self.first_day()).days)
        df['day'] = days
        return df

    def generate_table(self, df, lastDays=20):
        # the following block is just for displaying the input data, with some unused augmentation
        df['cases_diff'] = df.diff()['cases']
        df['cases_growth_%'] = round(
            df['cases_diff'] / (df['cases'] - df['cases_diff']) * 100, 1)
        # show just last lastDays
        return df[-lastDays:]

    def first_day(self):
        return datetime(2020, 1, 1) - timedelta(days=1)

    def plot_by_country_json(self):
        plot_df = self.generate_table(self.df)
        return [go.Scatter(x=plot_df['date'], y=plot_df['cases_growth_%'])]