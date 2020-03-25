import xarray as xr
import os
import numpy as np
import scipy.stats as stats
import time
import pickle
import matplotlib.pyplot as plt
import copy

from plants_and_TCR.analysis_parameters import params
from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.process_data import reindex_time
from plants_and_TCR.analyze_data import grab_cmip_dataset
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.process_data import regrid_and_process_datafiles
from plants_and_TCR.process_data import area_weighting

CDICT_NAMES = params.CDICT_NAMES
RUNNAME_1PCTCO2='1pctCO2'
DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES
CDICT = pickle.load(open(DIR_CMIP_DICTS+'cmip_dict.pickle', "rb"))
DEFAULT_VARNAME='tas'
modelnames_short = get_CMIP_info.get_modelnames_short('CMIP5and6')
pi_adjustments = get_CMIP_info.get_PI_adjustment('CMIP5and6')
DIR_PI_CONTROL_DATA = directory_information.DIR_DATA+'processed_data/global_avg_data/'

def get_pi_control_nametag(modelname, varname, average_type):
    nametag = modelname+'_'+varname+'_'+average_type
    return nametag

def align_times(modelname):
    model_ind = modelnames_short.index(modelname)
    pi_adjustment = pi_adjustments[model_ind]
    
    #------------------------get datasets------------------------
    ds_1pctCO2_original = grab_cmip_dataset.grab_cmip_dataset(CDICT,
                                                     Mname=modelname,
                                                     Rname=RUNNAME_1PCTCO2,
                                                     Vname=DEFAULT_VARNAME)
    
    ds_pi_original = grab_cmip_dataset.grab_cmip_dataset(CDICT,
                                                Mname=modelname,
                                                Rname='piControl',
                                                Vname=DEFAULT_VARNAME)
    ds_1pctCO2 = copy.deepcopy(ds_1pctCO2_original)
    ds_pi = copy.deepcopy(ds_pi_original)
    
    #----------------- reindex times (and adjust 1pctCO2 year)
    
    newtimes = reindex_time.reindex_time(startingtimes=ds_1pctCO2['time'], yr_adjustment=pi_adjustment)
    ds_1pctCO2['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
    
    newtimes = reindex_time.reindex_time(startingtimes=ds_pi['time'], yr_adjustment=0)
    ds_pi['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
    
    #------------------------take annual averages of datasets
    ds_1pctCO2_annual = ds_1pctCO2.groupby('time.year').mean('time')
    ds_pi_annual = ds_pi.groupby('time.year').mean('time')
    
    #----------------------- find min and max times of 1pctCO2 experiment
    min_year = ds_1pctCO2_annual['year'].values[0]
    max_year = ds_1pctCO2_annual['year'].values[-1]
    
    #----------------------- subset PI control
    ds_pi_annual_subset = ds_pi_annual.sel(year=slice(min_year, max_year))
    
    return ds_pi_annual, ds_1pctCO2_annual, ds_pi_annual_subset

def calculate_linear_trend(ds):
    vals = ds.values
    years = ds['year'].values
    [slope, intercept, _, _, _] = stats.linregress(years, vals)
    linearfit = (slope*years)+intercept
    ds_linear_fit = ds
    ds_linear_fit = xr.DataArray(linearfit,
                                 dims=('year'),
                                 coords={'year': ds['year']})
    return ds_linear_fit

def calculate_pi_for_model(modelname, average_type, varname=DEFAULT_VARNAME,
                           save_calculation=False, use_calculated_value=False):
    nametag = get_pi_control_nametag(modelname, varname, average_type)
    file_location = DIR_PI_CONTROL_DATA + nametag+'.nc'
    # if you're supposed to use the calculated file and that file exists, use it!
    if (use_calculated_value) and (os.path.isfile(file_location)):
        print('>> using previously calculated PI control')
        ds = xr.open_dataset(file_location)
        ds_annual_global_avg_linear = ds[average_type+'_avg_linear_fit']
        ds_annual_global_avg = ds[average_type+'_avg']
    else:
        if (use_calculated_value) and (not os.path.isfile(file_location)):
            print('>> previously calculated PI control file does not exist')
        print('>> calculating PI control')
        [ds_pi_annual, ds_1pctCO2_annual, ds_pi_annual_subset] = align_times(modelname)
        ds_annual_global_avg = area_weighting.get_global_mean_timeseries(ds_pi_annual_subset, modelname, average_type)
        ds_annual_global_avg_linear = calculate_linear_trend(ds_annual_global_avg)
    
    if save_calculation:
        # only save calculation if not using precalculated value
        if use_calculated_value:
            print('>> not saving PI control because using previously calculated data')
        else:
            # remove old file if the file already exists
            if os.path.isfile(file_location):
                os.remove(file_location)
                print('>> deleting previously calculated PI control')

            # Save ds_annual_global_avg_linear as netcdf
            ds = ds_annual_global_avg_linear.to_dataset(name=average_type+'_avg_linear_fit')
            ds[average_type+'_avg']=ds_annual_global_avg.load()
            ds.to_netcdf(file_location)
    
    return ds_annual_global_avg, ds_annual_global_avg_linear


