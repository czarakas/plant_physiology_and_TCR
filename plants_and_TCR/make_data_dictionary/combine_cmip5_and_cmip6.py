"""
Add docstring
"""
import pickle

from plants_and_TCR.analysis_parameters import directory_information
DIR_CMIP_DICTS = directory_information.DIR_DATA_DICTIONARIES

CMIP6_DICT = pickle.load(open(DIR_CMIP_DICTS+'cmip6_dict.pickle', 'rb'))
CMIP5_DICT = pickle.load(open(DIR_CMIP_DICTS+'cmip5_dict.pickle', 'rb'))

def combine_cmip_dictionaries(cmip5_dict=CMIP5_DICT, cmip6_dict=CMIP6_DICT):
    cmip_dict = dict()
    
    for old_key in cmip6_dict.keys():
        ds = cmip6_dict[old_key]
        cmip_dict[old_key] = ds

    for old_key in cmip5_dict.keys():
        ds = cmip5_dict[old_key]
        key_components = old_key.split('_')
        new_key = ''
        if key_components[1] == 'esmFixClim1':
            key_components[1] = '1pctCO2-bgc'
        elif key_components[1] == 'esmFdbk1':
            key_components[1] = '1pctCO2-rad'
        for ind, key_component in enumerate(key_components):
            if ind == 0:
                new_key = new_key+key_component
            else:
                new_key = new_key+'_'+key_component
        cmip_dict[new_key] = ds
        
    return cmip_dict
