import numpy as np
import pandas as pd
from sklearn import linear_model

def _regularize_dataframe(df1, df2):
    """Function that forces the two dataframes to have the same lenght

    Parameters
    ----------
        df1 : pandas.DataFrame
            The first dataframe
        df2 : pandas.DataFrame
            The second fataframe
    
    Returns
    -------
        df1 : pandas.DataFrame
            A the first regularized dataframe
        df2 : pandas.DataFrame
            A the second regularized dataframe
    """
    _df1_cols = df1.columns.tolist()
    _df2_cols = df2.columns.tolist()
    _temp_df = pd.concat([df1, df2], axis=1,  join="inner")
    df1 = _temp_df[_df1_cols]
    df2 = _temp_df[_df2_cols]
    return df1, df2

class linearModel:
    def __init__(self, returns, factors):
        self.returns, self.factors = _regularize_dataframe(returns, factors)
        self.tickers = self.returns.columns.values.tolist()
    
    def complete(self, X_p):
        self.X_p = X_p
        self.results = {ticker:{'prediction':None,
                        'coefs':None,
                        'score':None} for ticker in self.tickers}
        self._model = linear_model.LinearRegression(fit_intercept=True)
        for ticker in self.tickers:
            X = self.factors
            Y = self.returns[ticker]
            lm = self._model.fit(X.values,Y)
            self.results[ticker]['prediction'] = lm.predict(self.X_p)[0]
            self.results[ticker]['coefs'] = np.insert(lm.coef_, 0, lm.intercept_)
            self.results[ticker]['score'] = lm.score(X.values, Y)
        return self.results

    def predict(self, X_p):
        self.X_p = X_p
        return {ticker:self.results[ticker]['prediction'] for ticker in self.tickers}

    def coefs(self):
        return {ticker:self.results[ticker]['coefs'] for ticker in self.tickers}

    def scores(self):
        return {ticker:self.results[ticker]['scores'] for ticker in self.tickers}