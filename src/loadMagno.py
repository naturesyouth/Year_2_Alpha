'''This module loads csv type magnotomerter data and preps it for further use.'''

import pandas as pd
import numpy as np
import datetime as dt
import pickle
import time
import os
import glob
import math

from multiprocessing import Pool, Queue

thread_count = 10

hfs = 2082844800  # seconds between 1904 and 1970.


def load_data_from_path(path):
    '''takes a list of filenames and opens them for processing in a thread pool,
     returning a list of pandas data frames.'''

    outq = Queue(maxsize=0)

    with Pool(processes=thread_count) as pool:
        result = pool.map(process_file, glob.iglob(path, recursive=True))

        outq.put(result)

    return list(outq.get())


def process_file(file_name):
    '''takes a file name and trys to load it into a pandas dataframe,
     converting from mac time to a datetime object.'''

    dataframe = pd.read_csv(file_name, names=['Date', 'Mag', 'Temp'])

    dataframe['Date'] = dataframe['Date'].apply(lambda x: dt.datetime.fromtimestamp(x - hfs))
    dataframe['Temp'] = dataframe['Temp'].apply(lambda x: round(x, 1-int(math.floor(math.log10(abs(x))))-1))

    return dataframe


if __name__ == "__main__":
    dataframe = load_data_from_path(path="data/raw/**/*.csv")
    dataframe = pd.concat(dataframe).sort_values(by='Date')

    pickle.dump(dataframe, open("data/processed_mag.p", "wb"))
