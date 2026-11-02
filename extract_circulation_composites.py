#!/usr/bin/env python3
"""Extract circulation composite statistics from ERA5 data"""

import pickle
import numpy as np
import sys
from pathlib import Path
import xarray as xr

# Regional definitions (lat, lon bounds)
regions = {
    'East Africa': {'lat': (-10, 20), 'lon': (30, 50)},
    'Southern Africa': {'lat': (-35, -10), 'lon': (10, 40)},
    'West Africa': {'lat': (-5, 20), 'lon': (-20, 20)},
    'Central Africa': {'lat': (-10, 15), 'lon': (5, 30)},
    'North Africa': {'lat': (15, 37), 'lon': (-20, 55)}
}

def calculate_regional_mean(data, lat_coord, lon_coord, lat_bounds, lon_bounds, region_name="", debug=False):
    """Calculate mean for a region"""
    try:
        lat_min, lat_max = lat_bounds
        lon_min, lon_max = lon_bounds

        # Use xarray's where with coordinate conditions
        region_data = data.where(
            (data[lat_coord] >= lat_min) &
            (data[lat_coord] <= lat_max) &
            (data[lon_coord] >= lon_min) &
            (data[lon_coord] <= lon_max),
            drop=False
        )

        # Get values and calculate mean
        values = region_data.values
        valid_mask = ~np.isnan(values)

        if not np.any(valid_mask):
            return np.nan

        mean_val = float(np.nanmean(values))
        return mean_val
    except Exception as e:
        print(f"  Error calculating mean for region {region_name}: {e}", file=sys.stderr)
        return np.nan

def calculate_wind_speed(u_data, v_data, lat_coord, lon_coord, lat_bounds, lon_bounds):
    """Calculate mean wind speed for a region"""
    try:
        lat_min, lat_max = lat_bounds
        lon_min, lon_max = lon_bounds

        # Select region for both components
        u_region = u_data.where(
            (u_data[lat_coord] >= lat_min) &
            (u_data[lat_coord] <= lat_max) &
            (u_data[lon_coord] >= lon_min) &
            (u_data[lon_coord] <= lon_max),
            drop=False
        )

        v_region = v_data.where(
            (v_data[lat_coord] >= lat_min) &
            (v_data[lat_coord] <= lat_max) &
            (v_data[lon_coord] >= lon_min) &
            (v_data[lon_coord] <= lon_max),
            drop=False
        )

        # Calculate wind speed
        wind_speed = np.sqrt(u_region**2 + v_region**2)
        mean_speed = float(np.nanmean(wind_speed.values))
        return mean_speed
    except Exception as e:
        print(f"  Error calculating wind speed: {e}", file=sys.stderr)
        return np.nan

# Check for saved circulation composite data
data_dir = Path('/home/msovara/lustre/DataDownloads/data/output/comprehensive_iod_statistics/data')
circulation_file = data_dir / 'atmospheric_circulation_composites.pkl'

print("Checking for circulation composite data...")
if not circulation_file.exists():
    print(f"⚠ Circulation composite data file not found: {circulation_file}")
    print("This script requires the circulation composites to be saved as a pickle file.")
    print("The data may be available in the ERA5 files directly.")
    sys.exit(1)

print(f"Loading circulation composite data from: {circulation_file}")
try:
    with open(circulation_file, 'rb') as f:
        data = pickle.load(f)
    print(f"✓ Loaded data file. Available variables: {list(data.keys())}")
except Exception as e:
    print(f"Error loading file: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("ERA5 CIRCULATION COMPOSITE STATISTICS")
print("="*80)

# Process each variable
for var_name in ['mslp', 'u850', 'v850', 'z500']:
    if var_name not in data:
        print(f"\n⚠ {var_name} not found in data")
        continue
    
    print(f"\n{var_name.upper()}:")
    print("="*80)
    
    var_data = data[var_name]
    
    # Get coordinate names
    lat_coord = 'lat' if 'lat' in var_data.coords else 'latitude'
    lon_coord = 'lon' if 'lon' in var_data.coords else 'longitude'
    
    # Process positive and negative IOD composites
    for iod_phase in ['positive_iod', 'negative_iod']:
        if iod_phase not in var_data:
            print(f"  ⚠ {iod_phase} not found")
            continue
        
        phase_data = var_data[iod_phase]
        
        if 'composite' in phase_data:
            composite = phase_data['composite']
            significant = phase_data.get('significant', None)
            
            print(f"\n  {iod_phase.replace('_', ' ').title()}:")
            
            # Calculate regional averages
            for region_name, bounds in regions.items():
                mean_val = calculate_regional_mean(composite, lat_coord, lon_coord,
                                                  bounds['lat'], bounds['lon'],
                                                  region_name=region_name)
                
                # Calculate significance percentage
                if significant is not None:
                    sig_region = significant.where(
                        (significant[lat_coord] >= bounds['lat'][0]) &
                        (significant[lat_coord] <= bounds['lat'][1]) &
                        (significant[lon_coord] >= bounds['lon'][0]) &
                        (significant[lon_coord] <= bounds['lon'][1]),
                        drop=False
                    )
                    sig_pct = float(np.nanmean(sig_region.values) * 100) if sig_region is not None else np.nan
                else:
                    sig_pct = np.nan
                
                unit = 'hPa' if var_name == 'mslp' else 'm' if var_name == 'z500' else 'm/s'
                print(f"    {region_name:20s}: {mean_val:7.3f} {unit} (sig: {sig_pct:.1f}%)")
            
            # Calculate global statistics
            global_mean = float(np.nanmean(composite.values))
            global_max = float(np.nanmax(composite.values))
            global_min = float(np.nanmin(composite.values))
            unit = 'hPa' if var_name == 'mslp' else 'm' if var_name == 'z500' else 'm/s'
            print(f"    Global mean: {global_mean:.3f} {unit}, range: [{global_min:.3f}, {global_max:.3f}] {unit}")

# Calculate wind vector statistics if both u850 and v850 are available
if 'u850' in data and 'v850' in data:
    print("\n" + "="*80)
    print("850 HPA WIND VECTOR STATISTICS")
    print("="*80)
    
    u_data = data['u850']
    v_data = data['v850']
    
    lat_coord = 'lat' if 'lat' in u_data.coords else 'latitude'
    lon_coord = 'lon' if 'lon' in u_data.coords else 'longitude'
    
    for iod_phase in ['positive_iod', 'negative_iod']:
        if iod_phase not in u_data or iod_phase not in v_data:
            continue
        
        u_phase = u_data[iod_phase].get('composite', None)
        v_phase = v_data[iod_phase].get('composite', None)
        
        if u_phase is None or v_phase is None:
            continue
        
        print(f"\n  {iod_phase.replace('_', ' ').title()}:")
        
        # Calculate regional wind speeds
        for region_name, bounds in regions.items():
            u_region = u_phase.where(
                (u_phase[lat_coord] >= bounds['lat'][0]) &
                (u_phase[lat_coord] <= bounds['lat'][1]) &
                (u_phase[lon_coord] >= bounds['lon'][0]) &
                (u_phase[lon_coord] <= bounds['lon'][1]),
                drop=False
            )
            
            v_region = v_phase.where(
                (v_phase[lat_coord] >= bounds['lat'][0]) &
                (v_phase[lat_coord] <= bounds['lat'][1]) &
                (v_phase[lon_coord] >= bounds['lon'][0]) &
                (v_phase[lon_coord] <= bounds['lon'][1]),
                drop=False
            )
            
            # Calculate mean wind speed and direction
            wind_speed = np.sqrt(u_region**2 + v_region**2)
            mean_speed = float(np.nanmean(wind_speed.values))
            
            mean_u = float(np.nanmean(u_region.values))
            mean_v = float(np.nanmean(v_region.values))
            
            # Calculate direction (meteorological convention: 0° = N, 90° = E)
            wind_dir = np.arctan2(mean_u, mean_v) * 180 / np.pi
            if wind_dir < 0:
                wind_dir += 360
            
            print(f"    {region_name:20s}: Speed: {mean_speed:.3f} m/s, U: {mean_u:.3f} m/s, V: {mean_v:.3f} m/s, Dir: {wind_dir:.1f}°")

print("\n" + "="*80)

