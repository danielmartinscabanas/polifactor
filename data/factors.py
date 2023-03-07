from ast import Bytes
from genericpath import isfile
import pandas as pd
import numpy as np
from sklearn import linear_model
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
import yfinance as yf
import requests
from bs4 import BeautifulSoup as bs
import zipfile
from io import BytesIO
import os


def clean_directory():
  if os.path.isfile('factors.csv'):
    os.remove('factors.csv')
  if os.path.isfile('F-F_Research_Data_5_Factors_2x3_daily.CSV'):
    os.remove('F-F_Research_Data_5_Factors_2x3_daily.CSV')

def get_factors(factors, start, end=None, nan_interpolation=False):
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
    #Remove os arquivos dos fatores que podem ter ficado do último uso
    clean_directory()

    #Baixa o arquivo contendo os dados dos fatores
    file_url = ('https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip')
    req = requests.get(file_url)
    zipfile = zipfile.ZipFile(BytesIO(req.content))
    zipfile.extractall()

    #Formata o arquivo
    a_file = open("F-F_Research_Data_5_Factors_2x3_daily.csv", "r")
    lines = a_file.readlines()
    a_file.close()

    del lines[0:4]

    new_file = open("factors.csv", "w+")
    new_file.write('Date,Mkt-RF,SMB,HML,RMW,CMA,RF \n')
    for line in lines:
        new_file.write(line)
    new_file.close()

    #Preparação do dataframe dos fatores
    factors = pd.read_csv('factors.csv', delimiter=',' )
    factors = factors.loc[factors['Date'] >= 20150502]
    if nan_interpolation:
      factors = factors.interpolate(method ='linear', limit_direction ='both')
    else:
      factors = factors.dropna()
      
    return factors