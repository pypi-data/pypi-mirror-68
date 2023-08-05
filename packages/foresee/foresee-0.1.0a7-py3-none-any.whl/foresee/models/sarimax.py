"""
sarimax from statsmodels
"""

import numpy as np
import pandas as pd
import statsmodels.api

# local module
from foresee.models import models_util

def sarimax_fit_forecast(ts, fcst_len):
    
    try:
        
        sarimax_model = statsmodels.api.tsa.statespace.SARIMAX(
                                                                    endog = ts,
                                                                    enforce_stationarity = False,
                                                                    enforce_invertibility = False,
                                                               ).fit()
        
        sarimax_fittedvalues = sarimax_model.fittedvalues
        sarimax_forecast = sarimax_model.predict(
                                                    start = len(ts),
                                                    end = len(ts) + fcst_len - 1,
                                                 )
        err = None
        
    except Exception as e:
        
        sarimax_model = None
        sarimax_fittedvalues = None
        sarimax_forecast = None
        err = str(e)
        
    return sarimax_fittedvalues, sarimax_forecast, err


def fit_sarimax(data_dict, freq, fcst_len, model_params, run_type, epsilon):
    
    model = 'sarimax'
    sarimax_params = model_params[model]
    
    complete_fact = data_dict['complete_fact']
    
    # dataframe to hold fitted values
    fitted_fact = pd.DataFrame()
    fitted_fact['y'] = complete_fact['y']
    fitted_fact['data_split'] = complete_fact['data_split']
    
    # dataframe to hold forecast values
    forecast_fact = pd.DataFrame()
    forecast_fact['y'] = np.full(fcst_len, 0)
    forecast_fact['data_split'] = np.full(fcst_len, 'Forecast')
    
    fit_fcst_fact = pd.concat([fitted_fact, forecast_fact], ignore_index=True)
    
    sarimax_wfa = None
    
    sarimax_fitted_values, sarimax_forecast, err = sarimax_fit_forecast(
                                                                            ts = complete_fact['y'],
                                                                            fcst_len = fcst_len,
                                                                        )
    
    
    if run_type in ['best_model', 'all_best']:
        
        train_fact = data_dict['train_fact']
        test_fact = data_dict['test_fact']
        
        fitted_values, forecast, err = sarimax_fit_forecast(
                                                            ts = train_fact['y'],
                                                            fcst_len = len(test_fact) ,
                                                        )
        
        if err is None:
            sarimax_wfa = models_util.compute_wfa(
                                    y = test_fact['y'].values,
                                    yhat = forecast.values,
                                    epsilon = epsilon,
                                )
            sarimax_fitted_values = fitted_values.append(forecast, ignore_index=True)
            
        else:
            sarimax_wfa = -1
            
    if err is None:
        fit_fcst_fact['sarimax_forecast'] = sarimax_fitted_values.append(sarimax_forecast).values
        fit_fcst_fact['sarimax_wfa'] = sarimax_wfa
        
    else:
        fit_fcst_fact['sarimax_forecast'] = 0
        fit_fcst_fact['sarimax_wfa'] = -1
        
            
    return fit_fcst_fact, sarimax_wfa, err


