
import pandas as pd
from datetime import date
import yfinance as yf

def get_stocks(tickers, start, end=None, nan_interpolation=False, returns=False):
    """Returns the price or the return of stocks from Yahoo Finance

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
        returns : bool, optional
            Decide if the function is going to return the returns or the price
            of the stock (default is False)

    Returns
    -------
        pandas.Dataframe
            A dataframe with the dates and the adjusted close prices of the 
            given stock tickers
    """
    yf.pdr_override()
    if end == None:
        today = date.today()
        end = today.strftime("%Y-%m-%d")
    ohlc = yf.download(tickers, start=start, end=end)
    df = pd.DataFrame(columns=['Adj Close'])
    price = ohlc['Adj Close']
    if nan_interpolation:
        price = price.interpolate(method ='linear', limit_direction ='both')
    if returns:
        returns = price/price.shift(1) - 1
        return returns.dropna()
    else:
        return price