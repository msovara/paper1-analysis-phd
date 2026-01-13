#!/usr/bin/env python3
"""Extract partial correlation statistics from results"""

import pickle
import numpy as np
import sys
from pathlib import Path

# Load data
data_file = Path('/home/msovara/lustre/DataDownloads/data/output/comprehensive_iod_statistics/data/partial_correlation_results.pkl')

print("Loading partial correlation data file...")
try:
    with open(data_file, 'rb') as f:
        data = pickle.load(f)
    print(f"✓ Loaded data file. Available indices: {list(data.keys())}")
except Exception as e:
    print(f"Error loading file: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("PARTIAL CORRELATION ANALYSIS RESULTS")
print("(Controlling for ENSO - Niño3.4)")
print("="*80)

regions = ['East Africa', 'Southern Africa', 'West Africa', 'Central Africa', 'North Africa']

for index_name in ['SPI3', 'SPI6', 'SPEI3', 'SPEI6']:
    if index_name not in data:
        print(f"\n⚠ {index_name} not found in data")
        continue
    
    print(f"\n{index_name}:")
    print("="*80)
    
    index_data = data[index_name]
    
    for region_name in regions:
        if region_name not in index_data:
            print(f"\n  ⚠ {region_name} not found")
            continue
        
        region_data = index_data[region_name]
        
        raw_corr = region_data.get('raw_correlation', np.nan)
        raw_pval = region_data.get('raw_p_value', np.nan)
        partial_corr = region_data.get('partial_correlation', np.nan)
        partial_pval = region_data.get('partial_p_value', np.nan)
        nino34_dmi = region_data.get('nino34_correlation_dmi', np.nan)
        nino34_drought = region_data.get('nino34_correlation_drought', np.nan)
        
        # Calculate independence ratio
        if not np.isnan(raw_corr) and raw_corr != 0:
            independence_ratio = abs(partial_corr / raw_corr) if not np.isnan(partial_corr) else np.nan
            independence_pct = independence_ratio * 100 if not np.isnan(independence_ratio) else np.nan
        else:
            independence_ratio = np.nan
            independence_pct = np.nan
        
        # Calculate reduction in correlation
        if not np.isnan(raw_corr) and not np.isnan(partial_corr):
            reduction = abs(raw_corr) - abs(partial_corr)
            reduction_pct = (reduction / abs(raw_corr)) * 100 if raw_corr != 0 else np.nan
        else:
            reduction = np.nan
            reduction_pct = np.nan
        
        print(f"\n  {region_name}:")
        print(f"    Raw correlation:        {raw_corr:7.3f} (p = {raw_pval:.4f})")
        print(f"    Partial correlation:    {partial_corr:7.3f} (p = {partial_pval:.4f})")
        print(f"    DMI-Niño3.4 correlation: {nino34_dmi:7.3f}")
        print(f"    Drought-Niño3.4 corr:    {nino34_drought:7.3f}")
        
        if not np.isnan(independence_ratio):
            print(f"    Independence ratio:    {independence_ratio:.2f} ({independence_pct:.1f}% of raw correlation remains)")
        
        if not np.isnan(reduction):
            print(f"    Correlation reduction:  {reduction:.3f} ({reduction_pct:.1f}% reduction)")
        
        # Interpretation
        if not np.isnan(partial_corr) and not np.isnan(raw_corr):
            if abs(partial_corr) < 0.1 * abs(raw_corr):
                interpretation = "Strongly ENSO-dependent (most signal removed)"
            elif abs(partial_corr) < 0.5 * abs(raw_corr):
                interpretation = "Moderately ENSO-dependent (substantial signal removed)"
            elif abs(partial_corr) < 0.8 * abs(raw_corr):
                interpretation = "Partially independent (some signal remains)"
            else:
                interpretation = "Largely independent (most signal remains)"
            print(f"    Interpretation:         {interpretation}")

print("\n" + "="*80)
print("SUMMARY: RAW VS PARTIAL CORRELATIONS BY REGION")
print("="*80)

for region_name in regions:
    print(f"\n{region_name}:")
    print(f"{'Index':<10} {'Raw r':>8} {'Partial r':>10} {'Indep %':>10} {'Reduction %':>12}")
    print("-" * 60)
    
    for idx in ['SPI3', 'SPI6', 'SPEI3', 'SPEI6']:
        if idx not in data or region_name not in data[idx]:
            print(f"{idx:<10} {'N/A':>8} {'N/A':>10} {'N/A':>10} {'N/A':>12}")
            continue
        
        region_data = data[idx][region_name]
        raw_corr = region_data.get('raw_correlation', np.nan)
        partial_corr = region_data.get('partial_correlation', np.nan)
        
        if not np.isnan(raw_corr) and raw_corr != 0 and not np.isnan(partial_corr):
            independence_ratio = abs(partial_corr / raw_corr)
            independence_pct = independence_ratio * 100
            reduction_pct = (1 - independence_ratio) * 100
        else:
            independence_pct = np.nan
            reduction_pct = np.nan
        
        raw_str = f"{raw_corr:.3f}" if not np.isnan(raw_corr) else "N/A"
        partial_str = f"{partial_corr:.3f}" if not np.isnan(partial_corr) else "N/A"
        indep_str = f"{independence_pct:.1f}%" if not np.isnan(independence_pct) else "N/A"
        red_str = f"{reduction_pct:.1f}%" if not np.isnan(reduction_pct) else "N/A"
        
        print(f"{idx:<10} {raw_str:>8} {partial_str:>10} {indep_str:>10} {red_str:>12}")

print("\n" + "="*80)
print("SUMMARY: ENSO CORRELATIONS")
print("="*80)

print("\nDMI-Niño3.4 Correlations by Region:")
print(f"{'Region':<20} {'SPI3':>8} {'SPI6':>8} {'SPEI3':>8} {'SPEI6':>8}")
print("-" * 60)
for region_name in regions:
    row = f"{region_name:<20}"
    for idx in ['SPI3', 'SPI6', 'SPEI3', 'SPEI6']:
        if idx in data and region_name in data[idx]:
            nino34_dmi = data[idx][region_name].get('nino34_correlation_dmi', np.nan)
            row += f" {nino34_dmi:>7.3f}" if not np.isnan(nino34_dmi) else f" {'N/A':>8}"
        else:
            row += f" {'N/A':>8}"
    print(row)

print("\nDrought-Niño3.4 Correlations by Region:")
print(f"{'Region':<20} {'SPI3':>8} {'SPI6':>8} {'SPEI3':>8} {'SPEI6':>8}")
print("-" * 60)
for region_name in regions:
    row = f"{region_name:<20}"
    for idx in ['SPI3', 'SPI6', 'SPEI3', 'SPEI6']:
        if idx in data and region_name in data[idx]:
            nino34_drought = data[idx][region_name].get('nino34_correlation_drought', np.nan)
            row += f" {nino34_drought:>7.3f}" if not np.isnan(nino34_drought) else f" {'N/A':>8}"
        else:
            row += f" {'N/A':>8}"
    print(row)

print("\n" + "="*80)

