import numpy as np
import pandas as pd
from sklearn import linear_model
import stats
from data.data_tools import *

class linearModel:
    def __init__(self, returns, factors):
        self.returns, self.factors = regularize_dataframe(returns, factors)
        self.tickers = self.returns.columns.values.tolist()

    def complete(self, X_p):
        """Get all the complete analysis for a linear models. Including the coefi-
        cients, the score and the prediction for each ticker

        Parameters
        ----------
            X_p : list[list]
                The list of the prediction of the factors
        
        Returns
        -------
            dict
                A dictionary containing the coeficicients of the multivariate
                linear regression, the score and the prediction for each given
                ticker
        """
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
        """The prediction for each ticker based on the multivariate linear re-
        gression fitted using all the given factors


        Parameters
        ----------
            X_p : list[list]
                The list of the prediction of the factors
        
        Returns
        -------
            dict
                A dictionary containing the predicion of each ticker based on
                the prediction of the factors
        """
        self.X_p = X_p
        self.predictions = {ticker:{'prediction':None} for ticker in self.tickers}
        self._model = linear_model.LinearRegression(fit_intercept=True)
        X = self.factors
        for ticker in self.tickers:
            Y = self.returns[ticker]
            lm = self._model.fit(X.values,Y)
            self.predictions[ticker]['prediction'] = lm.predict(self.X_p)[0]
        return self.predictions

    def coefs(self):
        """The coefficients of the multivariate linear regression
        
        Parameters
        ----------
            None

        Returns
        -------
            dict
                A dictionary containing the coefficients of the multivariate 
                linear regression fitted
        """
        self.coefs = {ticker:{'coef':None} for ticker in self.tickers}
        self._model = linear_model.LinearRegression(fit_intercept=True)
        X = self.factors
        for ticker in self.tickers:
            Y = self.returns[ticker]
            lm = self._model.fit(X.values,Y)
            self.coefs[ticker]['coef'] = np.insert(lm.coef_, 0, lm.intercept_)
        return self.coefs

    def coefs_ci(self, X_p, n_boot=1000, ci=0.95):
        """The confidence interval of coefficients of the multivariate linear 
        regression using the boostrapping method
        
        Parameters
        ----------
            X_p : list[list]
                The list of the prediction of the factors

            n_boot : int, optional
                Number of the resamples the algorithm is going to perform the
                bootstrap method
            ci : float, optional
                Confidence interval

        Returns
        -------
            dict
                A dictionary containing the coefficients of the multivariate 
                linear regression fitted, the score, the predicition of the 
                coefficients for each ticker"""


        tickers = self.returns.columns.values.tolist()
        results = {ticker:{'prediction':None,
                        'ci_coefs':None,
                        'score':None} for ticker in tickers}
        lm = linear_model.LinearRegression(fit_intercept=True)
        ci_coefs = []
        ci_intercepts = []
        for ticker in tickers:
            X = self.factors
            Y = self.returns[ticker]
            model = lm.fit(X.values,Y)
            prediction = lm.predict(X_p)
            coefs = lm.coef_
            intercept = lm.intercept_
            score = lm.score(X.values, Y)
            results[ticker]['prediction'] = prediction[0]
            results[ticker]['score'] = score
            E = [Y[i] - lm.predict([x])[0] for i, x in enumerate(X.values.tolist())]
            dict_boot = {'ticker':ticker}
            for i in range(len(self.factors.columns)+1):
                dict_boot['B'+str(i)] = []
            for b in range(n_boot):
                E_b = gen_resamples(E)[0]
                Y_b = [lm.predict([x]) + E_b[i] for i, x in enumerate(X.values.tolist())]
                lm_ = linear_model.LinearRegression(fit_intercept=True)
                model_ = lm_.fit(X.values, Y_b)
                dict_boot['B0'].append(lm_.intercept_[0])
                for i, Bi in enumerate(lm_.coef_[0].tolist()):
                    dict_boot['B'+str(i+1)].append(Bi)
            for coef in list(dict_boot.keys())[-(len(self.factors.columns)+1):]:
                coef_ci = confidence_interval(dict_boot[coef], confidence=ci)
                dict_boot[coef] = coef_ci
            results[ticker]['ci_coefs'] = {factor : dict_boot[factor] for factor in list(dict_boot.keys())[-(len(self.factors.columns)+1):]}

        return results

    def scores(self):
        """The score of the multivariate linear regression
        
        Parameters
        ----------
            None

        Returns
        -------
            dict
                A dictionary containing the scores of the multivariate linear 
                regression fitted
        """
        self.scores = {ticker:{'score':None} for ticker in self.tickers}
        self._model = linear_model.LinearRegression(fit_intercept=True)
        X = self.factors
        for ticker in self.tickers:
            Y = self.returns[ticker]
            lm = self._model.fit(X.values,Y)
            self.scores[ticker]['score'] = lm.score(X.values, Y)
        return self.scores