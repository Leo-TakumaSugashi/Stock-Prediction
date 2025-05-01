#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 2024
@author: leo Takuma SUGASHI

"""
#pip install alpha-vantage
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
ts = TimeSeries(key='H6RTR49ALCDO3XSA', output_format='pandas')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL',interval='60min', outputsize='full')
print(meta_data)
