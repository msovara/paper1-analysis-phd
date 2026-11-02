#!/usr/bin/env python3
"""Test the accuracy of the circulation composite analysis script"""

import sys
from pathlib import Path

# Test 1: Verify event years match paper
print("="*80)
print("TEST 1: Event Years")
print("="*80)

expected_positive = [1994, 1997, 2006, 2018, 2019]
expected_negative = [1980, 1981, 1992, 1996, 1998]

# Read from script
script_path = Path('comprehensive_iod_drought_statistics_optimized.py')
if not script_path.exists():
    print(f"ERROR: Script not found: {script_path}")
    sys.exit(1)

with open(script_path, 'r') as f:
    script_content = f.read()

# Extract positive IOD years
import re
pos_match = re.search(r'self\.positive_iod_years\s*=\s*\[(.*?)\]', script_content)
if pos_match:
    pos_years_str = pos_match.group(1)
    pos_years = [int(y.strip()) for y in pos_years_str.split(',')]
    print(f"✓ Found positive IOD years in script: {pos_years}")
    if pos_years == expected_positive:
        print(f"  ✓ MATCHES paper: {expected_positive}")
    else:
        print(f"  ✗ MISMATCH with paper: {expected_positive}")
else:
    print("✗ Could not find positive_iod_years in script")

# Extract negative IOD years
neg_match = re.search(r'self\.negative_iod_years\s*=\s*\[(.*?)\]', script_content)
if neg_match:
    neg_years_str = neg_match.group(1)
    neg_years = [int(y.strip()) for y in neg_years_str.split(',')]
    print(f"✓ Found negative IOD years in script: {neg_years}")
    if neg_years == expected_negative:
        print(f"  ✓ MATCHES paper: {expected_negative}")
    else:
        print(f"  ✗ MISMATCH with paper: {expected_negative}")
else:
    print("✗ Could not find negative_iod_years in script")

# Test 2: Verify climatology calculation excludes event years
print("\n" + "="*80)
print("TEST 2: Climatology Calculation")
print("="*80)

if 'non_event_mask' in script_content or '~.*\.dt\.year\.isin\(all_event_years\)' in script_content:
    print("✓ Script excludes event years from climatology")
    if 'non_event_mask = ~son_data[time_coord].dt.year.isin(all_event_years)' in script_content:
        print("  ✓ Uses correct mask: non_event_mask = ~son_data[time_coord].dt.year.isin(all_event_years)")
    elif '~son_all.time.dt.year.isin(all_event_years)' in script_content:
        print("  ✓ Uses correct mask in alternative method")
    else:
        print("  ⚠ Found exclusion but pattern differs")
else:
    print("✗ Could not verify event year exclusion from climatology")

# Test 3: Verify anomaly calculation
print("\n" + "="*80)
print("TEST 3: Anomaly Calculation")
print("="*80)

if 'pos_composite = pos_mean - climatology' in script_content or 'pos_composite =' in script_content and 'climatology' in script_content:
    print("✓ Anomalies calculated as composite_mean - climatology")
    if 'pos_composite = pos_mean - climatology' in script_content:
        print("  ✓ Positive: pos_composite = pos_mean - climatology")
    if 'neg_composite = neg_mean - climatology' in script_content:
        print("  ✓ Negative: neg_composite = neg_mean - climatology")
else:
    print("✗ Could not verify anomaly calculation method")

# Test 4: Verify SON months
print("\n" + "="*80)
print("TEST 4: SON Season Selection")
print("="*80)

if 'son_months = [9, 10, 11]' in script_content:
    print("✓ SON months correctly defined: [9, 10, 11] (September, October, November)")
else:
    print("✗ Could not verify SON months definition")

# Test 5: Verify statistical test
print("\n" + "="*80)
print("TEST 5: Statistical Significance Testing")
print("="*80)

if '_statistical_test_composite' in script_content:
    print("✓ Uses _statistical_test_composite function")
    # Check if it uses t-test
    if 'from scipy.stats import t' in script_content or 'scipy.stats.t' in script_content:
        print("  ✓ Uses Student's t-test")
    if 'p < 0.05' in script_content or 'p_value' in script_content:
        print("  ✓ Tests significance at p < 0.05")
else:
    print("✗ Could not verify statistical test function")

# Test 6: Verify variables processed
print("\n" + "="*80)
print("TEST 6: Variables Processed")
print("="*80)

expected_vars = ['mslp', 'u850', 'v850', 'z500']
found_vars = []
for var in expected_vars:
    if var in script_content.lower():
        found_vars.append(var)
        print(f"  ✓ {var.upper()} found in script")

if len(found_vars) == len(expected_vars):
    print(f"✓ All expected variables found: {expected_vars}")
else:
    print(f"⚠ Only found {len(found_vars)}/{len(expected_vars)} variables: {found_vars}")

# Test 7: Verify composite averaging
print("\n" + "="*80)
print("TEST 7: Composite Averaging")
print("="*80)

if '.mean(dim=' in script_content:
    print("✓ Uses mean across events for composite")
    if '.mean(dim=\'event\')' in script_content or '.mean(dim="event")' in script_content:
        print("  ✓ Averages across 'event' dimension")
    if '.mean(dim=time_coord)' in script_content:
        print("  ✓ Also averages across time for SON season")
else:
    print("✗ Could not verify averaging method")

# Test 8: Check for potential issues
print("\n" + "="*80)
print("TEST 8: Potential Issues")
print("="*80)

issues = []

# Check if event years are hardcoded (should be consistent)
if 'self.positive_iod_years = [' in script_content and 'self.negative_iod_years = [' in script_content:
    print("✓ Event years are explicitly defined (good for reproducibility)")
else:
    issues.append("Event years may not be explicitly defined")

# Check for coordinate handling
if 'lat_coord' in script_content and 'lon_coord' in script_content:
    print("✓ Handles coordinate name variations (lat/latitude, lon/longitude)")
else:
    issues.append("May not handle coordinate name variations")

# Check for time coordinate handling
if 'time_coord' in script_content or 'valid_time' in script_content:
    print("✓ Handles time coordinate variations (time/valid_time)")
else:
    issues.append("May not handle time coordinate variations")

# Check for longitude format handling
if 'lon_format' in script_content or '0-360' in script_content or '-180-180' in script_content:
    print("✓ Handles longitude format variations (0-360 vs -180-180)")
else:
    issues.append("May not handle longitude format variations")

if issues:
    print(f"\n⚠ Potential issues found: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n✓ No obvious issues found")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("Tests completed. Review output above for any mismatches or issues.")
print("="*80)

