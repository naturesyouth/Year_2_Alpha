'''This module calculates a polynomial expression to charecteise
    the temperature calibration of the magnotomerter'''

import math
import pandas as pd
import seaborn as sns
import collections
from multiprocessing import Pool, Queue


class Return_Class(collections.Iterable):
    ''' A wrapper class to pass more data to a mapable function.'''
    def __init__(self, name=None, dataframe=None):
        self.dataframe = dataframe
        self.todo = Queue()
        for i in name:
            self.todo.put(i)

    def __iter__(self):
        return self

    def __next__(self):
        return (next(self.todo.get()), self.dataframe)

def make_temp_data(df):

    temps = df.Temp.unique()
    result = []

    #pool_loader = Return_Class(temps, df)

    for i in temps:
        result.append(split_subframe((i, df)))

    for i in result:
        print(i.describe())


def split_subframe(input):
    temp, dataframe = input
    return dataframe[dataframe['Temp'] == temp]


if __name__ == "__main__":
    df = pd.read_pickle("data/mag.p")
    make_temp_data(df)


# df[df['colX'] == df['colY']]
