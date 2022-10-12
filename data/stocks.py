import pandas as pd
import datetime as dt
import yfinance as yf
import sqlite3
import datetime as dt
import holidays
import numpy as np

ONE_DAY = dt.timedelta(days=1)
HOLIDAYS_US = holidays.US()

def _next_business_day(date):
    next_day = dt.datetime.strptime(str(date), "%Y-%m-%d").date() + ONE_DAY
    while next_day.weekday() in holidays.WEEKEND or next_day in HOLIDAYS_US:
        next_day += ONE_DAY
    return next_day

def _last_business_day(date):
    last_day = dt.datetime.strptime(str(date), "%Y-%m-%d").date() - ONE_DAY
    while last_day.weekday() in holidays.WEEKEND or last_day in HOLIDAYS_US:
        last_day -= ONE_DAY
    return last_day

def _contains(lst1, lst2):
    for item in lst1:
        if item not in lst2:
            return False
    return True

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
    def _update_db(tickers, start, end):
        try:
            conn = sqlite3.connect('stocks_database')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS stocks_data (Date)')
            conn.commit()
            yf.pdr_override()
            ohlc = yf.download(tickers, start=start, end=end)
            price = ohlc['Adj Close']
            if len(tickers) == 1:
                price = price.to_frame()
                price.rename(columns = {price.columns.values[0]:tickers[0]}, inplace = True)
            price.to_sql(name='stocks_data', con=conn, if_exists='replace', index = True)
            conn.commit()
            c.execute("""SELECT * FROM stocks_data""")
            price_df = pd.DataFrame.from_records(c.fetchall(), columns=[desc[0] for desc in c.description])
            price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date
            c.close()
            return price_df.set_index('Date')[tickers]
        except sqlite3.Error as error:
            print("[INFO]: Failed to read data from sqlite table", error)

        finally:
            if conn:
                conn.close()

    if end == None:
        today = dt.datetime.today()
        end = today.strftime("%Y-%m-%d")
    start = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    if not bool(len(pd.bdate_range(start, start))):
        start = _next_business_day(start)
        print(f'[INFO]: The "start" date you chose is a holiday, so we are adopting the next business day, which is "{start}"')
    if not bool(len(pd.bdate_range(end, end))):
        end = _last_business_day(end)
        print(f'[INFO]: The "end" date you chose is a holiday, so we are adopting the last business day, which is "{end}"')
    try:
        conn = sqlite3.connect('stocks_database')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS stocks_data (Date)')
        conn.commit()
        dates_in_db = pd.read_sql("SELECT Date FROM stocks_data", conn)
        if dates_in_db.empty:
            print('[INFO]: The database is empty! Downloading data...')
            price_df = _update_db(tickers, start, end)
        else:
            min_date = dt.datetime.strptime(pd.read_sql("SELECT * FROM stocks_data WHERE Date = (SELECT min(Date) FROM stocks_data)", conn).values[0][0].split()[0], "%Y-%m-%d").date()
            max_date = dt.datetime.strptime(pd.read_sql("SELECT * FROM stocks_data WHERE Date = (SELECT max(Date) FROM stocks_data)", conn).values[0][0].split()[0], "%Y-%m-%d").date()
            if start < min_date or end > max_date + dt.timedelta(days=1):
                print('[INFO]: The period you require was not available yet! Downloading data...')
                price_df = _update_db(tickers, start, end)
            else:
                c = conn.execute("""SELECT * FROM stocks_data""")
                tickers_in_db = [d[0] for d in c.description]
                if not _contains(tickers, tickers_in_db):
                    print('[INFO]: The ticker you require was not available yet! Downloading data...')
                    price_df = _update_db(tickers, start, end)
                else:
                    print(['Date'] + tickers)
                    price_df = pd.DataFrame.from_records(c.fetchall(), columns=[desc[0] for desc in c.description])
                    price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date
                    price_df = price_df.set_index('Date')
        conn.close()
    except sqlite3.Error as error:
            print("[INFO]: Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("[INFO]: The SQLite connection is closed")

    return price_df[tickers]

print(get_stocks(['WEGE3.SA', 'ITSA4.SA'], '2022-10-01', '2022-10-12'))