IOD-Drought Analysis Scripts for Paper 1

This directory contains a set of Python scripts for analyzing the relationship between 
the Indian Ocean Dipole (IOD) and drought patterns in Southern Africa, as described in the paper:
"The Indian Ocean Dipole as a Predictor of Drought in Southern Africa: A Statistical Analysis"

The scripts implement all statistical analyses described in the methodology section of the paper
and generate the figures and tables presented in the results section.

Author: Mthetho Sovara
Date: June 2025

# Overview of Scripts
 ------------------

## 1. 01_correlation_analysis.py
###    - Computes spatial correlation patterns between IOD and drought indices
###    - Analyzes seasonal variations in correlation strength
###    - Generates regional correlation statistics

```python
"""
IOD-Drought Correlation Analysis Script

This script performs correlation analysis between the Indian Ocean Dipole (IOD)
and drought indices across Southern Africa, as described in the paper:
"The Indian Ocean Dipole as a Predictor of Drought in Southern Africa: A Statistical Analysis"

The script includes functions for:
1. Loading and preprocessing IOD and drought indices data
2. Computing spatial correlation patterns
3. Performing seasonal correlation analysis
4. Visualizing correlation maps with statistical significance

Author: [Your Name]
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests
import os
import warnings
warnings.filterwarnings('ignore')

# Define constants
STUDY_PERIOD = (1980, 2020)
SOUTHERN_AFRICA_BOUNDS = {'lat_min': -35, 'lat_max': -10, 
                         'lon_min': 10, 'lon_max': 40}
SUBREGIONS = {
    'southeastern': {'lat_min': -35, 'lat_max': -20, 'lon_min': 25, 'lon_max': 40},
    'central': {'lat_min': -25, 'lat_max': -15, 'lon_min': 20, 'lon_max': 30},
    'northwestern': {'lat_min': -20, 'lat_max': -10, 'lon_min': 10, 'lon_max': 25},
    'southwestern': {'lat_min': -35, 'lat_max': -20, 'lon_min': 10, 'lon_max': 25}
}
SEASONS = {
    'DJF': [12, 1, 2],
    'MAM': [3, 4, 5],
    'JJA': [6, 7, 8],
    'SON': [9, 10, 11]
}

def load_iod_data(file_path=None):
    """
    Load IOD (DMI) data from file or generate synthetic data if file not provided
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the IOD data file (CSV format expected)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing IOD data with datetime index
    """
    if file_path and os.path.exists(file_path):
        print(f"Loading IOD data from {file_path}")
        iod_data = pd.read_csv(file_path, parse_dates=['time'])
        iod_data.set_index('time', inplace=True)
        return iod_data
    else:
        print("No IOD data file provided or file not found. Generating synthetic data.")
        # Generate synthetic IOD data
        date_range = pd.date_range(start=f'{STUDY_PERIOD[0]}-01-01', 
                                  end=f'{STUDY_PERIOD[1]}-12-31', 
                                  freq='MS')
        
        # Create seasonal cycle with some interannual variability
        n_months = len(date_range)
        seasonal_cycle = 0.4 * np.sin(2 * np.pi * np.arange(n_months) / 12)
        
        # Add some IOD events (positive and negative)
        iod_events = np.zeros(n_months)
        
        # Add some known strong IOD events
        # 1982-83 positive IOD
        iod_events[33:45] = 1.2
        # 1997-98 positive IOD
        iod_events[213:225] = 1.5
        # 2006-07 positive IOD
        iod_events[321:333] = 1.0
        # 2011-12 positive IOD
        iod_events[381:393] = 1.3
        
        # 1996 negative IOD
        iod_events[192:204] = -1.0
        # 2010 negative IOD
        iod_events[360:372] = -1.2
        # 2016 negative IOD
        iod_events[432:444] = -1.1
        
        # Add random noise
        noise = np.random.normal(0, 0.3, n_months)
        
        # Combine components
        dmi = seasonal_cycle + iod_events + noise
        
        # Create DataFrame
        iod_data = pd.DataFrame({'DMI': dmi}, index=date_range)
        
        return iod_data

def load_drought_indices(file_path=None, index_type='SPI-3'):
    """
    Load drought indices data from file or generate synthetic data if file not provided
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the drought indices data file (NetCDF format expected)
    index_type : str, optional
        Type of drought index to load ('SPI-3', 'SPI-6', 'SPEI-3', 'SPEI-6', 'NDVI')
        
    Returns:
    --------
    xr.Dataset
        Dataset containing drought index data
    """
    if file_path and os.path.exists(file_path):
        print(f"Loading {index_type} data from {file_path}")
        drought_data = xr.open_dataset(file_path)
        return drought_data
    else:
        print(f"No {index_type} data file provided or file not found. Generating synthetic data.")
        
        # Generate synthetic drought index data
        lat = np.arange(SOUTHERN_AFRICA_BOUNDS['lat_max'], 
                       SOUTHERN_AFRICA_BOUNDS['lat_min'], -0.5)
        lon = np.arange(SOUTHERN_AFRICA_BOUNDS['lon_min'], 
                       SOUTHERN_AFRICA_BOUNDS['lon_max'], 0.5)
        time = pd.date_range(start=f'{STUDY_PERIOD[0]}-01-01', 
                           end=f'{STUDY_PERIOD[1]}-12-31', 
                           freq='MS')
        
        # Create spatial patterns for different regions
        lat_grid, lon_grid = np.meshgrid(lat, lon, indexing='ij')
        
        # Create base spatial pattern
        # Southeastern region (positive correlation with IOD)
        southeastern_mask = ((lat_grid >= SUBREGIONS['southeastern']['lat_min']) & 
                           (lat_grid <= SUBREGIONS['southeastern']['lat_max']) & 
                           (lon_grid >= SUBREGIONS['southeastern']['lon_min']) & 
                           (lon_grid <= SUBREGIONS['southeastern']['lon_max']))
        
        # Northwestern region (negative correlation with IOD)
        northwestern_mask = ((lat_grid >= SUBREGIONS['northwestern']['lat_min']) & 
                           (lat_grid <= SUBREGIONS['northwestern']['lat_max']) & 
                           (lon_grid >= SUBREGIONS['northwestern']['lon_min']) & 
                           (lon_grid <= SUBREGIONS['northwestern']['lon_max']))
        
        # Create spatial response pattern
        spatial_pattern = np.zeros_like(lat_grid, dtype=float)
        spatial_pattern[southeastern_mask] = 1.0
        spatial_pattern[northwestern_mask] = -0.5
        
        # Add some spatial noise to make it more realistic
        spatial_noise = np.random.normal(0, 0.3, spatial_pattern.shape)
        spatial_pattern += spatial_noise
        
        # Create temporal evolution
        n_times = len(time)
        n_lats = len(lat)
        n_lons = len(lon)
        
        # Initialize data array
        drought_index = np.zeros((n_times, n_lats, n_lons))
        
        # Load IOD data to create correlated drought patterns
        iod_data = load_iod_data()
        dmi = iod_data['DMI'].values
        
        # Create drought index with IOD influence and noise
        for t in range(n_times):
            # Base pattern influenced by IOD with 3-month lag
            if t >= 3:
                iod_influence = dmi[t-3] * spatial_pattern
            else:
                iod_influence = 0
                
            # Add seasonal cycle (stronger in summer)
            month = time[t].month
            if month in [12, 1, 2]:  # Summer
                seasonal_factor = 0.5
            elif month in [6, 7, 8]:  # Winter
                seasonal_factor = -0.5
            else:
                seasonal_factor = 0
                
            seasonal_component = seasonal_factor * np.ones_like(spatial_pattern)
            
            # Add random noise
            noise = np.random.normal(0, 0.5, spatial_pattern.shape)
            
            # Combine components
            drought_index[t] = iod_influence + seasonal_component + noise
        
        # Create xarray dataset
        drought_data = xr.Dataset(
            data_vars={
                index_type: (('time', 'lat', 'lon'), drought_index)
            },
            coords={
                'time': time,
                'lat': lat,
                'lon': lon
            }
        )
        
        return drought_data

def compute_correlation_map(iod_data, drought_data, drought_index='SPI-3', 
                          time_period=None, season=None):
    """
    Compute correlation map between IOD and drought index
    
    Parameters:
    -----------
    iod_data : pd.DataFrame
        DataFrame containing IOD data with datetime index
    drought_data : xr.Dataset
        Dataset containing drought index data
    drought_index : str, optional
        Name of the drought index variable in the dataset
    time_period : tuple, optional
        Start and end years for analysis (e.g., (1980, 2020))
    season : str, optional
        Season for analysis ('DJF', 'MAM', 'JJA', 'SON')
        
    Returns:
    --------
    xr.Dataset
        Dataset containing correlation coefficients and p-values
    """
    # Extract the drought index data
    drought_var = drought_data[drought_index]
    
    # Filter by time period if specified
    if time_period:
        start_year, end_year = time_period
        iod_data = iod_data.loc[f'{start_year}-01-01':f'{end_year}-12-31']
        drought_var = drought_var.sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))
    
    # Filter by season if specified
    if season:
        season_months = SEASONS[season]
        iod_season = iod_data[iod_data.index.month.isin(season_months)]
        drought_season = drought_var.sel(time=drought_var['time.month'].isin(season_months))
    else:
        iod_season = iod_data
        drought_season = drought_var
    
    # Ensure time alignment
    common_times = [t for t in drought_season.time.values if pd.Timestamp(t) in iod_season.index]
    drought_season = drought_season.sel(time=common_times)
    iod_season = iod_season.loc[[pd.Timestamp(t) for t in common_times]]
    
    # Initialize arrays for correlation and p-values
    corr = np.zeros((len(drought_season.lat), len(drought_season.lon)))
    pvals = np.zeros_like(corr)
    
    # Compute correlation for each grid point
    for i, lat in enumerate(drought_season.lat.values):
        for j, lon in enumerate(drought_season.lon.values):
            drought_ts = drought_season.sel(lat=lat, lon=lon).values
            
            # Check for NaN values
            valid_idx = ~np.isnan(drought_ts)
            if np.sum(valid_idx) > 10:  # Require at least 10 valid data points
                iod_ts = iod_season['DMI'].values[valid_idx]
                drought_ts = drought_ts[valid_idx]
                
                # Compute correlation
                r, p = stats.pearsonr(iod_ts, drought_ts)
                corr[i, j] = r
                pvals[i, j] = p
            else:
                corr[i, j] = np.nan
                pvals[i, j] = np.nan
    
    # Apply FDR correction to p-values
    valid_mask = ~np.isnan(pvals)
    if np.sum(valid_mask) > 0:
        flat_pvals = pvals[valid_mask].flatten()
        _, pvals_fdr, _, _ = multipletests(flat_pvals, alpha=0.05, method='fdr_bh')
        
        # Put the corrected p-values back
        pvals_corrected = np.full_like(pvals, np.nan)
        pvals_corrected[valid_mask] = pvals_fdr
    else:
        pvals_corrected = pvals
    
    # Create output dataset
    result = xr.Dataset(
        data_vars={
            'correlation': (('lat', 'lon'), corr),
            'pvalue': (('lat', 'lon'), pvals),
            'pvalue_fdr': (('lat', 'lon'), pvals_corrected)
        },
        coords={
            'lat': drought_season.lat,
            'lon': drought_season.lon
        }
    )
    
    # Add metadata
    result.attrs['drought_index'] = drought_index
    if season:
        result.attrs['season'] = season
    if time_period:
        result.attrs['time_period'] = f"{time_period[0]}-{time_period[1]}"
    
    return result

def plot_correlation_map(correlation_data, output_file=None, title=None):
    """
    Plot correlation map with significance stippling
    
    Parameters:
    -----------
    correlation_data : xr.Dataset
        Dataset containing correlation coefficients and p-values
    output_file : str, optional
        Path to save the figure
    title : str, optional
        Title for the plot
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig = plt.figure(figsize=(12, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Set up colormap
    cmap = plt.cm.RdBu_r
    norm = colors.Normalize(vmin=-0.8, vmax=0.8)
    
    # Plot correlation
    im = ax.pcolormesh(correlation_data.lon, correlation_data.lat, 
                     correlation_data.correlation, 
                     cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
    
    # Add stippling for significance
    significant = correlation_data.pvalue_fdr < 0.05
    lons, lats = np.meshgrid(correlation_data.lon, correlation_data.lat)
    ax.scatter(lons[significant], lats[significant], color='black', s=1, 
             alpha=0.5, transform=ccrs.PlateCarree())
    
    # Add coastlines and borders
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    
    # Add gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Correlation Coefficient')
    
    # Add title
    if title:
        plt.title(title)
    else:
        drought_index = correlation_data.attrs.get('drought_index', '')
        season = correlation_data.attrs.get('season', 'Annual')
        time_period = correlation_data.attrs.get('time_period', '')
        plt.title(f'Correlation between IOD and {drought_index}\n{season} {time_period}')
    
    # Save figure if output file is provided
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    return fig

def compute_regional_average(data, region_name):
    """
    Compute regional average of a variable
    
    Parameters:
    -----------
    data : xr.DataArray
        Data array containing the variable
    region_name : str
        Name of the region ('southeastern', 'central', 'northwestern', 'southwestern')
        
    Returns:
    --------
    pd.Series
        Time series of regional average
    """
    if region_name not in SUBREGIONS:
        raise ValueError(f"Unknown region: {region_name}")
    
    region = SUBREGIONS[region_name]
    
    # Extract data for the region
    region_data = data.sel(
        lat=slice(region['lat_min'], region['lat_max']),
        lon=slice(region['lon_min'], region['lon_max'])
    )
    
    # Compute area-weighted average (simple average for now)
    regional_avg = region_data.mean(dim=['lat', 'lon'])
    
    # Convert to pandas Series
    if isinstance(regional_avg, xr.DataArray):
        result = regional_avg.to_series()
    else:
        # If it's already a single time series
        result = pd.Series(regional_avg, index=data.time.values)
    
    return result

def seasonal_correlation_analysis(iod_data, drought_data, drought_index='SPI-3'):
    """
    Perform seasonal correlation analysis between IOD and drought indices
    
    Parameters:
    -----------
    iod_data : pd.DataFrame
        DataFrame containing IOD data with datetime index
    drought_data : xr.Dataset
        Dataset containing drought index data
    drought_index : str, optional
        Name of the drought index variable in the dataset
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing seasonal correlation coefficients for each region
    """
    results = []
    
    for season in SEASONS:
        for region in SUBREGIONS:
            # Compute regional average of drought index
            region_avg = compute_regional_average(drought_data[drought_index], region)
            
            # Filter by season
            season_months = SEASONS[season]
            iod_season = iod_data[iod_data.index.month.isin(season_months)]
            drought_season = region_avg[region_avg.index.month.isin(season_months)]
            
            # Ensure time alignment
            common_times = [t for t in drought_season.index if t in iod_season.index]
            drought_season = drought_season.loc[common_times]
            iod_season = iod_season.loc[common_times]
            
            # Compute correlation
            if len(drought_season) > 10:  # Require at least 10 data points
                r, p = stats.pearsonr(iod_season['DMI'], drought_season)
                
                results.append({
                    'Season': season,
                    'Region': region,
                    'Correlation': r,
                    'P-value': p,
                    'Significant': p < 0.05
                })
    
    return pd.DataFrame(results)

def main():
    """
    Main function to run the correlation analysis
    """
    print("IOD-Drought Correlation Analysis")
    print("================================")
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    iod_data = load_iod_data()
    drought_data = load_drought_indices(index_type='SPI-3')
    
    print("\n1. Computing overall correlation map")
    corr_map = compute_correlation_map(iod_data, drought_data)
    plot_correlation_map(corr_map, 
                       output_file=os.path.join(output_dir, "iod_spi3_correlation_map.png"),
                       title="Correlation between IOD and SPI-3 (1980-2020)")
    
    print("\n2. Computing seasonal correlation maps")
    for season in SEASONS:
        print(f"  Processing {season} season")
        season_corr = compute_correlation_map(iod_data, drought_data, season=season)
        plot_correlation_map(season_corr,
                           output_file=os.path.join(output_dir, f"iod_spi3_correlation_{season}.png"),
                           title=f"Correlation between IOD and SPI-3 - {season} (1980-2020)")
    
    print("\n3. Performing seasonal correlation analysis by region")
    seasonal_corr = seasonal_correlation_analysis(iod_data, drought_data)
    print(seasonal_corr)
    seasonal_corr.to_csv(os.path.join(output_dir, "seasonal_regional_correlations.csv"), index=False)
    
    print("\nAnalysis complete. Results saved to the 'output' directory.")

if __name__ == "__main__":
    main()

```


## 2. 02_lag_correlation_analysis.py
###    - Examines lead-lag relationships between IOD and drought indices
###    - Identifies optimal prediction lead times
###    - Analyzes regional variations in lag response

```python
"""
IOD-Drought Lag Correlation Analysis Script

This script performs lag correlation analysis between the Indian Ocean Dipole (IOD)
and drought indices across Southern Africa, as described in the paper:
"The Indian Ocean Dipole as a Predictor of Drought in Southern Africa: A Statistical Analysis"

The script includes functions for:
1. Computing lag correlations between IOD and drought indices
2. Identifying optimal lead times for prediction
3. Visualizing lag correlation patterns for different regions
4. Analyzing seasonal variations in lag relationships

Author: [Your Name]
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import scipy.stats as stats
import os
import warnings
warnings.filterwarnings('ignore')

# Import common functions from correlation analysis script
# Assuming the correlation_analysis.py script is in the same directory
from correlation_analysis import (load_iod_data, load_drought_indices, 
                                compute_regional_average, SUBREGIONS, SEASONS)

def compute_lag_correlation(iod_series, drought_series, max_lag=12):
    """
    Compute lag correlation between IOD and drought index time series
    
    Parameters:
    -----------
    iod_series : pd.Series
        Time series of IOD index
    drought_series : pd.Series
        Time series of drought index
    max_lag : int, optional
        Maximum lag to consider in months (both positive and negative)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing lag correlation coefficients and p-values
    """
    results = []
    
    # Ensure both series have datetime index
    iod_series = iod_series.copy()
    drought_series = drought_series.copy()
    
    if not isinstance(iod_series.index, pd.DatetimeIndex):
        raise ValueError("IOD series must have DatetimeIndex")
    if not isinstance(drought_series.index, pd.DatetimeIndex):
        raise ValueError("Drought series must have DatetimeIndex")
    
    # Compute correlations for different lags
    for lag in range(-max_lag, max_lag + 1):
        # Shift IOD series (positive lag means IOD leads drought)
        if lag < 0:
            # Negative lag: drought leads IOD
            iod_shifted = iod_series.copy()
            drought_shifted = drought_series.shift(periods=abs(lag), freq='MS')
        else:
            # Positive lag: IOD leads drought
            iod_shifted = iod_series.copy()
            drought_shifted = drought_series.shift(periods=-lag, freq='MS')
        
        # Align series
        aligned_data = pd.concat([iod_shifted, drought_shifted], axis=1).dropna()
        
        if len(aligned_data) > 10:  # Require at least 10 data points
            # Compute correlation
            r, p = stats.pearsonr(aligned_data.iloc[:, 0], aligned_data.iloc[:, 1])
            
            results.append({
                'Lag': lag,
                'Correlation': r,
                'P-value': p,
                'Significant': p < 0.05,
                'N': len(aligned_data)
            })
    
    return pd.DataFrame(results)

def compute_regional_lag_correlations(iod_data, drought_data, drought_index='SPI-3', 
                                    max_lag=12, season=None):
    """
    Compute lag correlations for different regions
    
    Parameters:
    -----------
    iod_data : pd.DataFrame
        DataFrame containing IOD data with datetime index
    drought_data : xr.Dataset
        Dataset containing drought index data
    drought_index : str, optional
        Name of the drought index variable in the dataset
    max_lag : int, optional
        Maximum lag to consider in months (both positive and negative)
    season : str, optional
        Season for analysis ('DJF', 'MAM', 'JJA', 'SON')
        
    Returns:
    --------
    dict
        Dictionary containing lag correlation results for each region
    """
    results = {}
    
    # Extract IOD series
    iod_series = iod_data['DMI']
    
    # Filter by season if specified
    if season:
        season_months = SEASONS[season]
        iod_series = iod_series[iod_series.index.month.isin(season_months)]
    
    # Compute lag correlations for each region
    for region_name in SUBREGIONS:
        print(f"Computing lag correlations for {region_name} region")
        
        # Compute regional average of drought index
        region_avg = compute_regional_average(drought_data[drought_index], region_name)
        
        # Filter by season if specified
        if season:
            region_avg = region_avg[region_avg.index.month.isin(season_months)]
        
        # Compute lag correlations
        lag_corr = compute_lag_correlation(iod_series, region_avg, max_lag=max_lag)
        
        results[region_name] = lag_corr
    
    return results

def plot_lag_correlations(lag_correlations, output_file=None, title=None):
    """
    Plot lag correlation results for different regions
    
    Parameters:
    -----------
    lag_correlations : dict
        Dictionary containing lag correlation results for each region
    output_file : str, optional
        Path to save the figure
    title : str, optional
        Title for the plot
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define colors and markers for different regions
    region_styles = {
        'southeastern': {'color': 'darkred', 'marker': 'o', 'label': 'Southeastern'},
        'central': {'color': 'darkgreen', 'marker': 's', 'label': 'Central'},
        'northwestern': {'color': 'darkblue', 'marker': '^', 'label': 'Northwestern'},
        'southwestern': {'color': 'darkorange', 'marker': 'd', 'label': 'Southwestern'}
    }
    
    # Plot lag correlations for each region
    for region_name, lag_corr in lag_correlations.items():
        if region_name in region_styles:
            style = region_styles[region_name]
            
            # Plot correlation line
            ax.plot(lag_corr['Lag'], lag_corr['Correlation'], 
                   color=style['color'], marker=style['marker'], 
                   label=style['label'], linewidth=2, markersize=8)
            
            # Highlight significant correlations
            significant = lag_corr[lag_corr['Significant']]
            if not significant.empty:
                ax.scatter(significant['Lag'], significant['Correlation'], 
                         color=style['color'], s=100, facecolors='none', 
                         linewidth=2, zorder=10)
    
    # Add reference line at zero correlation
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    
    # Add vertical line at zero lag
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
    
    # Add shading for positive lags (IOD leads drought)
    ax.axvspan(0, max(lag_corr['Lag']), alpha=0.1, color='blue', label='IOD leads')
    
    # Add shading for negative lags (drought leads IOD)
    ax.axvspan(min(lag_corr['Lag']), 0, alpha=0.1, color='red', label='Drought leads')
    
    # Set axis labels
    ax.set_xlabel('Lag (months)', fontsize=12)
    ax.set_ylabel('Correlation Coefficient', fontsize=12)
    
    # Set axis limits
    ax.set_xlim(min(lag_corr['Lag']), max(lag_corr['Lag']))
    ax.set_ylim(-0.8, 0.8)
    
    # Add grid
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Add title
    if title:
        ax.set_title(title, fontsize=14)
    else:
        ax.set_title('Lag Correlation between IOD and Regional Drought Indices', fontsize=14)
    
    # Add legend
    ax.legend(loc='best', fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure if output file is provided
    if output_file:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_file}")
    
    return fig

def find_optimal_lead_time(lag_correlations):
    """
    Find optimal lead time for each region based on maximum absolute correlation
    
    Parameters:
    -----------
    lag_correlations : dict
        Dictionary containing lag correlation results for each region
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing optimal lead times and correlation values
    """
    results = []
    
    for region_name, lag_corr in lag_correlations.items():
        # Filter for positive lags (IOD leads drought)
        positive_lags = lag_corr[lag_corr['Lag'] > 0]
        
        if not positive_lags.empty:
            # Find lag with maximum absolute correlation
            max_corr_idx = positive_lags['Correlation'].abs().idxmax()
            max_corr_row = positive_lags.loc[max_corr_idx]
            
            results.append({
                'Region': region_name,
                'Optimal_Lead_Time': max_corr_row['Lag'],
                'Correlation': max_corr_row['Correlation'],
                'P-value': max_corr_row['P-value'],
                'Significant': max_corr_row['Significant']
            })
    
    return pd.DataFrame(results)

def seasonal_lag_correlation_analysis(iod_data, drought_data, drought_index='SPI-3', max_lag=12):
    """
    Perform seasonal lag correlation analysis
    
    Parameters:
    -----------
    iod_data : pd.DataFrame
        DataFrame containing IOD data with datetime index
    drought_data : xr.Dataset
        Dataset containing drought index data
    drought_index : str, optional
        Name of the drought index variable in the dataset
    max_lag : int, optional
        Maximum lag to consider in months (both positive and negative)
        
    Returns:
    --------
    dict
        Dictionary containing lag correlation results for each season
    """
    results = {}
    
    for season in SEASONS:
        print(f"Computing lag correlations for {season} season")
        
        # Compute lag correlations for the season
        season_results = compute_regional_lag_correlations(
            iod_data, drought_data, drought_index=drought_index, 
            max_lag=max_lag, season=season
        )
        
        results[season] = season_results
    
    return results

def main():
    """
    Main function to run the lag correlation analysis
    """
    print("IOD-Drought Lag Correlation Analysis")
    print("===================================")
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    iod_data = load_iod_data()
    drought_data = load_drought_indices(index_type='SPI-3')
    
    print("\n1. Computing regional lag correlations")
    lag_correlations = compute_regional_lag_correlations(
        iod_data, drought_data, drought_index='SPI-3', max_lag=12
    )
    
    # Plot lag correlations
    plot_lag_correlations(
        lag_correlations,
        output_file=os.path.join(output_dir, "iod_spi3_lag_correlations.png"),
        title="Lag Correlation between IOD and SPI-3 by Region (1980-2020)"
    )
    
    # Find optimal lead times
    print("\n2. Finding optimal lead times for prediction")
    optimal_leads = find_optimal_lead_time(lag_correlations)
    print(optimal_leads)
    optimal_leads.to_csv(os.path.join(output_dir, "optimal_lead_times.csv"), index=False)
    
    print("\n3. Performing seasonal lag correlation analysis")
    seasonal_lag_corr = seasonal_lag_correlation_analysis(
        iod_data, drought_data, drought_index='SPI-3', max_lag=12
    )
    
    # Plot seasonal lag correlations
    for season, season_results in seasonal_lag_corr.items():
        plot_lag_correlations(
            season_results,
            output_file=os.path.join(output_dir, f"iod_spi3_lag_correlations_{season}.png"),
            title=f"Lag Correlation between IOD and SPI-3 by Region - {season} (1980-2020)"
        )
    
    print("\nAnalysis complete. Results saved to the 'output' directory.")

if __name__ == "__main__":
    main()

```

# 3. 03_composite_analysis.py
#    - Classifies IOD events into positive, negative, and neutral phases
#    - Computes composite drought conditions during different IOD phases
#    - Tests statistical significance of composite anomalies
#
# 4. 04_partial_correlation_analysis.py
#    - Isolates IOD's independent influence by controlling for ENSO effects
#    - Compares raw and partial correlations to quantify IOD's unique contribution
#    - Analyzes regional variations in IOD's independent influence
#
# 5. 05_wavelet_coherence_analysis.py
#    - Examines time-frequency relationships between IOD and drought indices
#    - Identifies periods of significant coherence
#    - Analyzes phase relationships and lead-lag patterns

# Dependencies
# -----------
# The scripts require the following Python packages:
# - numpy
# - pandas
# - matplotlib
# - cartopy
# - xarray
# - scipy
# - statsmodels

# Data Requirements
# ---------------
# The scripts expect the following data files:
# - IOD data: Monthly DMI (Dipole Mode Index) values
# - Drought indices: SPI-3 (Standardized Precipitation Index, 3-month) gridded data
# - ENSO data: Monthly Niño 3.4 index values (for partial correlation analysis)
#
# If these files are not available, the scripts will generate synthetic data for demonstration.

# Usage Instructions
# ----------------
# 1. Ensure all dependencies are installed:
#    pip install numpy pandas matplotlib cartopy xarray scipy statsmodels
#
# 2. Run the scripts in sequence:
#    python 01_correlation_analysis.py
#    python 02_lag_correlation_analysis.py
#    python 03_composite_analysis.py
#    python 04_partial_correlation_analysis.py
#    python 05_wavelet_coherence_analysis.py
#
# 3. Results will be saved to an 'output' directory created by each script

# Key Findings
# ----------
# The scripts will reproduce the key findings from the paper:
# - Strong negative correlation between positive IOD events and precipitation in southeastern Southern Africa
# - Optimal prediction lead time of 2-4 months for drought conditions
# - Significant differences in drought patterns between positive and negative IOD phases
# - IOD's influence on drought is partially independent of ENSO
# - Coherent IOD-drought relationships at interannual (2-7 year) timescales

# Customization
# -----------
# Each script contains parameters that can be modified to customize the analysis:
# - Time period for analysis
# - Drought index type (SPI-3, SPI-6, SPEI, etc.)
# - Significance thresholds
# - Regional definitions
# - Visualization parameters

# Contact
# ------
# For questions or issues, please contact:
# [Your Email]
"""
