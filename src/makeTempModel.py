'''This module calculates a polynomial expression to charecteise
    the temperature calibration of the magnotomerter
    46nT for every deg farienhight
    '''

import math
import pickle
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

    with Pool() as pool:
        result = pool.map(split_subframe, result)
        result = [x for x in result if x is not None]
        #pool.map(make_data_plot, result)


    #for i in result:
    #    print(i.describe())
    #print(len(result))

    m = 1
    c = 1

    return (m, c)


def split_subframe(input):
    temp, dataframe = input
    dataframe = dataframe[dataframe['Temp'] == temp].sort_values(by=['Mag'])
    x, y = dataframe.shape
    if x >= 10:
        return dataframe
    else:
        return None

def make_data_plot(input):
    name = "Mag-Date-at-{}".format(str(input.iloc[0]['Temp']))
    print("Processing : {}".format(name))
    print(input.shape)
    plt.plot_date(x=input.Date, y=input.Mag)
    plt.savefig(name)


def apply_temp_correction(input):
    pass


def split_iqr(dataframe):
    qr = dataframe.quantile([.25, .75])
    dataframe = dataframe[(dataframe['Mag'] >= qr.iloc[0]['Mag']) &
                          (dataframe['Mag'] <= qr.iloc[1]['Mag'])]
    return dataframe


if __name__ == "__main__":
    df = pd.read_pickle("data/processed_mag.p")
    multiple, offset = make_temp_data(df)

    df['MagAdjust'] = df['Mag'].apply(lambda x: x + multiple * x + offset)

    pickle.dump(df, open("data/processed_compensated_mag.p", "wb"))

# df[df['colX'] == df['colY']]
