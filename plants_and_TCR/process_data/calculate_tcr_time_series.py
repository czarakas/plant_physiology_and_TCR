"""
Creates a data dictionary which contains the 20-year mean (global, land, or nonland) temperature
at each year (need to change to use the NATIVE GRID)
"""
import pickle
import numpy as np
import xarray as xr
import copy

from plants_and_TCR.analysis_parameters import params
from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analyze_data import grab_cmip_dataset
from plants_and_TCR.process_data import calculate_pi_baseline
from plants_and_TCR.process_data import reindex_time
from plants_and_TCR.process_data import area_weighting

DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES
DIR_TCR_DICT = directory_information.DIR_DATA+'processed_data/'
CDICT = pickle.load(open(DIR_CMIP_DICTS+'cmip_dict.pickle', "rb"))
CDICT_NAMES = params.CDICT_NAMES
DEFAULT_VARNAME='tas'
modelnames_short = get_CMIP_info.get_modelnames_short('CMIP5and6')
pi_adjustments = get_CMIP_info.get_PI_adjustment('CMIP5and6')

def get_nametag_tcr_dict(varname, runname, cdict_name, modelname):
    """Returns key for dictionary"""
    nametag = varname+'_'+runname+'_'+cdict_name+'_'+modelname
    return nametag

def get_ds_for_tcr_type(tcr_type, modelname, varname):
    """Add doc string"""
    if tcr_type == 'TOT-RAD':
        ds_original = grab_cmip_dataset.grab_cmip_dataset(cdict=CDICT, Mname=modelname,
                                                 Rname='1pctCO2', Vname=varname)
        ds2_original = grab_cmip_dataset.grab_cmip_dataset(cdict=CDICT, Mname=modelname,
                                                  Rname='1pctCO2-rad', Vname=varname)
        ds = copy.deepcopy(ds_original)
        ds2 = copy.deepcopy(ds2_original)
        
        if (ds is not None) and (ds2 is not None):
            ds[varname] = ds[varname] - ds2[varname]
        else:
            ds = None

    else:
        if tcr_type == 'TOT':
            runname = '1pctCO2'
        elif tcr_type == 'RAD':
            runname = '1pctCO2-rad'
        elif tcr_type == 'PHYS':
            runname = '1pctCO2-bgc'
        else:
            print('Invalid key')

        ds_original = grab_cmip_dataset.grab_cmip_dataset(cdict=CDICT, Mname=modelname,
                                                 Rname=runname, Vname=varname)
        ds = copy.deepcopy(ds_original)
        
    return ds

def calculate_tcr(ds_original, tcr_type, average_type, modelname, varname, recalculate_TCRs=True):
    """Add doc string"""
    
    model_ind = modelnames_short.index(modelname)
    pi_adjustment = pi_adjustments[model_ind]
    if recalculate_TCRs:
        save_calculation=True
        use_calculated_value=False
    else:
        save_calculation=False
        use_calculated_value=True
    
    
    # copy dataset
    ds = copy.deepcopy(ds_original)
    
    # adjust to PI control and take annual average
    newtimes = reindex_time.reindex_time(startingtimes=ds['time'], yr_adjustment=pi_adjustment)
    ds['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])    
    ds_annual = ds.groupby('time.year').mean('time')

    # Calculate weighted average for area type (global, land, ocean)
    ds_annual_global_original = area_weighting.get_global_mean_timeseries(ds_annual,
                                                                          modelname,
                                                                          average_type)
    ds_annual_global = copy.deepcopy(ds_annual_global_original)

    # Subtract preindustrial baseline if necessary
    if tcr_type == 'TOT-RAD':
        var_change_1d = ds_annual_global
    else:
        # Grab preindustrial baseline
        [_, ds_annual_global_avg_linear] = calculate_pi_baseline.calculate_pi_for_model(modelname=modelname,
                                                                                        average_type=average_type,
                                                                                        save_calculation=save_calculation,
                                                                                        use_calculated_value=use_calculated_value)
        var_change_1d = ds_annual_global - ds_annual_global_avg_linear

    return var_change_1d

def create_tcr_datasets(tcr_types, average_types,
                        varname=DEFAULT_VARNAME, save_tcr_dict=True, recalculate_TCRs=True):
    """Add docstring"""
    tcr_dict_1d = dict()

    # loop through all cdict types
    for cdict_name in CDICT_NAMES:
        modelnames = get_CMIP_info.get_modelnames_short(cdict_name)

        # loop through all models
        for modelname in modelnames:
            print(modelname)

            # loop through area average types
            for average_type in average_types:

                # loop through TCR calculation types
                for tcr_type in tcr_types:
                    print('------'+tcr_type+'------')
                    # Get data necessary for TCR type
                    ds = get_ds_for_tcr_type(tcr_type, modelname, varname)

                    if ds is not None:
                        # Calculate TCR time series
                        var_change_1d = calculate_tcr(ds, tcr_type, average_type,
                                                      modelname, varname, recalculate_TCRs)

                        # Save to dictionary
                        nametag = modelname+'_'+tcr_type+'_'+varname+'_'+average_type
                        tcr_dict_1d[nametag] = var_change_1d
                    else:
                        print('No data')
                        
    if save_tcr_dict:
        with open(DIR_TCR_DICT+'TCR_dict.pickle', 'wb') as handle:
            pickle.dump(tcr_dict_1d, handle, protocol=pickle.HIGHEST_PROTOCOL)
        

    return tcr_dict_1d
