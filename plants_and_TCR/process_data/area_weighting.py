"""
Needs docstring
"""

import pickle
import xarray as xr

from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analyze_data import grab_cmip_dataset

DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES
CDICT = pickle.load(open(DIR_CMIP_DICTS+'cmip_dict.pickle', "rb"))
EXAMPLE_RUNNAME = '1pctCO2'
DEFAULT_VARNAME = 'tas'
REF_MODELNAME = 'CESM1-BGC'
REF_CDICT_NAME = 'CMIP5'

def set_up_area_weightings(modelname, regrid_on=False):
    """ Needs docstring """
    
    if regrid_on:
        ds_area = CDICT[REF_MODELNAME +'_areacella']
        ds_land = CDICT[REF_MODELNAME +'_sftlf'] # in values of 0 to 100
        ds_glas = CDICT[REF_MODELNAME +'_sftgif']
        ds_example = grab_cmip_dataset.grab_cmip_dataset(CDICT,
                                                         Mname=REF_MODELNAME,
                                                         Rname=EXAMPLE_RUNNAME,
                                                         Vname=DEFAULT_VARNAME)
        
    else:
        ds_area = CDICT[modelname +'_areacella']
        ds_land = CDICT[modelname +'_sftlf'] # in values of 0 to 100
        ds_glas = CDICT[modelname +'_sftgif']
        ds_example = grab_cmip_dataset.grab_cmip_dataset(CDICT,
                                             Mname=modelname,
                                             Rname=EXAMPLE_RUNNAME,
                                             Vname=DEFAULT_VARNAME)
    ds_area = ds_area.reindex_like(ds_example, method='nearest', tolerance=0.01)
    ds_land = ds_land.reindex_like(ds_example, method='nearest', tolerance=0.01)
    ds_glas = ds_glas.reindex_like(ds_example, method='nearest', tolerance=0.01)
    ds_glas['sftgif'] = ds_glas['sftgif'].fillna(0)

    ds = ds_area

    ds['da_area'] = ds_area['areacella']
    ds['da_land'] = ds_land['sftlf']
    ds['da_glac'] = ds_glas['sftgif']

    if modelname == 'CESM2':
        for k, _ in ds.variables.items():
            if '_FillValue' in ds[k].encoding:
                ds[k].encoding['_FillValue'] = ds[k].encoding['missing_value']
            else:
                pass
    return ds

def calculate_area_weightings(modelname, regrid_on=False):
    """ Needs docstring """

    # Get data
    ds = set_up_area_weightings(modelname, regrid_on)

    global_area = ds['da_area'].sum(skipna=True)
    land_area = ds['da_area']*(ds['da_land']/100)
    da_glac = ds['da_glac']
    land_area_nonglaciated = land_area*(1-(da_glac/100))
    land_area_glaciated = land_area*((da_glac/100))
    ocean_area = ds['da_area'] - land_area

    global_area_land_nonglaciated = land_area_nonglaciated.sum(skipna=True)
    global_area_land_glaciated = land_area_glaciated.sum(skipna=True)
    global_area_ocean = ocean_area.sum(skipna=True)

    ds.attrs['landfrac'] = global_area_land_nonglaciated.values/global_area.values
    ds.attrs['glacierfrac'] = global_area_land_glaciated.values/global_area.values
    ds.attrs['nonlandfrac'] = global_area_ocean.values/global_area.values

    # Calculate Weights
    ds['area_weights'] = ds['da_area']/global_area
    ds['land_weights'] = land_area_nonglaciated/global_area_land_nonglaciated
    ds['glacier_weights'] = land_area_glaciated/global_area_land_glaciated
    ds['ocean_weights'] = ocean_area/global_area_ocean
    return ds

def get_global_mean_timeseries(ds, modelname, average_type):
    ds_area_weights = calculate_area_weightings(modelname)
    
    if average_type=='global':
        area_weights = ds_area_weights['area_weights']
    elif average_type=='land':
        area_weights = ds_area_weights['land_weights']
    elif average_type=='ocean':
        area_weights = ds_area_weights['ocean_weights']
    
    area_weights = area_weights.reindex_like(ds, method='nearest', tolerance=0.01)
    
    if isinstance(ds, xr.core.dataset.Dataset):
        ds_weighted = ds[DEFAULT_VARNAME]*area_weights
    elif isinstance(ds_pi_annual, xr.core.dataarray.DataArray):
        ds_weighted = ds*area_weights
    
    ds_global = ds_weighted.sum(dim=('lat','lon'))
    
    return ds_global