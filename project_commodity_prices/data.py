import yfinance as yf
import numpy as np
from random import randint
import pandas as pd

def get_data(online=False,market='ZS=F'):
    '''Get commodity stock history price from 2000-09-15 to 2022-01-28.
    Soy Bean ticker: ZS=F
    Soy Meal ticker: ZM=F
    Soy Oil ticker: ZL=F'''

    if online==False:
        dataframe = pd.read_csv('raw_data/soybean_daily_price.csv')
        return dataframe
    else:
        # get desired commodity stock
        zsf = yf.Ticker(market)
        # get stock info
        zsf.info
        # get historical market data
        df = zsf.history(start = '2000-09-15', end='2022-03-22')
        df = df.drop(columns=['Dividends','Stock Splits'])
        df = df.reset_index(level=0)
        return df


def subsample_sequence(df, length = 253):
    """
    Given the initial dataframe `df`, return a shorter dataframe sequence of length `length`.
    This shorter sequence should be selected at random
    """
    value = abs(randint(0, len(df) - 2*length))
    df_sample = df[value:length+value]
    return df_sample


def split_subsample_sequence(df, length=253):
    '''Create one single random (X,y) pair'''
    df_subsample = subsample_sequence(df, length)
    y_samples_index = []
    for step in range(0,length,22):
        # Pega os 12 próximos index (mês)
        index_passado = df_subsample.index[-1] + step
        y_samples_index.append(index_passado)
    # Pega os 12 valores de fechamento referentes aqueles index
    y_sample = df['Close'].to_numpy()[y_samples_index]
    X_sample = df_subsample[0:length -1]
    X_sample = X_sample.values
    return np.array(X_sample), np.array(y_sample)


def get_X_y(df, n_sequences=100, length=253):
    '''Return a list of samples (X, y)'''
    X, y = [], []
    for i in range(n_sequences):
        (xi, yi) = split_subsample_sequence(df, length)
        X.append(xi)
        y.append(yi)
    X = np.array(X)
    y = np.array(y)
    return X, y


def get_train_test_df(df):
    '''Return X and y for train and test data frames'''
    # Separar o dataframe em teste e treino
    len_ = int(0.8*df.shape[0])
    df_train = df[:len_]
    df_test = df[len_:]
    df_test.reset_index(drop = True, inplace = True)
    X_train, y_train = get_X_y(df_train, 100, 253)
    X_test, y_test = get_X_y(df_test, 100, 253)
    X_train=np.asarray(X_train[:,:,1:]).astype(np.float32)
    X_test=np.asarray(X_test[:,:,1:]).astype(np.float32)
    return X_train, y_train, X_test, y_test

if __name__ == '__main__':
    # Get initial data frame
    df = get_data()
    # Get X_train, y_train, X_test and y_test data frames
    X_train, y_train, X_test, y_test = get_train_test_df(df)
