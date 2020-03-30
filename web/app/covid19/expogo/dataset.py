import pandas as pd
import os


class WorldPopulation(object):
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def population_by_country(self, country):
        return self.df[self.df['Country Name'] == country].iloc[0, -3]


class Covid19DataSet(object):
    def __init__(self, csv_file):
        self.df = pd.read_csv(os.path.join(
            "datasets", "{0}.csv".format(csv_file)))

    def find_by(self, country='Brazil'):
        return self.df[self.df['Country/Region'] == country]

    def to_json(self):
        return self.df.to_json(orient='records')
