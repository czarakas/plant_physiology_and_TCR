"""
Add docstring
"""
from os import path
import xarray as xr

from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import params

OUTPUT_PATH = directory_information.DIR_PROCESSED_DATA
CDICT_NAMES = params.CDICT_NAMES
RUNNAMES = params.RUNNAMES_ALL

def get_file(nametag, filepath):
    """ Needs docstring """
    filename = filepath+nametag+'.nc'
    if path.isfile(filename):
        ds = xr.open_dataset(filename, use_cftime=True)
    else:
        ds = None
    return ds

def get_nametag(varname, runname, cdict_name, modelname):
    """Add docstring"""
    nametag = varname+'_'+runname+'_'+cdict_name+'_'+modelname
    return nametag

def create_variable_dictionary(runnames, varname, cdict_names=CDICT_NAMES,
                               input_path=OUTPUT_PATH, modelnames=None):
    """Creates dictionary with xarrays of all models and experiments for the
    variable of interest"""

    # initialize dictionary
    data_dict = dict()

    # loop through CMIP5 and CMIP6
    for cdict_name in cdict_names:

        # get modelnames and runnames for CMIP phase
        if modelnames==None:
            modelnames_short = get_CMIP_info.get_modelnames_short(cdict_name)
        else:
            modelnames_short = modelnames

        # loop through models
        for _, modelname in enumerate(modelnames_short):
            # loop through other experiments
            for runname in runnames:
                nametag = get_nametag(varname, runname, cdict_name, modelname)
                # Get processed xarray dataset
                ds = get_file(nametag, input_path)
                if ds is not None:
                    #Print information about dataset

                    # Save to dictionary
                    data_dict[nametag] = ds
                else:
                    data_dict[nametag] = None
                    print(nametag+' is not in the dictionary')
    return data_dict
