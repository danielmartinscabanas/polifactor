import numpy as np
import pandas as pd
import stats
from scipy.stats import norm
import matplotlib.pyplot as plt

def regularize_dataframe(df1, df2, nan_interpolation=True):
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

    if not df2.empty:
        if nan_interpolation:
            df1 = df1.interpolate(method ='linear', limit_direction ='both')
            df2 = df2.interpolate(method ='linear', limit_direction ='both')
        else:
            df1.dropna(inplace=True)
            df2.dropna(inplace=True)
        _df1_cols = df1.columns.tolist()
        _df2_cols = df2.columns.tolist()
        _temp_df = pd.concat([df1,df2], axis=1, join='inner')
        df1 = _temp_df[_df1_cols[1:]]
        df2 = _temp_df[_df2_cols]
        return df1, df2
    else:
        if nan_interpolation:
            df1 = df1.interpolate(method ='linear', limit_direction ='both')
        else:
            df1.dropna(inplace=True)
        return df1

def gen_resamples(sample, replicates=1):
    """Generate random resamples of the given sample
    
    Parameters
    ----------
        sample : list, pandas.Series, pandas.Dataframe, numpy.ndarray
            Data you want to randomly resample
        replicates : int, optional
            The number of random resamples you want to replicate (default is 
            one)

    Returns
    -------
        list[list[Any]]
            The data randomly resampled
    
    """
    if not isinstance(sample, list):
        if isinstance(sample, pd.Series):
            sample = sample.tolist()
        elif isinstance(sample, np.ndarray):
            sample = sample.tolist()
        else:
            sample = sample.iloc[:, 0].values.tolist()

    _len_sample = len(sample)
    rand_idxs = np.random.randint(_len_sample, size = (replicates, _len_sample))
    resampled_sample = []
    for lst in rand_idxs:
        _resample = []
        for i in lst:
            _resample.append(sample[i])
        resampled_sample.append(_resample)

    return resampled_sample

def confidence_interval(sample, confidence=0.95):
    """Function that returns the confidence interval for any kind of that, even
    if its required to use non-parametric methods

    Parameters
    ----------
        sample : list, pandas.Series, pandas.Dataframe, numpy.ndarray
            The sample you want to estimate the confidence interval
        confidence : float, optional
            The confidence you require for the calculus of the confidence
            interval (default is 0.95)

    Returns
    -------
        tuple
            Three values in a tuple, where the first value is the lower limit,
            the center value is the average of the sample, and the top value is 
            the upper limit
    
    """
    if not isinstance(sample, list):
        if isinstance(sample, pd.Series):
            sample = sample.tolist()
        elif isinstance(sample, np.ndarray):
            sample = sample.tolist()
        else:
            sample = sample.iloc[:, 0].values.tolist()

    shapiro_test = stats.shapiro(sample)
    # When its a normal series
    if shapiro_test[1] > 0.05:
        a = 1.0 * np.array(sample)
        n = len(a)
        m, se = np.mean(a), stats.sem(a)
        h = se * stats.t.ppf((1 + confidence) / 2., n-1)
        return m-h, m, m+h
    # When the sample is not normal we are going to use a non-parametric method
    # to find the confidence interval 
    else:
        _len_sample = len(sample)
        sorted_sample = sample.sort()
        lower = sample[round(_len_sample*((1-confidence)/2))-1]
        average = sum(sample)/_len_sample
        upper = sample[round(_len_sample*(confidence + (1-confidence)/2))-1]
        return lower, average, upper

def plot_normal(sample):
    """Function that plot the histogram of the sample and the normal distribution
adjusted 

    Parameters
    ----------
        sample : list, pandas.Series, pandas.Dataframe, numpy.ndarray
            The sample you want to plot

    Returns
    -------
        None
    """

    """if not isinstance(sample, pd.DataFrame):
        sample = pd.Series(sample).to_frame().to_numpy()"""
    mu, std = norm.fit(sample)

    if not isinstance(sample, np.ndarray):
        if isinstance(sample, pd.Series):
            sample = sample.to_numpy()
        elif isinstance(sample, list):
            sample = np.array(sample)
        else:
            sample = sample.iloc[:, 0].values.to_numpy()
    mu, std = norm.fit(sample)

    # Plotting the Histogram
    plt.hist(sample, bins=35, density=True)

    # Plotting the CDF
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    plt.plot(x, p, 'k', linewidth=2, color='red')
    # Verifying if the sample is normal by Shapiro Wilk's test
    shapiro_test = stats.shapiro(sample)
    if shapiro_test[1] > 0.05:
        title = f'A série (x̄={round(mu*100, 2)}%, s={round(std*100, 2)}%) é normal com {round(shapiro_test[0]*100, 2)}% de significância'
    else:
        title = f'A série (x̄={round(mu*100, 2)}%, s={round(std*100, 2)}%) não é normal com {round(shapiro_test[0]*100, 2)}% de significância'
    plt.title(title)

    plt.show()

def pretty_print_dict(d, indent=0):
    """Just a fucntion to print dictionaries more beautifully
    Parameters
    ----------
        d : dict
            A dictionary you want to print
    
    Returns
    -------
        None
    """
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print_dict(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))