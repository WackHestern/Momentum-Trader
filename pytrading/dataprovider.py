# -*- coding: utf-8 -*-
# TODO: Find a better name for this module
from alpha_vantage.timeseries import TimeSeries

def load(symbol):
    # TODO: Improve Error Handling
    ts = TimeSeries(key='5UQ13GR7ST5S6ZKB', output_format = 'pandas')
    try:
        data, meta_data = ts.get_daily_adjusted(symbol, outputsize='compact') 
    except:
        raise ValueError('Symbol not found!')

    if data is None:
        raise ValueError('No data found! Could be a wrong provider.')
    return data 
def loadCurrentValue(symbol):
    ts = TimeSeries(key='5UQ13GR7ST5S6ZKB', output_format = 'json')
    try:
        data, meta_data = ts.get_intraday(symbol, interval='1min', outputsize='compact') 
    except:
        raise ValueError('Symbol not found!')

    if data is None:
        raise ValueError('No data found! Could be a wrong provider.')
    if ("16:00:00" not in meta_data['3. Last Refreshed']):
        raise ValueError("Not refreshed on closing!")
    return data[meta_data['3. Last Refreshed']]['4. close']

