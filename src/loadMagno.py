'''This module loads csv type magnotomerter data and preps it for further use.'''

import pandas as pd
import numpy as np
import datetime as dt
import pickle
import time
import os
import glob

from multiprocessing import Pool, Queue

thread_count = 10

hfs = dt.datetime.strptime("01-01-1904", "%m-%d-%Y")  # create a ref time.
print(hfs)


def load_data_from_path(path):
    '''takes a list of filenames and opens them for processing in a thread pool,
     returning a list of pandas data frames.'''

    outq = Queue(maxsize=0)

    def en_queue_dataframe(x):
        print(type(x))

    with Pool(processes=thread_count) as pool:
        pool.map(process_file, glob.iglob(path, recursive=True), 10,)

    print(outq.qsize())
    return list(outq.get())


def process_file(file_name):
    '''takes a file name and trys to load it into a pandas dataframe,
     converting from mac time to a datetime object.'''

    dataframe = pd.read_csv(file_name)

    dataframe[0] = dataframe[0].apply(lambda x: dt.datetime.fromtimestamp(x + hfs))

    print(dataframe.describe())




if __name__ == "__main__":
    print(load_data_from_path(path="data/raw/**/*.csv"))
