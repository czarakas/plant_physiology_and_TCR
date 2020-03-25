import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

####################### Set up directory structure ######################
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import get_CMIP_info

######------------------Get figure settings
CMIP_CHOICE = 'CMIP5and6'
COLORS = get_CMIP_info.get_colors(CMIP_CHOICE)
LINESYMBOLS=get_CMIP_info.get_line_style(CMIP_CHOICE)
SYMBOLS=get_CMIP_info.get_marker_style(CMIP_CHOICE)
MODELNAMES = get_CMIP_info.get_modelnames_short(CMIP_CHOICE)

FONTSIZE=40
MARKERSIZE=24
MARKEREDGEWIDTH=4
ALPHA = 0.7
LINEWIDTH=7
FIGSIZE=[21,15.8]
CMIP6_CUTOFF = 8

rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

def plot_scatter_CMIP(xvals, yvals, xlims, ylims,
                      one_to_one_line=False,
                      xlabel=None, ylabel=None, filepath=None, legend_on=False, filled=True):
    xmin=xlims[0]
    xmax=xlims[1]
    
    plt.rcParams.update({'font.size': FONTSIZE})
    fig, ax = plt.subplots(figsize=(FIGSIZE[0],FIGSIZE[1]))
    if filled:
        fillstyle_choice='full'
    else:
        fillstyle_choice='none'
    
    # Calculate multi-model means
    multimodel_mean_yvals_CMIP6 = np.nanmean(yvals[CMIP6_CUTOFF:100])
    multimodel_mean_xvals_CMIP6 = np.nanmean(xvals[CMIP6_CUTOFF:100])
    multimodel_mean_yvals_CMIP5 = np.nanmean(yvals[0:CMIP6_CUTOFF])
    multimodel_mean_xvals_CMIP5 = np.nanmean(xvals[0:CMIP6_CUTOFF])
    
    # Plot multi-model means
    plt.plot(xlims, [multimodel_mean_yvals_CMIP6, multimodel_mean_yvals_CMIP6],
             color='black', linestyle='-', linewidth=LINEWIDTH, alpha=ALPHA)
    plt.plot([multimodel_mean_xvals_CMIP6, multimodel_mean_xvals_CMIP6], xlims, 
             color='black', linestyle='-', linewidth=LINEWIDTH, alpha=ALPHA)
    plt.plot(xlims, [multimodel_mean_yvals_CMIP5, multimodel_mean_yvals_CMIP5],
             color='black',linestyle=':', linewidth=LINEWIDTH, alpha=ALPHA)
    plt.plot([multimodel_mean_xvals_CMIP5, multimodel_mean_xvals_CMIP5], xlims, 
             color='black',linestyle=':', linewidth=LINEWIDTH, alpha=ALPHA)
    
    # Plot points for each model
    for i in range(0,len(yvals)):
        plt.plot(xvals[i], yvals[i], 
                 marker=SYMBOLS[i], linestyle=LINESYMBOLS[i],
                 color=COLORS[i], label=MODELNAMES[i],
                 markersize=MARKERSIZE, fillstyle=fillstyle_choice, linewidth=0, markeredgewidth=MARKEREDGEWIDTH)
        
    # Adjust plot settings
    plt.xlim(xlims)
    plt.ylim(ylims)
    if one_to_one_line:
        plt.plot(xlims, xlims,
                 color='silver', alpha=0.5, ls='-', linewidth=LINEWIDTH*2)
    plt.grid()
    
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if legend_on:
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')

    
    # Save figure
    if filepath is not None:
        filepath=FIGURE_PATH+'land_ocean_T_contrast_scatter'
        fig.savefig(filepath+'.png', bbox_inches='tight')