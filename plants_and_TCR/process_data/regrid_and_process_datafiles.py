"""Add docstring"""

################################# SET UPWORKSPACE #########################################
import pickle
import cftime
import numpy as np
import xarray as xr
import xesmf as xe

from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import params
from plants_and_TCR.analyze_data import grab_cmip_dataset
from plants_and_TCR.process_data import reindex_time
from plants_and_TCR.process_data import area_weighting

CDICT_NAMES = params.CDICT_NAMES
OUTPUT_PATH = directory_information.DIR_PROCESSED_DATA
DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES
CDICT = pickle.load(open(DIR_CMIP_DICTS+'cmip_dict.pickle', "rb"))

REF_MODELNAME = 'CESM1-BGC'
REF_CDICT_NAME = 'CMIP5'
REGRID_ON = True

##################
def get_nametag(varname, runname, cdict_name, modelname):
    """Add docstring"""
    nametag = varname+'_'+runname+'_'+cdict_name+'_'+modelname
    return nametag

def create_reference_grid(modelname, runname, varname):
    """Creates reference grid to which all model output will be regridded"""
    thisdata = grab_cmip_dataset.grab_cmip_dataset(CDICT,
                                                   modelname,
                                                   runname,
                                                   varname)
    ds_out = xr.Dataset({'lat': thisdata['lat'],
                         'lon': thisdata['lon']})
    return ds_out

def regrid_model(ds, reference_grid, varname, latvariable='lat', lonvariable='lon'):
    """Regrids model output to a reference grid"""
    data_series = ds[varname]
    ds_in = xr.Dataset({'lat': data_series[latvariable],
                        'lon': data_series[lonvariable],
                        'time': data_series['time'],
                        varname: data_series})
    regridder = xe.Regridder(ds_in, reference_grid, 'bilinear', periodic=True)
    data_series_regridded = regridder(ds_in)
    data_series_regridded.attrs.update(data_series.attrs)
    return data_series_regridded

def subset_pi_control(ds, cdict_name, modelname, varname, temp_dict, runnames_all):
    """ Needs docstring """
    # Figure out years of 1pctCO2 simulations
    ds_1pctco2 = temp_dict[get_nametag(cdict_name=cdict_name,
                                       modelname=modelname,
                                       runname=runnames_all[2],
                                       varname=varname)]
    if modelname == 'HadGEM2-ES':
        min_date = ds_1pctco2['time'].values[0]
    else:
        min_date = ds_1pctco2['time'].values[0]
    max_date = ds_1pctco2['time'].values[-1]
    ds = ds.sel(time=slice(min_date, max_date))
    return ds

def process_data(varname, output_path=OUTPUT_PATH, cdict=CDICT):
    """Creates dictionary with xarrays of all models and experiments for the
    variable of interest"""

    final_grid = create_reference_grid(REF_MODELNAME,
                                       '1pctCO2',
                                       'tas')

    # initialize dictionary
    raw_data_dict = dict()
    
    # loop through CMIP5 and CMIP6
    for cdict_name in CDICT_NAMES:

        # get modelnames and runnames for CMIP phase
        [runnames_all, _, modelnames_short] = get_CMIP_info.get_CMIP_info(cdict_name)
        pi_adjustment = get_CMIP_info.get_PI_adjustment(cdict_name)

        # loop through models
        for model_num, modelname in enumerate(modelnames_short):

            # loop through other experiments
            for runname in ['1pctCO2-rad', '1pctCO2-bgc', '1pctCO2', 'piControl']:
                nametag = get_nametag(varname=varname, runname=runname,
                                      cdict_name=cdict_name, modelname=modelname)

                # Get xarray dataset
                ds_original = grab_cmip_dataset.grab_cmip_dataset(cdict,
                                                                  modelname,
                                                                  runname,
                                                                  varname)

                # Don't do anything if there is no dataset for that nametag
                if ds_original is None:
                    pass
                    print(nametag+' is not in the dictionary')

                else:
                    print(nametag)
                    ds = ds_original.copy(deep=True)
                                    # Skip these datasets

                    # reindex time for pi control
                    if runname == 'piControl':
                        newtimes = reindex_time.reindex_time(startingtimes=ds['time'],
                                                             yr_adjustment=0)
                        ds['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])
                        ds = subset_pi_control(ds,
                                               cdict_name,
                                               modelname,
                                               varname,
                                               raw_data_dict,
                                               runnames_all)

                    # reindex time for all other experiments
                    else:
                        #print('before: '+str(ds['time'].values[0]))
                        # Reindex times and line up with piControl
                        newtimes = reindex_time.reindex_time(startingtimes=ds['time'],
                                                yr_adjustment=pi_adjustment[model_num])
                        ds['time'] = xr.DataArray(newtimes, coords=[newtimes], dims=['time'])

                    # Add attribute information
                    ds.attrs['modelname'] = modelname
                    ds.attrs['CMIP_phase'] = cdict_name

                    if REGRID_ON:
                        # Regrid model to CESM1-BGC
                        ds = regrid_model(ds, final_grid, varname)
                    else:
                        pass

                    # Set up and calculate area weightings
                    ds_areas = area_weighting.calculate_area_weightings(modelname,
                                                                  regrid_on=REGRID_ON)
                    ds['area_weights'] = ds_areas['area_weights']
                    ds['land_weights'] = ds_areas['land_weights']
                    ds['ocean_weights'] = ds_areas['ocean_weights']
                    ds['da_area'] = ds_areas['da_area']
                    ds['da_land'] = ds_areas['da_land']
                    ds['da_glac'] = ds_areas['da_glac']
                    
                    # Export file
                    ds.chunk({'lat':-1, 'lon':-1, 'time':20})
                    ds.to_netcdf(path=output_path+nametag+'.nc')
                    
                    # Save to dictionary
                    raw_data_dict[nametag] = ds

