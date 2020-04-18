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
                                     model_list):
    """Add docstring"""
    ds_land = CDICT[modelname +'_sftlf'] # in values of 0 to 100
    daland = ds_land['sftlf'].values/100

    nametag = get_nametag(varname=varname, runname=runname,
                          cdict_name=cmipchoice, modelname=modelname)
    ds_grid = proc_data_dict[nametag]

    ds_out = xr.Dataset({'lat': ds_grid['lat'],
                         'lon': ds_grid['lon']})
    grid_dims = np.shape(ds_grid[varname].mean(dim='time').values)
    multi_model_sum = xr.DataArray(np.zeros(grid_dims),
                                   dims={'lat': ds_grid['lat'], 'lon':ds_grid['lon']})
    positive_change_count = xr.DataArray(np.zeros(grid_dims),
                                         dims={'lat': ds_grid['lat'], 'lon':ds_grid['lon']})
    negative_change_count = xr.DataArray(np.zeros(grid_dims),
                                         dims={'lat': ds_grid['lat'], 'lon':ds_grid['lon']})

    # Make dataset for all models
    ds_all_models = ds_grid.mean(dim='time')
    grid_dims_geo = np.shape(ds_all_models[varname].values)
    ds_all_models = ds_all_models.drop(varname)
    ds_all_models = ds_all_models.assign_coords(modelname=model_list)
    grid_dims = [grid_dims_geo[0], grid_dims_geo[1], len(model_list)]
    var_array = xr.DataArray(np.zeros(grid_dims),
                             dims={'lat': ds_all_models['lat'],
                                   'lon':ds_all_models['lon'],
                                   'modelname':ds_all_models['modelname']})
    var_array = var_array.where(var_array > 0)
    ds_all_models[varname] = var_array

    return ds_all_models, multi_model_sum, positive_change_count, negative_change_count

##########Calculate difference between runs for given model#########################
def calculate_diff(proc_data_dict,
                   cmipchoice,
                   modelname,
                   runname2,
                   runname1,
                   varname,
                   end_yr,
                   month_filter=None):
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
        if month_filter is not None:
            ds2 = ds2.where(ds2['time.month']==month_filter,drop=True)
            ds1 = ds1.where(ds1['time.month']==month_filter,drop=True)
            endvals2 = ds2[varname].isel(time=range((end_yr-10),
                                                    (end_yr+10))).groupby('time.year').mean(dim='time')
            endvals1 = ds1[varname].isel(time=range((end_yr-10),
                                                    (end_yr+10))).groupby('time.year').mean(dim='time')
            delta = endvals1 - endvals2
            
        else:
            endvals2 = ds2[varname].isel(time=range((end_yr-10)*12,
                                                    (end_yr+10)*12)).groupby('time.year').mean(dim='time')
            endvals1 = ds1[varname].isel(time=range((end_yr-10)*12,
                                                    (end_yr+10)*12)).groupby('time.year').mean(dim='time')

            delta = endvals1 - endvals2
    else:
        delta = None
    return delta

def increment_counts(model_data,
                     change_cutoff,
                     positive_change_count,
                     negative_change_count):
    """ Add docstring """
    model_pos_count = model_data.where(model_data <= change_cutoff)
    model_pos_count = model_pos_count.fillna(1)
    model_pos_count = model_pos_count.where(model_pos_count > change_cutoff)
    model_pos_count = model_pos_count.fillna(0)
    positive_change_count = positive_change_count + model_pos_count

    model_neg_count = model_data.where(model_data >= -change_cutoff)
    model_neg_count = model_neg_count.fillna(-1)
    model_neg_count = model_neg_count.where(model_neg_count < change_cutoff)
    model_neg_count = model_neg_count.fillna(0)
    negative_change_count = negative_change_count + model_neg_count

    return positive_change_count, negative_change_count

def combine_models(proc_data_dict,
                   model_list,
                   runname_inds,
                   varname,
                   end_yr,
                   change_cutoff,
                   ds_all_models,
                   multi_model_sum,
                   positive_change_count,
                   negative_change_count,
                   cmip_names=CMIP_NAMES,
                   month_filter=None):
    """Add docstring"""
    num_models_with_data = 0
    ind = 0
    for cmipchoice in cmip_names:
        model_list = get_CMIP_info.get_modelnames_short(cmipchoice)

        if len(runname_inds) == 2:
            runname1 = runnames_all[runname_inds[0]] #1pctCO2-rad
            runname2 = runnames_all[runname_inds[1]] #1pctCO2
            for modelname in model_list:
                print(modelname)

                delta = calculate_diff(proc_data_dict,
                                       cmipchoice,
                                       modelname,
                                       runname2,
                                       runname1,
                                       varname,
                                       end_yr,
                                       month_filter)
                if delta is not None:
                    model_data = delta.mean(dim='year')

                    [positive_change_count,
                     negative_change_count] = increment_counts(model_data,
                                                               change_cutoff,
                                                               positive_change_count,
                                                               negative_change_count)

                    #### Add model to dataset
                    if ds_all_models['modelname'][ind] == modelname:
                        ds_all_models[varname][:, :, ind] = model_data
                    else:
                        print('problem!')
                    #ds_all_models[modelname]=model_data

                    ########Update all-model arrays
                    multi_model_sum = multi_model_sum + model_data
                    num_models_with_data = num_models_with_data + 1
                else:
                    print('No data for '+modelname)
                ind = ind+1
        elif len(runname_inds) == 4:
            runname1 = runnames_all[runname_inds[0]] #1pctCO2-rad
            runname2 = runnames_all[runname_inds[1]] #1pctCO2
            runname3 = runnames_all[runname_inds[2]]
            runname4 = runnames_all[runname_inds[3]]
            for modelname in model_list:
                delta1 = calculate_diff(proc_data_dict,
                                        cmipchoice,
                                        modelname,
                                        runname2,
                                        runname1,
                                        varname,
                                        end_yr,
                                        month_filter)
                delta2 = calculate_diff(proc_data_dict,
                                        cmipchoice,
                                        modelname,
                                        runname4,
                                        runname3,
                                        varname,
                                        end_yr,
                                        month_filter)
                if (delta1 is not None) and (delta2 is not None):
                    model_data = delta1.mean(dim='year') - delta2.mean(dim='year')

                    [positive_change_count,
                     negative_change_count] = increment_counts(model_data,
                                                               change_cutoff,
                                                               positive_change_count,
                                                               negative_change_count)

                    #### Add model to dataset
                    if ds_all_models['modelname'][ind] == modelname:
                        ds_all_models[varname][:, :, ind] = model_data
                    else:
                        print('problem!')
                    #ds_all_models[modelname]=model_data

                    ########Update all-model arrays
                    multi_model_sum = multi_model_sum + model_data
                    num_models_with_data = num_models_with_data + 1
                else:
                    print('No data for '+modelname)
                ind = ind+1

    multi_model_sum = multi_model_sum/num_models_with_data
    negative_change_count = -negative_change_count
    return [ds_all_models, multi_model_sum, positive_change_count,
            negative_change_count, num_models_with_data]

def get_mm_mean(proc_data_dict, varname, end_yr, change_cutoff,
                runname_inds, cmip_names=CMIP_NAMES, month_filter=None):
    """ Add docstring"""
    if len(cmip_names) > 1:
        model_list = get_CMIP_info.get_modelnames_short('CMIP5and6')
    elif len(cmip_names) == 1:
        model_list = get_CMIP_info.get_modelnames_short(cmip_names[0])

    [ds_all_models,
     multi_model_sum,
     positive_change_count,
     negative_change_count] = initialize_multimodel_mean_array(proc_data_dict=proc_data_dict,
                                                               cmipchoice='CMIP5',
                                                               modelname='CanESM2',
                                                               runname='1pctCO2',
                                                               varname=varname,
                                                               model_list=model_list)

    [ds_all_models,
     multi_model_sum,
     positive_change_count,
     negative_change_count,
     num_models_with_data] = combine_models(proc_data_dict=proc_data_dict,
                                            varname=varname,
                                            end_yr=end_yr,
                                            change_cutoff=change_cutoff,
                                            ds_all_models=ds_all_models,
                                            multi_model_sum=multi_model_sum,
                                            positive_change_count=positive_change_count,
                                            negative_change_count=negative_change_count,
                                            model_list=model_list,
                                            runname_inds=runname_inds,
                                            cmip_names=cmip_names,
                                            month_filter=month_filter)

    return [ds_all_models, multi_model_sum, positive_change_count,
            negative_change_count, num_models_with_data]

def calculate_where_models_mostly_agree(positive_change_count,
                                        negative_change_count,
                                        cut_off_num, num_models):
    """if >cutoffNum agree on sign, val=-1; if <cutoffNum agree on sign, val=1"""
    mostly_agree = abs(positive_change_count-negative_change_count)
    mostly_agree = mostly_agree.where(mostly_agree >= (2*cut_off_num - num_models - 0.01))
    mostly_agree = mostly_agree.fillna(-1)
    mostly_agree = mostly_agree.where(mostly_agree < 0)
    mostly_agree = mostly_agree.fillna(1)

    return -mostly_agree
