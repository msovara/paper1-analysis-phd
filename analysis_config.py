#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis Configuration File

This file contains all configuration parameters for the IOD-Drought analysis
workflow. It provides a centralized way to manage analysis settings and
ensures consistency across all analysis scripts.

Author: Mthetho Sovara
Date: October 2025
"""

import os
from pathlib import Path

# ============================================================================
# Directory Configuration
# ============================================================================

# Base directories
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'output'

# Analysis-specific directories
IOD_ANALYSIS_DIR = OUTPUT_DIR / 'iod_drought_analysis'
HIERARCHICAL_MODEL_DIR = OUTPUT_DIR / 'hierarchical_model_analysis'
ENSEMBLE_FORECAST_DIR = OUTPUT_DIR / 'ensemble_forecast_analysis'

# Subdirectories for each analysis
ANALYSIS_DIRS = {
    'iod_drought': {
        'base': IOD_ANALYSIS_DIR,
        'plots': IOD_ANALYSIS_DIR / 'plots',
        'data': IOD_ANALYSIS_DIR / 'data',
        'results': IOD_ANALYSIS_DIR / 'results'
    },
    'hierarchical_model': {
        'base': HIERARCHICAL_MODEL_DIR,
        'plots': HIERARCHICAL_MODEL_DIR / 'plots',
        'data': HIERARCHICAL_MODEL_DIR / 'data',
        'results': HIERARCHICAL_MODEL_DIR / 'results'
    },
    'ensemble_forecast': {
        'base': ENSEMBLE_FORECAST_DIR,
        'plots': ENSEMBLE_FORECAST_DIR / 'plots',
        'data': ENSEMBLE_FORECAST_DIR / 'data',
        'results': ENSEMBLE_FORECAST_DIR / 'results'
    }
}

# ============================================================================
# Data Configuration
# ============================================================================

# DMI data sources
DMI_SOURCES = {
    'era5': {
        'file_pattern': 'dmi_era5_*.csv',
        'description': 'DMI extracted from ERA5 data'
    },
    'jamstec': {
        'file_pattern': 'dmi_jamstec_*.csv',
        'description': 'DMI from JAMSTEC'
    },
    'noaa': {
        'file_pattern': 'dmi_noaa_*.csv',
        'description': 'DMI from NOAA'
    },
    'bom': {
        'file_pattern': 'dmi_bom_*.csv',
        'description': 'DMI from BOM'
    }
}

# Drought indices
DROUGHT_INDICES = {
    'spi3': {
        'name': 'Standardized Precipitation Index (3-month)',
        'description': '3-month SPI for short-term drought assessment'
    },
    'spi6': {
        'name': 'Standardized Precipitation Index (6-month)',
        'description': '6-month SPI for medium-term drought assessment'
    },
    'spi12': {
        'name': 'Standardized Precipitation Index (12-month)',
        'description': '12-month SPI for long-term drought assessment'
    },
    'spei3': {
        'name': 'Standardized Precipitation Evapotranspiration Index (3-month)',
        'description': '3-month SPEI including evapotranspiration'
    },
    'spei6': {
        'name': 'Standardized Precipitation Evapotranspiration Index (6-month)',
        'description': '6-month SPEI including evapotranspiration'
    }
}

# ============================================================================
# Regional Configuration
# ============================================================================

# Southern Africa regions
SOUTHERN_AFRICA_REGIONS = {
    'southeastern': {
        'lat_min': -35, 'lat_max': -25,
        'lon_min': 25, 'lon_max': 35,
        'description': 'Southeastern Africa (strongest IOD signal)',
        'countries': ['South Africa', 'Lesotho', 'Swaziland', 'Mozambique']
    },
    'central': {
        'lat_min': -25, 'lat_max': -15,
        'lon_min': 20, 'lon_max': 30,
        'description': 'Central Southern Africa (moderate IOD signal)',
        'countries': ['Zimbabwe', 'Botswana', 'Namibia', 'Zambia']
    },
    'northwestern': {
        'lat_min': -15, 'lat_max': -5,
        'lon_min': 10, 'lon_max': 20,
        'description': 'Northwestern Southern Africa (weakest IOD signal)',
        'countries': ['Angola', 'Democratic Republic of Congo']
    },
    'southwestern': {
        'lat_min': -35, 'lat_max': -25,
        'lon_min': 15, 'lon_max': 25,
        'description': 'Southwestern Africa (intermediate IOD signal)',
        'countries': ['Namibia', 'South Africa']
    }
}

# ============================================================================
# Temporal Configuration
# ============================================================================

# Analysis time period
ANALYSIS_PERIOD = {
    'start_year': 1980,
    'end_year': 2020,
    'start_date': '1980-01-01',
    'end_date': '2020-12-31'
}

# Seasons
SEASONS = {
    'DJF': {
        'months': [12, 1, 2],
        'name': 'December-January-February',
        'description': 'Southern Hemisphere summer'
    },
    'MAM': {
        'months': [3, 4, 5],
        'name': 'March-April-May',
        'description': 'Southern Hemisphere autumn'
    },
    'JJA': {
        'months': [6, 7, 8],
        'name': 'June-July-August',
        'description': 'Southern Hemisphere winter'
    },
    'SON': {
        'months': [9, 10, 11],
        'name': 'September-October-November',
        'description': 'Southern Hemisphere spring'
    }
}

# ============================================================================
# Analysis Parameters
# ============================================================================

# Correlation analysis parameters
CORRELATION_PARAMS = {
    'min_valid_points': 10,
    'significance_level': 0.05,
    'max_lag_months': 12,
    'correlation_method': 'pearson'
}

# IOD event thresholds
IOD_THRESHOLDS = {
    'event_threshold': 0.5,
    'strong_threshold': 1.0,
    'extreme_threshold': 1.5
}

# ---------------------------------------------------------------------------
# Single source of truth: African domain & IOD SON composite years (1980–2020)
# ---------------------------------------------------------------------------
# Continental maps, regional composites, drought statistics (`comprehensive_*`).
AFRICA_ANALYSIS_BOUNDS = {
    'lat_min': -35,
    'lat_max': 37,
    'lon_min': -20,
    'lon_max': 55,
}

# ERA5 overturning diagnostics (`plot_iod_circulation_cross_section.py`): narrower
# zonal-mean band over the eastern sector. Cite separately from AFRICA_ANALYSIS_BOUNDS
# in methods (full continent vs circulation slice).
IOD_CIRCULATION_DIAGNOSTIC_LON = {
    'lon_west': 10.0,
    'lon_east': 50.0,
}

# SON composites use explicit calendar years for reproducibility across scripts.
# Literature often flags |SON DMI| > 0.5 °C-style events (`IOD_THRESHOLDS`); lists here
# are the operational definition for this codebase unless rebuilt from thresholds.
IOD_COMPOSITE_SON_YEARS = {
    'positive': [1994, 1997, 2006, 2012, 2015, 2018, 2019],
    'negative': [1980, 1981, 1992, 1996, 1998],
}

# ENSO classification for stratified composites: SON-mean Niño-3.4 (same season as peak IOD).
ENSO_SON_NINO34_THRESHOLD_C = 0.5

# Drought thresholds
DROUGHT_THRESHOLDS = {
    'spi3': {
        'moderate': -1.0,
        'severe': -1.5,
        'extreme': -2.0
    },
    'spi6': {
        'moderate': -1.0,
        'severe': -1.5,
        'extreme': -2.0
    },
    'spi12': {
        'moderate': -1.0,
        'severe': -1.5,
        'extreme': -2.0
    }
}

# ============================================================================
# Model Configuration
# ============================================================================

# Hierarchical model levels
HIERARCHICAL_MODEL_LEVELS = {
    'global': {
        'name': 'Global Scale (ICON)',
        'description': 'Global climate model for large-scale patterns',
        'resolution': '~13 km',
        'domain': 'Global'
    },
    'regional': {
        'name': 'Regional Scale (MPAS)',
        'description': 'Regional climate model for mesoscale patterns',
        'resolution': '~3 km',
        'domain': 'Southern Africa'
    },
    'local': {
        'name': 'Local Scale (AI/ML)',
        'description': 'Machine learning models for local patterns',
        'resolution': '~1 km',
        'domain': 'Local regions'
    }
}

# Model approaches
MODEL_APPROACHES = {
    'physics_informed': {
        'name': 'Physics-Informed',
        'description': 'Models incorporating physical processes',
        'advantages': ['Physical consistency', 'Interpretability', 'Generalization']
    },
    'pure_data_driven': {
        'name': 'Pure Data-Driven',
        'description': 'Models based purely on data patterns',
        'advantages': ['Flexibility', 'Non-linear relationships', 'Pattern recognition']
    }
}

# ============================================================================
# Ensemble Configuration
# ============================================================================

# Ensemble parameters
ENSEMBLE_PARAMS = {
    'n_members': 20,
    'max_lead_times': 6,
    'uncertainty_quantification': True,
    'probability_thresholds': [0.1, 0.3, 0.5, 0.7, 0.9]
}

# Forecast verification
VERIFICATION_METRICS = {
    'continuous': ['RMSE', 'MAE', 'Bias', 'Correlation', 'R²'],
    'categorical': ['POD', 'FAR', 'CSI', 'HSS'],
    'probabilistic': ['Brier Score', 'Reliability', 'Resolution', 'Sharpness']
}

# ============================================================================
# Visualization Configuration
# ============================================================================

# Plot settings
PLOT_SETTINGS = {
    'figure_size': (12, 10),
    'dpi': 300,
    'style': 'seaborn-v0_8-whitegrid',
    'context': 'paper',
    'font_scale': 1.2
}

# Color schemes
COLOR_SCHEMES = {
    'correlation': 'RdBu_r',
    'drought': 'YlOrRd',
    'iod_phases': {
        'positive': 'red',
        'negative': 'blue',
        'neutral': 'gray'
    },
    'regions': {
        'southeastern': '#1f77b4',
        'central': '#ff7f0e',
        'northwestern': '#2ca02c',
        'southwestern': '#d62728'
    }
}

# Map settings
MAP_SETTINGS = {
    'projection': 'PlateCarree',
    'extent': [10, 40, -35, -10],  # [lon_min, lon_max, lat_min, lat_max]
    'coastline': True,
    'borders': True,
    'gridlines': True
}

# ============================================================================
# File Naming Conventions
# ============================================================================

# File naming patterns
FILE_PATTERNS = {
    'dmi_data': 'dmi_{source}_{start_year}_{end_year}.csv',
    'correlation_map': 'correlation_{drought_index}_{season}_{lag}lag.png',
    'time_series': 'time_series_{region}_{drought_index}.png',
    'composite': 'composite_{drought_index}_{season}.png',
    'ensemble_forecast': 'ensemble_forecast_lead{lead_time}.png',
    'verification': 'verification_lead{lead_time}.png'
}

# ============================================================================
# Utility Functions
# ============================================================================

def create_directories():
    """Create all necessary directories for analysis"""
    for analysis_type, dirs in ANALYSIS_DIRS.items():
        for dir_name, dir_path in dirs.items():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {dir_path}")

def get_dmi_file_path(source='era5'):
    """Get the path to DMI data file"""
    if source not in DMI_SOURCES:
        raise ValueError(f"Unknown DMI source: {source}")
    
    pattern = DMI_SOURCES[source]['file_pattern']
    data_dir = Path(DATA_DIR)
    
    # Look for matching files
    matching_files = list(data_dir.glob(f"**/{pattern}"))
    if not matching_files:
        raise FileNotFoundError(f"No DMI files found for source: {source}")
    
    return matching_files[0]

def get_analysis_output_dir(analysis_type):
    """Get output directory for specific analysis type"""
    if analysis_type not in ANALYSIS_DIRS:
        raise ValueError(f"Unknown analysis type: {analysis_type}")
    
    return ANALYSIS_DIRS[analysis_type]['base']

def get_plot_output_dir(analysis_type):
    """Get plots directory for specific analysis type"""
    if analysis_type not in ANALYSIS_DIRS:
        raise ValueError(f"Unknown analysis type: {analysis_type}")
    
    return ANALYSIS_DIRS[analysis_type]['plots']

# ============================================================================
# Validation Functions
# ============================================================================

def validate_config():
    """Validate configuration parameters"""
    errors = []
    
    # Check if base directories exist
    if not DATA_DIR.exists():
        errors.append(f"Data directory does not exist: {DATA_DIR}")
    
    # Check analysis period
    if ANALYSIS_PERIOD['start_year'] >= ANALYSIS_PERIOD['end_year']:
        errors.append("Start year must be before end year")
    
    # Check correlation parameters
    if CORRELATION_PARAMS['min_valid_points'] < 1:
        errors.append("Minimum valid points must be at least 1")
    
    if CORRELATION_PARAMS['significance_level'] <= 0 or CORRELATION_PARAMS['significance_level'] >= 1:
        errors.append("Significance level must be between 0 and 1")
    
    if errors:
        raise ValueError("Configuration validation failed:\n" + "\n".join(errors))
    
    print("✓ Configuration validation passed")
    return True

# ============================================================================
# Main Configuration
# ============================================================================

if __name__ == "__main__":
    print("Analysis Configuration")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Validate configuration
    validate_config()
    
    print("\nConfiguration Summary:")
    print(f"  Data directory: {DATA_DIR}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Analysis period: {ANALYSIS_PERIOD['start_year']}-{ANALYSIS_PERIOD['end_year']}")
    print(f"  Regions: {list(SOUTHERN_AFRICA_REGIONS.keys())}")
    print(f"  Drought indices: {list(DROUGHT_INDICES.keys())}")
    print(f"  Seasons: {list(SEASONS.keys())}")
    print("\n✓ Configuration loaded successfully")

