import numpy as np
import pandas as pd
from sklearn import linear_model

class LinearModel():
    def __init__(self,):
        pass
    
    def _regularize_dataframe(df1, df2):
        """Function that forces the two dataframes to have the same lenght

        Parameters
        ----------
            df1 : pandas.Dataframe
                The first dataframe
            df2 : pandas.Dataframe
                The second fataframe
        
        Returns
        -------
            df1 : pandas.Dataframe
                A the first regularized dataframe
            df2 : pandas.Dataframe
                A the second regularized dataframe
        """
        _df1_cols = df1.columns.tolist()
        _df2_cols = df2.columns.tolist()
        _temp_df = pd.concat([df1, df2], axis=1,  join="inner")
        df1 = _temp_df[_df1_cols]
        df2 = _temp_df[_df2_cols]
        return df1, df2

    def multifactor_model(returns, factors, X_p):
        """ multifactor model"""
        
        tickers = returns.columns.values.tolist()
        results = {ticker:{'prediction':None,
                        'coefs':None,
                        'score':None} for ticker in tickers}
        lm = linear_model.LinearRegression(fit_intercept=True)
        for ticker in tickers:
            X = factors
            Y = returns[ticker]
            model = lm.fit(X.values,Y)
            results[ticker]['prediction'] = lm.predict(X_p)[0]
            results[ticker]['coefs'] = np.insert(lm.coef_, 0, lm.intercept_)
            results[ticker]['score'] = lm.score(X.values, Y)

        return results