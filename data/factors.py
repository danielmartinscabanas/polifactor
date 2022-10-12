import pandas as pd
from sklearn import linear_model
import datetime as dt
from datetime import datetime
import yfinance as yf
import pandas_datareader.data as reader
import sqlite3


def get_stocks(factors, start, end=None, nan_interpolation=False):
    """Returns the factors values
    Parameters
    ----------
        factors : list[str]
            List of the factors you want to get the price for
        start : str
            The date you want to start retrieving data following the datetime 
            library format ('YYYY-MM-DD')
        end : str, optional
            The date you want to end retrieving data following the datetime 
            library format ('YYYY-MM-DD') (the default is None, which implies 
            the algorithm is going to get the actual date as end)
        nan_interpolation : bool, optional
            Interpolate missing factor values with adjacent values
            (default is False)

    Returns
    -------
        pandas.Dataframe
            A dataframe with the values of the desired factors
    """
nan_interpolation = False

start = dt.date(2015,5,5)
factors = reader.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench', start)

factors = factors[0]

if nan_interpolation:
  factors = factors.interpolate(method ='linear', limit_direction ='both')
else:
  factors = factors.dropna()

factors = factors/100

# Stablish connections with sqlite3
conn = sqlite3.connect('factors_data')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS factors (Date, SMB, HML, RMW, CMA, RF)')
conn.commit()

# Upload dataset to sql
factors.to_sql('factors_data', conn, if_exists='replace', index = True)
#cursor.execute("SELECT * FROM factors_database")

# Extract sql data
factors = pd.read_sql("SELECT * FROM factors_data", conn)
factors["Date"] = pd.to_datetime(factors.Date, format="%Y-%m-%d")
factors = factors.set_index("Date")

# Em produção, pegar data mínima / máxima
# data = pd.read_sql("SELECT * FROM factors_data WHERE Date = (SELECT min(Date) FROM factors_data)", conn)
# print(data.values[0][0])
# data = pd.to_datetime(data["Date"])
# print(data)


parameters = {
                'tickers': ['MSFT', 'GOGL'],
                'start': '2015-5-2',
                'end' : '2022-6-30',
                'nan_interpolation': False
              }

def get_prices(tickers, start, end, nan_interpolation):
  yf.pdr_override()
  ohlc = yf.download(tickers, start, end)
  df = pd.DataFrame(columns = ['Adj Close'])
  df = ohlc['Adj Close']
  if nan_interpolation:
    df = df.interpolate(method ='linear', limit_direction ='both')
  return df

original_df = get_prices(**parameters) 
returns = original_df/original_df.shift(1) - 1
returns.dropna(inplace=True)

def regularize_dataframe(df1, df2):
  _df1_cols = df1.columns.tolist()
  _df2_cols = df2.columns.tolist()
  _temp_df = pd.concat([df1,df2], axis=1, join='inner')
  df1 = _temp_df[_df1_cols[1:]]
  df2 = _temp_df[_df2_cols]
  return df1, df2
factors, returns = regularize_dataframe(factors, returns)

def multifactor_model(returns, factors, X_p):
    tickers = returns.columns.values.tolist()
    results = {ticker:{'prediction':None,
                       'coefs':None,
                       'intercept':None,
                       'scores':None} for ticker in tickers}
    lm = linear_model.LinearRegression(fit_intercept=True)
    for ticker in tickers:
        X = factors
        Y = returns[ticker]
        model = lm.fit(X.values,Y)
        results[ticker]['prediction'] = lm.predict(X_p)
        results[ticker]['coefs'] = lm.coef_
        results[ticker]['intercept'] = lm.intercept_
        results[ticker]['score'] = lm.score(X.values, Y)

    return results