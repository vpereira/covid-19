import requests


class GetDatasets(object):

    GITHUB_PATH = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'

    DATASETS = ['Confirmed', 'Deaths', 'Recovered']

    def __init__(self, path):
        self.path = path

    def datasets(self):
        for df in self.DATASETS:
            self.download_and_save(df)

    def download_and_save(self, df_name):
        req = requests.get(self.read_covid19(df_name))
        with open(self.file_path(df_name), 'wb') as f:
            f.write(req.content)

    def read_covid19(self, k):
        # get data file names, we guess date until yesterday because of some delay with dataset publishing
        return '{0}/time_series_19-covid-{1}.csv'.format(self.GITHUB_PATH, k)

    def file_path(self, name):
        return '{0}/{1}.csv'.format(self.path, name.lower())
