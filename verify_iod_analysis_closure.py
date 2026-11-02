#!/usr/bin/env python3
"""Verify inputs and outputs for IOD–drought analysis closure (offline-safe)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from analysis_config import (
        AFRICA_ANALYSIS_BOUNDS,
        IOD_COMPOSITE_SON_YEARS,
        IOD_CIRCULATION_DIAGNOSTIC_LON,
    )
except ImportError:
    AFRICA_ANALYSIS_BOUNDS = {'lat_min': -35, 'lat_max': 37, 'lon_min': -20, 'lon_max': 55}
    IOD_COMPOSITE_SON_YEARS = {
        'positive': [1994, 1997, 2006, 2012, 2015, 2018, 2019],
        'negative': [1980, 1981, 1992, 1996, 1998],
    }
    IOD_CIRCULATION_DIAGNOSTIC_LON = {'lon_west': 10.0, 'lon_east': 50.0}

# Required deliverables for a closed analysis package
REQUIRED_PICKLES = [
    'lag_correlation_results.pkl',
    'partial_correlation_results.pkl',
    'seasonal_analysis_results.pkl',
    'multiple_index_comparison_results.pkl',
    'composite_drought_results.pkl',
    'enso_stratified_composite_results.pkl',
]

OPTIONAL_PICKLES = [
    'spatial_correlation_results.pkl',
    'wavelet_coherence_results.pkl',
    'atmospheric_circulation_composites.pkl',
]

REQUIRED_PLOTS = [
    'lag_correlation_analysis.png',
    'partial_correlation_analysis.png',
    'multiple_index_comparison.png',
    'enso_stratified_composite_SPI3_SPEI3.png',
    'enso_stratified_composite_SPI6_SPEI6.png',
    'enso_stratified_composite_summary_table.png',
]

OPTIONAL_PLOTS = [
    'atmospheric_circulation_geopotential_height_mercator.png',
    'atmospheric_circulation_wind_vectors.png',
    'atmospheric_circulation_composites.png',
]

CIRCULATION_PLOTS = [
    'iod_circulation_cross_section_positive_negative_iod.png',
    'iod_circulation_lonpressure_positive_negative_iod.png',
]

DROUGHT_INDEX_NAMES = ['SPI3', 'SPEI3', 'SPI6', 'SPEI6']


def _glob_any(root: Path, patterns: list[str]) -> list[Path]:
    found = []
    for pat in patterns:
        found.extend(root.glob(pat))
    return sorted(set(found))


def check_inputs(data_dir: Path) -> tuple[bool, list[str]]:
    """Return (ok, messages)."""
    msgs: list[str] = []
    ok = True

    msgs.append('--- Config (analysis_config.py) ---')
    msgs.append(f"  Africa bounds: {AFRICA_ANALYSIS_BOUNDS}")
    msgs.append(f"  +IOD SON years (n={len(IOD_COMPOSITE_SON_YEARS['positive'])}): "
                f"{IOD_COMPOSITE_SON_YEARS['positive']}")
    msgs.append(f"  -IOD SON years (n={len(IOD_COMPOSITE_SON_YEARS['negative'])}): "
                f"{IOD_COMPOSITE_SON_YEARS['negative']}")
    msgs.append(f"  Circulation lon band: {IOD_CIRCULATION_DIAGNOSTIC_LON}")

    search_roots = [
        data_dir,
        data_dir / 'data',
        data_dir / 'data' / 'drought_reanalysis',
        data_dir / 'spi_data',
        Path('.'),
    ]

    # DMI
    dmi_files = []
    for r in search_roots:
        if r.exists():
            dmi_files.extend(_glob_any(r, ['**/dmi_*.csv', 'dmi_*.csv']))
    dmi_files = sorted(set(dmi_files))
    if dmi_files:
        msgs.append(f"✓ DMI: {dmi_files[0]}")
    else:
        ok = False
        msgs.append('✗ DMI: no dmi_*.csv found')

    # Niño 3.4
    nino_files = []
    for r in search_roots:
        if r.exists():
            nino_files.extend(_glob_any(r, ['**/*nino*', '**/*NINO*', 'nino34*.csv']))
    nino_files = [f for f in sorted(set(nino_files)) if f.suffix.lower() in ('.csv', '.txt', '.dat')]
    if nino_files:
        msgs.append(f"✓ Niño 3.4: {nino_files[0]}")
    else:
        ok = False
        msgs.append('✗ Niño 3.4: no index file found')

    # Drought indices
    drought_hits = {}
    for idx in DROUGHT_INDEX_NAMES:
        hits = []
        for r in search_roots:
            if not r.exists():
                continue
            for pat in [
                f'**/{idx}*genlogistic*era5*.nc',
                f'**/{idx.lower()}*genlogistic*era5*.nc',
                f'**/{idx}*gamma*era5*.nc',
                f'**/{idx.lower()}*gamma*era5*.nc',
            ]:
                hits.extend(r.glob(pat))
        drought_hits[idx] = sorted(set(hits))
        if drought_hits[idx]:
            msgs.append(f"✓ {idx}: {len(drought_hits[idx])} NetCDF file(s)")
        else:
            ok = False
            msgs.append(f"✗ {idx}: no NetCDF files found")

    # Atmospheric (for circulation composites in comprehensive script)
    atmos_nc = data_dir / 'atmospheric' / 'data_stream-moda_stepType-avgua.nc'
    atmos_grib = list((data_dir / 'atmospheric').glob('*.grib')) if (data_dir / 'atmospheric').exists() else []
    if atmos_nc.exists():
        msgs.append(f"✓ Atmospheric monthly: {atmos_nc.name}")
    elif atmos_grib:
        msgs.append(f"✓ Atmospheric GRIB: {len(atmos_grib)} file(s) in atmospheric/")
    else:
        msgs.append('⚠ Atmospheric: no avgua.nc or GRIB (circulation composites may skip)')

    # ERA5 omega/u for cross-section script
    if atmos_grib:
        msgs.append('✓ Cross-section GRIB: present')
    else:
        msgs.append('⚠ Cross-section: no GRIB in atmospheric/ (run plot script after copying GRIB)')

    return ok, msgs


def check_outputs(stats_dir: Path, circ_dir: Path, strict: bool) -> tuple[bool, list[str]]:
    msgs: list[str] = []
    ok = True
    data_dir = stats_dir / 'data'
    plots_dir = stats_dir / 'plots'

    msgs.append('--- Statistics outputs ---')
    for name in REQUIRED_PICKLES:
        p = data_dir / name
        if p.exists() and p.stat().st_size > 0:
            msgs.append(f"✓ data/{name}")
        else:
            ok = False
            msgs.append(f"✗ data/{name} missing")

    for name in OPTIONAL_PICKLES:
        p = data_dir / name
        if p.exists() and p.stat().st_size > 0:
            msgs.append(f"✓ data/{name} (optional)")
        else:
            msgs.append(f"⚠ data/{name} missing (optional)")

    for name in REQUIRED_PLOTS:
        p = plots_dir / name
        if p.exists() and p.stat().st_size > 0:
            msgs.append(f"✓ plots/{name}")
        else:
            ok = False
            msgs.append(f"✗ plots/{name} missing")

    for name in OPTIONAL_PLOTS:
        p = plots_dir / name
        if p.exists() and p.stat().st_size > 0:
            msgs.append(f"✓ plots/{name} (optional)")
        else:
            msgs.append(f"⚠ plots/{name} missing (optional)")

    # Per-index seasonal plots (at least one)
    seasonal = list(plots_dir.glob('seasonal_analysis_*.png'))
    if seasonal:
        msgs.append(f"✓ seasonal plots: {len(seasonal)} file(s)")
    else:
        ok = False
        msgs.append('✗ no seasonal_analysis_*.png')

    composite_maps = list(plots_dir.glob('composite_drought_*_maps.png'))
    if composite_maps:
        msgs.append(f"✓ composite drought maps: {len(composite_maps)} file(s)")
    else:
        ok = False
        msgs.append('✗ no composite_drought_*_maps.png')

    msgs.append('--- Circulation cross-section outputs ---')
    for name in CIRCULATION_PLOTS:
        p = circ_dir / name
        if p.exists() and p.stat().st_size > 0:
            msgs.append(f"✓ {p}")
        else:
            ok = False
            msgs.append(f"✗ {p} missing")

    return ok, msgs


def main() -> int:
    parser = argparse.ArgumentParser(description='Verify IOD analysis closure')
    parser.add_argument('--data-dir', default='.', help='Project data root (drought, DMI, atmospheric)')
    parser.add_argument('--stats-output', default='output/comprehensive_iod_statistics',
                        help='Output dir for comprehensive_iod_drought_statistics_optimized.py')
    parser.add_argument('--circ-output', default='output/iod_circulation',
                        help='Output dir for plot_iod_circulation_cross_section.py')
    parser.add_argument('--check-inputs', action='store_true')
    parser.add_argument('--check-outputs', action='store_true')
    parser.add_argument('--strict', action='store_true',
                        help='Fail if optional atmospheric plots missing')
    args = parser.parse_args()

    if not args.check_inputs and not args.check_outputs:
        args.check_inputs = True
        args.check_outputs = True

    data_dir = Path(args.data_dir)
    stats_dir = Path(args.stats_output)
    circ_dir = Path(args.circ_output)
    exit_code = 0

    if args.check_inputs:
        print('INPUT CHECK')
        ok, msgs = check_inputs(data_dir)
        print('\n'.join(msgs))
        if not ok:
            exit_code = 1
        print()

    if args.check_outputs:
        print('OUTPUT CHECK')
        ok, msgs = check_outputs(stats_dir, circ_dir, args.strict)
        print('\n'.join(msgs))
        if not ok:
            exit_code = 1

    if exit_code == 0:
        print('\nCLOSURE: all checked items present.')
    else:
        print('\nCLOSURE: incomplete — run run_iod_analysis_closure.sh or fix missing inputs.')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
