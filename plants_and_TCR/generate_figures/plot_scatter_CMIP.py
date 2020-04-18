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

FONTSIZE=72
MARKERSIZE=33
MARKEREDGEWIDTH=4
ALPHA = 0.7
LINEWIDTH=9
FIGSIZE=[39.9,30]
CMIP6_CUTOFF = 8

rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

def plot_scatter_CMIP(xvals, yvals, xlims, ylims,
                      one_to_one_line=False, fig_dims=FIGSIZE, markersize=MARKERSIZE,
                      xlabel=None, ylabel=None, filepath=None, legend_on=False, 
                      filled=True, dt=None, axes_on=False,cross_scalar=0.1):
    xmin=xlims[0]
    xmax=xlims[1]
    ymin = ylims[0]
    ymax = ylims[1]
    
    plt.rcParams.update({'font.size': FONTSIZE})
    fig, ax = plt.subplots(figsize=(fig_dims[0],fig_dims[1]))
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
    xrange = xmax-xmin
    yrange = ymax-ymin
    xlims_means = np.array([-cross_scalar*xrange, cross_scalar*xrange])
    ylims_means = np.array([-cross_scalar*yrange, cross_scalar*yrange])
    
    if one_to_one_line:
        plt.plot(xlims, xlims,
                 color='silver', alpha=0.5, ls='-', linewidth=(LINEWIDTH+2)*2)
    if axes_on:
        plt.plot(xlims, [0,0],
                 color='silver', alpha=0.5, ls='-', linewidth=(LINEWIDTH+2)*2)
        plt.plot([0,0], ylims,
                 color='silver', alpha=0.5, ls='-', linewidth=(LINEWIDTH+2)*2)
    
    plt.plot(xlims_means+multimodel_mean_xvals_CMIP6,
             [multimodel_mean_yvals_CMIP6, multimodel_mean_yvals_CMIP6],
             color='black', linestyle='-', linewidth=LINEWIDTH*2,
             alpha=ALPHA, label='CMIP6 Mean')
    plt.plot([multimodel_mean_xvals_CMIP6, multimodel_mean_xvals_CMIP6],
             ylims_means+multimodel_mean_yvals_CMIP6, 
             color='black', linestyle='-', linewidth=LINEWIDTH*2, alpha=ALPHA)
    plt.plot(xlims_means+multimodel_mean_xvals_CMIP5,
             [multimodel_mean_yvals_CMIP5, multimodel_mean_yvals_CMIP5],
             color='black',linestyle=':', linewidth=LINEWIDTH*1.5, alpha=ALPHA, label='CMIP5 Mean')
    plt.plot([multimodel_mean_xvals_CMIP5, multimodel_mean_xvals_CMIP5],
             ylims_means+multimodel_mean_yvals_CMIP5, 
             color='black',linestyle=':', linewidth=LINEWIDTH*1.5, alpha=ALPHA)
    
    # Plot points for each model
    for i in range(0,len(yvals)):
        plt.plot(xvals[i], yvals[i], label=MODELNAMES[i],
                 marker=SYMBOLS[i], linestyle=LINESYMBOLS[i], linewidth=LINEWIDTH,
                 color=COLORS[i], markersize=markersize, 
                 fillstyle=fillstyle_choice, markeredgewidth=MARKEREDGEWIDTH)
        
    # Adjust plot settings
    plt.xlim(xlims)
    plt.ylim(ylims)
    if dt is not None:
        plt.yticks(np.arange(ylims[0], ylims[1]+dt, dt))
        if ylims[1]==xlims[1]:
            plt.xticks(np.arange(xlims[0], xlims[1]+dt, dt))
    
    plt.grid()
    
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if legend_on:
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')

    
    # Save figure
    if filepath is not None:
        fig.savefig(filepath+'.png', bbox_inches='tight')