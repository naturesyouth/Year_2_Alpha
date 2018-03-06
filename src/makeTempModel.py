'''This module calculates a polynomial expression to charecteise
    the temperature calibration of the magnotomerter'''

import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections
from multiprocessing import Pool, Queue


def make_temp_data(df):

    temps = df.Temp.unique()
    result = []
    for i in temps:
        result.append((i,df))
    #print(result)

    pool = Pool()

    result = pool.map(split_subframe, result)

    result = [x for x in result if x is not None]

    tmp_set = pd.concat(result)

    sns.boxplot(x="Temp", y="Mag", data=tmp_set)

    plt.show()

    #for i in result:
    #    print(i.describe())
    #print(len(result))


def split_subframe(input):
    temp, dataframe = input
    dataframe = dataframe[dataframe['Temp'] == temp].sort_values(by=['Mag'])
    x, y = dataframe.shape
    if x >= 20:
        return dataframe
    else:
        return None


def split_iqr(dataframe):
    qr = dataframe.quantile([.25, .75])
    dataframe = dataframe[(dataframe['Mag'] >= qr.iloc[0]['Mag']) &
                          (dataframe['Mag'] <= qr.iloc[1]['Mag'])]
    return dataframe

if __name__ == "__main__":
    df = pd.read_pickle("data/mag.p")
    make_temp_data(df)

# df[df['colX'] == df['colY']]
