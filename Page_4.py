import os
import numpy as np
import xarray as xr
from pylab import rcParams
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm


def plot_map(ds, colormap, k, mticks, option):
    # Plot settings
    import numpy as np
    import xarray as xr
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    from matplotlib import rcParams

    font = {'family': option['font']}
    matplotlib.rc('font', **font)

    params = {'backend': 'ps',
              'axes.labelsize': option['labelsize'],
              'grid.linewidth': 0.2,
              'font.size': option['labelsize'],
              'xtick.labelsize': option['xtick'],
              'xtick.direction': 'out',
              'ytick.labelsize': option['ytick'],
              'ytick.direction': 'out',
              'legend.handlelength': 1,
              'legend.handleheight': 1,
              'savefig.bbox': 'tight',
              'axes.unicode_minus': False,
              "mathtext.default": "regular",
              'text.usetex': False}
    rcParams.update(params)

    # Set the region of the map based on self.Max_lat, self.Min_lat, self.Max_lon, self.Min_lon
    # Extract variables
    lat = ds.lat  # .values
    lon = ds.lon  # .values
    # lat, lon = np.meshgrid(lat[::-1], lon)
    option['min_lon'], option['max_lon'], option['min_lat'], option[
        'max_lat'] = lon.min().values, lon.max().values, lat.min().values, lat.max().values
    # var = ds.transpose("lon", "lat")[:, ::-1].values

    fig = plt.figure(figsize=(option['x_wise'], option['y_wise']))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    var = ds.values
    # cs = ax.contourf(lon, lat, var, levels=levels, cmap=colormap, norm=normalize, extend=option['extend'])
    cs = ax.imshow(var[::-1, :], cmap=colormap,
                   extent=(option['min_lon'], option['max_lon'], option['min_lat'], option['max_lat']),
                   vmin=option['vmin'], vmax=option['vmax'])
    ax.set_extent([option['min_lon'], option['max_lon'], option['min_lat'], 45])
    coastline = cfeature.NaturalEarthFeature(
        'physical', 'coastline', '50m', edgecolor='0.6', facecolor='none')
    rivers = cfeature.NaturalEarthFeature(
        'physical', 'rivers_lake_centerlines', '110m', edgecolor='0.6', facecolor='none')
    ax.add_feature(cfeature.LAND, facecolor='0.95')
    ax.add_feature(coastline, linewidth=0.6)
    ax.add_feature(cfeature.LAKES, alpha=1, facecolor='white', edgecolor='white')
    ax.add_feature(rivers, linewidth=0.8)
    ax.gridlines(draw_labels=False, linestyle=':', linewidth=0.7, color='grey', alpha=0.8)

    ax.set_xticks(np.arange(-70, -130, - 10)[::-1], crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(45, 24, -10)[::-1], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # ax.set_xlabel(option['xticklabel'], fontsize=option['xtick'] + 1, labelpad=20)
    # ax.set_ylabel(option['yticklabel'], fontsize=option['ytick'] + 1, labelpad=40)
    # plt.title(option['title'], fontsize=option['title_size'])

    pos = ax.get_position()  # .bounds
    left, right, bottom, width, height = pos.x0, pos.x1, pos.y0, pos.width, pos.height
    cbaxes = fig.add_axes([left + width / 20 , bottom - 0.1, width / 20 * 18, 0.03])

    cb = fig.colorbar(cs, cax=cbaxes, ticks=mticks, spacing='uniform', label=option['colorbar_label'], drawedges=False,
                      orientation='horizontal')
    cb.ax.yaxis.set_tick_params(direction='out', width=1.5)  # 微调
    cb.set_label('Percent bias', fontsize=option['labelsize'] + 2, fontweight='bold')

    plt.savefig(f'Page_4.jpg', format=f'jpg', dpi=300)
    plt.savefig(f'Page_4.eps', format=f'eps', dpi=300)
    plt.close()


def make_plot_index(ds, option):
    ticks = matplotlib.ticker.MultipleLocator(base=option['colorbar_ticks'])
    mticks = ticks.tick_values(vmin=option['vmin'], vmax=option['vmax'])
    mticks = [round(tick, 2) if isinstance(tick, float) and len(str(tick).split('.')[1]) > 2 else tick for tick in
              mticks][1:-1]
    cmap = cm.get_cmap(option['cmap'])
    plot_map(ds, cmap, 'metrics', mticks, option)


if __name__ == '__main__':
    file = "/media/zhwei/data02/Plot/Crop_Yield_Corn_ref_CropYield_GDHY_sim_CoLM2024_percent_bias.nc"
    metrics = 'percent_bias'
    ds = xr.open_dataset(file)[metrics]
    option = {
        'vmin': -100,
        'vmax': 100,
        'colorbar_ticks': 20,
        'colorbar_label': metrics.replace('_', ' ').title(),
        'extend': 'neither',  # Default value
        'cmap': 'RdYlBu_r',
        'colorbar_position': 'horizontal',
        'labelsize': 20,
        'xtick': 20,
        'ytick': 20,
        'x_wise': 10,
        'y_wise': 6,

        'min_lon': -125,
        'max_lon': -65,
        'min_lat': 20,
        'max_lat': 52,
        'font': 'Times New Roman',

    }
    make_plot_index(ds, option)
# region = [-124, -66, 24, 50]

# level = np.linspace(-100, 100, 11)
# cmap = cmaps.cmp_b2r
