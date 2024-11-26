import pandas as pd
import numpy as np

def get_tables(path):
    tables = pd.read_html(path)
    return tables

def get_date(x):
    if len(x) == 19:
        return x.split(' ')[0]
    return np.nan
def get_time(x):
    if len(x) == 19:
        return x.split(' ')[1]
    return x

def get_minutes(x):
    return int(pd.Timedelta(x).total_seconds()/60)

def handle_time(df,col,drop=True):
    df['Date'] = df[col].apply(get_date)
    df['Date'] = df['Date'].ffill()
    df['Time'] = df[col].apply(get_time)
    df[col] = pd.to_datetime(df['Date']+' '+df['Time'], format='%Y-%m-%d %H:%M:%S')
    if drop:
        df.drop(['Date','Time'],axis=1,inplace=True)
        
def handle_duration(df,col):
    df[col] = df[col].apply(get_minutes)

def remove_percent(df,col):
    df[col] = df[col].str.replace(' %','').astype(float)

def remove_mwh(df, col):
    df[col] = df[col].str.replace(',', '').str.replace(' mWh', '').astype(float)