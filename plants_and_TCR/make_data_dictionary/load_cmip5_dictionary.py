"""
This will load relevant output from CMIP5 models and return a
dictionary with all of the xarray datasets in it.

Modified from code from Abby Swann.
"""

#-----------------------------------------------------------------------------------------
### Import Libraries
import glob
import xarray as xr

#-----------------------------------------------------------------------------------------
### List of models, runs, and variables

# data path location
DATAPATH_ORIGINAL = '/home/disk/eos3/aswann/Shared/Data/CMIP5_CCycle/'
DATAPATH_NEW = '/home/disk/eos9/czarakas/Data/CMIP5/'

#----- List of all of the models
MODELLIST = ['MPI-ESM-LR', 'HadGEM2-ES', 'NorESM1-ME', 'bcc-csm1-1',
             'CanESM2', 'CESM1-BGC', 'GFDL-ESM2M', 'IPSL-CM5A-LR',
             'MIROC-ESM', 'MRI-ESM1', 'BNU-ESM']
#'MPI-ESM-LR','inmcm4' # other models for which I have at least some output

RUNNAMELIST = ['esmFixClim1', '1pctCO2', 'esmFdbk1', 'piControl', 'abrupt4xCO2']
# other possible run names for which I have some data:
# 'rcp45','esmFdbk2','esmrcp85','esmHistorical','esmControl'

VARLIST = ['hfls', 'hfss', 'hurs', 'huss', 'ps', 'evspsbl', 'tas', 'ts',
           'ps', 'pr', 'sfcWind', 'tran', 'gpp', 'lai', 'mrro', 'mrso', 'mrsls', 'rlds',
           'rlus', 'rlut', 'rsds', 'rsdt', 'rsus', 'rsut', 'rldscs', 'rluscs', 'rsdscs',
           'rsuscs', 'rsutcs', 'rlutcs', 'clt']

# weights for months
MONTHWEIGHTS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#-----------------------------------------------------------------------------------------
# This loops over models, runs, and variables to load all of the xarray datasets into a dictionary
def load_dictionary(modellist=MODELLIST, runnlist=RUNNAMELIST, varlist=VARLIST, datapath_original=DATAPATH_ORIGINAL, datapath_new=DATAPATH_NEW):
    
    # create a dictionary to store the output
    CMIP_DICT = dict()

    for md, modelname in enumerate(modellist):
        print('loading model: ' +modelname)

        datapath = datapath_original
        fxRun = 'esmHistorical'

        #---- add grid information at the model level
        #-- Area of gridcells
        varname = 'areacella'
        nametag = modelname +'_' +varname
        filepath = datapath +modelname +'/' +varname +'/' +varname +'_*_' +modelname +'*' +fxRun+'*'
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist)
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #-- Land fraction
        varname = 'sftlf' # land fraction
        nametag = modelname +'_' +varname
        filepath = datapath +modelname +'/' +varname +'/' +varname +'_*_' +modelname +'*' +fxRun+'*'
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist)
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #-- Glacier fraction
        varname = 'sftgif' # glacier fraction
        nametag = modelname +'_' +varname
        filepath = datapath +'gridcell_masks/' +varname +'_*_' +modelname +'_*'
        filenamelist = sorted(glob.glob(filepath)) # find the combination of all of these lists
        if len(filenamelist) > 0:
            print('variable: ' +varname)
            # load all of the files for a single variable into one xarray dataset
            ds_cmip = xr.open_mfdataset(filenamelist)
            # add them to the dictionary
            CMIP_DICT[nametag] = ds_cmip.copy(deep=True)

        #---- Loop over runs
        for rn, runname in enumerate(runnlist):
            runname = runnlist[rn]
            print('loading run: ' +runname)

            #---- Loop over variables
            for v, varname in enumerate(varlist):
                if runname in ('piControl', 'abrupt4xCO2'):
                    datapath = datapath_new
                elif modelname == 'MPI-ESM-LR':
                    datapath = datapath_new
                elif varname in ('ts', 'huss', 'rldscs', 'rluscs', 'rsdscs', 'rsuscs', 'rsutcs',
                                 'rlutcs', 'clt'):
                    datapath = datapath_new
                else:
                    datapath = datapath_original
                #print('variable: ' +varname)
                nametag = modelname +'_' +runname +'_' +varname
                #filepath = datapath +modelname +'/' +varname +'/*' +modelname +'_' +runname +'*r1i1p1*'
                filepath = datapath +modelname +'/' +varname +'/' +varname +\
                           '_*_'+modelname +'_' +runname +'*r1i1p1*'

                # find the combination of all of these lists
                filenamelist = sorted(glob.glob(filepath))

                if len(filenamelist) > 0:
                    print('variable: ' +varname)
                    # load all of the files for a single variable into one xarray dataset
                    ds_cmip = xr.open_mfdataset(filenamelist)

                    CMIP_DICT[nametag] = ds_cmip.copy(deep=True)
    return CMIP_DICT

#-----------------------------------------------------------------------------------------
### Delete problematic fields

#-- BCC model seems to have an error reporting problem for runoff - discard
#modelname = 'bcc-csm1-1'
#varname='mrro'
#---- Loop over variables
#---- Loop over runs
#for rn in range(len(runnamelist)):
#    runname = runnamelist[rn]
#    nametag = modelname +'_' +runname +'_' +varname
#    del cmip_dict[nametag] # delete the variable from the dictionary



#-----------------------------------------------------------------------------------------
