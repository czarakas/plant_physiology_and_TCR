"""
Define CO2 concentrations for time series
"""
import numpy as np

def define_co2_concentrations(len_time=200):
    """ Creates time series of CO2 concentrations of given length time"""
    co2_start = 284.31
    co2_1pctco2 = np.zeros([len_time, 1])
    co2_1pctco2[0] = co2_start
    for i in np.arange(1, len_time):
        co2_1pctco2[i] = 1.01*co2_1pctco2[i-1]
    return co2_1pctco2

co2_1pctco2 = define_co2_concentrations()
co2_double = co2_1pctco2[70]
co2_startAvg = co2_1pctco2[60]
co2_endAvg = co2_1pctco2[80]
