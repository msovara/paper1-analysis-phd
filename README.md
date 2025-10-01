## Recommended time period for DMI analysis
### Standard Research Period (1980-2020): 40-year period provides robust statistical analysis and coveres major IOD events (1997-98, 2006-07, 2011-12, 2016). Sufficient for drought analysis (minimum 20 years required)

# DMI Extraction from HadISST Data - Complete Guide

This guide shows you how to extract DMI (Dipole Mode Index) data from your HadISST sea surface temperature dataset for the 1980-2020 period.

## 📊 What is DMI?

The Dipole Mode Index (DMI) measures the Indian Ocean Dipole (IOD) by calculating the difference in sea surface temperature between:
- **Western Indian Ocean** (50°E-70°E, 10°S-10°N)
- **Eastern Indian Ocean** (90°E-110°E, 10°S-0°N)

**Formula**: DMI = Western SST - Eastern SST

## 🎯 Your HadISST Data

Your file contains:
- **Time period**: 1870-present (1867 time steps)
- **Spatial resolution**: 1° × 1° (180 lat × 360 lon)
- **Temporal resolution**: Monthly
- **Study period**: 1980-2020 (492 months)

## 🚀 Quick Start

### Step 1: Prepare Your Environment
```bash
# On Lengau cluster
ssh -X msovara@lengau.chpc.ac.za
cd /path/to/your/DataDownloads

# Make sure HadISST_sst.nc is in your directory
ls -la HadISST_sst.nc
```

### Step 2: Run DMI Extraction
```bash
# Make the script executable
chmod +x run_dmi_extraction_lengau.sh

# Run the extraction
./run_dmi_extraction_lengau.sh
```

### Step 3: Check Results
```bash
# View the extracted DMI data
head -20 output/processed/dmi_hadisst_1980_2020.csv

# View the analysis plot
ls -la output/plots/
```

## 📈 What the Script Does

### 1. **Data Loading**
- Loads HadISST data for 1980-2020 period
- Handles time conversion from days since 1870
- Selects appropriate spatial and temporal subset

### 2. **DMI Calculation**
- Defines Western Indian Ocean region (50°E-70°E, 10°S-10°N)
- Defines Eastern Indian Ocean region (90°E-110°E, 10°S-0°N)
- Calculates area-weighted mean SST for each region
- Computes DMI = Western SST - Eastern SST

### 3. **Data Processing**
- Creates monthly DMI time series
- Adds year and month columns
- Removes any missing values
- Formats data for analysis

### 4. **Analysis**
- Calculates basic statistics (mean, std, min, max)
- Identifies positive and negative IOD events
- Creates seasonal cycle analysis
- Generates annual means

### 5. **Visualization**
- Time series plot with thresholds
- Seasonal cycle analysis
- Distribution histogram
- Annual means plot

## 📁 Output Files

After running the script, you'll get:

```
output/
├── processed/
│   └── dmi_hadisst_1980_2020.csv    # DMI time series data
└── plots/
    └── dmi_analysis_hadisst.png     # Analysis plots

logs/
└── dmi_extraction_YYYYMMDD_HHMMSS.log  # Detailed log file
```

## 📊 DMI Data Format

The output CSV file contains:
```csv
time,month,year,DMI
1980-01-01,1,1980,0.123
1980-02-01,2,1980,-0.456
...
2020-12-01,12,2020,0.789
```

## 🔍 Understanding DMI Values

- **DMI > 0.5**: Positive IOD event (warm western, cool eastern Indian Ocean)
- **DMI < -0.5**: Negative IOD event (cool western, warm eastern Indian Ocean)
- **|DMI| > 1.0**: Strong IOD event
- **|DMI| < 0.5**: Neutral conditions

## 📈 Expected Results

Based on your 1980-2020 period, you should see:

### **Major IOD Events Captured:**
- **1982-83**: Strong positive IOD
- **1997-98**: Strong positive IOD (coincided with El Niño)
- **2006-07**: Strong positive IOD
- **2011-12**: Strong positive IOD
- **2016**: Strong negative IOD

### **Statistical Summary:**
- **Mean DMI**: ~0.0 (neutral)
- **Standard Deviation**: ~0.5-0.8
- **Positive Events**: 15-25 months
- **Negative Events**: 15-25 months
- **Strong Events**: 5-10 months

## 🛠️ Customization Options

### **Modify Time Period**
```python
# In extract_dmi_from_hadisst.py, change:
self.start_year = 1980
self.end_year = 2020
```

### **Modify IOD Regions**
```python
# Western region
self.western_region = {
    'lon_min': 50, 'lon_max': 70,
    'lat_min': -10, 'lat_max': 10
}

# Eastern region
self.eastern_region = {
    'lon_min': 90, 'lon_max': 110,
    'lat_min': -10, 'lat_max': 0
}
```

### **Change Event Thresholds**
```python
# In identify_iod_events method:
threshold = 0.5  # Change to 0.4 or 0.6 as needed
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **File Not Found**
   ```bash
   # Check if HadISST file exists
   ls -la HadISST_sst.nc
   
   # If not found, check the path in the script
   ```

2. **Memory Issues**
   ```bash
   # Load more memory modules
   module load python/3.8.5
   module load gcc/9.3.0
   ```

3. **Time Conversion Issues**
   - The script handles different time formats automatically
   - Check the log file for any time conversion errors

### **Check Results:**
```bash
# View DMI data
head -20 output/processed/dmi_hadisst_1980_2020.csv

# Check data quality
python3 -c "
import pandas as pd
df = pd.read_csv('output/processed/dmi_hadisst_1980_2020.csv', index_col=0, parse_dates=True)
print(f'Records: {len(df)}')
print(f'Period: {df.index.min()} to {df.index.max()}')
print(f'DMI range: {df.DMI.min():.3f} to {df.DMI.max():.3f}')
"
```

## 📊 Data Analysis

After extraction, you can analyze the DMI data:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load DMI data
df = pd.read_csv('output/processed/dmi_hadisst_1980_2020.csv', index_col=0, parse_dates=True)

# Basic statistics
print("DMI Statistics:")
print(df['DMI'].describe())

# Plot time series
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['DMI'], 'b-', linewidth=1)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7)
plt.axhline(y=-0.5, color='blue', linestyle='--', alpha=0.7)
plt.title('DMI Time Series (1980-2020)')
plt.xlabel('Date')
plt.ylabel('DMI')
plt.grid(True, alpha=0.3)
plt.show()
```

## 🎯 Next Steps

After extracting DMI data:

1. **Integrate with drought analysis** - Use DMI data in your drought correlation studies
2. **Compare with other sources** - Validate against JAMSTEC, NOAA, BOM data
3. **Create correlation analysis** - Analyze DMI-drought relationships
4. **Generate reports** - Create comprehensive analysis reports

## 📚 References

- **HadISST**: Rayner et al. (2003) - Global analyses of sea surface temperature
- **IOD Definition**: Saji et al. (1999) - A dipole mode in the tropical Indian Ocean
- **DMI Calculation**: Webster et al. (1999) - Coupled ocean-atmosphere dynamics

This extraction gives you high-quality DMI data directly from sea surface temperature observations, which is often more reliable than downloaded index data!


## 1. Correlation Analysis

Performing a correlation analysis between DMI (Dipole Mode Index) and drought indices (e.g., SPI – Standardized Precipitation Index, SPEI – Standardized Precipitation Evapotranspiration Index) is a common approach in climate and environmental studies to understand how large-scale climate patterns like the Indian Ocean Dipole influence regional drought conditions.

🧪 1. Understand Your Data
You’ll need:
- DMI dataset: Monthly or seasonal DMI values (usually from agencies like JMA or NOAA)
- Drought index dataset: e.g., SPI/SPEI at a specific time scale (e.g., SPI-3, SPI-6, SPI-12)

*Ensure both datasets are aligned in time (same start/end dates, same temporal resolution — monthly is ideal)*


### Python script template that:
- Loads your DMI and drought index data
- Aligns the time series
- Performs both Pearson and Spearman correlation
- Includes lagged analysis
- Visualizes the results

```python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

# -----------------------------
# 1. Load Your Data
# -----------------------------
# Replace these with your actual file paths
dmi_file = 'dmi_monthly.csv'     # e.g., columns: date, DMI
drought_file = 'spi_monthly.csv' # e.g., columns: date, SPI/SPEI

# Load data
dmi_df = pd.read_csv(dmi_file, parse_dates=['date'], index_col='date')
drought_df = pd.read_csv(drought_file, parse_dates=['date'], index_col='date')

# Rename column for clarity (optional)
dmi_df.columns = ['DMI']
drought_df.columns = ['Drought_Index']

# -----------------------------
# 2. Align Time Series
# -----------------------------
# Merge datasets on date
combined = pd.merge(dmi_df, drought_df, left_index=True, right_index=True, how='inner')

# Optional: Resample if needed (e.g., to monthly or seasonal)
# combined = combined.resample('M').mean()

print("Data successfully loaded and aligned.")
print(f"Time range: {combined.index.min()} to {combined.index.max()}")
print(f"Total overlapping months: {len(combined)}\n")

# -----------------------------
# 3. Basic Correlation Analysis
# -----------------------------
pear_corr, pear_p = pearsonr(combined['DMI'], combined['Drought_Index'])
spear_corr, spear_p = spearmanr(combined['DMI'], combined['Drought_Index'])

print(f"Pearson Correlation: {pear_corr:.3f}, p-value: {pear_p:.4f}")
print(f"Spearman Correlation: {spear_corr:.3f}, p-value: {spear_p:.4f}\n")

# -----------------------------
# 4. Lagged Correlation Analysis
# -----------------------------
max_lag = 6  # test up to 6 months lag
lag_results = []

for lag in range(0, max_lag + 1):
    lagged = combined.copy()
    lagged['DMI'] = lagged['DMI'].shift(lag)
    lagged.dropna(inplace=True)

    if len(lagged) == 0:
        continue

    corr, p = pearsonr(lagged['DMI'], lagged['Drought_Index'])
    lag_results.append({'lag': lag, 'correlation': corr, 'p_value': p})

lag_df = pd.DataFrame(lag_results)
print("Lagged Pearson Correlation Results:")
print(lag_df.to_string(index=False))

# -----------------------------
# 5. Visualization
# -----------------------------

# A. Scatter Plot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='DMI', y='Drought_Index', data=combined)
plt.title(f"DMI vs Drought Index\nPearson r = {pear_corr:.2f}")
plt.xlabel("DMI")
plt.ylabel("Drought Index")
plt.grid(True)
plt.tight_layout()
plt.show()

# B. Time Series Plot
fig, ax1 = plt.subplots(figsize=(12, 6))
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('DMI', color=color)
ax1.plot(combined.index, combined['DMI'], label='DMI', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Drought Index', color=color)
ax2.plot(combined.index, combined['Drought_Index'], label='Drought Index', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title("DMI and Drought Index Over Time")
plt.grid(True)
plt.show()

# C. Lagged Correlation Plot
plt.figure(figsize=(10, 5))
sns.barplot(x='lag', y='correlation', data=lag_df, palette='viridis')
plt.axhline(0, color='black', linewidth=0.8)
plt.title("Lagged Pearson Correlation Between DMI and Drought Index")
plt.xlabel("Lag (months)")
plt.ylabel("Correlation Coefficient")
plt.grid(True, axis='y', linestyle='--')
plt.tight_layout()
plt.show()
```
Manus created three comprehensive Python scripts for the results section of your PhD thesis on drought prediction in Southern Africa. These scripts will help you analyze and visualize the key findings from your research:
1. - **IOD-Drought Correlation Analysis** - This script analyzes the relationship between the Indian Ocean Dipole and drought patterns across Southern Africa, including correlation maps, time series analysis, composite analysis, and lag correlation.
2. - **Hierarchical Model Performance Analysis** - This script evaluates your three-level prediction model (Global/ICON, Regional/MPAS, Local/AI), comparing physics-informed vs. pure data-driven approaches and analyzing case studies of major drought events.
3. - **Ensemble Forecast Visualization** - This script visualizes ensemble drought forecasts with uncertainty quantification, probability mapping, and verification metrics to demonstrate the robustness of your predictions.


## ```iod_drought_correlation_analysis.py```
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IOD-Drought Correlation Analysis Script

This script analyzes the correlation between the Indian Ocean Dipole (IOD) index
and drought indices across Southern Africa. It generates correlation maps,
time series analyses, and statistical significance tests to quantify the
relationship between IOD phases and drought conditions.

Author: [Your Name]
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import xarray as xr
from scipy import stats
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import os

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

# Create output directory for figures
os.makedirs("figures", exist_ok=True)

# ============================================================================
# Data Loading Functions
# ============================================================================

def load_iod_index(file_path=None):
    """
    Load the Indian Ocean Dipole (DMI) index data.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Returns:
        pd.DataFrame: Monthly IOD index with datetime index
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        iod_data = pd.read_csv(file_path, parse_dates=['date'])
        iod_data.set_index('date', inplace=True)
        return iod_data
    else:
        # Generate synthetic IOD index data for demonstration
        print("Generating synthetic IOD index data for demonstration")
        dates = pd.date_range(start='1980-01-01', end='2020-12-31', freq='MS')
        
        # Create seasonal cycle with random variations
        annual_cycle = np.sin(np.linspace(0, 2*np.pi, 12))
        monthly_values = np.tile(annual_cycle, len(dates)//12 + 1)[:len(dates)]
        
        # Add multi-year variability and random noise
        years = np.arange(len(dates)) / 12
        multi_year = 0.5 * np.sin(2 * np.pi * years / 3)  # ~3 year cycle
        noise = np.random.normal(0, 0.3, len(dates))
        
        iod_values = monthly_values + multi_year + noise
        
        # Create DataFrame
        iod_data = pd.DataFrame({
            'DMI': iod_values
        }, index=dates)
        
        return iod_data

def load_drought_data(file_path=None):
    """
    Load drought index data (SPI/SPEI) for Southern Africa.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Returns:
        xr.Dataset: Drought indices with lat, lon, time dimensions
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        drought_data = xr.open_dataset(file_path)
        return drought_data
    else:
        # Generate synthetic drought data for demonstration
        print("Generating synthetic drought index data for demonstration")
        
        # Define grid for Southern Africa
        lats = np.linspace(-35, -10, 50)
        lons = np.linspace(10, 40, 50)
        times = pd.date_range(start='1980-01-01', end='2020-12-31', freq='MS')
        
        # Create lat/lon meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Initialize data arrays
        spi3_data = np.zeros((len(times), len(lats), len(lons)))
        spi6_data = np.zeros((len(times), len(lats), len(lons)))
        
        # Generate base spatial pattern (more drought-prone in southeast)
        base_pattern = ((lat_grid + 35) / 25) * ((lon_grid - 10) / 30)
        
        # Generate temporal patterns
        for t in range(len(times)):
            # Seasonal cycle
            month = times[t].month
            seasonal = np.sin(2 * np.pi * (month - 3) / 12)  # Peak in March
            
            # Multi-year variability (simplified IOD/ENSO influence)
            year_frac = times[t].year + (times[t].month - 1) / 12
            multi_year = 0.5 * np.sin(2 * np.pi * (year_frac - 1980) / 3)
            
            # Spatial variation (southeast more affected by IOD)
            spatial_effect = base_pattern * multi_year
            
            # Random noise with spatial correlation
            noise = np.random.normal(0, 0.3, (len(lats), len(lons)))
            
            # Combine components
            spi3_data[t] = seasonal + spatial_effect + noise
            
            # SPI-6 has more temporal smoothing
            if t >= 3:
                spi6_data[t] = np.mean(spi3_data[t-3:t+1], axis=0)
            else:
                spi6_data[t] = spi3_data[t]
        
        # Create xarray dataset
        drought_data = xr.Dataset(
            data_vars={
                'spi3': (['time', 'lat', 'lon'], spi3_data),
                'spi6': (['time', 'lat', 'lon'], spi6_data),
            },
            coords={
                'lat': lats,
                'lon': lons,
                'time': times,
            }
        )
        
        return drought_data

# ============================================================================
# Analysis Functions
# ============================================================================

def calculate_correlation_map(iod_data, drought_data, drought_index='spi3', 
                             season=None, lag_months=0):
    """
    Calculate correlation between IOD index and drought index across Southern Africa.
    
    Args:
        iod_data (pd.DataFrame): IOD index data with datetime index
        drought_data (xr.Dataset): Drought index data
        drought_index (str): Name of drought index to use ('spi3' or 'spi6')
        season (str, optional): Season to analyze ('DJF', 'MAM', 'JJA', 'SON')
        lag_months (int): Lag in months (positive means IOD leads drought)
    
    Returns:
        xr.Dataset: Correlation coefficients and p-values
    """
    # Extract the drought index data
    drought_var = drought_data[drought_index]
    
    # Align time indices
    common_times = sorted(set(drought_var.time.values).intersection(
        set(pd.DatetimeIndex(iod_data.index).values)))
    
    drought_aligned = drought_var.sel(time=common_times)
    iod_aligned = iod_data.loc[common_times]
    
    # Apply lag if specified
    if lag_months != 0:
        if lag_months > 0:  # IOD leads drought
            iod_times = common_times[:-lag_months]
            drought_times = common_times[lag_months:]
        else:  # Drought leads IOD
            iod_times = common_times[-lag_months:]
            drought_times = common_times[:lag_months]
            
        drought_aligned = drought_var.sel(time=drought_times)
        iod_aligned = iod_data.loc[iod_times]
    
    # Filter by season if specified
    if season:
        season_months = {
            'DJF': [12, 1, 2],
            'MAM': [3, 4, 5],
            'JJA': [6, 7, 8],
            'SON': [9, 10, 11]
        }
        
        # Extract month numbers from datetime index
        months = pd.DatetimeIndex(drought_aligned.time.values).month
        season_mask = np.isin(months, season_months[season])
        
        drought_aligned = drought_aligned.isel(time=season_mask)
        iod_aligned = iod_aligned.iloc[season_mask]
    
    # Initialize correlation and p-value arrays
    corr = np.zeros((len(drought_aligned.lat), len(drought_aligned.lon)))
    pval = np.zeros((len(drought_aligned.lat), len(drought_aligned.lon)))
    
    # Calculate correlation for each grid point
    for i, lat in enumerate(drought_aligned.lat.values):
        for j, lon in enumerate(drought_aligned.lon.values):
            drought_series = drought_aligned.sel(lat=lat, lon=lon).values
            iod_series = iod_aligned['DMI'].values
            
            # Remove any NaN values
            valid_mask = ~np.isnan(drought_series) & ~np.isnan(iod_series)
            if np.sum(valid_mask) > 10:  # Require at least 10 valid data points
                r, p = stats.pearsonr(iod_series[valid_mask], drought_series[valid_mask])
                corr[i, j] = r
                pval[i, j] = p
            else:
                corr[i, j] = np.nan
                pval[i, j] = np.nan
    
    # Create output dataset
    result = xr.Dataset(
        data_vars={
            'correlation': (['lat', 'lon'], corr),
            'pvalue': (['lat', 'lon'], pval),
        },
        coords={
            'lat': drought_aligned.lat,
            'lon': drought_aligned.lon,
        }
    )
    
    return result

def analyze_regional_time_series(iod_data, drought_data, region_bounds, 
                               drought_index='spi3'):
    """
    Analyze time series relationship between IOD and regional drought index.
    
    Args:
        iod_data (pd.DataFrame): IOD index data
        drought_data (xr.Dataset): Drought index data
        region_bounds (dict): Dictionary with 'lat_min', 'lat_max', 'lon_min', 'lon_max'
        drought_index (str): Name of drought index to use
    
    Returns:
        pd.DataFrame: Time series of IOD and regional drought index
    """
    # Extract regional drought data
    regional_drought = drought_data[drought_index].sel(
        lat=slice(region_bounds['lat_min'], region_bounds['lat_max']),
        lon=slice(region_bounds['lon_min'], region_bounds['lon_max'])
    )
    
    # Calculate regional average
    regional_avg = regional_drought.mean(dim=['lat', 'lon'])
    
    # Convert to DataFrame
    regional_df = regional_avg.to_dataframe(name=drought_index)
    
    # Align with IOD data
    common_times = sorted(set(regional_df.index).intersection(set(iod_data.index)))
    aligned_data = pd.DataFrame({
        'DMI': iod_data.loc[common_times, 'DMI'],
        drought_index: regional_df.loc[common_times, drought_index]
    })
    
    return aligned_data

def composite_analysis(iod_data, drought_data, drought_index='spi3', 
                      threshold=0.5, season=None):
    """
    Perform composite analysis of drought conditions during different IOD phases.
    
    Args:
        iod_data (pd.DataFrame): IOD index data
        drought_data (xr.Dataset): Drought index data
        drought_index (str): Name of drought index to use
        threshold (float): Threshold for defining IOD phases
        season (str, optional): Season to analyze
    
    Returns:
        xr.Dataset: Composite drought patterns for positive, negative, and neutral IOD
    """
    # Extract drought index data
    drought_var = drought_data[drought_index]
    
    # Align time indices
    common_times = sorted(set(drought_var.time.values).intersection(
        set(pd.DatetimeIndex(iod_data.index).values)))
    
    drought_aligned = drought_var.sel(time=common_times)
    iod_aligned = iod_data.loc[common_times]
    
    # Filter by season if specified
    if season:
        season_months = {
            'DJF': [12, 1, 2],
            'MAM': [3, 4, 5],
            'JJA': [6, 7, 8],
            'SON': [9, 10, 11]
        }
        
        # Extract month numbers from datetime index
        months = pd.DatetimeIndex(drought_aligned.time.values).month
        season_mask = np.isin(months, season_months[season])
        
        drought_aligned = drought_aligned.isel(time=season_mask)
        iod_aligned = iod_aligned.iloc[season_mask]
    
    # Define IOD phases
    positive_mask = iod_aligned['DMI'] > threshold
    negative_mask = iod_aligned['DMI'] < -threshold
    neutral_mask = (iod_aligned['DMI'] >= -threshold) & (iod_aligned['DMI'] <= threshold)
    
    # Calculate composites
    positive_composite = drought_aligned.isel(time=positive_mask).mean(dim='time')
    negative_composite = drought_aligned.isel(time=negative_mask).mean(dim='time')
    neutral_composite = drought_aligned.isel(time=neutral_mask).mean(dim='time')
    
    # Calculate differences
    pos_minus_neg = positive_composite - negative_composite
    pos_minus_neutral = positive_composite - neutral_composite
    neg_minus_neutral = negative_composite - neutral_composite
    
    # Create output dataset
    result = xr.Dataset(
        data_vars={
            'positive_iod': (['lat', 'lon'], positive_composite.values),
            'negative_iod': (['lat', 'lon'], negative_composite.values),
            'neutral_iod': (['lat', 'lon'], neutral_composite.values),
            'pos_minus_neg': (['lat', 'lon'], pos_minus_neg.values),
            'pos_minus_neutral': (['lat', 'lon'], pos_minus_neutral.values),
            'neg_minus_neutral': (['lat', 'lon'], neg_minus_neutral.values),
        },
        coords={
            'lat': drought_aligned.lat,
            'lon': drought_aligned.lon,
        }
    )
    
    # Add metadata
    result.attrs['positive_count'] = np.sum(positive_mask)
    result.attrs['negative_count'] = np.sum(negative_mask)
    result.attrs['neutral_count'] = np.sum(neutral_mask)
    
    return result

# ============================================================================
# Visualization Functions
# ============================================================================

def plot_correlation_map(correlation_data, title=None, output_file=None):
    """
    Plot correlation map between IOD and drought index.
    
    Args:
        correlation_data (xr.Dataset): Output from calculate_correlation_map
        title (str, optional): Plot title
        output_file (str, optional): Path to save figure
    """
    fig = plt.figure(figsize=(12, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # Set map extent to Southern Africa
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    # Create colormap with white at zero
    cmap = plt.cm.RdBu_r
    
    # Plot correlation
    im = ax.pcolormesh(
        correlation_data.lon, 
        correlation_data.lat, 
        correlation_data.correlation,
        cmap=cmap, 
        vmin=-0.8, 
        vmax=0.8,
        transform=ccrs.PlateCarree()
    )
    
    # Add significance stippling
    significant = correlation_data.pvalue < 0.05
    lons, lats = np.meshgrid(correlation_data.lon, correlation_data.lat)
    ax.scatter(
        lons[significant], 
        lats[significant], 
        color='black', 
        s=1, 
        alpha=0.5,
        transform=ccrs.PlateCarree()
    )
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Correlation Coefficient')
    
    # Add gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    
    # Add title
    if title:
        plt.title(title)
    else:
        plt.title('IOD-Drought Index Correlation')
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_time_series_comparison(time_series_data, title=None, output_file=None):
    """
    Plot time series comparison of IOD and regional drought index.
    
    Args:
        time_series_data (pd.DataFrame): Output from analyze_regional_time_series
        title (str, optional): Plot title
        output_file (str, optional): Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Get column names
    iod_col = 'DMI'
    drought_col = [col for col in time_series_data.columns if col != 'DMI'][0]
    
    # Plot IOD index
    ax1.plot(time_series_data.index, time_series_data[iod_col], 
            color='darkblue', linewidth=1.5)
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.fill_between(time_series_data.index, 
                    time_series_data[iod_col], 0, 
                    where=time_series_data[iod_col] > 0, 
                    color='darkred', alpha=0.3)
    ax1.fill_between(time_series_data.index, 
                    time_series_data[iod_col], 0, 
                    where=time_series_data[iod_col] < 0, 
                    color='darkblue', alpha=0.3)
    ax1.set_ylabel('IOD Index (DMI)')
    ax1.set_title('Indian Ocean Dipole Index')
    
    # Plot drought index
    ax2.plot(time_series_data.index, time_series_data[drought_col], 
            color='darkgreen', linewidth=1.5)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.fill_between(time_series_data.index, 
                    time_series_data[drought_col], 0, 
                    where=time_series_data[drought_col] > 0, 
                    color='darkblue', alpha=0.3)  # Wet conditions
    ax2.fill_between(time_series_data.index, 
                    time_series_data[drought_col], 0, 
                    where=time_series_data[drought_col] < 0, 
                    color='darkred', alpha=0.3)  # Dry conditions
    ax2.set_ylabel(f'Drought Index ({drought_col.upper()})')
    ax2.set_title(f'Regional Drought Index ({drought_col.upper()})')
    
    # Format x-axis
    ax2.set_xlabel('Year')
    fig.autofmt_xdate()
    
    # Calculate and display correlation
    corr = time_series_data[iod_col].corr(time_series_data[drought_col])
    r, p = stats.pearsonr(time_series_data[iod_col], time_series_data[drought_col])
    
    fig.text(0.5, 0.01, f'Correlation: r = {r:.2f} (p = {p:.4f})', 
            ha='center', fontsize=12)
    
    # Add overall title if provided
    if title:
        fig.suptitle(title, fontsize=16, y=1.02)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_composite_maps(composite_data, output_file=None):
    """
    Plot composite maps of drought conditions during different IOD phases.
    
    Args:
        composite_data (xr.Dataset): Output from composite_analysis
        output_file (str, optional): Path to save figure
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), 
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Define plot parameters
    plot_vars = [
        ('positive_iod', 'Positive IOD'),
        ('negative_iod', 'Negative IOD'),
        ('neutral_iod', 'Neutral IOD'),
        ('pos_minus_neg', 'Positive - Negative IOD'),
        ('pos_minus_neutral', 'Positive - Neutral IOD'),
        ('neg_minus_neutral', 'Negative - Neutral IOD')
    ]
    
    # Create colormap with white at zero
    cmap = plt.cm.RdBu_r
    
    # Plot each composite
    for i, (var_name, title) in enumerate(plot_vars):
        ax = axes[i]
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        
        # Set map extent to Southern Africa
        ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
        
        # Determine appropriate color scale
        if 'minus' in var_name:
            vmin, vmax = -1.5, 1.5
        else:
            vmin, vmax = -2, 2
        
        # Plot data
        im = ax.pcolormesh(
            composite_data.lon, 
            composite_data.lat, 
            composite_data[var_name],
            cmap=cmap, 
            vmin=vmin, 
            vmax=vmax,
            transform=ccrs.PlateCarree()
        )
        
        # Add gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                         linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        
        # Only show lat/lon labels on the edges
        if i % 3 == 0:  # Left column
            gl.left_labels = True
        else:
            gl.left_labels = False
            
        if i >= 3:  # Bottom row
            gl.bottom_labels = True
        else:
            gl.bottom_labels = False
        
        # Add title
        ax.set_title(title)
        
        # Add sample count for the first three plots
        if i < 3:
            count_key = f"{var_name.split('_')[0]}_count"
            if count_key in composite_data.attrs:
                ax.text(0.5, -0.1, f"n = {composite_data.attrs[count_key]}", 
                       transform=ax.transAxes, ha='center')
    
    # Add colorbar
    cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
    cbar = fig.colorbar(im, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Drought Index Anomaly')
    
    # Add overall title
    plt.suptitle('Composite Drought Patterns During Different IOD Phases', 
                fontsize=16, y=0.98)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout(rect=[0, 0.07, 1, 0.95])
    plt.show()

def plot_lag_correlation_analysis(iod_data, drought_data, region_bounds, 
                                drought_index='spi3', max_lag=12, 
                                output_file=None):
    """
    Plot lag correlation analysis between IOD and regional drought index.
    
    Args:
        iod_data (pd.DataFrame): IOD index data
        drought_data (xr.Dataset): Drought index data
        region_bounds (dict): Dictionary with 'lat_min', 'lat_max', 'lon_min', 'lon_max'
        drought_index (str): Name of drought index to use
        max_lag (int): Maximum lag in months to analyze
        output_file (str, optional): Path to save figure
    """
    # Extract regional drought data
    regional_drought = drought_data[drought_index].sel(
        lat=slice(region_bounds['lat_min'], region_bounds['lat_max']),
        lon=slice(region_bounds['lon_min'], region_bounds['lon_max'])
    )
    
    # Calculate regional average
    regional_avg = regional_drought.mean(dim=['lat', 'lon'])
    
    # Convert to DataFrame
    regional_df = regional_avg.to_dataframe(name=drought_index)
    
    # Align with IOD data
    common_times = sorted(set(regional_df.index).intersection(set(iod_data.index)))
    aligned_data = pd.DataFrame({
        'DMI': iod_data.loc[common_times, 'DMI'],
        drought_index: regional_df.loc[common_times, drought_index]
    })
    
    # Calculate lag correlations
    lags = range(-max_lag, max_lag + 1)
    correlations = []
    p_values = []
    
    for lag in lags:
        if lag < 0:  # IOD lags drought
            x = aligned_data[drought_index].iloc[:lag].values
            y = aligned_data['DMI'].iloc[-lag:].values
        elif lag > 0:  # IOD leads drought
            x = aligned_data['DMI'].iloc[:-lag].values
            y = aligned_data[drought_index].iloc[lag:].values
        else:  # No lag
            x = aligned_data['DMI'].values
            y = aligned_data[drought_index].values
        
        # Remove NaN values
        mask = ~np.isnan(x) & ~np.isnan(y)
        if np.sum(mask) > 10:  # Require at least 10 valid data points
            r, p = stats.pearsonr(x[mask], y[mask])
            correlations.append(r)
            p_values.append(p)
        else:
            correlations.append(np.nan)
            p_values.append(np.nan)
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot correlation bars
    bars = ax.bar(lags, correlations, width=0.8, alpha=0.7)
    
    # Color bars by significance
    for i, (bar, p) in enumerate(zip(bars, p_values)):
        if p < 0.05:
            bar.set_color('darkred')
        else:
            bar.set_color('gray')
    
    # Add reference line at zero
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add significance threshold lines
    n = len(aligned_data)
    r_crit = 2 / np.sqrt(n)  # Approximate critical r for p=0.05
    ax.axhline(y=r_crit, color='red', linestyle='--', alpha=0.5)
    ax.axhline(y=-r_crit, color='red', linestyle='--', alpha=0.5)
    
    # Add labels and title
    ax.set_xlabel('Lag (months)')
    ax.set_ylabel('Correlation Coefficient')
    ax.set_title(f'Lag Correlation Analysis: IOD vs {drought_index.upper()}')
    
    # Add text explaining lag direction
    ax.text(0.05, 0.95, 'Negative lag: Drought leads IOD', 
           transform=ax.transAxes, ha='left', va='top')
    ax.text(0.95, 0.95, 'Positive lag: IOD leads Drought', 
           transform=ax.transAxes, ha='right', va='top')
    
    # Add significance note
    ax.text(0.5, -0.15, 'Red bars indicate significant correlation (p < 0.05)', 
           transform=ax.transAxes, ha='center')
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# Main Analysis
# ============================================================================

def main():
    """
    Main analysis function.
    """
    print("Starting IOD-Drought Correlation Analysis")
    
    # Load data
    print("Loading data...")
    iod_data = load_iod_index()
    drought_data = load_drought_data()
    
    # Define regions of interest
    regions = {
        'southeastern': {'lat_min': -35, 'lat_max': -25, 'lon_min': 25, 'lon_max': 35},
        'central': {'lat_min': -25, 'lat_max': -15, 'lon_min': 20, 'lon_max': 30},
        'southwestern': {'lat_min': -35, 'lat_max': -25, 'lon_min': 15, 'lon_max': 25},
    }
    
    # 1. Calculate and plot correlation maps
    print("\nCalculating correlation maps...")
    for drought_index in ['spi3', 'spi6']:
        for season in [None, 'DJF', 'MAM', 'JJA', 'SON']:
            season_str = season if season else 'Annual'
            print(f"  Processing {drought_index.upper()} for {season_str} season...")
            
            corr_data = calculate_correlation_map(
                iod_data, drought_data, drought_index=drought_index, season=season)
            
            title = f"IOD-{drought_index.upper()} Correlation ({season_str})"
            output_file = f"figures/correlation_{drought_index}_{season_str}.png"
            
            plot_correlation_map(corr_data, title=title, output_file=output_file)
    
    # 2. Analyze and plot regional time series
    print("\nAnalyzing regional time series...")
    for region_name, region_bounds in regions.items():
        for drought_index in ['spi3', 'spi6']:
            print(f"  Processing {region_name} region with {drought_index.upper()}...")
            
            ts_data = analyze_regional_time_series(
                iod_data, drought_data, region_bounds, drought_index=drought_index)
            
            title = f"IOD and {drought_index.upper()} Relationship in {region_name.title()} Southern Africa"
            output_file = f"figures/time_series_{region_name}_{drought_index}.png"
            
            plot_time_series_comparison(ts_data, title=title, output_file=output_file)
    
    # 3. Perform and plot composite analysis
    print("\nPerforming composite analysis...")
    for drought_index in ['spi3', 'spi6']:
        for season in [None, 'SON']:  # Focus on annual and SON (peak IOD season)
            season_str = season if season else 'Annual'
            print(f"  Processing {drought_index.upper()} for {season_str} season...")
            
            composite_data = composite_analysis(
                iod_data, drought_data, drought_index=drought_index, 
                threshold=0.5, season=season)
            
            output_file = f"figures/composite_{drought_index}_{season_str}.png"
            
            plot_composite_maps(composite_data, output_file=output_file)
    
    # 4. Perform and plot lag correlation analysis
    print("\nPerforming lag correlation analysis...")
    for region_name, region_bounds in regions.items():
        for drought_index in ['spi3', 'spi6']:
            print(f"  Processing {region_name} region with {drought_index.upper()}...")
            
            output_file = f"figures/lag_correlation_{region_name}_{drought_index}.png"
            
            plot_lag_correlation_analysis(
                iod_data, drought_data, region_bounds, 
                drought_index=drought_index, max_lag=12, 
                output_file=output_file)
    
    print("\nAnalysis complete. All figures saved to 'figures/' directory.")

if __name__ == "__main__":
    main()
```
---

## ```hierachical_model_performance_analysis.py```
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hierarchical Model Performance Analysis Script

This script analyzes the performance of the hierarchical prediction model for
drought forecasting in Southern Africa. It evaluates the three-level architecture
(Global/ICON, Regional/MPAS, Local/AI) and compares physics-informed vs. 
pure data-driven approaches.

Author: [Your Name]
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import xarray as xr
from scipy import stats
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import r2_score, explained_variance_score
import os

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

# Create output directory for figures
os.makedirs("figures", exist_ok=True)

# ============================================================================
# Data Loading Functions
# ============================================================================

def load_model_performance_data(file_path=None):
    """
    Load model performance data for different approaches.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Returns:
        pd.DataFrame: Performance metrics for different models and regions
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        performance_data = pd.read_csv(file_path)
        return performance_data
    else:
        # Generate synthetic performance data for demonstration
        print("Generating synthetic model performance data for demonstration")
        
        # Define models, regions, and metrics
        models = [
            'Hierarchical (Full)',
            'Global Only (ICON)',
            'Regional Only (MPAS)',
            'Local Only (AI)',
            'Physics-Informed',
            'Pure Data-Driven'
        ]
        
        regions = [
            'Southeastern',
            'Central',
            'Northwestern',
            'Southwestern'
        ]
        
        metrics = [
            'RMSE',
            'MAE',
            'R²',
            'Correlation',
            'Bias',
            'Explained Variance'
        ]
        
        lead_times = [1, 2, 3]
        
        # Create empty list to store data
        data = []
        
        # Generate synthetic performance data
        for model in models:
            # Base performance varies by model
            if model == 'Hierarchical (Full)':
                base_perf = 0.75
            elif model in ['Global Only (ICON)', 'Regional Only (MPAS)', 'Local Only (AI)']:
                base_perf = 0.6
            elif model == 'Physics-Informed':
                base_perf = 0.7
            else:  # Pure Data-Driven
                base_perf = 0.55
            
            for region in regions:
                # Regional variation (southeast has better performance due to stronger IOD signal)
                region_factor = 1.0 if region == 'Southeastern' else \
                               0.9 if region == 'Central' else \
                               0.8 if region == 'Northwestern' else 0.85
                
                for lead_time in lead_times:
                    # Performance decreases with lead time
                    lead_factor = 1.0 if lead_time == 1 else \
                                 0.85 if lead_time == 2 else 0.7
                    
                    # Calculate adjusted performance
                    adj_perf = base_perf * region_factor * lead_factor
                    
                    # Add random variation
                    adj_perf += np.random.normal(0, 0.05)
                    
                    # Ensure performance is within reasonable bounds
                    adj_perf = max(min(adj_perf, 0.95), 0.3)
                    
                    # Calculate metrics based on adjusted performance
                    rmse = 0.5 * (1 - adj_perf) + 0.2  # Lower is better
                    mae = 0.4 * (1 - adj_perf) + 0.15   # Lower is better
                    r2 = adj_perf ** 1.5                # Higher is better
                    correlation = adj_perf              # Higher is better
                    bias = 0.1 * np.random.normal()     # Closer to 0 is better
                    exp_var = adj_perf ** 1.2           # Higher is better
                    
                    # Add to data list
                    data.append({
                        'Model': model,
                        'Region': region,
                        'Lead_Time': lead_time,
                        'RMSE': rmse,
                        'MAE': mae,
                        'R²': r2,
                        'Correlation': correlation,
                        'Bias': bias,
                        'Explained_Variance': exp_var
                    })
        
        # Convert to DataFrame
        performance_df = pd.DataFrame(data)
        
        return performance_df

def load_case_study_data(event_name, file_path=None):
    """
    Load case study data for a specific drought event.
    
    Args:
        event_name (str): Name of the drought event
        file_path (str, optional): Path to data file
        
    Returns:
        dict: Dictionary containing observed and predicted drought data
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        case_data = xr.open_dataset(file_path)
        return case_data
    else:
        # Generate synthetic case study data for demonstration
        print(f"Generating synthetic case study data for {event_name}")
        
        # Define grid for Southern Africa
        lats = np.linspace(-35, -10, 50)
        lons = np.linspace(10, 40, 50)
        
        # Create lat/lon meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Generate base spatial pattern (more drought-prone in southeast)
        base_pattern = ((lat_grid + 35) / 25) * ((lon_grid - 10) / 30)
        
        # Different patterns for different events
        if event_name == '2015-2016 El Niño Drought':
            # Severe drought in southeastern regions
            observed = -1.5 * base_pattern - 0.5 + 0.3 * np.random.randn(*base_pattern.shape)
            
            # Predictions from different models
            hierarchical = observed + 0.3 * np.random.randn(*base_pattern.shape)
            physics_informed = observed + 0.4 * np.random.randn(*base_pattern.shape)
            data_driven = observed + 0.6 * np.random.randn(*base_pattern.shape)
            
            # Dates for this event
            dates = pd.date_range(start='2015-10-01', end='2016-03-01', freq='MS')
            
        elif event_name == '2018-2019 Drought':
            # Moderate drought with different spatial pattern
            observed = -1.0 * base_pattern - 0.3 + 0.3 * np.random.randn(*base_pattern.shape)
            
            # Predictions from different models
            hierarchical = observed + 0.35 * np.random.randn(*base_pattern.shape)
            physics_informed = observed + 0.45 * np.random.randn(*base_pattern.shape)
            data_driven = observed + 0.7 * np.random.randn(*base_pattern.shape)
            
            # Dates for this event
            dates = pd.date_range(start='2018-11-01', end='2019-04-01', freq='MS')
            
        else:  # Generic case
            observed = -1.0 * base_pattern - 0.4 + 0.3 * np.random.randn(*base_pattern.shape)
            hierarchical = observed + 0.4 * np.random.randn(*base_pattern.shape)
            physics_informed = observed + 0.5 * np.random.randn(*base_pattern.shape)
            data_driven = observed + 0.7 * np.random.randn(*base_pattern.shape)
            dates = pd.date_range(start='2010-01-01', end='2010-06-01', freq='MS')
        
        # Create xarray dataset
        case_data = xr.Dataset(
            data_vars={
                'observed': (['time', 'lat', 'lon'], np.array([observed] * len(dates)).reshape(len(dates), *observed.shape)),
                'hierarchical': (['time', 'lat', 'lon'], np.array([hierarchical] * len(dates)).reshape(len(dates), *hierarchical.shape)),
                'physics_informed': (['time', 'lat', 'lon'], np.array([physics_informed] * len(dates)).reshape(len(dates), *physics_informed.shape)),
                'data_driven': (['time', 'lat', 'lon'], np.array([data_driven] * len(dates)).reshape(len(dates), *data_driven.shape)),
            },
            coords={
                'lat': lats,
                'lon': lons,
                'time': dates,
            }
        )
        
        # Add metadata
        case_data.attrs['event_name'] = event_name
        
        return case_data

def load_ensemble_forecast_data(file_path=None):
    """
    Load ensemble forecast data for uncertainty analysis.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Returns:
        xr.Dataset: Ensemble forecast data
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        ensemble_data = xr.open_dataset(file_path)
        return ensemble_data
    else:
        # Generate synthetic ensemble forecast data for demonstration
        print("Generating synthetic ensemble forecast data for demonstration")
        
        # Define grid for Southern Africa
        lats = np.linspace(-35, -10, 30)
        lons = np.linspace(10, 40, 30)
        
        # Create lat/lon meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Generate base spatial pattern (more drought-prone in southeast)
        base_pattern = ((lat_grid + 35) / 25) * ((lon_grid - 10) / 30)
        
        # Number of ensemble members
        n_members = 20
        
        # Create ensemble data
        ensemble_members = []
        for i in range(n_members):
            # Add random variation to base pattern
            member = -1.0 * base_pattern - 0.3 + 0.5 * np.random.randn(*base_pattern.shape)
            ensemble_members.append(member)
        
        # Calculate ensemble mean and standard deviation
        ensemble_mean = np.mean(ensemble_members, axis=0)
        ensemble_std = np.std(ensemble_members, axis=0)
        
        # Calculate drought probability (SPI < -1)
        drought_prob = np.zeros_like(ensemble_mean)
        for i in range(len(lats)):
            for j in range(len(lons)):
                # Assuming normal distribution of ensemble members
                drought_prob[i, j] = stats.norm.cdf(-1, loc=ensemble_mean[i, j], scale=ensemble_std[i, j])
        
        # Create xarray dataset
        ensemble_data = xr.Dataset(
            data_vars={
                'ensemble_mean': (['lat', 'lon'], ensemble_mean),
                'ensemble_std': (['lat', 'lon'], ensemble_std),
                'drought_prob': (['lat', 'lon'], drought_prob),
            },
            coords={
                'lat': lats,
                'lon': lons,
            }
        )
        
        # Add ensemble members
        for i in range(n_members):
            ensemble_data[f'member_{i+1}'] = (['lat', 'lon'], ensemble_members[i])
        
        return ensemble_data

# ============================================================================
# Analysis Functions
# ============================================================================

def calculate_performance_metrics(observed, predicted):
    """
    Calculate performance metrics for model evaluation.
    
    Args:
        observed (np.ndarray): Observed values
        predicted (np.ndarray): Predicted values
        
    Returns:
        dict: Dictionary of performance metrics
    """
    # Flatten arrays and remove NaN values
    obs_flat = observed.flatten()
    pred_flat = predicted.flatten()
    
    mask = ~np.isnan(obs_flat) & ~np.isnan(pred_flat)
    obs_clean = obs_flat[mask]
    pred_clean = pred_flat[mask]
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(obs_clean, pred_clean))
    mae = mean_absolute_error(obs_clean, pred_clean)
    r2 = r2_score(obs_clean, pred_clean)
    corr, p_value = stats.pearsonr(obs_clean, pred_clean)
    bias = np.mean(pred_clean - obs_clean)
    exp_var = explained_variance_score(obs_clean, pred_clean)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2,
        'Correlation': corr,
        'P-Value': p_value,
        'Bias': bias,
        'Explained_Variance': exp_var
    }

def compare_model_components(performance_data, metric='Correlation'):
    """
    Compare performance of different model components.
    
    Args:
        performance_data (pd.DataFrame): Model performance data
        metric (str): Metric to compare
        
    Returns:
        pd.DataFrame: Summarized comparison data
    """
    # Filter for relevant models
    component_models = [
        'Hierarchical (Full)',
        'Global Only (ICON)',
        'Regional Only (MPAS)',
        'Local Only (AI)'
    ]
    
    filtered_data = performance_data[performance_data['Model'].isin(component_models)]
    
    # Group by model, region, and lead time
    grouped = filtered_data.groupby(['Model', 'Region', 'Lead_Time'])[metric].mean().reset_index()
    
    # Calculate improvement over component models
    hierarchical = grouped[grouped['Model'] == 'Hierarchical (Full)'].copy()
    hierarchical = hierarchical.rename(columns={metric: 'Hierarchical'})
    
    component_data = grouped[grouped['Model'] != 'Hierarchical (Full)'].copy()
    
    # Pivot to get component models as columns
    component_pivot = component_data.pivot_table(
        index=['Region', 'Lead_Time'],
        columns='Model',
        values=metric
    ).reset_index()
    
    # Merge with hierarchical data
    merged = pd.merge(
        hierarchical[['Region', 'Lead_Time', 'Hierarchical']],
        component_pivot,
        on=['Region', 'Lead_Time']
    )
    
    # Calculate improvements
    for model in component_models[1:]:  # Skip hierarchical
        if metric in ['RMSE', 'MAE', 'Bias']:  # Lower is better
            merged[f'Improvement_over_{model}'] = (merged[model] - merged['Hierarchical']) / merged[model] * 100
        else:  # Higher is better
            merged[f'Improvement_over_{model}'] = (merged['Hierarchical'] - merged[model]) / merged[model] * 100
    
    return merged

def compare_physics_vs_datadriven(performance_data, metric='Correlation'):
    """
    Compare performance of physics-informed vs. pure data-driven approaches.
    
    Args:
        performance_data (pd.DataFrame): Model performance data
        metric (str): Metric to compare
        
    Returns:
        pd.DataFrame: Summarized comparison data
    """
    # Filter for relevant models
    approach_models = [
        'Physics-Informed',
        'Pure Data-Driven'
    ]
    
    filtered_data = performance_data[performance_data['Model'].isin(approach_models)]
    
    # Group by model, region, and lead time
    grouped = filtered_data.groupby(['Model', 'Region', 'Lead_Time'])[metric].mean().reset_index()
    
    # Pivot to get approaches as columns
    approach_pivot = grouped.pivot_table(
        index=['Region', 'Lead_Time'],
        columns='Model',
        values=metric
    ).reset_index()
    
    # Calculate improvement
    if metric in ['RMSE', 'MAE', 'Bias']:  # Lower is better
        approach_pivot['Improvement'] = (approach_pivot['Pure Data-Driven'] - approach_pivot['Physics-Informed']) / approach_pivot['Pure Data-Driven'] * 100
    else:  # Higher is better
        approach_pivot['Improvement'] = (approach_pivot['Physics-Informed'] - approach_pivot['Pure Data-Driven']) / approach_pivot['Pure Data-Driven'] * 100
    
    return approach_pivot

def analyze_case_study(case_data, time_index=0):
    """
    Analyze case study data for a specific time point.
    
    Args:
        case_data (xr.Dataset): Case study data
        time_index (int): Time index to analyze
        
    Returns:
        dict: Dictionary of performance metrics for each model
    """
    # Extract data for the specified time
    observed = case_data['observed'].isel(time=time_index).values
    hierarchical = case_data['hierarchical'].isel(time=time_index).values
    physics_informed = case_data['physics_informed'].isel(time=time_index).values
    data_driven = case_data['data_driven'].isel(time=time_index).values
    
    # Calculate metrics for each model
    hierarchical_metrics = calculate_performance_metrics(observed, hierarchical)
    physics_metrics = calculate_performance_metrics(observed, physics_informed)
    datadriven_metrics = calculate_performance_metrics(observed, data_driven)
    
    return {
        'Hierarchical': hierarchical_metrics,
        'Physics-Informed': physics_metrics,
        'Data-Driven': datadriven_metrics
    }

def analyze_ensemble_uncertainty(ensemble_data):
    """
    Analyze ensemble forecast uncertainty.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        
    Returns:
        dict: Dictionary of uncertainty metrics
    """
    # Extract ensemble mean and standard deviation
    ensemble_mean = ensemble_data['ensemble_mean'].values
    ensemble_std = ensemble_data['ensemble_std'].values
    
    # Calculate coefficient of variation (relative uncertainty)
    cv = np.abs(ensemble_std / ensemble_mean)
    cv[np.isnan(cv) | np.isinf(cv)] = np.nan
    
    # Calculate regional statistics
    mean_cv = np.nanmean(cv)
    median_cv = np.nanmedian(cv)
    max_cv = np.nanmax(cv)
    
    # Calculate drought probability statistics
    drought_prob = ensemble_data['drought_prob'].values
    mean_prob = np.nanmean(drought_prob)
    high_prob_area = np.sum(drought_prob > 0.7) / np.sum(~np.isnan(drought_prob))
    
    return {
        'mean_cv': mean_cv,
        'median_cv': median_cv,
        'max_cv': max_cv,
        'mean_drought_prob': mean_prob,
        'high_prob_area_fraction': high_prob_area
    }

# ============================================================================
# Visualization Functions
# ============================================================================

def plot_model_performance_comparison(performance_data, metric='Correlation', 
                                     output_file=None):
    """
    Plot comparison of model performance across regions and lead times.
    
    Args:
        performance_data (pd.DataFrame): Model performance data
        metric (str): Metric to compare
        output_file (str, optional): Path to save figure
    """
    # Filter for hierarchical model and component models
    models = [
        'Hierarchical (Full)',
        'Global Only (ICON)',
        'Regional Only (MPAS)',
        'Local Only (AI)'
    ]
    
    filtered_data = performance_data[performance_data['Model'].isin(models)]
    
    # Create figure with subplots for each lead time
    lead_times = sorted(filtered_data['Lead_Time'].unique())
    fig, axes = plt.subplots(1, len(lead_times), figsize=(16, 6), sharey=True)
    
    # Color palette
    palette = {
        'Hierarchical (Full)': '#1f77b4',
        'Global Only (ICON)': '#ff7f0e',
        'Regional Only (MPAS)': '#2ca02c',
        'Local Only (AI)': '#d62728'
    }
    
    # Plot for each lead time
    for i, lead_time in enumerate(lead_times):
        ax = axes[i]
        
        # Filter for current lead time
        lead_data = filtered_data[filtered_data['Lead_Time'] == lead_time]
        
        # Create grouped bar plot
        sns.barplot(
            data=lead_data,
            x='Region',
            y=metric,
            hue='Model',
            palette=palette,
            ax=ax
        )
        
        # Set title and labels
        ax.set_title(f'Lead Time: {lead_time} Month{"s" if lead_time > 1 else ""}')
        ax.set_xlabel('Region')
        
        if i == 0:
            ax.set_ylabel(metric)
        else:
            ax.set_ylabel('')
        
        # Rotate x-tick labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Only show legend for the first subplot
        if i > 0:
            ax.get_legend().remove()
    
    # Adjust legend
    axes[0].legend(title='Model', bbox_to_anchor=(0, 1.02, 1, 0.2), 
                  loc="lower left", mode="expand", ncol=len(models))
    
    # Add overall title
    plt.suptitle(f'Model Performance Comparison ({metric})', fontsize=16, y=1.05)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.show()

def plot_physics_vs_datadriven_comparison(performance_data, metrics=None, 
                                         output_file=None):
    """
    Plot comparison of physics-informed vs. pure data-driven approaches.
    
    Args:
        performance_data (pd.DataFrame): Model performance data
        metrics (list, optional): List of metrics to compare
        output_file (str, optional): Path to save figure
    """
    if metrics is None:
        metrics = ['Correlation', 'RMSE', 'R²']
    
    # Filter for relevant models
    approach_models = [
        'Physics-Informed',
        'Pure Data-Driven'
    ]
    
    filtered_data = performance_data[performance_data['Model'].isin(approach_models)]
    
    # Create figure with subplots for each metric
    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 6), sharey=False)
    
    # Color palette
    palette = {
        'Physics-Informed': '#1f77b4',
        'Pure Data-Driven': '#ff7f0e'
    }
    
    # Plot for each metric
    for i, metric in enumerate(metrics):
        ax = axes[i]
        
        # Create grouped bar plot
        sns.barplot(
            data=filtered_data,
            x='Region',
            y=metric,
            hue='Model',
            palette=palette,
            ax=ax
        )
        
        # Set title and labels
        ax.set_title(metric)
        ax.set_xlabel('Region')
        ax.set_ylabel(metric)
        
        # Rotate x-tick labels
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Only show legend for the first subplot
        if i > 0:
            ax.get_legend().remove()
    
    # Adjust legend
    axes[0].legend(title='Approach', bbox_to_anchor=(0, 1.02, 1, 0.2), 
                  loc="lower left", mode="expand", ncol=len(approach_models))
    
    # Add overall title
    plt.suptitle('Physics-Informed vs. Pure Data-Driven Approaches', fontsize=16, y=1.05)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.show()

def plot_improvement_heatmap(comparison_data, output_file=None):
    """
    Plot heatmap of performance improvement.
    
    Args:
        comparison_data (pd.DataFrame): Comparison data from compare_model_components
        output_file (str, optional): Path to save figure
    """
    # Extract improvement columns
    improvement_cols = [col for col in comparison_data.columns if 'Improvement' in col]
    
    # Reshape data for heatmap
    heatmap_data = comparison_data.melt(
        id_vars=['Region', 'Lead_Time'],
        value_vars=improvement_cols,
        var_name='Comparison',
        value_name='Improvement (%)'
    )
    
    # Clean up comparison names
    heatmap_data['Comparison'] = heatmap_data['Comparison'].str.replace('Improvement_over_', '')
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create heatmap
    heatmap = sns.heatmap(
        heatmap_data.pivot_table(
            index=['Region', 'Lead_Time'],
            columns='Comparison',
            values='Improvement (%)'
        ),
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        center=0,
        linewidths=0.5,
        cbar_kws={'label': 'Improvement (%)'}
    )
    
    # Set title and labels
    plt.title('Performance Improvement of Hierarchical Model over Component Models', fontsize=16)
    plt.tight_layout()
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.show()

def plot_case_study_maps(case_data, time_index=0, output_file=None):
    """
    Plot maps for case study comparison.
    
    Args:
        case_data (xr.Dataset): Case study data
        time_index (int): Time index to plot
        output_file (str, optional): Path to save figure
    """
    # Extract data for the specified time
    observed = case_data['observed'].isel(time=time_index).values
    hierarchical = case_data['hierarchical'].isel(time=time_index).values
    physics_informed = case_data['physics_informed'].isel(time=time_index).values
    data_driven = case_data['data_driven'].isel(time=time_index).values
    
    # Calculate errors
    hierarchical_error = hierarchical - observed
    physics_error = physics_informed - observed
    datadriven_error = data_driven - observed
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10),
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Define plot data
    plot_data = [
        (observed, 'Observed', 0),
        (hierarchical, 'Hierarchical Model', 1),
        (physics_informed, 'Physics-Informed', 2),
        (data_driven, 'Pure Data-Driven', 3),
        (hierarchical_error, 'Hierarchical Error', 4),
        (physics_error, 'Physics-Informed Error', 5),
        (datadriven_error, 'Data-Driven Error', 6)
    ]
    
    # Create colormap with white at zero
    drought_cmap = plt.cm.RdBu_r
    error_cmap = plt.cm.RdBu
    
    # Plot each dataset
    for i, (data, title, ax_idx) in enumerate(plot_data):
        ax = axes[ax_idx]
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        
        # Set map extent to Southern Africa
        ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
        
        # Determine appropriate colormap and scale
        if 'Error' in title:
            cmap = error_cmap
            vmin, vmax = -2, 2
        else:
            cmap = drought_cmap
            vmin, vmax = -3, 3
        
        # Plot data
        im = ax.pcolormesh(
            case_data.lon, 
            case_data.lat, 
            data,
            cmap=cmap, 
            vmin=vmin, 
            vmax=vmax,
            transform=ccrs.PlateCarree()
        )
        
        # Add gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                         linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        
        # Only show lat/lon labels on the edges
        if ax_idx < 4:  # Top row
            gl.bottom_labels = False
        if ax_idx % 4 != 0:  # Not leftmost column
            gl.left_labels = False
        
        # Add title
        ax.set_title(title)
        
        # Add colorbar for each row
        if ax_idx == 3:  # Last in first row
            cbar_ax = fig.add_axes([0.92, 0.55, 0.02, 0.3])
            cbar = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
            cbar.set_label('Drought Index')
        elif ax_idx == 6:  # Last in second row
            cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.3])
            cbar = fig.colorbar(im, cax=cbar_ax, orientation='vertical')
            cbar.set_label('Error')
    
    # Remove empty subplot
    axes[7].set_visible(False)
    
    # Add event name and date as overall title
    event_name = case_data.attrs.get('event_name', 'Drought Event')
    date_str = pd.to_datetime(case_data.time.values[time_index]).strftime('%B %Y')
    plt.suptitle(f'{event_name}: {date_str}', fontsize=16, y=0.98)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    plt.show()

def plot_case_study_metrics(case_metrics, output_file=None):
    """
    Plot performance metrics for case study.
    
    Args:
        case_metrics (dict): Dictionary of performance metrics for each model
        output_file (str, optional): Path to save figure
    """
    # Extract metrics for each model
    models = list(case_metrics.keys())
    metrics = list(case_metrics[models[0]].keys())
    
    # Filter metrics to plot
    plot_metrics = ['RMSE', 'MAE', 'R²', 'Correlation', 'Bias']
    metrics = [m for m in metrics if m in plot_metrics]
    
    # Create data for plotting
    data = []
    for model in models:
        for metric in metrics:
            data.append({
                'Model': model,
                'Metric': metric,
                'Value': case_metrics[model][metric]
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Create figure with subplots for each metric
    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 6), sharey=False)
    
    # Color palette
    palette = {
        'Hierarchical': '#1f77b4',
        'Physics-Informed': '#ff7f0e',
        'Data-Driven': '#2ca02c'
    }
    
    # Plot for each metric
    for i, metric in enumerate(metrics):
        ax = axes[i]
        
        # Filter for current metric
        metric_data = df[df['Metric'] == metric]
        
        # Create bar plot
        sns.barplot(
            data=metric_data,
            x='Model',
            y='Value',
            palette=palette,
            ax=ax
        )
        
        # Set title and labels
        ax.set_title(metric)
        ax.set_xlabel('')
        ax.set_ylabel(metric)
        
        # Add value labels on bars
        for j, p in enumerate(ax.patches):
            ax.annotate(
                f'{p.get_height():.3f}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center',
                va='bottom',
                fontsize=10,
                rotation=0
            )
    
    # Add overall title
    plt.suptitle('Model Performance Comparison for Case Study', fontsize=16, y=1.05)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.show()

def plot_ensemble_forecast(ensemble_data, output_file=None):
    """
    Plot ensemble forecast and uncertainty.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        output_file (str, optional): Path to save figure
    """
    # Extract data
    ensemble_mean = ensemble_data['ensemble_mean'].values
    ensemble_std = ensemble_data['ensemble_std'].values
    drought_prob = ensemble_data['drought_prob'].values
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6),
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Plot ensemble mean
    ax = axes[0]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im1 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        ensemble_mean,
        cmap=plt.cm.RdBu_r, 
        vmin=-3, 
        vmax=3,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    ax.set_title('Ensemble Mean Forecast')
    
    cbar1 = plt.colorbar(im1, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar1.set_label('Drought Index')
    
    # Plot ensemble standard deviation
    ax = axes[1]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im2 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        ensemble_std,
        cmap='viridis', 
        vmin=0, 
        vmax=1.5,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Forecast Uncertainty (Standard Deviation)')
    
    cbar2 = plt.colorbar(im2, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar2.set_label('Standard Deviation')
    
    # Plot drought probability
    ax = axes[2]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im3 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        drought_prob,
        cmap='YlOrRd', 
        vmin=0, 
        vmax=1,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Drought Probability (SPI < -1)')
    
    cbar3 = plt.colorbar(im3, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar3.set_label('Probability')
    
    # Add overall title
    plt.suptitle('Ensemble Drought Forecast', fontsize=16, y=1.05)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_lead_time_performance(performance_data, metric='Correlation', 
                              output_file=None):
    """
    Plot performance degradation with lead time.
    
    Args:
        performance_data (pd.DataFrame): Model performance data
        metric (str): Metric to plot
        output_file (str, optional): Path to save figure
    """
    # Filter for hierarchical model
    hierarchical_data = performance_data[performance_data['Model'] == 'Hierarchical (Full)']
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create line plot
    sns.lineplot(
        data=hierarchical_data,
        x='Lead_Time',
        y=metric,
        hue='Region',
        marker='o',
        markersize=8,
        linewidth=2
    )
    
    # Set title and labels
    plt.title(f'Performance Degradation with Lead Time ({metric})', fontsize=16)
    plt.xlabel('Lead Time (months)')
    plt.ylabel(metric)
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust legend
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# Main Analysis
# ============================================================================

def main():
    """
    Main analysis function.
    """
    print("Starting Hierarchical Model Performance Analysis")
    
    # Load data
    print("Loading data...")
    performance_data = load_model_performance_data()
    
    # 1. Compare model components
    print("\nComparing model components...")
    for metric in ['Correlation', 'RMSE', 'R²']:
        print(f"  Analyzing {metric}...")
        
        component_comparison = compare_model_components(
            performance_data, metric=metric)
        
        output_file = f"figures/component_comparison_{metric}.png"
        plot_model_performance_comparison(
            performance_data, metric=metric, output_file=output_file)
        
        output_file = f"figures/improvement_heatmap_{metric}.png"
        plot_improvement_heatmap(component_comparison, output_file=output_file)
    
    # 2. Compare physics-informed vs. pure data-driven approaches
    print("\nComparing physics-informed vs. pure data-driven approaches...")
    metrics = ['Correlation', 'RMSE', 'R²']
    
    output_file = "figures/physics_vs_datadriven.png"
    plot_physics_vs_datadriven_comparison(
        performance_data, metrics=metrics, output_file=output_file)
    
    for metric in metrics:
        print(f"  Analyzing {metric}...")
        approach_comparison = compare_physics_vs_datadriven(
            performance_data, metric=metric)
        print(f"  Average improvement: {approach_comparison['Improvement'].mean():.2f}%")
    
    # 3. Analyze lead time performance
    print("\nAnalyzing lead time performance...")
    for metric in ['Correlation', 'RMSE']:
        output_file = f"figures/lead_time_{metric}.png"
        plot_lead_time_performance(
            performance_data, metric=metric, output_file=output_file)
    
    # 4. Analyze case studies
    print("\nAnalyzing case studies...")
    case_studies = [
        '2015-2016 El Niño Drought',
        '2018-2019 Drought'
    ]
    
    for case_name in case_studies:
        print(f"  Analyzing {case_name}...")
        case_data = load_case_study_data(case_name)
        
        # Analyze middle time point
        time_idx = len(case_data.time) // 2
        case_metrics = analyze_case_study(case_data, time_index=time_idx)
        
        output_file = f"figures/case_study_maps_{case_name.replace(' ', '_').lower()}.png"
        plot_case_study_maps(case_data, time_index=time_idx, output_file=output_file)
        
        output_file = f"figures/case_study_metrics_{case_name.replace(' ', '_').lower()}.png"
        plot_case_study_metrics(case_metrics, output_file=output_file)
    
    # 5. Analyze ensemble forecast uncertainty
    print("\nAnalyzing ensemble forecast uncertainty...")
    ensemble_data = load_ensemble_forecast_data()
    uncertainty_metrics = analyze_ensemble_uncertainty(ensemble_data)
    
    print("  Uncertainty metrics:")
    for metric, value in uncertainty_metrics.items():
        print(f"    {metric}: {value:.3f}")
    
    output_file = "figures/ensemble_forecast.png"
    plot_ensemble_forecast(ensemble_data, output_file=output_file)
    
    print("\nAnalysis complete. All figures saved to 'figures/' directory.")

if __name__ == "__main__":
    main()
```
---

## ```ensemble_forecast_visualization```
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensemble Forecast Visualization Script

This script visualizes ensemble drought forecasts for Southern Africa,
focusing on uncertainty quantification, probability mapping, and
forecast verification. It supports the hierarchical model results
presented in the PhD thesis.

Author: [Your Name]
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import xarray as xr
from scipy import stats
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import r2_score, explained_variance_score
import os
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.5)

# Create output directory for figures
os.makedirs("figures", exist_ok=True)

# ============================================================================
# Data Loading Functions
# ============================================================================

def load_ensemble_forecast_data(file_path=None, n_members=20, n_lead_times=6):
    """
    Load ensemble forecast data for multiple lead times.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Args:
        file_path (str, optional): Path to data file
        n_members (int): Number of ensemble members
        n_lead_times (int): Number of lead times
        
    Returns:
        xr.Dataset: Ensemble forecast data
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        ensemble_data = xr.open_dataset(file_path)
        return ensemble_data
    else:
        # Generate synthetic ensemble forecast data for demonstration
        print("Generating synthetic ensemble forecast data for demonstration")
        
        # Define grid for Southern Africa
        lats = np.linspace(-35, -10, 30)
        lons = np.linspace(10, 40, 30)
        lead_times = np.arange(1, n_lead_times + 1)
        
        # Create lat/lon meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Generate base spatial pattern (more drought-prone in southeast)
        base_pattern = ((lat_grid + 35) / 25) * ((lon_grid - 10) / 30)
        
        # Initialize arrays for ensemble data
        ensemble_members = np.zeros((n_lead_times, n_members, len(lats), len(lons)))
        
        # Generate ensemble members for each lead time
        for t in range(n_lead_times):
            # Base forecast degrades with lead time
            lead_factor = 1.0 - 0.1 * t
            
            # Generate base forecast for this lead time
            base_forecast = -1.0 * base_pattern * lead_factor - 0.3
            
            # Add random variation for each ensemble member
            for m in range(n_members):
                # Uncertainty increases with lead time
                uncertainty = 0.3 + 0.1 * t
                ensemble_members[t, m] = base_forecast + uncertainty * np.random.randn(*base_pattern.shape)
        
        # Calculate ensemble statistics for each lead time
        ensemble_mean = np.mean(ensemble_members, axis=1)
        ensemble_std = np.std(ensemble_members, axis=1)
        
        # Calculate drought probability (SPI < -1) for each lead time
        drought_prob = np.zeros((n_lead_times, len(lats), len(lons)))
        for t in range(n_lead_times):
            for i in range(len(lats)):
                for j in range(len(lons)):
                    # Assuming normal distribution of ensemble members
                    drought_prob[t, i, j] = stats.norm.cdf(-1, 
                                                         loc=ensemble_mean[t, i, j], 
                                                         scale=ensemble_std[t, i, j])
        
        # Create xarray dataset
        ensemble_data = xr.Dataset(
            data_vars={
                'ensemble_mean': (['lead_time', 'lat', 'lon'], ensemble_mean),
                'ensemble_std': (['lead_time', 'lat', 'lon'], ensemble_std),
                'drought_prob': (['lead_time', 'lat', 'lon'], drought_prob),
            },
            coords={
                'lat': lats,
                'lon': lons,
                'lead_time': lead_times,
            }
        )
        
        # Add ensemble members
        for m in range(n_members):
            ensemble_data[f'member_{m+1}'] = (['lead_time', 'lat', 'lon'], 
                                             ensemble_members[:, m, :, :])
        
        return ensemble_data

def load_verification_data(file_path=None, n_lead_times=6):
    """
    Load verification data for ensemble forecast evaluation.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Args:
        file_path (str, optional): Path to data file
        n_lead_times (int): Number of lead times
        
    Returns:
        xr.Dataset: Verification data
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        verification_data = xr.open_dataset(file_path)
        return verification_data
    else:
        # Generate synthetic verification data for demonstration
        print("Generating synthetic verification data for demonstration")
        
        # Define grid for Southern Africa
        lats = np.linspace(-35, -10, 30)
        lons = np.linspace(10, 40, 30)
        lead_times = np.arange(1, n_lead_times + 1)
        
        # Create lat/lon meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Generate base spatial pattern (more drought-prone in southeast)
        base_pattern = ((lat_grid + 35) / 25) * ((lon_grid - 10) / 30)
        
        # Initialize arrays for verification data
        observed = np.zeros((n_lead_times, len(lats), len(lons)))
        
        # Generate observed data for each lead time
        for t in range(n_lead_times):
            # Base pattern with random variation
            observed[t] = -1.0 * base_pattern - 0.3 + 0.4 * np.random.randn(*base_pattern.shape)
        
        # Create xarray dataset
        verification_data = xr.Dataset(
            data_vars={
                'observed': (['lead_time', 'lat', 'lon'], observed),
            },
            coords={
                'lat': lats,
                'lon': lons,
                'lead_time': lead_times,
            }
        )
        
        return verification_data

def load_regional_forecast_data(file_path=None, n_members=20, n_lead_times=6):
    """
    Load regional forecast data for time series analysis.
    
    If file_path is None, generates synthetic data for demonstration.
    
    Args:
        file_path (str, optional): Path to data file
        n_members (int): Number of ensemble members
        n_lead_times (int): Number of lead times
        
    Returns:
        pd.DataFrame: Regional forecast data
    """
    if file_path and os.path.exists(file_path):
        # Load actual data if file exists
        regional_data = pd.read_csv(file_path)
        return regional_data
    else:
        # Generate synthetic regional forecast data for demonstration
        print("Generating synthetic regional forecast data for demonstration")
        
        # Define regions
        regions = ['Southeastern', 'Central', 'Northwestern', 'Southwestern']
        lead_times = np.arange(1, n_lead_times + 1)
        
        # Initialize data list
        data = []
        
        # Generate data for each region
        for region in regions:
            # Base forecast varies by region
            if region == 'Southeastern':
                base_forecast = -1.5  # More severe drought
            elif region == 'Central':
                base_forecast = -1.0
            elif region == 'Northwestern':
                base_forecast = -0.5
            else:  # Southwestern
                base_forecast = -0.8
            
            # Generate observed values
            for t in lead_times:
                # Observed value with random variation
                observed = base_forecast + 0.4 * np.random.randn()
                
                # Generate ensemble members
                for m in range(1, n_members + 1):
                    # Forecast degrades with lead time
                    lead_factor = 1.0 - 0.1 * (t - 1)
                    
                    # Uncertainty increases with lead time
                    uncertainty = 0.3 + 0.1 * (t - 1)
                    
                    # Generate forecast
                    forecast = base_forecast * lead_factor + uncertainty * np.random.randn()
                    
                    # Add to data list
                    data.append({
                        'Region': region,
                        'Lead_Time': t,
                        'Member': m,
                        'Forecast': forecast,
                        'Observed': observed
                    })
        
        # Convert to DataFrame
        regional_df = pd.DataFrame(data)
        
        return regional_df

# ============================================================================
# Analysis Functions
# ============================================================================

def calculate_verification_metrics(ensemble_data, verification_data, lead_time=1):
    """
    Calculate verification metrics for ensemble forecast.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        verification_data (xr.Dataset): Verification data
        lead_time (int): Lead time to analyze
        
    Returns:
        dict: Dictionary of verification metrics
    """
    # Extract data for the specified lead time
    ensemble_mean = ensemble_data['ensemble_mean'].sel(lead_time=lead_time).values
    observed = verification_data['observed'].sel(lead_time=lead_time).values
    
    # Flatten arrays and remove NaN values
    ens_flat = ensemble_mean.flatten()
    obs_flat = observed.flatten()
    
    mask = ~np.isnan(ens_flat) & ~np.isnan(obs_flat)
    ens_clean = ens_flat[mask]
    obs_clean = obs_flat[mask]
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(obs_clean, ens_clean))
    mae = mean_absolute_error(obs_clean, ens_clean)
    r2 = r2_score(obs_clean, ens_clean)
    corr, p_value = stats.pearsonr(obs_clean, ens_clean)
    bias = np.mean(ens_clean - obs_clean)
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'R²': r2,
        'Correlation': corr,
        'Bias': bias,
        'Lead_Time': lead_time
    }

def calculate_reliability_data(ensemble_data, verification_data, lead_time=1):
    """
    Calculate reliability diagram data for ensemble forecast.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        verification_data (xr.Dataset): Verification data
        lead_time (int): Lead time to analyze
        
    Returns:
        tuple: (forecast_probs, observed_freqs, bin_counts)
    """
    # Extract data for the specified lead time
    drought_prob = ensemble_data['drought_prob'].sel(lead_time=lead_time).values
    observed = verification_data['observed'].sel(lead_time=lead_time).values
    
    # Define drought threshold
    drought_threshold = -1.0
    
    # Convert observed to binary drought/no-drought
    observed_drought = observed < drought_threshold
    
    # Flatten arrays and remove NaN values
    prob_flat = drought_prob.flatten()
    obs_flat = observed_drought.flatten()
    
    mask = ~np.isnan(prob_flat) & ~np.isnan(obs_flat)
    prob_clean = prob_flat[mask]
    obs_clean = obs_flat[mask]
    
    # Define probability bins
    bins = np.linspace(0, 1, 11)  # 0.0, 0.1, 0.2, ..., 1.0
    bin_indices = np.digitize(prob_clean, bins) - 1
    bin_indices = np.clip(bin_indices, 0, len(bins) - 2)
    
    # Calculate observed frequency in each bin
    forecast_probs = []
    observed_freqs = []
    bin_counts = []
    
    for i in range(len(bins) - 1):
        mask = bin_indices == i
        if np.sum(mask) > 0:
            forecast_probs.append((bins[i] + bins[i+1]) / 2)
            observed_freqs.append(np.mean(obs_clean[mask]))
            bin_counts.append(np.sum(mask))
    
    return forecast_probs, observed_freqs, bin_counts

def calculate_rank_histogram_data(ensemble_data, verification_data, lead_time=1):
    """
    Calculate rank histogram data for ensemble forecast.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        verification_data (xr.Dataset): Verification data
        lead_time (int): Lead time to analyze
        
    Returns:
        np.ndarray: Rank histogram counts
    """
    # Extract data for the specified lead time
    observed = verification_data['observed'].sel(lead_time=lead_time).values
    
    # Get number of ensemble members
    member_vars = [var for var in ensemble_data.data_vars if 'member_' in var]
    n_members = len(member_vars)
    
    # Initialize rank counts
    rank_counts = np.zeros(n_members + 1)
    
    # Iterate over grid points
    for i in range(len(ensemble_data.lat)):
        for j in range(len(ensemble_data.lon)):
            # Extract observed value
            obs_value = observed[i, j]
            
            # Skip if NaN
            if np.isnan(obs_value):
                continue
            
            # Extract ensemble forecasts for this point
            ensemble_values = np.array([
                ensemble_data[f'member_{m+1}'].sel(lead_time=lead_time).values[i, j]
                for m in range(n_members)
            ])
            
            # Skip if any NaN
            if np.any(np.isnan(ensemble_values)):
                continue
            
            # Count members less than observed
            rank = np.sum(ensemble_values < obs_value)
            
            # Increment rank count
            rank_counts[rank] += 1
    
    return rank_counts

def calculate_spread_skill_data(ensemble_data, verification_data):
    """
    Calculate spread-skill relationship data.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        verification_data (xr.Dataset): Verification data
        
    Returns:
        pd.DataFrame: Spread-skill data
    """
    # Initialize data list
    data = []
    
    # Iterate over lead times
    for lead_time in ensemble_data.lead_time.values:
        # Extract data for this lead time
        ensemble_mean = ensemble_data['ensemble_mean'].sel(lead_time=lead_time).values
        ensemble_std = ensemble_data['ensemble_std'].sel(lead_time=lead_time).values
        observed = verification_data['observed'].sel(lead_time=lead_time).values
        
        # Calculate error
        error = ensemble_mean - observed
        
        # Flatten arrays and remove NaN values
        spread_flat = ensemble_std.flatten()
        error_flat = error.flatten()
        
        mask = ~np.isnan(spread_flat) & ~np.isnan(error_flat)
        spread_clean = spread_flat[mask]
        error_clean = error_flat[mask]
        
        # Calculate RMSE
        rmse = np.sqrt(np.mean(error_clean**2))
        
        # Calculate mean spread
        mean_spread = np.mean(spread_clean)
        
        # Add to data list
        data.append({
            'Lead_Time': lead_time,
            'RMSE': rmse,
            'Spread': mean_spread,
            'Ratio': rmse / mean_spread if mean_spread > 0 else np.nan
        })
    
    # Convert to DataFrame
    spread_skill_df = pd.DataFrame(data)
    
    return spread_skill_df

def calculate_regional_forecast_statistics(regional_data, region='Southeastern'):
    """
    Calculate statistics for regional forecast.
    
    Args:
        regional_data (pd.DataFrame): Regional forecast data
        region (str): Region to analyze
        
    Returns:
        pd.DataFrame: Regional forecast statistics
    """
    # Filter for specified region
    region_data = regional_data[regional_data['Region'] == region]
    
    # Initialize data list
    data = []
    
    # Iterate over lead times
    for lead_time in sorted(region_data['Lead_Time'].unique()):
        # Filter for this lead time
        lead_data = region_data[region_data['Lead_Time'] == lead_time]
        
        # Get observed value (should be the same for all members)
        observed = lead_data['Observed'].iloc[0]
        
        # Get ensemble forecasts
        forecasts = lead_data['Forecast'].values
        
        # Calculate statistics
        mean_forecast = np.mean(forecasts)
        median_forecast = np.median(forecasts)
        std_forecast = np.std(forecasts)
        q10 = np.percentile(forecasts, 10)
        q90 = np.percentile(forecasts, 90)
        
        # Calculate error
        error = mean_forecast - observed
        
        # Add to data list
        data.append({
            'Lead_Time': lead_time,
            'Observed': observed,
            'Mean_Forecast': mean_forecast,
            'Median_Forecast': median_forecast,
            'Std_Forecast': std_forecast,
            'Q10': q10,
            'Q90': q90,
            'Error': error,
            'RMSE': np.sqrt(error**2)
        })
    
    # Convert to DataFrame
    stats_df = pd.DataFrame(data)
    
    return stats_df

# ============================================================================
# Visualization Functions
# ============================================================================

def plot_ensemble_forecast_maps(ensemble_data, lead_time=1, output_file=None):
    """
    Plot ensemble forecast maps for a specific lead time.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        lead_time (int): Lead time to plot
        output_file (str, optional): Path to save figure
    """
    # Extract data for the specified lead time
    ensemble_mean = ensemble_data['ensemble_mean'].sel(lead_time=lead_time).values
    ensemble_std = ensemble_data['ensemble_std'].sel(lead_time=lead_time).values
    drought_prob = ensemble_data['drought_prob'].sel(lead_time=lead_time).values
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6),
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Plot ensemble mean
    ax = axes[0]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im1 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        ensemble_mean,
        cmap=plt.cm.RdBu_r, 
        vmin=-3, 
        vmax=3,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    ax.set_title('Ensemble Mean Forecast')
    
    cbar1 = plt.colorbar(im1, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar1.set_label('Drought Index')
    
    # Plot ensemble standard deviation
    ax = axes[1]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im2 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        ensemble_std,
        cmap='viridis', 
        vmin=0, 
        vmax=1.5,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Forecast Uncertainty (Standard Deviation)')
    
    cbar2 = plt.colorbar(im2, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar2.set_label('Standard Deviation')
    
    # Plot drought probability
    ax = axes[2]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    # Create custom colormap for probability
    colors = [(1, 1, 1), (1, 0.8, 0.8), (1, 0.6, 0.6), (1, 0.4, 0.4), 
             (1, 0.2, 0.2), (0.8, 0, 0)]
    cmap_prob = LinearSegmentedColormap.from_list('prob_cmap', colors)
    
    im3 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        drought_prob,
        cmap=cmap_prob, 
        vmin=0, 
        vmax=1,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Drought Probability (SPI < -1)')
    
    cbar3 = plt.colorbar(im3, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar3.set_label('Probability')
    
    # Add overall title
    plt.suptitle(f'Ensemble Drought Forecast (Lead Time: {lead_time} month{"s" if lead_time > 1 else ""})', 
                fontsize=16, y=1.05)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def create_forecast_animation(ensemble_data, output_file=None):
    """
    Create animation of ensemble forecast across lead times.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        output_file (str, optional): Path to save animation
    """
    # Create figure with subplots
    fig, ax = plt.subplots(figsize=(10, 8),
                         subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    # Add gridlines
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    # Create custom colormap for probability
    colors = [(1, 1, 1), (1, 0.8, 0.8), (1, 0.6, 0.6), (1, 0.4, 0.4), 
             (1, 0.2, 0.2), (0.8, 0, 0)]
    cmap_prob = LinearSegmentedColormap.from_list('prob_cmap', colors)
    
    # Initial plot
    lead_time = ensemble_data.lead_time.values[0]
    drought_prob = ensemble_data['drought_prob'].sel(lead_time=lead_time).values
    
    # Create mesh plot
    mesh = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        drought_prob,
        cmap=cmap_prob, 
        vmin=0, 
        vmax=1,
        transform=ccrs.PlateCarree()
    )
    
    # Add colorbar
    cbar = plt.colorbar(mesh, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Drought Probability (SPI < -1)')
    
    # Add title
    title = ax.set_title(f'Lead Time: {lead_time} month{"s" if lead_time > 1 else ""}', 
                        fontsize=14)
    
    # Animation update function
    def update(frame):
        lead_time = ensemble_data.lead_time.values[frame]
        drought_prob = ensemble_data['drought_prob'].sel(lead_time=lead_time).values
        
        # Update mesh data
        mesh.set_array(drought_prob.flatten())
        
        # Update title
        title.set_text(f'Lead Time: {lead_time} month{"s" if lead_time > 1 else ""}')
        
        return mesh, title
    
    # Create animation
    anim = FuncAnimation(
        fig, update, frames=len(ensemble_data.lead_time),
        interval=1000, blit=False
    )
    
    # Save animation if output file is specified
    if output_file:
        anim.save(output_file, writer='pillow', fps=1, dpi=100)
        print(f"Animation saved to {output_file}")
    
    plt.tight_layout()
    plt.show()
    
    return anim

def plot_verification_metrics(verification_metrics, output_file=None):
    """
    Plot verification metrics across lead times.
    
    Args:
        verification_metrics (list): List of dictionaries with verification metrics
        output_file (str, optional): Path to save figure
    """
    # Convert to DataFrame
    metrics_df = pd.DataFrame(verification_metrics)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Define metrics to plot
    plot_metrics = ['RMSE', 'MAE', 'Correlation', 'Bias']
    
    # Plot each metric
    for i, metric in enumerate(plot_metrics):
        ax = axes[i]
        
        # Create line plot
        sns.lineplot(
            data=metrics_df,
            x='Lead_Time',
            y=metric,
            marker='o',
            markersize=8,
            linewidth=2,
            ax=ax
        )
        
        # Set title and labels
        ax.set_title(metric)
        ax.set_xlabel('Lead Time (months)')
        ax.set_ylabel(metric)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add overall title
    plt.suptitle('Forecast Verification Metrics', fontsize=16, y=0.98)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def plot_reliability_diagram(forecast_probs, observed_freqs, bin_counts, 
                           lead_time=1, output_file=None):
    """
    Plot reliability diagram for ensemble forecast.
    
    Args:
        forecast_probs (list): Forecast probabilities
        observed_freqs (list): Observed frequencies
        bin_counts (list): Bin counts
        lead_time (int): Lead time
        output_file (str, optional): Path to save figure
    """
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), 
                                 gridspec_kw={'width_ratios': [3, 1]})
    
    # Plot reliability diagram
    ax1.plot([0, 1], [0, 1], 'k--', label='Perfect reliability')
    
    # Plot no-skill line
    climo = np.mean(observed_freqs)
    ax1.plot([0, 1], [climo, climo], 'k:', label='No skill')
    ax1.plot([climo, climo], [0, 1], 'k:')
    
    # Plot reliability curve
    ax1.plot(forecast_probs, observed_freqs, 'o-', linewidth=2, markersize=8,
            label='Forecast')
    
    # Set title and labels
    ax1.set_title(f'Reliability Diagram (Lead Time: {lead_time} month{"s" if lead_time > 1 else ""})')
    ax1.set_xlabel('Forecast Probability')
    ax1.set_ylabel('Observed Frequency')
    
    # Add grid and legend
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend(loc='upper left')
    
    # Set axis limits
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    
    # Plot histogram of forecast probabilities
    ax2.bar(forecast_probs, bin_counts, width=0.1, alpha=0.7)
    
    # Set title and labels
    ax2.set_title('Forecast Probability Histogram')
    ax2.set_xlabel('Forecast Probability')
    ax2.set_ylabel('Count')
    
    # Set x-axis limits
    ax2.set_xlim([0, 1])
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_rank_histogram(rank_counts, lead_time=1, output_file=None):
    """
    Plot rank histogram for ensemble forecast.
    
    Args:
        rank_counts (np.ndarray): Rank histogram counts
        lead_time (int): Lead time
        output_file (str, optional): Path to save figure
    """
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot rank histogram
    plt.bar(np.arange(len(rank_counts)), rank_counts, width=0.8, alpha=0.7)
    
    # Add reference line for uniform distribution
    uniform_height = np.sum(rank_counts) / len(rank_counts)
    plt.axhline(y=uniform_height, color='r', linestyle='--', 
               label='Uniform distribution')
    
    # Set title and labels
    plt.title(f'Rank Histogram (Lead Time: {lead_time} month{"s" if lead_time > 1 else ""})')
    plt.xlabel('Rank')
    plt.ylabel('Count')
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_spread_skill_relationship(spread_skill_data, output_file=None):
    """
    Plot spread-skill relationship.
    
    Args:
        spread_skill_data (pd.DataFrame): Spread-skill data
        output_file (str, optional): Path to save figure
    """
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot RMSE and spread vs. lead time
    ax1.plot(spread_skill_data['Lead_Time'], spread_skill_data['RMSE'], 
            'o-', linewidth=2, markersize=8, label='RMSE')
    ax1.plot(spread_skill_data['Lead_Time'], spread_skill_data['Spread'], 
            'o--', linewidth=2, markersize=8, label='Spread')
    
    # Set title and labels
    ax1.set_title('RMSE and Spread vs. Lead Time')
    ax1.set_xlabel('Lead Time (months)')
    ax1.set_ylabel('RMSE / Spread')
    
    # Add grid and legend
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    
    # Plot spread-skill ratio vs. lead time
    ax2.plot(spread_skill_data['Lead_Time'], spread_skill_data['Ratio'], 
            'o-', linewidth=2, markersize=8, color='darkgreen')
    
    # Add reference line for perfect spread-skill relationship
    ax2.axhline(y=1.0, color='r', linestyle='--', 
               label='Perfect spread-skill')
    
    # Set title and labels
    ax2.set_title('Spread-Skill Ratio vs. Lead Time')
    ax2.set_xlabel('Lead Time (months)')
    ax2.set_ylabel('RMSE / Spread Ratio')
    
    # Add grid and legend
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    
    # Add overall title
    plt.suptitle('Spread-Skill Relationship', fontsize=16, y=1.05)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_regional_forecast(regional_stats, region='Southeastern', output_file=None):
    """
    Plot regional forecast with uncertainty.
    
    Args:
        regional_stats (pd.DataFrame): Regional forecast statistics
        region (str): Region name
        output_file (str, optional): Path to save figure
    """
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot observed values
    plt.plot(regional_stats['Lead_Time'], regional_stats['Observed'], 
            'o-', linewidth=2, markersize=8, color='black', label='Observed')
    
    # Plot mean forecast
    plt.plot(regional_stats['Lead_Time'], regional_stats['Mean_Forecast'], 
            'o--', linewidth=2, markersize=8, color='darkblue', label='Mean Forecast')
    
    # Plot uncertainty range
    plt.fill_between(regional_stats['Lead_Time'], 
                    regional_stats['Q10'], regional_stats['Q90'], 
                    color='lightblue', alpha=0.5, label='10-90% Range')
    
    # Set title and labels
    plt.title(f'Regional Forecast for {region}')
    plt.xlabel('Lead Time (months)')
    plt.ylabel('Drought Index')
    
    # Add grid and legend
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Add drought threshold line
    plt.axhline(y=-1.0, color='r', linestyle='--', 
               label='Drought Threshold (SPI < -1)')
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_regional_comparison(regional_data, lead_time=3, output_file=None):
    """
    Plot comparison of forecasts across regions.
    
    Args:
        regional_data (pd.DataFrame): Regional forecast data
        lead_time (int): Lead time to analyze
        output_file (str, optional): Path to save figure
    """
    # Filter for specified lead time
    lead_data = regional_data[regional_data['Lead_Time'] == lead_time]
    
    # Get unique regions
    regions = sorted(lead_data['Region'].unique())
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create violin plots for each region
    sns.violinplot(
        data=lead_data,
        x='Region',
        y='Forecast',
        inner='quartile',
        palette='Set3'
    )
    
    # Add observed values as points
    for i, region in enumerate(regions):
        region_data = lead_data[lead_data['Region'] == region]
        observed = region_data['Observed'].iloc[0]
        plt.scatter(i, observed, color='red', s=100, marker='*', 
                   label='Observed' if i == 0 else '')
    
    # Set title and labels
    plt.title(f'Regional Forecast Comparison (Lead Time: {lead_time} month{"s" if lead_time > 1 else ""})')
    plt.xlabel('Region')
    plt.ylabel('Drought Index')
    
    # Add drought threshold line
    plt.axhline(y=-1.0, color='r', linestyle='--', 
               label='Drought Threshold (SPI < -1)')
    
    # Add legend
    handles, labels = plt.gca().get_legend_handles_labels()
    handles.append(plt.Line2D([0], [0], color='r', linestyle='--'))
    labels.append('Drought Threshold (SPI < -1)')
    plt.legend(handles, labels, loc='lower right')
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

def plot_forecast_verification_map(ensemble_data, verification_data, 
                                 lead_time=1, output_file=None):
    """
    Plot forecast verification map.
    
    Args:
        ensemble_data (xr.Dataset): Ensemble forecast data
        verification_data (xr.Dataset): Verification data
        lead_time (int): Lead time to analyze
        output_file (str, optional): Path to save figure
    """
    # Extract data for the specified lead time
    ensemble_mean = ensemble_data['ensemble_mean'].sel(lead_time=lead_time).values
    observed = verification_data['observed'].sel(lead_time=lead_time).values
    
    # Calculate error
    error = ensemble_mean - observed
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6),
                           subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Plot ensemble mean
    ax = axes[0]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im1 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        ensemble_mean,
        cmap=plt.cm.RdBu_r, 
        vmin=-3, 
        vmax=3,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    ax.set_title('Ensemble Mean Forecast')
    
    cbar1 = plt.colorbar(im1, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar1.set_label('Drought Index')
    
    # Plot observed
    ax = axes[1]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im2 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        observed,
        cmap=plt.cm.RdBu_r, 
        vmin=-3, 
        vmax=3,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Observed')
    
    cbar2 = plt.colorbar(im2, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar2.set_label('Drought Index')
    
    # Plot error
    ax = axes[2]
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_extent([10, 40, -35, -10], crs=ccrs.PlateCarree())
    
    im3 = ax.pcolormesh(
        ensemble_data.lon, 
        ensemble_data.lat, 
        error,
        cmap=plt.cm.RdBu, 
        vmin=-2, 
        vmax=2,
        transform=ccrs.PlateCarree()
    )
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                     linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.left_labels = False
    
    ax.set_title('Forecast Error')
    
    cbar3 = plt.colorbar(im3, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar3.set_label('Error (Forecast - Observed)')
    
    # Add overall title
    plt.suptitle(f'Forecast Verification (Lead Time: {lead_time} month{"s" if lead_time > 1 else ""})', 
                fontsize=16, y=1.05)
    
    # Save figure if output file is specified
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# Main Analysis
# ============================================================================

def main():
    """
    Main analysis function.
    """
    print("Starting Ensemble Forecast Visualization")
    
    # Load data
    print("Loading data...")
    ensemble_data = load_ensemble_forecast_data()
    verification_data = load_verification_data()
    regional_data = load_regional_forecast_data()
    
    # 1. Plot ensemble forecast maps for different lead times
    print("\nPlotting ensemble forecast maps...")
    for lead_time in ensemble_data.lead_time.values:
        print(f"  Processing lead time {lead_time}...")
        
        output_file = f"figures/ensemble_forecast_lead{lead_time}.png"
        plot_ensemble_forecast_maps(
            ensemble_data, lead_time=lead_time, output_file=output_file)
    
    # 2. Create forecast animation
    print("\nCreating forecast animation...")
    output_file = "figures/forecast_animation.gif"
    create_forecast_animation(ensemble_data, output_file=output_file)
    
    # 3. Calculate and plot verification metrics
    print("\nCalculating verification metrics...")
    verification_metrics = []
    
    for lead_time in ensemble_data.lead_time.values:
        print(f"  Processing lead time {lead_time}...")
        
        metrics = calculate_verification_metrics(
            ensemble_data, verification_data, lead_time=lead_time)
        verification_metrics.append(metrics)
    
    output_file = "figures/verification_metrics.png"
    plot_verification_metrics(verification_metrics, output_file=output_file)
    
    # 4. Calculate and plot reliability diagrams
    print("\nCalculating reliability diagrams...")
    for lead_time in [1, 3, 6]:  # Selected lead times
        if lead_time in ensemble_data.lead_time.values:
            print(f"  Processing lead time {lead_time}...")
            
            forecast_probs, observed_freqs, bin_counts = calculate_reliability_data(
                ensemble_data, verification_data, lead_time=lead_time)
            
            output_file = f"figures/reliability_diagram_lead{lead_time}.png"
            plot_reliability_diagram(
                forecast_probs, observed_freqs, bin_counts, 
                lead_time=lead_time, output_file=output_file)
    
    # 5. Calculate and plot rank histograms
    print("\nCalculating rank histograms...")
    for lead_time in [1, 3, 6]:  # Selected lead times
        if lead_time in ensemble_data.lead_time.values:
            print(f"  Processing lead time {lead_time}...")
            
            rank_counts = calculate_rank_histogram_data(
                ensemble_data, verification_data, lead_time=lead_time)
            
            output_file = f"figures/rank_histogram_lead{lead_time}.png"
            plot_rank_histogram(
                rank_counts, lead_time=lead_time, output_file=output_file)
    
    # 6. Calculate and plot spread-skill relationship
    print("\nCalculating spread-skill relationship...")
    spread_skill_data = calculate_spread_skill_data(ensemble_data, verification_data)
    
    output_file = "figures/spread_skill_relationship.png"
    plot_spread_skill_relationship(spread_skill_data, output_file=output_file)
    
    # 7. Calculate and plot regional forecasts
    print("\nCalculating regional forecasts...")
    for region in ['Southeastern', 'Central', 'Northwestern', 'Southwestern']:
        print(f"  Processing {region} region...")
        
        regional_stats = calculate_regional_forecast_statistics(
            regional_data, region=region)
        
        output_file = f"figures/regional_forecast_{region.lower()}.png"
        plot_regional_forecast(
            regional_stats, region=region, output_file=output_file)
    
    # 8. Plot regional comparison
    print("\nPlotting regional comparison...")
    for lead_time in [1, 3, 6]:  # Selected lead times
        if lead_time in regional_data['Lead_Time'].unique():
            print(f"  Processing lead time {lead_time}...")
            
            output_file = f"figures/regional_comparison_lead{lead_time}.png"
            plot_regional_comparison(
                regional_data, lead_time=lead_time, output_file=output_file)
    
    # 9. Plot forecast verification maps
    print("\nPlotting forecast verification maps...")
    for lead_time in ensemble_data.lead_time.values:
        print(f"  Processing lead time {lead_time}...")
        
        output_file = f"figures/forecast_verification_lead{lead_time}.png"
        plot_forecast_verification_map(
            ensemble_data, verification_data, 
            lead_time=lead_time, output_file=output_file)
    
    print("\nAnalysis complete. All figures saved to 'figures/' directory.")

if __name__ == "__main__":
    main()
```
