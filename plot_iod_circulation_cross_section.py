#!/usr/bin/env python3
"""
Vertical Cross-Section: Zonal-Mean Omega and Zonal Wind During IOD Events

Creates the diagnostic figure requested by supervisor:
- 2-panel figure: (a) Positive IOD, (b) Negative IOD
- Vertical cross-section over continental Africa in latitude (defaults below)
- Zonal average 10°E–50°E (Indian Ocean / East Africa sector; change with --lon-west/--lon-east)
- Omega (vertical velocity, Pa/s): color shading
- Zonal wind (u): contours

Physical interpretation:
- Positive IOD: subsidence over Central Africa → drought; ascent over Horn → rainfall
- Negative IOD: opposite pattern (ascent over Central Africa → rainfall)

Data sources: ERA5 reanalysis (or ICON/MPAS output for Paper 2 validation)

Usage:
  python plot_iod_circulation_cross_section.py [--data-dir PATH] [--output-dir PATH]
  python plot_iod_circulation_cross_section.py --single-panel  # Positive IOD only
  python plot_iod_circulation_cross_section.py --download     # Download ERA5 via CDS API
"""

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from analysis_config import IOD_COMPOSITE_SON_YEARS, IOD_CIRCULATION_DIAGNOSTIC_LON
except ImportError:
    IOD_COMPOSITE_SON_YEARS = {
        'positive': [1994, 1997, 2006, 2012, 2015, 2018, 2019],
        'negative': [1980, 1981, 1992, 1996, 1998],
    }
    IOD_CIRCULATION_DIAGNOSTIC_LON = {'lon_west': 10.0, 'lon_east': 50.0}

# Default IOD event years — same lists as drought composites (analysis_config.py)
POSITIVE_IOD_YEARS = list(IOD_COMPOSITE_SON_YEARS['positive'])
NEGATIVE_IOD_YEARS = list(IOD_COMPOSITE_SON_YEARS['negative'])
# --- Geographic domain (user-controlled via --lat-south / --lat-north / --lon-west / --lon-east) ---
# Approximate mainland Africa N/S extent (round numbers used in many atlases / regional means).
# Southern limit ~ Cape area; northern ~ Tunisia / northern Mediterranean African coast.
AFRICA_CONTINENTAL_LAT_SOUTH = -35.0
AFRICA_CONTINENTAL_LAT_NORTH = 37.0
LAT_SOUTH = AFRICA_CONTINENTAL_LAT_SOUTH
LAT_NORTH = AFRICA_CONTINENTAL_LAT_NORTH
LON_WEST = float(IOD_CIRCULATION_DIAGNOSTIC_LON['lon_west'])
LON_EAST = float(IOD_CIRCULATION_DIAGNOSTIC_LON['lon_east'])
SON_MONTHS = [9, 10, 11]


def find_era5_files(data_dir, var_names=('omega', 'u')):
    """Find ERA5 pressure-level files for omega and u."""
    data_dir = Path(data_dir)
    found = {}
    for var in var_names:
        patterns = [
            f'**/*{var}*pressure*.nc',
            f'**/*{var}*pl*.nc',
            f'**/era5*{var}*.nc',
            f'**/atmospheric/*{var}*.nc',
        ]
        for pat in patterns:
            for f in data_dir.glob(pat):
                if 'drought_reanalysis' not in str(f):
                    found.setdefault(var, []).append(f)
        if var == 'omega':
            # Omega may be named w, omega, vertical_velocity
            for pat in ['**/*omega*.nc', '**/*vertical*.nc', '**/*w_*.nc']:
                for f in data_dir.glob(pat):
                    if 'drought_reanalysis' not in str(f):
                        found.setdefault(var, []).append(f)
    return found


def _has_omega_and_u(ds):
    """Check if dataset has both omega and u on pressure levels."""
    lev_dims = ['level', 'lev', 'pressure_level', 'plev', 'isobaricInhPa']
    omega_var = u_var = None
    for v in ds.data_vars:
        v_lower = v.lower()
        if v_lower == 'v':
            continue
        if any(x in v_lower for x in ['omega', 'w', 'vertical_velocity', 'vertical']):
            if any(ld in ds[v].dims for ld in lev_dims):
                omega_var = v
        elif v_lower in ('u', 'u_component', 'u_component_of_wind', 'u_wind'):
            if any(ld in ds[v].dims for ld in lev_dims):
                u_var = v
    return omega_var, u_var


def load_era5_pressure_levels(data_dir, var_name, pressure_levels=None, prefer_file=None):
    """Load ERA5 variable on pressure levels. Returns xarray DataArray.
    Looks in: data_dir/atmospheric/, data_dir/era5/, data_dir/
    ERA5 CDS output: variable 'w' (vertical velocity) or 'u' (zonal wind).
    If prefer_file is set, try that file first (ensures omega and u from same source)."""
    data_dir = Path(data_dir)
    if pressure_levels is None:
        pressure_levels = list(range(1000, 0, -50))

    search_paths = [
        data_dir / 'atmospheric',
        data_dir / 'era5',
        data_dir,
    ]
    files = []
    for p in search_paths:
        if not p.exists():
            continue
        for ext in ['*.nc', '*.grib', '*.grb', '*.grib2']:
            for f in p.glob(f'**/{ext}'):
                if 'drought_reanalysis' in str(f):
                    continue
                files.append(f)
    if not files:
        logger.warning(f"No atmospheric files (.nc, .grib) found in {data_dir}/atmospheric, {data_dir}/era5, or {data_dir}")

    # Prefer files with var name in filename (from download_era5_omega_u.py)
    if var_name == 'omega':
        pref = [f for f in files if 'omega' in f.name.lower() or 'vertical' in f.name.lower()]
        # GRIB from CDS often has hash filename; include all GRIB for omega search
        pref = pref + [f for f in files if f.suffix.lower() in ('.grib', '.grb', '.grib2') and f not in pref]
    else:
        pref = [f for f in files if f'_{var_name}_' in f.name or f'_{var_name}' in f.name]
    files = pref + [f for f in files if f not in pref]

    # When loading u, prefer the same file as omega (ensures same pressure levels)
    if prefer_file is not None and prefer_file in files:
        files = [prefer_file] + [f for f in files if f != prefer_file]

    var_data = None
    for f in files:
        try:
            engine = 'cfgrib' if f.suffix.lower() in ('.grib', '.grb', '.grib2') else None
            open_kw = {'engine': engine} if engine else {}
            if engine == 'cfgrib':
                # Skip corrupted messages (e.g. truncated download)
                open_kw['backend_kwargs'] = {'errors': 'ignore'}
            try:
                d = xr.open_dataset(f, **open_kw)
            except Exception as open_err:
                if engine == 'cfgrib':
                    try:
                        d = xr.open_dataset(f, engine='cfgrib', backend_kwargs={
                            'filter_by_keys': {'typeOfLevel': 'isobaricInhPa'},
                            'errors': 'ignore'
                        })
                    except Exception:
                        raise open_err
                else:
                    raise open_err
            for v in d.data_vars:
                v_lower = v.lower()
                if var_name == 'omega' and any(x in v_lower for x in ['omega', 'w', 'vertical_velocity', 'vertical']):
                    if v_lower == 'v':  # v is meridional wind
                        continue
                    cand = d[v]
                    break
                elif var_name == 'u' and v_lower in ('u', 'u_component', 'u_component_of_wind', 'u_wind'):
                    cand = d[v]
                    break
            else:
                d.close()
                continue
            lev_dims = ['level', 'lev', 'pressure_level', 'plev', 'isobaricInhPa']
            lev_dim = next((ld for ld in lev_dims if ld in cand.dims), None)
            if lev_dim is not None:
                n_lev = cand.sizes.get(lev_dim, 0)
                var_data = cand
                logger.info(f"  Loaded {var_name} from {f.name} ({n_lev} pressure levels)")
                break
            d.close()  # cand has no pressure level dim, try next file
        except Exception as e:
            logger.debug(f"  Skip {f}: {e}")
            continue

    if var_data is None:
        logger.warning(f"No {var_name} pressure-level data found. Create synthetic for demo.")
        return None
    return var_data


def create_synthetic_data(lat_range, lon_range, pressure_levels, all_years,
                          positive_iod_years, negative_iod_years):
    """Create synthetic omega and u for testing when ERA5 not available.
    Positive IOD: subsidence over Central Africa. Negative IOD: opposite (ascent)."""
    np.random.seed(42)
    lats = np.linspace(lat_range[0], lat_range[1], 25)
    lons = np.linspace(lon_range[0], lon_range[1], 21)
    n_years = len(all_years)
    n_times = n_years * 3  # SON months per year
    omega = np.random.randn(len(pressure_levels), len(lats), len(lons), n_times) * 0.008
    u_wind = np.random.randn(len(pressure_levels), len(lats), len(lons), n_times) * 2
    pos_set = set(positive_iod_years)
    neg_set = set(negative_iod_years)
    for t_idx, year in enumerate(all_years):
        for m in range(3):
            ti = t_idx * 3 + m
            for i, lat in enumerate(lats):
                if year in pos_set:
                    # Positive IOD: subsidence over Central Africa, ascent over Horn
                    if -10 < lat < 5:
                        omega[:, i, :, ti] -= 0.04
                    elif 8 < lat < 20:
                        omega[:, i, :, ti] += 0.03
                elif year in neg_set:
                    # Negative IOD: opposite (ascent over Central Africa, subsidence over Horn)
                    if -10 < lat < 5:
                        omega[:, i, :, ti] += 0.04
                    elif 8 < lat < 20:
                        omega[:, i, :, ti] -= 0.03
    return omega, u_wind, lats, lons, pressure_levels


def _load_grib_omega_and_u(grib_path):
    """Load both omega (w) and u from a GRIB file. cfgrib often returns one param per open;
    use filter_by_keys to get each and merge."""
    base_kw = {'engine': 'cfgrib', 'backend_kwargs': {'errors': 'ignore'}}
    omega_da = u_da = None
    # Try opening without filter first (some GRIB files return both in one dataset)
    try:
        d = xr.open_dataset(grib_path, **base_kw)
        omega_var, u_var = _has_omega_and_u(d)
        if omega_var and u_var:
            omega_da = d[omega_var].load()
            u_da = d[u_var].load()
            d.close()
            return omega_da, u_da
        d.close()
    except Exception:
        pass
    # Open each parameter separately with filter_by_keys (GRIB shortName: w=vertical velocity, u=zonal wind)
    for short_name, target in [('w', 'omega'), ('u', 'u')]:
        try:
            bk = {'errors': 'ignore', 'filter_by_keys': {'typeOfLevel': 'isobaricInhPa', 'shortName': short_name}}
            ds = xr.open_dataset(grib_path, engine='cfgrib', backend_kwargs=bk)
            v = list(ds.data_vars)[0] if ds.data_vars else None
            if v is not None:
                arr = ds[v].load()
                if target == 'omega':
                    omega_da = arr
                else:
                    u_da = arr
            ds.close()
        except Exception as e:
            logger.debug(f"  GRIB filter shortName={short_name}: {e}")
    if omega_da is not None and u_da is not None:
        return omega_da, u_da
    return None, None


def load_era5_omega_and_u(data_dir, pressure_levels):
    """Load omega and u from the same file when possible (ensures same pressure levels).
    Returns (omega_da, u_da, omega_source_file) or (None, None, None)."""
    data_dir = Path(data_dir)
    search_paths = [data_dir / 'atmospheric', data_dir / 'era5', data_dir]
    files = []
    for p in search_paths:
        if not p.exists():
            continue
        for ext in ['*.nc', '*.grib', '*.grb', '*.grib2']:
            for f in p.glob(f'**/{ext}'):
                if 'drought_reanalysis' in str(f):
                    continue
                files.append(f)
    # Prefer GRIB files first (user's file has both omega and u)
    pref = [f for f in files if f.suffix.lower() in ('.grib', '.grb', '.grib2')]
    pref += [f for f in files if 'era5' in f.name.lower() and ('omega' in f.name.lower() or 'u' in f.name.lower())]
    files = pref + [f for f in files if f not in pref]

    for f in files:
        try:
            is_grib = f.suffix.lower() in ('.grib', '.grb', '.grib2')
            if is_grib:
                omega_da, u_da = _load_grib_omega_and_u(f)
                if omega_da is not None and u_da is not None:
                    logger.info(f"  Loaded omega and u from same GRIB file: {f.name} (same pressure levels)")
                    return omega_da, u_da, f
                continue
            # NetCDF
            d = xr.open_dataset(f)
            omega_var, u_var = _has_omega_and_u(d)
            if omega_var and u_var:
                omega_da = d[omega_var]
                u_da = d[u_var]
                d.close()
                logger.info(f"  Loaded omega and u from same file: {f.name} (same pressure levels)")
                return omega_da, u_da, f
            d.close()
        except Exception as e:
            logger.debug(f"  Skip {f}: {e}")
            continue

    return None, None, None


def load_or_create_data(data_dir, positive_iod_years, negative_iod_years,
                        lat_range=(LAT_SOUTH, LAT_NORTH), lon_range=(LON_WEST, LON_EAST),
                        use_synthetic=True):
    """Load ERA5 omega and u, or create synthetic if use_synthetic=True. Returns (omega_da, u_da)."""
    data_dir = Path(data_dir) if data_dir else Path('.')
    pressure_levels = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100]
    all_years = list(range(1980, 2021))

    # First try loading both from the same file (ensures same pressure levels)
    omega_da, u_da, _ = load_era5_omega_and_u(data_dir, pressure_levels)
    if omega_da is None or u_da is None:
        # Fall back to loading separately
        omega_da = load_era5_pressure_levels(data_dir, 'omega', pressure_levels)
        u_da = load_era5_pressure_levels(data_dir, 'u', pressure_levels)

    if omega_da is not None and u_da is not None:
        # Warn if different pressure levels (e.g. omega from GRIB, u from avgua)
        o_lev = next((omega_da.sizes[d] for d in omega_da.dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), None)
        u_lev = next((u_da.sizes[d] for d in u_da.dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), None)
        if o_lev is not None and u_lev is not None and o_lev != u_lev:
            logger.warning(
                f"Omega has {o_lev} pressure levels, u has {u_lev}. "
                "For consistent cross-sections, use omega and u from the same source (e.g. download both via download_era5_omega_u.py). "
                "U will be interpolated to omega's grid."
            )

    if omega_da is None or u_da is None:
        if not use_synthetic:
            if omega_da is None:
                logger.error("Omega (vertical velocity) not found. Run: python download_era5_omega_u.py --output-dir atmospheric")
                logger.error("Or run: python check_atmospheric_omega.py .  to list variables in your files")
            return None, None
        logger.info("Creating synthetic data for demonstration. Download ERA5 for real analysis.")
        omega, u, lats, lons, levs = create_synthetic_data(
            lat_range, lon_range, pressure_levels,
            all_years, positive_iod_years, negative_iod_years
        )
        times = pd.date_range('1980-09-01', periods=len(all_years)*3, freq='MS')
        omega_da = xr.DataArray(
            omega,
            dims=['level', 'latitude', 'longitude', 'time'],
            coords={
                'level': levs,
                'latitude': lats,
                'longitude': lons,
                'time': times
            },
            attrs={'units': 'Pa/s', 'long_name': 'Vertical velocity'}
        )
        u_da = xr.DataArray(
            u,
            dims=['level', 'latitude', 'longitude', 'time'],
            coords={
                'level': levs,
                'latitude': lats,
                'longitude': lons,
                'time': times
            },
            attrs={'units': 'm/s', 'long_name': 'Zonal wind'}
        )
    return omega_da, u_da


_AFRICA_MASK_CACHE = {}


def _africa_land_mask_2d(lat, lon):
    """Boolean 2D mask (n_lat, n_lon) where African continental land == True.

    Uses Natural Earth 'admin_0_countries' filtered by CONTINENT == 'Africa' via cartopy + shapely.
    Returns None if cartopy/shapely unavailable."""
    key = (tuple(np.round(lat, 4)), tuple(np.round(lon, 4)))
    if key in _AFRICA_MASK_CACHE:
        return _AFRICA_MASK_CACHE[key]
    try:
        from cartopy.io import shapereader  # type: ignore
        import shapely.vectorized  # type: ignore
        from shapely.ops import unary_union  # type: ignore
    except Exception as e:
        logger.warning(f"Africa land-mask unavailable (cartopy/shapely missing: {e}); using lon band zonal mean.")
        _AFRICA_MASK_CACHE[key] = None
        return None
    try:
        shpfile = shapereader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
        geoms = [rec.geometry for rec in shapereader.Reader(shpfile).records()
                 if rec.attributes.get('CONTINENT') == 'Africa']
        if not geoms:
            logger.warning("No African country polygons found in Natural Earth shapefile.")
            _AFRICA_MASK_CACHE[key] = None
            return None
        africa = unary_union(geoms)
        lon_wrapped = np.where(lon > 180, lon - 360, lon)
        lon2d, lat2d = np.meshgrid(lon_wrapped, lat)
        mask = shapely.vectorized.contains(africa, lon2d, lat2d)
        _AFRICA_MASK_CACHE[key] = mask
        return mask
    except Exception as e:
        logger.warning(f"Africa land-mask construction failed ({e}); using lon band zonal mean.")
        _AFRICA_MASK_CACHE[key] = None
        return None


def compute_composite_meridional_mean(da, positive_iod_years, son_months=SON_MONTHS,
                                       lon_slice=(LON_WEST, LON_EAST), lat_slice=(LAT_SOUTH, LAT_NORTH),
                                       land_only=True):
    """Select SON months for IOD years, compute composite, then meridional mean over the lat band.

    Returns a DataArray on (level, longitude) suitable for a lon-pressure cross-section.
    If ``land_only`` is True, only African-continent cells contribute to the mean.
    """
    lon_names = ['lon', 'longitude', 'long']
    lat_names = ['lat', 'latitude']
    time_names = ['time', 'valid_time', 't']

    time_dim = next((d for d in da.dims if d.lower() in time_names), None)
    lon_dim = next((d for d in da.dims if d.lower() in lon_names), None)
    lat_dim = next((d for d in da.dims if d.lower() in lat_names), None)

    if time_dim:
        try:
            times = pd.DatetimeIndex(da[time_dim].values)
            mask = (times.year.isin(positive_iod_years)) & (times.month.isin(son_months))
            if mask.sum() == 0:
                logger.warning(f"No SON months found for years {positive_iod_years}; using all data")
                comp = da.mean(dim=time_dim)
            else:
                comp = da.isel({time_dim: mask}).mean(dim=time_dim)
        except Exception as e:
            logger.warning(f"Time selection failed: {e}; using mean over time")
            comp = da.mean(dim=time_dim)
    else:
        comp = da

    if lon_dim and lon_slice:
        comp = comp.sel({lon_dim: slice(lon_slice[0], lon_slice[1])})
    if lat_dim and lat_slice:
        lat_vals = np.asarray(comp[lat_dim].values)
        lat_min, lat_max = min(lat_slice), max(lat_slice)
        try:
            if len(lat_vals) > 0 and lat_vals[0] > lat_vals[-1]:
                comp = comp.sel({lat_dim: slice(lat_max, lat_min)})
            else:
                comp = comp.sel({lat_dim: slice(lat_min, lat_max)})
        except Exception as e:
            logger.warning(f"Lat slice failed ({e}); using full lat range")

    if land_only and lat_dim and lon_dim:
        lat_vals = np.asarray(comp[lat_dim].values)
        lon_vals = np.asarray(comp[lon_dim].values)
        africa_mask = _africa_land_mask_2d(lat_vals, lon_vals)
        if africa_mask is not None and africa_mask.any():
            mask_da = xr.DataArray(africa_mask, dims=(lat_dim, lon_dim),
                                   coords={lat_dim: lat_vals, lon_dim: lon_vals})
            comp = comp.where(mask_da)

    if lat_dim:
        comp_merid = comp.mean(dim=lat_dim, skipna=True)
    else:
        comp_merid = comp
    return comp_merid


def compute_composite_zonal_mean(da, positive_iod_years, son_months=SON_MONTHS,
                                  lon_slice=(LON_WEST, LON_EAST), lat_slice=(LAT_SOUTH, LAT_NORTH),
                                  land_only=True):
    """Select SON months for IOD years, compute composite, then zonal mean.

    If ``land_only`` is True, the composite is masked to the African continent
    (Natural Earth polygons) before the zonal mean so each latitude averages
    only over African land, not the Indian Ocean / Mediterranean.
    """
    lon_names = ['lon', 'longitude', 'long']
    lat_names = ['lat', 'latitude']
    lev_names = ['level', 'lev', 'pressure_level', 'plev', 'isobaricInhPa']
    time_names = ['time', 'valid_time', 't']

    time_dim = next((d for d in da.dims if d.lower() in time_names), None)
    lon_dim = next((d for d in da.dims if d.lower() in lon_names), None)
    lat_dim = next((d for d in da.dims if d.lower() in lat_names), None)

    if time_dim:
        # Select SON months and IOD years
        try:
            times = pd.DatetimeIndex(da[time_dim].values)
            mask = (times.year.isin(positive_iod_years)) & (times.month.isin(son_months))
            n_sel = mask.sum()
            if n_sel == 0:
                logger.warning(f"No SON months found for years {positive_iod_years}; using all data")
                comp = da.mean(dim=time_dim)
            else:
                da_sel = da.isel({time_dim: mask})
                comp = da_sel.mean(dim=time_dim)
        except Exception as e:
            logger.warning(f"Time selection failed: {e}; using mean over time")
            comp = da.mean(dim=time_dim)
    else:
        logger.warning("No time dimension in data; using as single snapshot")
        comp = da

    # Zonal mean (average over longitude)
    if lon_dim:
        if lon_slice:
            comp = comp.sel({lon_dim: slice(lon_slice[0], lon_slice[1])})
        if land_only and lat_dim:
            lat_vals = np.asarray(comp[lat_dim].values)
            lon_vals = np.asarray(comp[lon_dim].values)
            africa_mask = _africa_land_mask_2d(lat_vals, lon_vals)
            if africa_mask is not None and africa_mask.any():
                mask_da = xr.DataArray(africa_mask, dims=(lat_dim, lon_dim),
                                       coords={lat_dim: lat_vals, lon_dim: lon_vals})
                comp = comp.where(mask_da)
                land_frac = float(africa_mask.mean())
                logger.info(
                    "Applied African land mask for zonal mean (%.0f%% of lat\u00d7lon cells are continent).",
                    100 * land_frac,
                )
            else:
                logger.warning("African land mask empty or unavailable; falling back to full-band zonal mean.")
        comp_zonal = comp.mean(dim=lon_dim, skipna=True)
    else:
        comp_zonal = comp

    if lat_slice and lat_dim:
        lat_vals = np.asarray(comp_zonal[lat_dim].values)
        lat_min, lat_max = min(lat_slice), max(lat_slice)
        try:
            if len(lat_vals) > 0 and lat_vals[0] > lat_vals[-1]:
                comp_sel = comp_zonal.sel({lat_dim: slice(lat_max, lat_min)})
            else:
                comp_sel = comp_zonal.sel({lat_dim: slice(lat_min, lat_max)})
            if comp_sel[lat_dim].size > 0:
                comp_zonal = comp_sel
            else:
                logger.warning(f"Lat slice ({lat_min},{lat_max}) returned empty; using full lat range")
        except Exception as e:
            logger.warning(f"Lat slice failed ({e}); using full lat range")

    return comp_zonal


def _prepare_cross_section_data(omega_zonal, u_zonal):
    """Extract and prepare lat, lev, omega_vals, u_vals for plotting."""
    dims = list(omega_zonal.dims)
    lev_dim = next((d for d in dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), dims[0])
    lat_dim = next((d for d in dims if 'lat' in d.lower()), dims[1] if len(dims) > 1 else dims[0])

    lat = np.asarray(omega_zonal[lat_dim].values)
    lev = np.asarray(omega_zonal[lev_dim].values)
    omega_vals = np.asarray(omega_zonal.values)

    if omega_vals.size < 4 or len(lat) < 2 or len(lev) < 2:
        raise ValueError(
            f"Invalid data shape {omega_vals.shape} (lat={len(lat)}, lev={len(lev)}). "
            "GRIB file may be corrupted or incomplete—try re-downloading. "
            "Expected at least 2 lat x 2 lev for cross-section."
        )

    # Interpolate u to omega's grid when lev/lat differ (e.g. omega from GRIB, u from different NetCDF)
    u_vals = None
    if u_zonal is not None:
        u_dims = list(u_zonal.dims)
        u_lev_dim = next((d for d in u_dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), None)
        u_lat_dim = next((d for d in u_dims if 'lat' in d.lower()), None)
        if u_lev_dim and u_lat_dim:
            u_lev = np.asarray(u_zonal[u_lev_dim].values)
            u_lat = np.asarray(u_zonal[u_lat_dim].values)
            if u_lev.size != len(lev) or u_lat.size != len(lat):
                u_regrid = u_zonal.interp({u_lev_dim: lev, u_lat_dim: lat})
                u_vals = np.asarray(u_regrid.values)
                logger.debug(f"Regridded u from ({u_lev.size}x{u_lat.size}) to omega grid ({len(lev)}x{len(lat)})")
            else:
                u_vals = np.asarray(u_zonal.values)
        else:
            u_vals = np.asarray(u_zonal.values)

    # contourf(x=lat, y=lev, Z) requires Z shape (len(lev), len(lat)) = (n_lev, n_lat)
    if omega_vals.shape[0] == len(lat) and omega_vals.shape[1] == len(lev):
        omega_vals = omega_vals.T
    elif omega_vals.shape[0] != len(lev) or omega_vals.shape[1] != len(lat):
        raise ValueError(
            f"Data shape {omega_vals.shape} doesn't match lat({len(lat)}) x lev({len(lev)}). "
            "Need (n_lev, n_lat) or (n_lat, n_lev)."
        )
    if u_vals is not None:
        if u_vals.shape[0] == len(lat) and u_vals.shape[1] == len(lev):
            u_vals = u_vals.T
        elif u_vals.shape[0] != len(lev) or u_vals.shape[1] != len(lat):
            logger.warning(f"u shape {u_vals.shape} doesn't match grid ({len(lev)}x{len(lat)}); skipping u contours")
            u_vals = None

    if len(lev) > 1 and lev[0] < lev[-1]:
        lev = lev[::-1]
        omega_vals = np.flipud(omega_vals)
        if u_vals is not None:
            u_vals = np.flipud(u_vals)
    return lat, lev, omega_vals, u_vals


def _set_latitude_axis_extent(ax, lat_range):
    """Fix x-axis to the requested latitude bounds (continental / analysis box). No auto padding."""
    lo, hi = float(lat_range[0]), float(lat_range[1])
    ax.set_xlim(lo, hi)
    ax.margins(x=0)


def plot_cross_section(omega_zonal, u_zonal, output_file, title='Positive IOD: Zonal-Mean Circulation',
                       annotations=True, lat_range=(LAT_SOUTH, LAT_NORTH)):
    """Plot vertical cross-section: omega (color) + u-wind (contours)."""
    import matplotlib.pyplot as plt

    lat, lev, omega_vals, u_vals = _prepare_cross_section_data(omega_zonal, u_zonal)

    fig, ax = plt.subplots(figsize=(12, 8))

    vmax = max(abs(np.nanpercentile(omega_vals, 2)), abs(np.nanpercentile(omega_vals, 98)), 0.02)
    vmax = min(vmax, 0.1)
    levels_omega = np.linspace(-vmax, vmax, 21)

    cf = ax.contourf(lat, lev, omega_vals, levels=levels_omega, cmap='RdBu_r', extend='both')
    cbar = fig.colorbar(cf, ax=ax, orientation='vertical', shrink=0.8, pad=0.02)
    cbar.set_label('Omega (Pa/s)\nBlue: Ascent | Red: Subsidence', fontsize=11, fontweight='bold')

    if u_vals is not None:
        levels_u = np.linspace(-15, 15, 13)
        cs = ax.contour(lat, lev, u_vals, levels=levels_u, colors='black', linewidths=0.8, alpha=0.7)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%d')

    ax.set_xlabel('Latitude (°N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Pressure (hPa)', fontsize=12, fontweight='bold')
    _set_latitude_axis_extent(ax, lat_range)
    ax.set_ylim(lev.min(), lev.max())
    ax.invert_yaxis()
    ax.axhline(500, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(0, color='gray', linestyle='-', alpha=0.5)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    if annotations:
        ax.text(0.02, 0.95, 'Central Africa\n(subsidence → drought)', transform=ax.transAxes,
                fontsize=9, va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        ax.text(0.85, 0.95, 'Horn of Africa\n(ascent → rainfall)', transform=ax.transAxes,
                fontsize=9, va='top', ha='right', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"✓ Cross-section saved to: {output_file}")


def _draw_iod_cross_section_panel(ax, lat_p, lev_p, omega_vals, u_vals, levels_omega, panel_label, title,
                                    annot_left, annot_right, annot_south, annot_north, n_suffix='',
                                    lat_range=(LAT_SOUTH, LAT_NORTH)):
    """Shared map elements for (a)/(b) composite panels."""
    cf = ax.contourf(lat_p, lev_p, omega_vals, levels=levels_omega, cmap='RdBu_r', extend='both')
    if u_vals is not None:
        levels_u = np.linspace(-15, 15, 13)
        cs = ax.contour(lat_p, lev_p, u_vals, levels=levels_u, colors='black', linewidths=0.8, alpha=0.7)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%d')
    ax.set_xlabel('Latitude (°N)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Pressure (hPa)', fontsize=11, fontweight='bold')
    ax.set_ylim(lev_p.min(), lev_p.max())
    ax.invert_yaxis()
    ax.axhline(500, color='gray', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(0, color='k', linestyle='-', alpha=0.4, linewidth=0.8)
    ax.axvline(-23.5, color='gray', linestyle=':', alpha=0.4)
    ax.axvline(23.5, color='gray', linestyle=':', alpha=0.4)
    ax.text(0, 0.5, 'Eq.', transform=ax.get_xaxis_transform(), fontsize=7, va='center', color='gray')
    ax.text(-23.5, 1.02, 'Trop. Cap.', transform=ax.get_xaxis_transform(), fontsize=6, ha='center', color='gray')
    ax.text(23.5, 1.02, 'Trop. Can.', transform=ax.get_xaxis_transform(), fontsize=6, ha='center', color='gray')
    ax.set_title(f'{panel_label} {title}{n_suffix}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.95, annot_left, transform=ax.transAxes, fontsize=9, va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.85))
    ax.text(0.85, 0.95, annot_right, transform=ax.transAxes, fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.85))
    lo, hi = float(lat_range[0]), float(lat_range[1])
    _set_latitude_axis_extent(ax, lat_range)
    pad = max(2.0, 0.04 * (hi - lo))
    ax.text(lo + pad, 950, annot_south, fontsize=8, va='bottom', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.85))
    ax.text(hi - pad, 950, annot_north, fontsize=8, va='bottom', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.85))
    ax.text(1.02, 500, '500 hPa\n(mid-trop.)', transform=ax.get_yaxis_transform(), fontsize=7,
            va='center', color='gray')
    return cf


def plot_cross_section_dual_panel(omega_pos, u_pos, omega_neg, u_neg, output_file,
                                   lon_range=(LON_WEST, LON_EAST), lat_range=(LAT_SOUTH, LAT_NORTH),
                                   n_pos=None, n_neg=None, land_only=True):
    """Plot 3-panel figure: (a) Positive IOD, (b) Negative IOD, (c) Difference (Pos − Neg)."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable

    lat_p, lev_p, omega_p, u_p = _prepare_cross_section_data(omega_pos, u_pos)
    _, _, omega_n, u_n = _prepare_cross_section_data(omega_neg, u_neg)

    omega_diff = omega_p - omega_n

    u_diff = None
    if u_p is not None and u_n is not None and u_p.shape == u_n.shape:
        u_diff = u_p - u_n

    vmax = max(
        abs(np.nanpercentile(omega_p, 2)), abs(np.nanpercentile(omega_p, 98)),
        abs(np.nanpercentile(omega_n, 2)), abs(np.nanpercentile(omega_n, 98)),
        0.02
    )
    vmax = min(vmax, 0.1)
    levels_omega = np.linspace(-vmax, vmax, 21)

    vmax_d = max(
        abs(np.nanpercentile(omega_diff, 2)), abs(np.nanpercentile(omega_diff, 98)),
        0.01
    )
    vmax_d = min(vmax_d, 0.12)
    levels_diff = np.linspace(-vmax_d, vmax_d, 21)

    # Layout: (a)|(b) on top; (c) centered below. 2 rows x 4 cols grid.
    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(2, 4, hspace=0.40, wspace=0.35)
    ax_a = fig.add_subplot(gs[0, 0:2])
    ax_b = fig.add_subplot(gs[0, 2:4], sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, 1:3], sharey=ax_a)
    axes = [ax_a, ax_b, ax_c]

    _draw_iod_cross_section_panel(
        axes[0], lat_p, lev_p, omega_p, u_p, levels_omega, '(a)', 'Positive IOD',
        'Central Africa\n(subsidence → drought)', 'Horn of Africa\n(ascent → rainfall)',
        'Southern Africa\n(subsidence → drought)', 'Northern Africa\n(subsidence → drought)',
        n_suffix=f' (n={n_pos})' if n_pos else '', lat_range=lat_range)
    _draw_iod_cross_section_panel(
        axes[1], lat_p, lev_p, omega_n, u_n, levels_omega, '(b)', 'Negative IOD',
        'Central Africa\n(ascent → rainfall)', 'Horn of Africa\n(subsidence → drought)',
        'Southern Africa\n(ascent → rainfall)', 'Northern Africa\n(ascent → rainfall)',
        n_suffix=f' (n={n_neg})' if n_neg else '', lat_range=lat_range)

    ax = axes[2]
    cf_d = ax.contourf(lat_p, lev_p, omega_diff, levels=levels_diff, cmap='RdBu_r', extend='both')
    if u_diff is not None:
        levels_ud = np.linspace(-20, 20, 11)
        cs = ax.contour(lat_p, lev_p, u_diff, levels=levels_ud, colors='black', linewidths=0.8, alpha=0.7)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%d')
    ax.set_xlabel('Latitude (°N)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Pressure (hPa)', fontsize=11, fontweight='bold')
    _set_latitude_axis_extent(ax, lat_range)
    ax.set_ylim(lev_p.min(), lev_p.max())
    ax.invert_yaxis()
    ax.axhline(500, color='gray', linestyle='--', alpha=0.6, linewidth=1)
    ax.axvline(0, color='k', linestyle='-', alpha=0.4, linewidth=0.8)
    ax.axvline(-23.5, color='gray', linestyle=':', alpha=0.4)
    ax.axvline(23.5, color='gray', linestyle=':', alpha=0.4)
    ax.text(0, 0.5, 'Eq.', transform=ax.get_xaxis_transform(), fontsize=7, va='center', color='gray')
    ax.text(-23.5, 1.02, 'Trop. Cap.', transform=ax.get_xaxis_transform(), fontsize=6, ha='center', color='gray')
    ax.text(23.5, 1.02, 'Trop. Can.', transform=ax.get_xaxis_transform(), fontsize=6, ha='center', color='gray')
    ax.set_title('(c) Difference (Pos − Neg IOD)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.text(0.5, 0.95, 'ΔΩ = Ω_Pos − Ω_Neg\n(same colors: blue ascent, red subsidence)',
            transform=ax.transAxes, fontsize=9, va='top', ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    ax.text(0.5, 0.06, 'Contours: Δu = u_Pos − u_Neg (m/s)' if u_diff is not None else '',
            transform=ax.transAxes, fontsize=8, ha='center', style='italic', color='dimgray')
    ax.text(1.02, 500, '500 hPa\n(mid-trop.)', transform=ax.get_yaxis_transform(), fontsize=7,
            va='center', color='gray')

    # Horizontal colorbars BELOW each row
    # Composites: shared colorbar centered under row 1 (panels a & b)
    cbar_ax1 = fig.add_axes([0.18, 0.505, 0.64, 0.013])
    sm0 = ScalarMappable(norm=Normalize(vmin=-vmax, vmax=vmax), cmap='RdBu_r')
    sm0.set_array([])
    cb1 = fig.colorbar(sm0, cax=cbar_ax1, orientation='horizontal')
    cb1.set_label('Ω composite (Pa/s) — Blue: Ascent | Red: Subsidence',
                  fontsize=10, fontweight='bold')
    # Difference: colorbar under panel (c)
    cbar_ax2 = fig.add_axes([0.34, 0.045, 0.32, 0.013])
    cb2 = fig.colorbar(cf_d, cax=cbar_ax2, orientation='horizontal')
    cb2.set_label('Ω difference (Pa/s) — Pos IOD − Neg IOD',
                  fontsize=10, fontweight='bold')

    lat0, lat1 = lat_range
    lat0_s = f'{abs(lat0)}°S' if lat0 < 0 else f'{lat0}°N'
    lat1_s = f'{lat1}°N' if lat1 >= 0 else f'{abs(lat1)}°S'
    fig.suptitle(
        f'Zonal-Mean Vertical Velocity During IOD Events (SON, {lon_range[0]}°E–{lon_range[1]}°E, '
        f'{lat0_s}–{lat1_s})',
        fontsize=14, fontweight='bold', y=0.98,
    )
    mask_note = 'African continent only (Natural Earth land mask)' if land_only else 'full 10–50°E band (ocean + land)'
    fig.text(0.5, 0.94,
             f'Black contours: zonal wind u (m/s) on (a,b); Δu on (c). ERA5 reanalysis. Zonal mean: {mask_note}.',
             ha='center', fontsize=9, style='italic', color='gray')
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.10, top=0.92)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"✓ Three-panel cross-section (incl. Pos−Neg difference) saved to: {output_file}")


def _prepare_lon_pressure_data(omega_merid, u_merid):
    """Extract (lon, lev, omega[n_lev,n_lon], u[n_lev,n_lon]) for lon-pressure cross-section."""
    dims = list(omega_merid.dims)
    lev_dim = next((d for d in dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), dims[0])
    lon_dim = next((d for d in dims if 'lon' in d.lower()), dims[-1])
    lon = np.asarray(omega_merid[lon_dim].values)
    lev = np.asarray(omega_merid[lev_dim].values)
    omega_vals = np.asarray(omega_merid.values)

    u_vals = None
    if u_merid is not None:
        u_dims = list(u_merid.dims)
        u_lev_dim = next((d for d in u_dims if 'lev' in d.lower() or 'level' in d.lower() or 'pressure' in d.lower() or 'isobaric' in d.lower()), None)
        u_lon_dim = next((d for d in u_dims if 'lon' in d.lower()), None)
        if u_lev_dim and u_lon_dim:
            u_lev = np.asarray(u_merid[u_lev_dim].values)
            u_lon = np.asarray(u_merid[u_lon_dim].values)
            if u_lev.size != len(lev) or u_lon.size != len(lon):
                u_regrid = u_merid.interp({u_lev_dim: lev, u_lon_dim: lon})
                u_vals = np.asarray(u_regrid.values)
            else:
                u_vals = np.asarray(u_merid.values)

    if omega_vals.shape[0] == len(lon) and omega_vals.shape[1] == len(lev):
        omega_vals = omega_vals.T
    elif omega_vals.shape[0] != len(lev) or omega_vals.shape[1] != len(lon):
        raise ValueError(f"omega shape {omega_vals.shape} incompatible with lon({len(lon)}) x lev({len(lev)})")
    if u_vals is not None:
        if u_vals.shape[0] == len(lon) and u_vals.shape[1] == len(lev):
            u_vals = u_vals.T
        elif u_vals.shape[0] != len(lev) or u_vals.shape[1] != len(lon):
            u_vals = None

    if len(lev) > 1 and lev[0] < lev[-1]:
        lev = lev[::-1]
        omega_vals = np.flipud(omega_vals)
        if u_vals is not None:
            u_vals = np.flipud(u_vals)
    return lon, lev, omega_vals, u_vals


def _draw_lon_pressure_panel(ax, lon, lev, omega_vals, u_vals, levels_omega, title, lon_range):
    """Single lon-pressure panel: omega shading + u contours, African coast guide lines."""
    cf = ax.contourf(lon, lev, omega_vals, levels=levels_omega, cmap='RdBu_r', extend='both')
    if u_vals is not None:
        cs = ax.contour(lon, lev, u_vals, levels=np.linspace(-15, 15, 13),
                        colors='black', linewidths=0.8, alpha=0.7)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%d')
    ax.set_xlabel('Longitude (°E)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Pressure (hPa)', fontsize=11, fontweight='bold')
    ax.set_xlim(float(lon_range[0]), float(lon_range[1]))
    ax.margins(x=0)
    ax.set_ylim(lev.min(), lev.max())
    ax.invert_yaxis()
    ax.axhline(500, color='gray', linestyle='--', alpha=0.6, linewidth=1)
    # Approximate reference longitudes along equatorial Africa
    for lon_ref, label in [(20, 'Central Africa'), (38, 'Horn')]:
        if lon_range[0] <= lon_ref <= lon_range[1]:
            ax.axvline(lon_ref, color='gray', linestyle=':', alpha=0.4)
            ax.text(lon_ref, 1.02, label, transform=ax.get_xaxis_transform(),
                    fontsize=6, ha='center', color='gray')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    return cf


def plot_lon_pressure_dual_panel(omega_pos, u_pos, omega_neg, u_neg, output_file,
                                 lon_range=(LON_WEST, LON_EAST), lat_range=(LAT_SOUTH, LAT_NORTH),
                                 n_pos=None, n_neg=None, land_only=True):
    """3-panel longitude-pressure cross-section: Pos IOD, Neg IOD, Pos−Neg difference."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from matplotlib.cm import ScalarMappable

    lon, lev, omega_p, u_p = _prepare_lon_pressure_data(omega_pos, u_pos)
    _, _, omega_n, u_n = _prepare_lon_pressure_data(omega_neg, u_neg)
    omega_diff = omega_p - omega_n
    u_diff = (u_p - u_n) if (u_p is not None and u_n is not None and u_p.shape == u_n.shape) else None

    vmax = max(abs(np.nanpercentile(omega_p, 2)), abs(np.nanpercentile(omega_p, 98)),
               abs(np.nanpercentile(omega_n, 2)), abs(np.nanpercentile(omega_n, 98)), 0.02)
    vmax = min(vmax, 0.1)
    levels_omega = np.linspace(-vmax, vmax, 21)
    vmax_d = min(max(abs(np.nanpercentile(omega_diff, 2)), abs(np.nanpercentile(omega_diff, 98)), 0.01), 0.12)
    levels_diff = np.linspace(-vmax_d, vmax_d, 21)

    fig = plt.figure(figsize=(14, 12))
    gs = fig.add_gridspec(2, 4, hspace=0.40, wspace=0.35)
    ax_a = fig.add_subplot(gs[0, 0:2])
    ax_b = fig.add_subplot(gs[0, 2:4], sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, 1:3], sharey=ax_a)
    axes = [ax_a, ax_b, ax_c]
    _draw_lon_pressure_panel(axes[0], lon, lev, omega_p, u_p, levels_omega,
                             f'(a) Positive IOD' + (f' (n={n_pos})' if n_pos else ''), lon_range)
    _draw_lon_pressure_panel(axes[1], lon, lev, omega_n, u_n, levels_omega,
                             f'(b) Negative IOD' + (f' (n={n_neg})' if n_neg else ''), lon_range)

    ax = axes[2]
    cf_d = ax.contourf(lon, lev, omega_diff, levels=levels_diff, cmap='RdBu_r', extend='both')
    if u_diff is not None:
        cs = ax.contour(lon, lev, u_diff, levels=np.linspace(-20, 20, 11),
                        colors='black', linewidths=0.8, alpha=0.7)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%d')
    ax.set_xlabel('Longitude (°E)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Pressure (hPa)', fontsize=11, fontweight='bold')
    ax.set_xlim(float(lon_range[0]), float(lon_range[1]))
    ax.margins(x=0)
    ax.set_ylim(lev.min(), lev.max())
    ax.invert_yaxis()
    ax.axhline(500, color='gray', linestyle='--', alpha=0.6, linewidth=1)
    ax.set_title('(c) Difference (Pos − Neg IOD)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Horizontal colorbars BELOW each row
    cbar_ax1 = fig.add_axes([0.18, 0.505, 0.64, 0.013])
    sm0 = ScalarMappable(norm=Normalize(vmin=-vmax, vmax=vmax), cmap='RdBu_r'); sm0.set_array([])
    cb1 = fig.colorbar(sm0, cax=cbar_ax1, orientation='horizontal')
    cb1.set_label('Ω composite (Pa/s) — Blue: Ascent | Red: Subsidence',
                  fontsize=10, fontweight='bold')
    cbar_ax2 = fig.add_axes([0.34, 0.045, 0.32, 0.013])
    cb2 = fig.colorbar(cf_d, cax=cbar_ax2, orientation='horizontal')
    cb2.set_label('Ω difference (Pa/s) — Pos IOD − Neg IOD',
                  fontsize=10, fontweight='bold')

    lat0, lat1 = lat_range
    lat_label = f'{abs(lat0)}°S' if lat0 < 0 else f'{lat0}°N'
    lat_label += '–' + (f'{lat1}°N' if lat1 >= 0 else f'{abs(lat1)}°S')
    mask_note = 'African land only' if land_only else 'full lon band (ocean + land)'
    fig.suptitle(
        f'Longitude–Pressure Cross-Section of Vertical Velocity (SON, '
        f'lat band {lat_label}; {lon_range[0]}°E–{lon_range[1]}°E; meridional mean, {mask_note})',
        fontsize=13, fontweight='bold', y=0.98,
    )
    fig.text(0.5, 0.94, 'Black contours: zonal wind u (m/s) on (a,b); Δu on (c). ERA5 reanalysis.',
             ha='center', fontsize=9, style='italic', color='gray')
    fig.subplots_adjust(left=0.06, right=0.98, bottom=0.10, top=0.92)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"✓ Three-panel lon-pressure cross-section saved to: {output_file}")


def download_era5_omega_u(output_dir, years=None):
    """Download ERA5 omega and u on pressure levels via CDS API."""
    try:
        import cdsapi
    except ImportError:
        logger.error("Install cdsapi: pip install cdsapi. Then set CDS_API_KEY or ~/.cdsapirc")
        return False

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    years = years or list(range(1980, 2021))

    c = cdsapi.Client()
    # ERA5 pressure levels monthly
    for var, cds_var in [('omega', 'vertical_velocity'), ('u', 'u_component_of_wind')]:
        out_file = output_dir / f'era5_{var}_pressure_levels_{years[0]}-{years[-1]}.nc'
        if out_file.exists():
            logger.info(f"Skipping {var} (exists)")
            continue
        try:
            c.retrieve(
                'reanalysis-era5-pressure-levels-monthly-means',
                {
                    'product_type': 'monthly_averaged_reanalysis',
                    'variable': cds_var,
                    'pressure_level': ['1000', '925', '850', '700', '600', '500', '400', '300', '250', '200', '150', '100'],
                    'year': [str(y) for y in years],
                    'month': ['09', '10', '11'],
                    'time': '00:00',
                    'area': [LAT_NORTH, LON_WEST, LAT_SOUTH, LON_EAST],
                    'format': 'netcdf',
                },
                str(out_file)
            )
            logger.info(f"✓ Downloaded {var}")
        except Exception as e:
            logger.error(f"CDS download failed for {var}: {e}")
    return True


def main():
    parser = argparse.ArgumentParser(description='IOD circulation vertical cross-section')
    parser.add_argument('--data-dir', default=None, help='Path to ERA5 atmospheric data')
    parser.add_argument('--output-dir', default='output/iod_circulation', help='Output directory')
    parser.add_argument(
        '--lat-south', type=float, default=LAT_SOUTH,
        help=f'Southern latitude bound (°N, negative = °S). Default {LAT_SOUTH} (continental Africa).',
    )
    parser.add_argument(
        '--lat-north', type=float, default=LAT_NORTH,
        help=f'Northern latitude bound (°N). Default {LAT_NORTH} (continental Africa).',
    )
    parser.add_argument('--lon-west', type=float, default=LON_WEST,
                        help='Western longitude for zonal mean (°E).')
    parser.add_argument('--lon-east', type=float, default=LON_EAST,
                        help='Eastern longitude for zonal mean (°E).')
    parser.add_argument('--download', action='store_true', help='Download ERA5 omega/u via CDS API')
    parser.add_argument('--positive-iod-years', nargs='+', type=int, default=POSITIVE_IOD_YEARS,
                        help='Positive IOD event years')
    parser.add_argument('--negative-iod-years', nargs='+', type=int, default=NEGATIVE_IOD_YEARS,
                        help='Negative IOD event years')
    parser.add_argument('--single-panel', action='store_true', help='Plot only positive IOD (legacy)')
    parser.add_argument('--no-synthetic', action='store_true',
                        help='Exit with error if ERA5 omega/u data not found (do not use synthetic)')
    parser.add_argument(
        '--no-land-mask', dest='land_only', action='store_false',
        help='Disable African-continent land mask. Default: zonal mean uses only African land '
             '(ocean / Mediterranean cells ignored via Natural Earth polygons).',
    )
    parser.set_defaults(land_only=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data_dir = Path(args.data_dir) if args.data_dir else Path('/home/msovara/lustre/DataDownloads/data')
    if not data_dir.exists():
        data_dir = Path('.')

    if args.download:
        download_era5_omega_u(data_dir / 'atmospheric', years=list(range(1980, 2021)))
        data_dir = data_dir / 'atmospheric'

    lat_range = (args.lat_south, args.lat_north)
    lon_range = (args.lon_west, args.lon_east)

    logger.info(
        "Analysis domain: zonal mean %.1f°E–%.1f°E, latitude %.1f° to %.1f°N (south negative = °S)",
        lon_range[0], lon_range[1], lat_range[0], lat_range[1],
    )
    logger.info("Loading ERA5 omega and u-wind...")
    omega_da, u_da = load_or_create_data(
        data_dir, args.positive_iod_years, args.negative_iod_years, lat_range, lon_range,
        use_synthetic=not args.no_synthetic
    )
    if omega_da is None or u_da is None:
        logger.error("ERA5 omega/u data not found. Place files in atmospheric/ or era5/ subdir.")
        logger.error("See IOD_CIRCULATION_CROSS_SECTION_README.md for download and path instructions.")
        return 1

    logger.info(
        "Zonal-mean mask: %s",
        "African continent land only (Natural Earth)" if args.land_only else "full lon band (10\u201350\u00b0E, ocean included)",
    )

    if args.single_panel:
        logger.info("Computing positive IOD composite...")
        omega_zonal = compute_composite_zonal_mean(
            omega_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        )
        u_zonal = compute_composite_zonal_mean(
            u_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        ) if u_da is not None else None
        title = f'Positive IOD Composite: Zonal-Mean Circulation (SON, {args.lon_west}°E–{args.lon_east}°E)\nn={len(args.positive_iod_years)} years'
        out_file = output_dir / 'iod_circulation_cross_section_positive_iod.png'
        plot_cross_section(omega_zonal, u_zonal, out_file, title=title, lat_range=lat_range)
    else:
        logger.info("Computing positive and negative IOD composites...")
        omega_pos = compute_composite_zonal_mean(
            omega_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        )
        omega_neg = compute_composite_zonal_mean(
            omega_da, args.negative_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        )
        u_pos = compute_composite_zonal_mean(
            u_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        ) if u_da is not None else None
        u_neg = compute_composite_zonal_mean(
            u_da, args.negative_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        ) if u_da is not None else None
        out_file = output_dir / 'iod_circulation_cross_section_positive_negative_iod.png'
        plot_cross_section_dual_panel(
            omega_pos, u_pos, omega_neg, u_neg, out_file,
            lon_range=lon_range, lat_range=lat_range,
            n_pos=len(args.positive_iod_years), n_neg=len(args.negative_iod_years),
            land_only=args.land_only,
        )

        # Second figure: longitude-pressure cross-section (east-west structure over 10–50°E)
        logger.info("Computing longitude-pressure (meridional-mean) composites...")
        omega_pos_lp = compute_composite_meridional_mean(
            omega_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        )
        omega_neg_lp = compute_composite_meridional_mean(
            omega_da, args.negative_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        )
        u_pos_lp = compute_composite_meridional_mean(
            u_da, args.positive_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        ) if u_da is not None else None
        u_neg_lp = compute_composite_meridional_mean(
            u_da, args.negative_iod_years, lon_slice=lon_range, lat_slice=lat_range,
            land_only=args.land_only,
        ) if u_da is not None else None
        out_file_lp = output_dir / 'iod_circulation_lonpressure_positive_negative_iod.png'
        plot_lon_pressure_dual_panel(
            omega_pos_lp, u_pos_lp, omega_neg_lp, u_neg_lp, out_file_lp,
            lon_range=lon_range, lat_range=lat_range,
            n_pos=len(args.positive_iod_years), n_neg=len(args.negative_iod_years),
            land_only=args.land_only,
        )

    logger.info("Done. For real analysis, download ERA5 omega and u from Copernicus CDS.")


if __name__ == '__main__':
    import sys
    sys.exit(main() or 0)
