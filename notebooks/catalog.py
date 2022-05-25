"""
Placeholder module for real catalog functionality
"""
import os
from glob import glob

import cftime
import xarray as xr

USER = os.environ['USER']

component_system = dict(
    pop='ocn',
    cam='atm',
    cice='ice',
)


def _preprocess_pop(ds):
    tb_var = ds.time.attrs["bounds"]
    time_units = ds.time.units
    calendar = ds.time.calendar

    ds['time'] = cftime.num2date(
        ds[tb_var].mean('d2'),
        units=time_units,
        calendar=calendar,
    )
    ds.time.encoding.update(dict(
        calendar=calendar,
        units=time_units,
    ))
    return ds.set_coords(["KMT", "TAREA"])
    

def _get_assets(case, component, stream, archive_root):
    """
    list file assets assuming short term archiver has run
    """
    
    try:
        system = component_system[component]
    except KeyError:
        print(f'missing system definition for {component}')
        raise
        
    glob_expression = f'{archive_root}/{case}/{system}/hist/{case}.{component}.{stream}.*.nc'
    assets = sorted(glob(glob_expression))
    
    assert assets, f'no files found.\nsearched using: {glob_expression}'

    return assets


def to_dataset_dict(case, component, stream, archive_root=None, cdf_kwargs={}):
    
    if archive_root is None:
        archive_root = f'/glade/scratch/{USER}/archive'
    assert os.path.exists(archive_root)
    
    if isinstance(case, str):
        case = [case]
        
    if isinstance(component, str):
        component = [component]
    
    if isinstance(stream, str):
        stream = [stream]

        
    component_cdf_kwargs = dict(
        pop=dict(
            coords="minimal",
            combine="by_coords",
            compat="override",
            preprocess=_preprocess_pop,
            decode_times=False,
        ),
    )
                        
    dsets = {}
    for case_i, component_i, stream_i in zip(case, component, stream):        
        assets = _get_assets(case_i, component_i, stream_i, archive_root)
        key = f'{case_i}.{component_i}.{stream_i}'
        cdf_kwargs = component_cdf_kwargs[component_i]
        
        dsets[key] = xr.open_mfdataset(assets[:12], **cdf_kwargs)
                
    return dsets