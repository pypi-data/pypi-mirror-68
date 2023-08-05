import copy
from .gitinfo import __gitVersion__, __gitPath__
import os
import netCDF4 as nc
import numpy as np

from snowav.database.database import convert_watershed_names
from snowav import __version__
from tablizer.tablizer import summarize, store


def calculate(array, pixel, masks=None, method='sum', convert=None,
              units='TAF', decimals=3):
    '''
    Calculate values from iSnobal output snow.nc and em.nc files
    and convert to desired units:
        mean SWE depth
        total SWE volume
        total 'available' SWE volume (based on cold content)
        total 'unavailable' SWE volume (based on cold content)
        mean snow depth
        total SWI volume
        mean SWI depth
        mean evaporation
        total cold content
        mean density

    Applies all masks that are passed. Typically this is a basin mask, an
    elevation bin mask, and a snow mask if a 0 value has meaning for the
    calculated value (such as a mean density).

    This is referenced as an example in scripts.sample_process.py and README,
    so if changes are made those may require updating.

    Args
    ------
    array : np.array
        iSnobal model outputs from snow.nc or em.nc file
    pixel : int
        [m] model pixel size
    masks : list
        list of np.array or bool masks, optional
    method : str
        method of calcution, options are 'sum', 'mean'
    convert : str
        conversion property, options are 'depth', 'snow_depth', 'volume', None
    units : str
        conversion units, options are 'TAF', 'SI'
    decimals : int

    Returns
    ------
    value : np.array

    '''

    method_options = ['sum', 'mean']
    unit_options = ['TAF', 'SI']

    if method not in method_options:
        raise Exception('method options are {}'.format(method_options))

    if units not in unit_options:
        raise Exception('units options are {}'.format(unit_options))

    if units == 'TAF':

        # mm to inches
        if convert == 'depth':
            factor = 0.03937

        # m to inches
        elif convert == 'snow_depth':
            factor = 39.37

        # mm/pixel to TAF
        elif convert == 'volume':
            factor = (pixel ** 2) * 0.000000810713194 * 0.001

        else:
            factor = 1

    if units == 'SI':

        # mm to cm
        if convert == 'depth':
            factor = 0.1

        # m to cm
        elif convert == 'snow_depth':
            factor = 100

        # mm/pixel to MM^3
        elif convert == 'volume':
            factor = (pixel ** 2) * 0.000000810713194 * 1233.48 / 1e9

        else:
            factor = 1

    if convert is None:
        factor = 1

    if masks is not None:
        if type(masks) != list:
            masks = [masks]

        for i, mask in enumerate(masks):
            if mask.shape != array.shape:
                raise Exception('mask {}, {} and array {} do not '
                                'match'.format(i, mask.shape, array.shape))

            # use nan because output zero values have meaning
            mask = mask.astype('float')
            mask[mask < 1] = np.nan
            array = array * mask

    # make calculation and convert
    if method == 'sum':
        if np.sum(np.isnan(array)) == array.size:
            value = np.nan
        else:
            value = np.nansum(array) * factor

    if method == 'mean':
        value = np.nanmean(array) * factor

    if not np.isnan(value):
        value = value.round(decimals)

    return value


def snow_line(array, dem, masks=None, limit=0.01):
    """ Calculate mean snow line in image.

    Args
    ------
    array {arr}: snow.nc swe_z
    dem {arr}: dem
    masks {list}: list of masks to apply
    limit {float}: limit for swe_z line

    Returns
    ------
    value {int}: snow line
    """

    if masks is not None:
        if type(masks) != list:
            masks = [masks]

        for i, mask in enumerate(masks):
            if mask.shape != array.shape:
                raise Exception('mask {}, {} and array {} do not '
                                'match'.format(i, mask.shape, array.shape))

            # use nan because output zero values have meaning
            mask = mask.astype('float')
            mask[mask < 1] = np.nan
            array = array * mask

    ix = array > limit
    if np.sum(ix) > 0:
        value = int(np.nanpercentile(dem[ix].flatten(), [2, 90])[0])
    else:
        value = np.nan

    return value


def masks(dempath, convert, plotorder=None, plotlabels=None):
    '''
    Load dem, build snowav masks dictionary from topo.nc file. See
    CoreConfig.ini for more information on some config options and behavior.

    Currently 'Cherry Creek' is an exception.

    Args
    ------
    dempath : str
        Path to topo.nc file, which is intended to be built by basin_setup
        package.
    convert : bool
        Convert watershed name to existing snowav database
    plotorder : list
        Optional, default is all mask strings that appear in topo.nc file found
        in dempath.
    plotlabels : list
        Optional, default is mask_names.

    Returns
    ------
    out : dict

    '''

    out = {}
    masks = {}
    labels = {}
    logger = []

    if not os.path.isfile(dempath):
        raise Exception('dempath {} not a valid file'.format(dempath))

    ncf = nc.Dataset(dempath, 'r')
    dem = ncf.variables['dem'][:]
    veg_type = ncf.variables['veg_type'][:]

    mask_names = [ncf.variables['mask'].long_name]
    mask_names_total = ncf.variables['mask'].long_name

    for v in ncf.variables.items():

        # without the space before mask we get the basin total twice
        if ' mask' in v[0]:
            mask_names += [v[1].long_name]

    if plotorder is None:
        plotorder = mask_names
        plotorder = ['Cherry Creek' if x == 'Cherry' else x for x in plotorder]

    else:
        if len(plotorder) > len(mask_names):
            raise Exception(' Config option [snowav] masks: {} for {}, but '
                            'found {}'.format(plotorder, dempath, mask_names))

        for lbl in plotorder:
            if (lbl not in mask_names) and (lbl != 'Cherry Creek'):
                raise Exception(' Config option [snowav] masks: {} for {}, but '
                                'found {}'.format(plotorder, dempath, mask_names))

    if plotlabels is None:
        for name in plotorder:
            labels[name] = name

    else:
        if len(plotlabels) != len(plotorder):
            logger.append(' Config option [snowav] plotlabels {} not equal to '
                          '{}, setting plotlabels to '
                          'defaults'.format(plotlabels, plotorder))
            for name in plotorder:
                labels[name] = name

        elif plotlabels is None:
            for name in plotorder:
                labels[name] = name

        else:
            for i, name in enumerate(plotorder):
                logger.append(' Assigning plot label {} '.format(plotlabels[i]) +
                              'for topo.nc long_name field {}'.format(name))
                labels[name] = plotlabels[i]

    nrows = len(dem[:, 0])
    ncols = len(dem[0, :])

    for lbl in plotorder:

        if lbl == 'Cherry Creek':
            nclbl = 'Cherry'
        else:
            nclbl = lbl

        if lbl != mask_names_total:
            masks[lbl] = {'mask': ncf[nclbl + ' mask'][:], 'label': lbl}
        else:
            masks[lbl] = {'mask': ncf['mask'][:], 'label': nclbl}

    ncf.close()

    if convert:
        old_key = plotorder[0]
        new_key = convert_watershed_names(old_key)
        masks[new_key] = masks.pop(old_key)
        labels[new_key] = labels.pop(old_key)

    out['dem'] = dem
    out['veg_type'] = veg_type
    out['masks'] = masks
    out['nrows'] = nrows
    out['ncols'] = ncols
    out['plotorder'] = plotorder
    out['labels'] = labels
    out['logger'] = logger

    return out


def sum_precip(precip_path, percent_snow_path):
    """ Sum in place for precip and rain images.

    Args
    ------
    precip_path: path to precip.nc
    percent_snow_path: path to percent_snow.nc
    precip_total: array of total precip for the run
    rain_total: array of total rain for the run

    Returns
    ------
    precip: array, daily total precip
    rain: array, daily total rain
    """

    ppt = nc.Dataset(precip_path, 'r')
    percent_snow = nc.Dataset(percent_snow_path, 'r')

    # For the wy2019 daily runs, precip.nc always has an extra hour, but
    # in some WRF forecast runs there are fewer than 24...
    if len(ppt.variables['precip'][:]) > 24:
        nb = 24
    else:
        nb = len(ppt.variables['precip'][:])

    for nb in range(0, nb):
        pre = ppt['precip'][nb]
        ps = percent_snow['percent_snow'][nb]

        if nb == 0:
            rain = np.multiply(pre, (1 - ps))
            precip = copy.deepcopy(pre)
        else:
            rain = rain + np.multiply(pre, (1 - ps))
            precip = precip + copy.deepcopy(pre)

    # rain_total = rain_total + rain
    # precip_total = precip_total + precip

    ppt.close()
    percent_snow.close()

    return precip, rain


def input_summary(path, variable, methods, percentiles, database, location,
                  run_name, basin_id, run_id, masks):
    """ Summarize smrf outputs with tablizer.

    Args
    ------
    path {str}: nc path
    variable {str}: snowav variable
    methods {list}: list of summary methods
    percentiles {arr}: if using percentiles
    database {str}: connector string
    location {str}: database location
    run_name {str}: snowav run name
    basin_id {dict}: snowav basin id
    run_id {int}: snowav run_id
    masks {list}: masks to filter with
    """

    if not os.path.isfile(path):
        raise OSError('invalid file -> {}'.format(path))

    ncf = nc.Dataset(path, 'r')
    array = ncf.variables[variable][:]
    dates = ncf.variables['time'][:]
    date_units = ncf.variables['time'].units
    ncf.close()

    if len(array[:]) > 24:
        nb = 24
    else:
        nb = len(array[:])

    if variable in ['snow_density', 'precip_temp']:
        mask_zero_values = True
    else:
        mask_zero_values = False

    for nb in range(0, nb):
        date = nc.num2date(dates[nb], date_units)
        img = array[nb, :, :]
        results = summarize(img,
                            date,
                            methods,
                            percentiles=[percentiles[0], percentiles[1]],
                            decimals=3,
                            masks=masks,
                            mask_zero_values=mask_zero_values)
        store(results, variable, database, location, run_name, basin_id,
              run_id, date)


def getgitinfo():
    """gitignored file that contains specific SNOWAV version and path

    Input:
        - none
    Output:
        - path to base SNOWAV directory
    """
    # return git describe if in git tracked SMRF
    if len(__gitVersion__) > 1:
        return __gitVersion__

    # return overarching version if not in git tracked SMRF
    else:
        version = 'v' + __version__
        return version


def get_config_header():
    """
    Produces the string for the main header for the config file.
    """
    hdr = ("Configuration File for SNOWAV {0}\n").format(getgitinfo())

    return hdr


def get_snowav_path():
    """gitignored file that contains specific SNOWAV version and path

    Input:
        - none
    Output:
        - path to base SNOWAV directory
    """
    # find the absolute path and return
    snowav_path = os.path.abspath(__gitPath__)

    return snowav_path
