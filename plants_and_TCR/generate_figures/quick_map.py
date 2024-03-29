"""
Makes a map given user parameters and data (2D), lat, lon values
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

def quick_map(mapdata, lat, lon, 
              title=None, cb_ttl=None,
              cmap=plt.cm.viridis, clim=None, norm=None, 
              contours=False, color_interval=0.2, extend_choice='both', cbar_inds=None, clevels=None,
              filepath=None, 
              sighatch=False, p=None, sigmask=None, markerstyle='x', markersize=0.3, alpha_choice=0.8):
    """ Creates map """

    fig = plt.figure(figsize=(12, 9))

    ax = plt.axes(projection=ccrs.Robinson())
    ax.coastlines(resolution='110m') #learn how to add resolution here??
    ax.set_global()

    cyclic_data, cyclic_lons = add_cyclic_point(mapdata, coord=lon)

    if contours:
        if clevels is None:
            if clim:
                clevels= np.arange(clim[0],clim[1]+color_interval,color_interval)
                cs = plt.contourf(cyclic_lons, lat, cyclic_data, clevels, cmap = cmap, extend=extend_choice,
                                  transform=ccrs.PlateCarree())#, vmin=-1.5, vmax=1.5)
            else:
                cs = plt.contourf(cyclic_lons, lat, cyclic_data, cmap = cmap,
                                  transform=ccrs.PlateCarree())
        else:
            cs = plt.contourf(cyclic_lons, lat, cyclic_data, clevels, cmap = cmap, extend=extend_choice,
                                  transform=ccrs.PlateCarree())
    else:
        if norm:
            cs = plt.pcolormesh(cyclic_lons, lat, cyclic_data,
                                transform=ccrs.PlateCarree())
        else:
            cs = plt.pcolormesh(cyclic_lons, lat, cyclic_data,
                                transform=ccrs.PlateCarree(), norm=norm)

    # Choose your colormap
    plt.set_cmap(cmap)

    if sighatch:
        cyclic_sig, cyclic_lons = add_cyclic_point(sigmask, coord=lon)

        CLN, CLT = np.meshgrid(cyclic_lons, sigmask['lat'])

        # only put the hatches where the sigmask is < p 
        lat_sig = np.where(cyclic_sig < p, CLT, np.nan)
        lon_sig = np.where(cyclic_sig < p, CLN, np.nan)
        
        hatch = ax.scatter(lon_sig,
                           lat_sig,
                           marker=markerstyle,
                           s=markersize,
                           c=[0.6, 0.6, 0.6],
                           alpha=alpha_choice,
                           transform=ccrs.PlateCarree())
    
    ax.patch.set_alpha(1.0)

    if title:
        plt.title(title, fontsize=16, y=1.05, loc='left')

    if clim:
        plt.clim(clim)
        cs.set_clim(clim[0], clim[1])
        cs.set_clim(clim)
        

    if cbar_inds is not None:
        cbar = plt.colorbar(ax=ax, orientation='horizontal',
                        extend='both', pad=.02, shrink=0.9, ticks=cbar_inds)
    else:
        cbar = plt.colorbar(ax=ax, orientation='horizontal',
                        extend='both', pad=.02, shrink=0.9)
    cbar.ax.tick_params(labelsize=14)

    if clim:
        cbar.set_clim(clim)

    if cb_ttl:
        cbar.set_label(cb_ttl, fontsize=14)

    plt.show()

    if filepath:
        fig.savefig(filepath, dpi=300, facecolor=None, edgecolor=None,
                    bbox_inches='tight', transparent=True, pad_inches=0.2, linewidth=2)

        print('done saving file')

    plt.close()

    return fig, ax, cs, cbar
