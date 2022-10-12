import pandas as pd
import datetime as dt
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
    if end == None:
        today = dt.datetime.today()
        end = today.strftime("%Y-%m-%d")
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    conn = sqlite3.connect('stocks_database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS stocks_data (Date)')
    conn.commit()
    dates_in_db = pd.read_sql("SELECT Date FROM stocks_data", conn)
    if dates_in_db.empty:
        print('[INFO]: The database is empty! Downloading data...')
        yf.pdr_override()
        ohlc = yf.download(tickers, start=start, end=end)
        df = pd.DataFrame(columns=['Adj Close'])
        price = ohlc['Adj Close']
        #if nan_interpolation:
        #    price = price.interpolate(method ='linear', limit_direction ='both')
        price.to_sql('stocks_data', conn, if_exists='replace', index = True)
        c.execute("""SELECT * FROM stocks_data""")
        price_df = pd.DataFrame(c.fetchall(), columns=['Date'] + tickers)
        price_df['Date'] = pd.to_datetime(price_df.Date, format="%Y-%m-%d")
    else:
        min_date = dt.datetime.strptime(pd.read_sql("SELECT * FROM stocks_data WHERE Date = (SELECT min(Date) FROM stocks_data)", conn).values[0][0].split()[0], "%Y-%m-%d").date()
        max_date = dt.datetime.strptime(pd.read_sql("SELECT * FROM stocks_data WHERE Date = (SELECT max(Date) FROM stocks_data)", conn).values[0][0].split()[0], "%Y-%m-%d").date()
        if start + dt.timedelta(days=1) < min_date or end - dt.timedelta(days=1) > max_date:
            print('[INFO]: The period you require was not available yet! Downloading data...')
            yf.pdr_override()
            ohlc = yf.download(tickers, start=start, end=end)
            df = pd.DataFrame(columns=['Adj Close'])
            price = ohlc['Adj Close']
            price.to_sql('stocks_data', conn, if_exists='replace', index = True)
            c.execute("""SELECT * FROM stocks_data""")
            price_df = pd.DataFrame(c.fetchall(), columns=['Date'] + tickers)
            price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date
        else:
            c.execute("""SELECT * FROM stocks_data""")
            price_df = pd.DataFrame(c.fetchall(), columns=['Date'] + tickers)
            price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date
    return price_df.set_index('Date')

print(get_stocks(['ITSA4.SA', 'WEGE3.SA'], '2022-05-01'))