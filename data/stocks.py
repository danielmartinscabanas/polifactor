import pandas as pd
from datetime import date
import yfinance as yf
import sqlite3
import datetime as dt

def get_stocks(tickers, start, end=None, nan_interpolation=False):
    """The price of stocks from Yahoo Finance

    Parameters
    ----------
        tickers : list[str]
            List of the ticker's stocks you want to get the price
        start : str
            The date you want to start retrieving data following the datetime 
            library format ('YYYY-MM-DD')
        end : str, optional
            The date you want to end retrieving data following the datetime 
            library format ('YYYY-MM-DD') (the default is None, which implies 
            the algorithm is going to get the actual date as end)
        nan_interpolation : bool, optional
            Proceed a both side linear interpolation of the missing data 
            (default is False)

    Price
    -------
        pandas.Dataframe
            A dataframe with the dates and the adjusted close prices of the 
            given stock tickers
    """
    conn = sqlite3.connect('stocks_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stocks_data (date)')
    conn.commit()
    dates_in_db = pd.read_sql("SELECT Date FROM stocks_data", conn)
    dates_in_db = pd.to_datetime(dates_in_db['Date'], format="%Y-%m-%d")
    min_date = 
    max_date = 
    missing_date = pd.concat([dates_in_db, ], axis=1,  join="outer")

    yf.pdr_override()
    if end == None:
        today = date.today()
        end = today.strftime("%Y-%m-%d")
    ohlc = yf.download(tickers, start=start, end=end)
    df = pd.DataFrame(columns=['Adj Close'])
    price = ohlc['Adj Close']
    if nan_interpolation:
        price = price.interpolate(method ='linear', limit_direction ='both')
    price.to_sql('stocks_data', conn, if_exists='replace', index = True)
    c.execute("""SELECT * FROM stocks_data""")
    price_df = pd.DataFrame(c.fetchall(), columns=['Date'] + tickers)
    price_df['Date'] = pd.to_datetime(price_df.Date, format="%Y-%m-%d")
    return price_df.set_index('Date')

#print(get_stocks(['ITSA4.SA', 'WEGE3.SA'], '2022-05-01'))