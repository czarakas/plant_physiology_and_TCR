"""

Add docstring
"""

######################## Load modules ###################################
import pickle
import sys

import numpy as np
import xarray as xr

from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import get_CMIP_info

DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES
CDICT = pickle.load(open(DIR_CMIP_DICTS+'cmip_dict.pickle', "rb"))
CMIP_NAMES = ['CMIP5', 'CMIP6']
runnames_all = ['1pctCO2-rad', '1pctCO2-bgc', '1pctCO2', 'piControl']

def get_nametag(varname, runname, cdict_name, modelname):
    nametag = varname+'_'+runname+'_'+cdict_name+'_'+modelname
    return nametag

##########Set Up MultiModelMean Empty Array###############################
def initialize_multimodel_mean_array(proc_data_dict,
                                     cmipchoice,
                                     modelname,
                                     runname,
                                     varname,
                                     model_list,
                                     end_yr):
    """Add docstring"""
    ds_land = CDICT[modelname +'_sftlf'] # in values of 0 to 100
    daland = ds_land['sftlf'].values/100

    nametag = get_nametag(varname=varname, runname=runname,
                          cdict_name=cmipchoice, modelname=modelname)
    ds_grid = proc_data_dict[nametag]
    times = np.arange(0, len(ds_grid['time'].isel(time=range((end_yr-10)*12, (end_yr+10)*12))))

    ds_out = xr.Dataset({'lat': ds_grid['lat'],
                         'lon': ds_grid['lon'],
                         'time':times})
    grid_dims = np.shape(ds_grid[varname].isel(time=range((end_yr-10)*12, (end_yr+10)*12)).values)

    # Make dataset for all models
    ds_all_models = ds_grid.isel(time=range((end_yr-10)*12, (end_yr+10)*12))
    ds_all_models['time'] = times
    grid_dims_geo = np.shape(ds_all_models[varname].values)
    ds_all_models = ds_all_models.drop(varname)
    ds_all_models = ds_all_models.assign_coords(modelname=model_list)
    grid_dims = [grid_dims_geo[0], grid_dims_geo[1], grid_dims_geo[2], len(model_list)]
    var_array = xr.DataArray(np.zeros(grid_dims),
                             dims={'time':ds_all_models['time'],
                                   'lat': ds_all_models['lat'],
                                   'lon':ds_all_models['lon'],
                                   'modelname':ds_all_models['modelname']})
    var_array = var_array.where(var_array > 0)
    ds_all_models[varname] = var_array

    return ds_all_models

##########Calculate difference between runs for given model#########################
def calculate_diff(proc_data_dict,
                   cmipchoice,
                   modelname,
                   runname2,
                   runname1,
                   varname,
                   end_yr):
    """ Creates dataset which contains the difference
    between the two run names, during the 20 year window around the
    user-specified end year. The data is 2D (lat/lon)"""
    # get datasets
    nametag = get_nametag(varname=varname, runname=runname2,
                          cdict_name=cmipchoice, modelname=modelname)
    ds2 = proc_data_dict[nametag]
    nametag = get_nametag(varname=varname, runname=runname1,
                          cdict_name=cmipchoice, modelname=modelname)
    ds1 = proc_data_dict[nametag]

    if ((ds2 is not None) and (ds1 is not None)):
        endvals2 = ds2[varname].isel(time=range((end_yr-10)*12,
                                                (end_yr+10)*12))
        endvals1 = ds1[varname].isel(time=range((end_yr-10)*12,
                                                (end_yr+10)*12))

        delta = endvals1 - endvals2
        delta['time'] = np.arange(0, len(delta))
    else:
        delta = None
    return delta

##########Calculate difference between runs for given model#########################
def calculate_baseline(proc_data_dict,
                       cmipchoice,
                       modelname,
                       runname,
                       varname,
                       end_yr):
    """ Creates dataset which contains the difference
    between the two run names, during the 20 year window around the
    user-specified end year. The data is 2D (lat/lon)"""
    # get datasets
    nametag = get_nametag(varname=varname, runname=runname,
                          cdict_name=cmipchoice, modelname=modelname)
    ds1 = proc_data_dict[nametag]

    if ds1 is not None:
        endvals1 = ds1[varname].isel(time=range((end_yr-10)*12,
                                                (end_yr+10)*12))
        endvals1['time'] = np.arange(0, len(endvals1))
    else:
        endvals1 = None
    return endvals1

def combine_models(proc_data_dict,
                   model_list,
                   runname_inds,
                   varname,
                   end_yr,
                   ds_all_models,
                   cmip_names=CMIP_NAMES,
                   delta_or_baseline='Delta'):
    """Add docstring"""
    num_models_with_data = 0
    ind = 0
    for cmipchoice in cmip_names:
        model_list = get_CMIP_info.get_modelnames_short(cmipchoice)
        if len(runname_inds) == 2:
            runname1 = runnames_all[runname_inds[0]] #1pctCO2-rad
            runname2 = runnames_all[runname_inds[1]] #1pctCO2
            for modelname in model_list:
                if delta_or_baseline == 'Delta':
                    delta = calculate_diff(proc_data_dict,
                                           cmipchoice,
                                           modelname,
                                           runname2,
                                           runname1,
                                           varname,
                                           end_yr)
                elif delta_or_baseline == 'Baseline':
                    delta = calculate_baseline(proc_data_dict,
                                               cmipchoice,
                                               modelname,
                                               runname2,
                                               varname,
                                               end_yr)
                if delta is not None:
                    model_data = delta
                    model_data['time'] = np.arange(0, len(delta))
                    #### Add model to dataset
                    if ds_all_models['modelname'][ind] == modelname:
                        if len(delta)<240:
                            ds_all_models[varname][0:len(delta), :, :, ind] = model_data
                        else:
                            ds_all_models[varname][:, :, :, ind] = model_data
                    else:
                        print('problem!')
                    #ds_all_models[modelname]=model_data

                else:
                    print('No data for '+modelname)
                ind = ind+1

    return ds_all_models

def get_mm_mean(proc_data_dict, varname, end_yr, runname_inds,
                cmip_names=CMIP_NAMES, delta_or_baseline='Delta',
                cmipchoice_init='CMIP5', modelname_init='CanESM2',
               runname_init='1pctCO2'):
    """ Add docstring"""
    if len(cmip_names) > 1:
        model_list = get_CMIP_info.get_modelnames_short('CMIP5and6')
    elif len(cmip_names) == 1:
        model_list = get_CMIP_info.get_modelnames_short(cmip_names[0])

    ds_all_models = initialize_multimodel_mean_array(proc_data_dict=proc_data_dict,
                                                     cmipchoice=cmipchoice_init,
                                                     modelname=modelname_init,
                                                     runname=runname_init,
                                                     varname=varname,
                                                     model_list=model_list,
                                                     end_yr=end_yr)
    ds_all_models = combine_models(proc_data_dict=proc_data_dict,
                                   varname=varname,
                                   end_yr=end_yr,
                                   ds_all_models=ds_all_models,
                                   model_list=model_list,
                                   runname_inds=runname_inds,
                                   cmip_names=cmip_names,
                                   delta_or_baseline=delta_or_baseline)

    return ds_all_models
