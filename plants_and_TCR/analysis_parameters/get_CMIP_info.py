def get_CMIP_info(cdict_name):
    if cdict_name == 'CMIP6':
        runnames_all = ['1pctCO2-rad', '1pctCO2-bgc', '1pctCO2', 'piControl']
       # modelnames_long = get_modelnames_long(cdict_name)
        modelnames_short = get_modelnames_short(cdict_name)
    elif cdict_name == 'CMIP5':
        runnames_all = ['esmFdbk1', 'esmFixClim1', '1pctCO2', 'piControl', 'esmControl']
        #modelnames_long = get_modelnames_long(cdict_name)
        modelnames_short = get_modelnames_short(cdict_name)

    elif cdict_name == 'CMIP5and6':
        runnames_all = None
        #modelnames_long = get_modelnames_long(cdict_name)
        modelnames_short = get_modelnames_short(cdict_name)

    return runnames_all, modelnames_short, modelnames_short

#-------------------------------------------------------------------------------------
def get_modelnames_short(cdict_name):
    if cdict_name == 'CMIP6':
        modelnames = ['CNRM-ESM2-1', 'BCC-CSM2-MR', 'CanESM5',
                      'CESM2', 'GISS-E2-1-G', 'UKESM1-0-LL',
                      'GFDL-ESM4', 'IPSL-CM6A-LR', 'MIROC-ES2L',
                      'NorESM2-LM','MPI-ESM1-2-LR','ACCESS-ESM1-5']
    elif cdict_name == 'CMIP5':
        modelnames = ['bcc-csm1-1', 'CanESM2', 'CESM1-BGC',
                      'GFDL-ESM2M', 'HadGEM2-ES', 'IPSL-CM5A-LR',
                      'NorESM1-ME', 'MPI-ESM-LR']
    elif cdict_name == 'CMIP5and6':
        modelnames = get_modelnames_short('CMIP5')+get_modelnames_short('CMIP6')
    return modelnames

#def get_modelnames_long(cdict_name):
#    if cdict_name == 'CMIP6':
#        modelnames = ['BCC-CSM2-MR', 'BCC-ESM1', 'CAMS-CSM1-0', 'CanESM5', 'CESM2',
#                      'CESM2-WACCM', 'CNRM-CM6-1', 'CNRM-ESM2-1', 'E3SM-1-0',
#                      'GFDL-ESM4', 'GISS-E2-1-G', 'GISS-E2-1-H', 'HadGEM3-GC31-LL',
#                      'IPSL-CM6A-LR', 'MIROC6', 'MRI-ESM2-0', 'NESM3', 'SAM0-UNICON',
#                      'UKESM1-0-LL', 'EC-Earth3-Veg', 'MIROC-ES2L', 'MRI-ESM2']
#    elif cdict_name == 'CMIP5':
#        modelnames = ['bcc-csm1-1', 'CanESM2', 'CESM1-BGC', 'GFDL-ESM2M', 'HadGEM2-ES',\
#                    'IPSL-CM5A-LR', 'NorESM1-ME', 'MRI-ESM1', 'MPI-ESM-LR']#'MIROC-ESM', 'BNU-ESM']
#    elif cdict_name == 'CMIP5and6':
#        modelnames = get_modelnames_long('CMIP5')+get_modelnames_long('CMIP6')
#    return modelnames

#-------------------------------------------------------------------------------------
def get_num_models(cdict_name):
    modelnames = get_modelnames_short(cdict_name)
    num_models = len(modelnames)
    return num_models

#-------------------------------------------------------------------------------------
def get_PI_adjustment(cdict_name):
    if cdict_name == 'CMIP6':
        pi_adjustment = [0, 0, 3351,
                         500, 0, 110,
                         100, 20, 0,
                         1600, 0, 0] # NEED TO CHECK LAST 3
    elif cdict_name == 'CMIP5':
        pi_adjustment = [0, 471, 100,
                         0, 0, 0,
                         900, 30]
    elif cdict_name == 'CMIP5and6':
        pi_adjustment = get_PI_adjustment('CMIP5')+get_PI_adjustment('CMIP6')
    return pi_adjustment
#-------------------------------------------------------------------------------------
def get_line_width(cdict_name):
    if cdict_name == 'CMIP6':
        linewidth = 4
    elif cdict_name == 'CMIP5':
        linewidth = 4
    elif cdict_name == 'CMIP5and6':
        len_cmip5 = get_num_models('CMIP5')
        len_cmip6 = get_num_models('CMIP6')
        cmip5_linewidth = [get_line_width('CMIP5')] * len_cmip5
        cmip6_linewidth = [get_line_width('CMIP6')] * len_cmip6
        linewidth = cmip5_linewidth+cmip6_linewidth
    return linewidth

def get_line_style(cdict_name):
    if cdict_name == 'CMIP6':
        linestyle = '-'
    elif cdict_name == 'CMIP5':
        linestyle = ':'
    elif cdict_name == 'CMIP5and6':
        len_cmip5 = get_num_models('CMIP5')
        len_cmip6 = get_num_models('CMIP6')
        cmip5_lines = [get_line_style('CMIP5')] * len_cmip5
        cmip6_lines = [get_line_style('CMIP6')] * len_cmip6
        linestyle = cmip5_lines+cmip6_lines
    return linestyle

def get_marker_style(cdict_name):
    if cdict_name == 'CMIP6':
        markerstyle = 'v'
    elif cdict_name == 'CMIP5':
        markerstyle = 'o'
    elif cdict_name == 'CMIP5and6':
        len_cmip5 = get_num_models('CMIP5')
        len_cmip6 = get_num_models('CMIP6')
        cmip5_markers = [get_marker_style('CMIP5')] * len_cmip5
        cmip6_markers = [get_marker_style('CMIP6')] * len_cmip6
        markerstyle = cmip5_markers+cmip6_markers
    return markerstyle

def get_colors(cdict_name):
    cmip6_colors = ['lightcoral', 'darkorchid', 'seagreen', 
                    'mediumblue', 'darkorange', 'firebrick',
                    'thistle', 'gold', 'darkgoldenrod',
                    'cornflowerblue', 'mediumturquoise','grey']
    cmip5_colors = ['darkorchid', 'seagreen', 'mediumblue',
                    'thistle', 'firebrick', 'gold',
                    'cornflowerblue', 'mediumturquoise']
    if cdict_name == 'CMIP6':
        return cmip6_colors
    elif cdict_name == 'CMIP5':
        return cmip5_colors
    elif cdict_name == 'CMIP5and6':
        return cmip5_colors + cmip6_colors
