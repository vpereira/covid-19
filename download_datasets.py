#!/usr/bin/env python3
from fetcher.get_datasets import GetDatasets
import datetime

if __name__ == '__main__':
    gt = GetDatasets('datasets')
    gt.datasets()
    with open('web/app/datasets/last_run.txt', 'w') as file:
        file.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S\n"))
