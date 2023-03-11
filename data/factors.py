import pandas as pd

def get_ff_factors(start_date):
    """
    This function retrieves Fama-French 5-factor data from the Ken French Data Library website,
    starting from a selected date, and returns a pandas dataframe with the data.
    
    Parameters:
        - start_date: string, in the format 'YYYY-MM-DD', representing the start date for the data.
        
    Returns:
        - df: pandas dataframe with the Fama-French 5-factor data.
    """
    # Construct the URL for the Fama-French 5-factor data.
    #url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip'
    # Construct the URL for the Fama-French 5-factor data.
    url = 'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip'
    
    df = pd.read_csv(url, sep=',', skiprows=3, index_col=0)
    df.index = pd.to_datetime(df.index, format="%Y%m%d").strftime("%Y-%m-%d")

    # Filter the dataframe to include only the data starting from the given date.
    df = df[df.index >= start_date]

    # Return the resulting dataframe.
    return df
