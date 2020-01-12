"""
Finance API comparisons.
Different API's sampled:
    -Alpha Vantage
    -Quandl
"""

from alpha_vantage.timeseries import TimeSeries
import quandl
import matplotlib.pyplot as plt

alpha_vantage_api_key = "YOUR API KEY HERE"
quandl_api_key = "YOUR API KEY HERE"

def pull_intraday_time_series_alpha_vantage(alpha_vantage_api_key, ticker_name, data_interval = '15min'):
    """
    Pull intraday time series data by stock ticker name.
    Args:
        alpha_vantage_api_key: Str. Alpha Vantage API key.
        ticker_name: Str. Ticker name that we want to pull.
        data_interval: String. Desired data interval for the data. Can be '1min', '5min', '15min', '30min', '60min'.
    Outputs:
        data: Dataframe. Time series data, including open, high, low, close, and datetime values.
        metadata: Dataframe. Metadata associated with the time series.   
    """
    #Generate Alpha Vantage time series object
    ts = TimeSeries(key = alpha_vantage_api_key, output_format = 'pandas')
    #Retrieve the data for the past sixty days (outputsize = full)
    data, meta_data = ts.get_intraday(ticker_name, outputsize = 'full', interval= data_interval)
    data['date_time'] = data.index
    return data, meta_data

def pull_daily_time_series_alpha_vantage(alpha_vantage_api_key, ticker_name, output_size = "compact"):
    """
    Pull daily time series by stock ticker name.
    Args:
        alpha_vantage_api_key: Str. Alpha Vantage API key.
        ticker_name: Str. Ticker name that we want to pull.
        output_size: Str. Can be "full" or "compact". If "compact", then the past 100 days of data
        is returned. If "full" the complete time series is returned (could be 20 years' worth of data!)
    Outputs:
        data: Dataframe. Time series data, including open, high, low, close, and datetime values.
        metadata: Dataframe. Metadata associated with the time series.  
    """
    #Generate Alpha Vantage time series object
    ts = TimeSeries(key = alpha_vantage_api_key, output_format = 'pandas')
    data, meta_data = ts.get_daily_adjusted(ticker_name, outputsize = output_size)
    data['date_time'] = data.index
    return data, meta_data

def plot_data(df, x_variable, y_variable, title):
    """
    Plot the x- and y- variables against each other, where the variables are columns in
    a pandas dataframe
    Args:
        df: Pandas dataframe, containing x_variable and y_variable columns. 
        x_variable: String. Name of x-variable column
        y_variable: String. Name of y-variable column
        title: String. Desired title name in the plot.
    Outputs:
        Plot in the console. 
    """
    fig, ax = plt.subplots()
    ax.plot_date(df[x_variable], 
                 df[y_variable], marker='', linestyle='-', label=y_variable)
    fig.autofmt_xdate()
    plt.title(title)
    plt.show()

if __name__== "__main__":
    #Use the Alpha Vantage API to pull time series data
    #Pull intraday Google Stock Data
    ts_data, ts_metadata = pull_intraday_time_series_alpha_vantage(alpha_vantage_api_key, ticker_name = "GOOGL")
    #Plot the high prices
    plot_data(df = ts_data, 
              x_variable = "date_time", 
              y_variable = "2. high", 
              title ="High Values, Google Stock, 15 Minute Data")
    #Pull daily data for Berkshire Hathaway
    ts_data, ts_metadata = pull_daily_time_series_alpha_vantage(alpha_vantage_api_key, ticker_name = "BRK.B", output_size = "compact") 
    #Plot the high prices
    plot_data(df = ts_data, 
              x_variable = "date_time", 
              y_variable = "2. high", 
              title ="High Values, Berkshire Hathaway Stock, Daily Data")
    
    #Use the Quandl API to pull data
    quandl.ApiConfig.api_key = quandl_api_key
    #Pull GDP Data
    data = quandl.get('FRED/GDP')
    data["date_time"] = data.index
    #Plot the GDP time series
    plot_data(df = data, 
              x_variable = "date_time", 
              y_variable = "Value", 
              title ="Quarterly GDP Data")
    #Pull daily stock closing data
    data = quandl.get_table('WIKI/PRICES', ticker = ['MSFT'])
    plot_data(df = data, 
              x_variable = "date", 
              y_variable = "open", 
              title ="Daily Microsoft Stock Prices, Opening Price")
