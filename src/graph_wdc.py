'''Basic script to graph wdc data for a given date range.'''

import pandas as pd
import seaborn as sns

def main(filename=None, date_start=None, date_end=None):

    dataframe = []

    print(filename)

    for name in filename:
        dataframe.append( pd.read_csv(name) )

    df = pd.concat(dataframe)

    print(df.info())

    df = df.melt('TIME', var_name='cols', value_name='vals')
    sns_plot = sns.factorplot(x='TIME', y='vals', hue='cols', data=df )
    sns_plot.savefig("wdc.png")

if __name__ == '__main__':
    main(["data/wdc_download/kir2016.csv"])
