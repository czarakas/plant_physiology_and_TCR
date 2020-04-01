import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

####################### Set up directory structure ######################
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import co2_concentrations
from plants_and_TCR.analysis_parameters import params
from plants_and_TCR.analyze_data import make_tcr_dataset
from plants_and_TCR.analyze_data import moving_average as movingaverage

CDICT_NAMES=params.CDICT_NAMES
PATH_FIGURES = directory_information.DIR_OUTPUT_FIGURES
CO2_1PCTCO2 = co2_concentrations.co2_1pctco2
DEFAULT_VARNAME = params.DEFAULT_VARNAME
CDICT_NAMES = params.CDICT_NAMES
runnames_all = params.RUNNAMES_ALL
CMIP_linestyles = params.CMIP_LINESTYLES
FONTSIZE=72

def plot_climate_response_timeseries(averageType,
                                     tcr_type,
                                     ylims,
                                     plttitle,
                                     tcr_dict,
                                     end_yr = 70,
                                     smooth_len = 20,
                                     dt=0.1,
                                     smoothing = True,
                                     varname=DEFAULT_VARNAME,
                                     legend_on=True,
                                     filepath=None,
                                    fig_size=[45,30]):
    """Creates time series with CO2 concentration on x-axis
    and average temperature change on y-axis"""
    plt.rcParams.update({'font.size': FONTSIZE})
    [y1, y2] = ylims
    x1 = 0
    x2_axis = 140
    fig = plt.figure(figsize=(fig_size[0], fig_size[1]))
    ax1 = plt.axes()
    linewidth = 9

    ####################### Make rectangles indicating averaging period ############################
    ax1.plot([CO2_1PCTCO2[end_yr], CO2_1PCTCO2[end_yr]], [y1, y2], linestyle='-', color='gray')
    ax1.plot([CO2_1PCTCO2[x1], CO2_1PCTCO2[x2_axis]], [0, 0], linestyle='-', color='gray')
    ax1.add_patch(mpl.patches.Rectangle((CO2_1PCTCO2[end_yr-10], y1),
                                        (CO2_1PCTCO2[end_yr+10] - CO2_1PCTCO2[end_yr-10]),
                                        y2-y1, fill=True, color='lightgray'))

    for cdict_name in CDICT_NAMES:
        linestyle = get_CMIP_info.get_line_style(cdict_name)
        colors = get_CMIP_info.get_colors(cdict_name)
        [_, _, modelnames] = get_CMIP_info.get_CMIP_info(cdict_name)
        runname_1pctco2 = runnames_all[2]
        if cdict_name=='CMIP5':
            x2 = 121
        elif cdict_name=='CMIP6':
            x2 = 131
            
        for m in range(0, np.size(modelnames)):
            modelname = modelnames[m]
            nametag = modelname+'_'+tcr_type+'_'+varname+'_'+averageType
            if nametag in tcr_dict:
                ds_annual = tcr_dict[nametag]

                plotvals_unsmoothed = ds_annual.values

                plotvals_smoothed = movingaverage.movingaverage(plotvals_unsmoothed, smooth_len)
                co2_smoothed = movingaverage.movingaverage(CO2_1PCTCO2[:, 0], smooth_len)

                if smoothing:
                    len_time = np.size(plotvals_smoothed)
                    if len_time > x2:
                        len_time = x2
                    elif len_time < x2:
                        len_time = len_time
                    xvals = co2_smoothed[0:len_time]
                    yvals = plotvals_smoothed[0:len_time]
                    ax1.plot(xvals, yvals,
                             color=colors[m],
                             linestyle=linestyle,
                             label=modelname,
                             linewidth=linewidth)#+', TCR= '+str(np.round(this_TCR,2)))
                else:
                    len_time = np.size(plotvals)
                    if len_time > x2:
                        len_time = x2
                    xvals = CO2_1PCTCO2[0:len_time]
                    yvals = plotvals[0:len_time]
                    ax1.plot(xvals, yvals,
                             color=colors[m],
                             linestyle=linestyle,
                             label=modelname,
                            linewidth=linewidth)#+', TCR= '+str(np.round(this_TCR,2)))
                    
                if m==0:
                    value_sum = yvals[0:121]
                    num_ind=0
                else:
                    value_sum = value_sum+yvals[0:121]
                    num_ind=num_ind+1
        ax1.plot(xvals[0:121], value_sum/num_ind,
                 color='black',linestyle=linestyle,linewidth=linewidth*2,alpha=0.7)

    # Format Figure
    if legend_on:
        ax1.legend(loc='upper left', bbox_transform='None',
                   fontsize=FONTSIZE*0.8, ncol=4, framealpha=1) #'lower right'
    plt.grid()
    plt.ylim(ylims)
    plt.yticks(np.arange(y1, y2, dt))
    plt.xlim([CO2_1PCTCO2[x1], CO2_1PCTCO2[x2_axis]])
    plt.ylabel('Change in Temperature', wrap=True)
    plt.xlabel('CO$_2$ Concentration (ppm)')
    plt.show()
    
    
    #fname = plttitle
    if filepath is not None:
        fig.savefig(filepath+'.png', bbox_inches='tight')
    return fig