"""
This will load relevant output from CMIP6 models and return a
dictionary with all of the xarray datasets in it.

Modified from code from Abby Swann.
"""

#-----------------------------------------------------------------------------------------
### Import Libraries
import glob
import xarray as xr
from plants_and_TCR.analysis_parameters import directory_information
#-----------------------------------------------------------------------------------------
### List of models, runs, and variables

# data path location
DATAPATH = directory_information.DIR_DATA_RAW_CMIP6_1
DATAPATH_NOT_C4MIP = directory_information.DIR_DATA_RAW_CMIP6_2

#----- List of all of the models
MODELLIST = ['BCC-CSM2-MR', 'CanESM5', 'CESM2',
             'CNRM-ESM2-1', 'GFDL-ESM4', 'GISS-E2-1-G',
             'IPSL-CM6A-LR', 'MIROC-ES2L', 'MRI-ESM2-0', 'UKESM1-0-LL',
             'ACCESS-ESM1-5','NorESM2-LM', 'MPI-ESM1-2-LR']

RUNNAMELIST = ['1pctCO2-bgc', '1pctCO2-rad', '1pctCO2', 'piControl', 'esm-piControl']#'piSST-4xCO2-rad']

# list of all of the variables wanted
VARLIST = ['hfls', 'hfss', 'evspsbl', 'tas', 'ts', 'tran', 'lai', 
           'rlds', 'rlus', 'rsds', 'rsus', 
           'rldscs', 'rluscs', 'rsdscs', 'rsuscs', 
           'clt'] 
# Other variables of interest: 'hurs', 'huss', 'prw', 'hus', 'gpp', 'evspsblpot', 'pr', 'rsdt', 'rlut', 'rsut',
# 'rsutcs','rlutcs', 'ta', 'vegHeight', 'ps', 'zg','va','vas','ua','uas','wap','psl'

# weights for months
MONTHWEIGHTS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#-----------------------------------------------------------------------------------------
# This loops over models, runs, and variables to load all of the xarray datasets into a dictionary
def load_dictionary(modellist=MODELLIST, runnlist=RUNNAMELIST, varlist=VARLIST, datapath=DATAPATH):
    # create a dictionary to store the output
    CMIP_DICT = dict()

    for md, modelname in enumerate(modellist):
        print('******************')
        print('loading model: ' +modelname)

        #---- add grid information at the model level
        #-- Area of gridcells
        varname = 'areacella'
        nametag = modelname +'_' +varname
        filepath = datapath +modelname+'/'+varname +'_*' +modelname +'_' +'*'
       # print(filepath)
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist, combine='by_coords')
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #-- Land fraction
        varname = 'sftlf' # land fraction
        nametag = modelname +'_' +varname
        filepath = datapath +modelname+'/'+varname +'_*' +modelname +'_' +'*'
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist, combine='by_coords')
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #-- Glacier fraction
        varname = 'sftgif' # glacier fraction
        nametag = modelname +'_' +varname
        filepath = DATAPATH +modelname+'/'+varname +'_*' +modelname +'_' +'*'
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist, combine='by_coords')
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #---- Loop over runs
        for rn, runname in enumerate(runnlist):
            print('loading run: ' +runname)

            #---- Loop over variables
            for v, varname in enumerate(varlist):
                #print(filepath)
                nametag = modelname +'_' +runname +'_' +varname
                filepath = (DATAPATH +modelname+'/'+varname+'/'+
                                varname +'_*' +modelname +'_' +runname +'_*') #r1i1p1*'

                # find the combination of all of these lists
                filenamelist = sorted(glob.glob(filepath))

                if len(filenamelist) > 0:
                    print('variable: ' +varname)
                    # load all of the files for a single variable into one xarray dataset
                    ds_cmip = xr.open_mfdataset(filenamelist)#, combine='by_coords' ,combine='nested'
                    CMIP_DICT[nametag] = ds_cmip.copy(deep=True)
                    
    return CMIP_DICT
