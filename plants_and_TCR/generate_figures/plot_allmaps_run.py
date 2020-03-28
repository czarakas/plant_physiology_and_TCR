import sys
import pickle
import matplotlib.pyplot as plt
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs

from plants_and_TCR.analyze_data import grab_cmip_dataset
from plants_and_TCR.analysis_parameters import get_CMIP_info
from plants_and_TCR.analysis_parameters import directory_information
from plants_and_TCR.analysis_parameters import co2_concentrations

DEFAULT_VARNAME = 'tas'
CMIP_NAMES = ['CMIP5', 'CMIP6']
FONTSIZE=20

CO2_1PCTCO2 = co2_concentrations.co2_1pctco2
dir_CMIPdicts = directory_information.DIR_DATA_DICTIONARIES
cmip_dict = pickle.load(open(dir_CMIPdicts+'cmip_dict.pickle',"rb"))
runnames_all = ['1pctCO2-rad','1pctCO2-bgc','1pctCO2','piControl']

def plot_allmaps_run(runname_inds,
                     varname,
                     end_yr=70,
                     clim=None,
                     unitname=None,
                     cmap=None,
                     filename=None,
                     mask_type=None,
                     show_fig=True):
    latdata_all = dict()
    londata_all = dict()
    mapdata_all = dict()
    fig = plt.figure(figsize=(30, 20))
    
    md = 0
    ############### Get information for CMIP #########################################
    for cmipchoice in CMIP_NAMES:
        modellist= get_CMIP_info.get_modelnames_short(cmipchoice)
        PIadjustment=get_CMIP_info.get_PI_adjustment(cmipchoice)
        runname1 = runnames_all[runname_inds[0]] #1pctCO2-rad
        runname2 = runnames_all[runname_inds[1]] #1pctCO2

        #Loop over models
        for modelname in modellist:
            # get datasets
            ds2 = grab_cmip_dataset.grab_cmip_dataset(cmip_dict,
                                                      modelname,
                                                      runname2,
                                                      varname)
            ds1 = grab_cmip_dataset.grab_cmip_dataset(cmip_dict,
                                                      modelname,
                                                      runname1,
                                                      varname)
            
            
            ax=plt.subplot(5, 4, md+1, projection=ccrs.Robinson())
            plt.title(modelname, fontsize=FONTSIZE, y=1)

            if ((ds2 is not None) and (ds1 is not None)): #
                vals2 = ds2[varname].groupby('time.year').mean(dim='time')
                vals1 = ds1[varname].groupby('time.year').mean(dim='time')
                if runname1 == 'piControl':
                    vals1['year'] = vals1['year']-PIadjustment[md]
                elif runname2 == 'piControl':
                    vals2['year'] = vals2['year']-PIadjustment[md]
                delta = vals1-vals2
                delta = delta.isel(year=range((end_yr-10), (end_yr+10)))
                
                if mask_type == 'land':
                    land_area_mask = cmip_dict[modelname +'_' +'sftlf']['sftlf'].values/100
                    delta = delta*land_area_mask
                elif mask_type == 'ocean':
                    land_area_mask = cmip_dict[modelname +'_' +'sftlf']['sftlf'].values/100
                    delta = delta*(1-land_area_mask)
                else:
                    pass
                
                ######################## Make map for subplot ##########################
                mapdata = delta.mean(dim='year').values
                lat = ds1['lat'].values
                lon = ds1['lon'].values  
                mapdata_all[modelname] = mapdata
                latdata_all[modelname] = lat
                londata_all[modelname] = lon

                ax.coastlines()
                ax.set_global()
                cyclic_data, cyclic_lons = add_cyclic_point(mapdata, coord=lon)

                # plot our data:
                cs = plt.pcolormesh(cyclic_lons, lat, cyclic_data, transform=ccrs.PlateCarree())


                # Choose your colormap
                if cmap:
                    plt.set_cmap(cmap)
                else:
                    plt.set_cmap(plt.cm.RdYlBu)

                if clim: 
                    plt.clim(clim) 
            md = md+1

    ################ Full figure formatting ##########################################

    # adjust the subplots to make space for a colorbar and to decrease spacing between subplots
    plt.subplots_adjust(bottom=0.08, right=None, top=None, wspace=.02, hspace=.15)

    # make an axes for the colorbar
    cax = plt.axes([0.25, 0.05, 0.5, 0.018], frameon='no')

    # add a colorbar:
    cbar = plt.colorbar(cax=cax,orientation='horizontal', extend='both')
    cbar.ax.tick_params(labelsize=FONTSIZE) 

    # set color limits for the colorbar
    if clim:
        cs.set_clim(clim)
        cbar.set_clim(clim)

    # put a label on the colorbar, e.g. with the units of your field
    cbar.set_label(varname, fontsize=14)

    # show the plot:
    if show_fig:
        plt.show()

    # save and close the plot
    if filename is not None:
        fig.savefig(filename +'.png', bbox_inches='tight')
        print('done saving file')
    plt.close()
    
    return fig, mapdata_all, latdata_all, londata_all
    
    ##################################
    
def plot_allmaps_from_data(mapdata_all,
                           latdata_all,
                           londata_all,
                           varname,
                           clim=None,
                           unitname=None,
                           cmap=None,
                           filename=None,
                           show_fig=True):
    fig = plt.figure(figsize=(30, 20))
    
    md = 0
    ############### Get information for CMIP #########################################
    for cmipchoice in CMIP_NAMES:
        modellistF = get_CMIP_info.get_modelnames_short(cmipchoice)

        #Loop over models
        for modelname in modellistF:
            ax=plt.subplot(5, 4, md+1, projection=ccrs.Robinson())
            plt.title(modelname, fontsize=FONTSIZE, y=1)
            
            if modelname in mapdata_all: #
                mapdata = mapdata_all[modelname]
                lat = latdata_all[modelname]
                lon = londata_all[modelname]
                
                ######################## Make map for subplot ##########################

                ax.coastlines()
                ax.set_global()
                cyclic_data, cyclic_lons = add_cyclic_point(mapdata,coord=lon)

                # plot our data:
                cs = plt.pcolormesh(cyclic_lons, lat, cyclic_data, transform=ccrs.PlateCarree())
                

                # Choose your colormap
                if cmap:
                    plt.set_cmap(cmap)
                else:
                    plt.set_cmap(plt.cm.RdYlBu)

                if clim:
                    plt.clim(clim) 
            md = md+1

    ################ Full figure formatting ##########################################

    # adjust the subplots to make space for a colorbar and to decrease spacing between subplots
    plt.subplots_adjust(bottom=0.08, right=None, top=None, wspace=.02, hspace=.15)

    # make an axes for the colorbar
    cax = plt.axes([0.25, 0.05, 0.5, 0.018], frameon='no')

    # add a colorbar:
    cbar = plt.colorbar(cax=cax,orientation='horizontal', extend='both')
    cbar.ax.tick_params(labelsize=FONTSIZE)

    # set color limits for the colorbar
    if clim:
        cs.set_clim(clim)
        cbar.set_clim(clim)

    # put a label on the colorbar, e.g. with the units of your field
    cbar.set_label(varname, fontsize=FONTSIZE)

    # show the plot:
    if show_fig:
        plt.show()

    # save and close the plot
    if filename is not None:
        fig.savefig(filename +'.png', bbox_inches='tight')
        print('done saving file')
    plt.close()
    
    return fig
    
    ##################################
