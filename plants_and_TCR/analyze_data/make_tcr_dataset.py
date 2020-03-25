import pandas as pd
import numpy as np

from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import params

CDICT_NAMES = params.CDICT_NAMES

def make_tcr_dataset(tcr_dict, end_yr, varname, average_type,
                     tcr_types=['PHYS', 'TOT', 'RAD', 'TOT-RAD']):
    #################### SET UP DATAFRAME #################
    modelinds = []
    for cdict_name in CDICT_NAMES:
        [_, _, modelnames_short] = get_CMIP_info.get_CMIP_info(cdict_name)
        modelnames = modelnames_short
        for m in range(0, len(modelnames)):
            modelinds.append(modelnames[m])
    tcrs = pd.DataFrame(index=modelinds)

    ################## PULL IN DATA ########################
    for t in range(0, len(tcr_types)):
        tcr_type = tcr_types[t]
        exampledata = []
        for cdict_name in CDICT_NAMES:
            [_, _, modelnames_short] = get_CMIP_info.get_CMIP_info(cdict_name)
            modelnames = modelnames_short
            for m in range(0, len(modelnames)):
                modelname = modelnames[m]
                nametag = modelname+'_'+tcr_type+'_'+varname+'_'+average_type
                if nametag in tcr_dict:
                    ds_annual = tcr_dict[nametag]
                    exampledata.append(np.mean(ds_annual[(end_yr-10):(end_yr+10)].values))
                else:
                    exampledata.append(np.nan)

        tcrs[tcr_type] = exampledata
    return tcrs
