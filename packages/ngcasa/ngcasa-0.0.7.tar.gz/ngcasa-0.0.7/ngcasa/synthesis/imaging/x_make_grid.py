#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from numba import jit
import numpy as np
import math

#Very broken. Need to revisit

def make_grid(vis_dataset, user_grid_parms):
    """
    Grids visibilities from Visibility Dataset.
    If to_disk is set to true the data is saved to disk.
    Parameters
    ----------
    vis_xds : xarray.core.dataset.Dataset
        input Visibility Dataset
    grid_parms : dictionary
          #keys ('chan_mode','imsize','cell','oversampling','support','to_disk','outfile')
    Returns
    -------
    grid_xds : xarray.core.dataset.Dataset

    """
    from numcodecs import Blosc
    import os
    from itertools import cycle
    import dask.array as da
    import xarray as xr
    import dask
    import time
    import copy
    
    from .synthesis_utils._check_parameters import _check_gridder_params
    from .synthesis_utils._standard_grid import _graph_standard_grid
    from .synthesis_utils._gridding_convolutional_kernels import _create_prolate_spheroidal_kernel, _create_prolate_spheroidal_kernel_1D

    grid_parms = copy.deepcopy(user_grid_parms)
    do_psf = False #Is added to grid_parms to reduce the number of graph nodes.
    assert(_check_gridder_params(grid_parms,vis_dataset)), "######### ERROR: Parameter checking failed"

    # Create dask graph of gridding
    grids_and_sum_weights, correcting_cgk_image = _graph_grid(vis_dataset, grid_parms)
    
    if grid_parms['chan_mode'] == 'continuum':
        freq_coords = [da.mean(vis_dataset.coords['chan'].values)]
        imag_chan_chunk_size = 1
    elif grid_parms['chan_mode'] == 'cube':
        freq_coords = vis_dataset.coords['chan'].values
        imag_chan_chunk_size = vis_dataset.DATA.chunks[2][0]

    # Create delayed xarray dataset
    chunks = vis_dataset.DATA.chunks
    n_imag_pol = chunks[3][0]
    grid_dict = {}
    coords = {'chan': freq_coords, 'pol': np.arange(n_imag_pol), 'u': np.arange(grid_parms['imsize_padded'][0]),
              'v': np.arange(grid_parms['imsize_padded'][1])}
    grid_dict['CORRECTING_CGK'] = xr.DataArray(da.array(correcting_cgk_image), dims=['u', 'v'])
    # grid_dict['VIS_GRID'] = xr.DataArray(grids_and_sum_weights[0], dims=['chan','pol','u', 'v'])
    grid_dict['VIS_GRID'] = xr.DataArray(grids_and_sum_weights[0], dims=['u', 'v', 'chan', 'pol'])
    grid_dict['SUM_WEIGHT'] = xr.DataArray(grids_and_sum_weights[1], dims=['chan','pol'])
    grid_xds = xr.Dataset(grid_dict, coords=coords)

    if grid_parms['to_disk'] == True:
        outfile = grid_parms['outfile']
        tmp = os.system("rm -fr " + outfile)
        tmp = os.system("mkdir " + outfile)

        compressor = Blosc(cname='zstd', clevel=2, shuffle=0)
        encoding = dict(zip(list(grid_xds.data_vars), cycle([{'compressor': compressor}])))
        start = time.time()
        xr.Dataset.to_zarr(grid_xds, store=outfile, mode='w', encoding=encoding)
        grid_time = time.time() - start
        print('Grid time ', time.time() - start)

        grid_xds = xr.open_zarr(outfile)
        grid_xds.attrs['grid_time'] = grid_time
        return grid_xds

    else:
        return grid_xds

