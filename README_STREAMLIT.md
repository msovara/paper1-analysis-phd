# Streamlit Data Visualization Dashboard

Interactive web dashboard for visualizing climate data inputs including DMI, NINO34, and drought indices.

## Features

- 📊 **Time Series Visualization**: Interactive plots with multiple variables
- 🔍 **Data Analysis**: Scatter plots, correlation matrices, and distributions  
- 📉 **Statistical Summary**: Comprehensive statistics and data insights
- ⚙️ **Data Information**: Data types, memory usage, and metadata
- 📥 **Export Options**: Download processed data and statistics

## Installation

1. Install required packages:
```bash
pip install -r requirements_streamlit.txt
```

Or install individually:
```bash
pip install streamlit pandas numpy plotly
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run streamlit_data_visualizer.py
```

2. The app will open in your default web browser (usually at `http://localhost:8501`)

3. Upload a CSV file or select from existing files:
   - `nino34.long.anom.csv`
   - `dmi_son_top_events.csv`
   - `dmi_son_annual_averages.csv`

## Features Overview

### 1. Data Overview Tab
- Basic statistics (rows, columns, missing data)
- Data preview
- Quick summary statistics

### 2. Time Series Tab
- Interactive time series plots
- Multiple variable selection
- Moving average overlay option
- Automatic date column detection

### 3. Analysis Tab
- Scatter plots with correlation
- Correlation heatmaps
- Distribution histograms

### 4. Statistics Tab
- Detailed descriptive statistics
- Additional metrics (skewness, kurtosis)
- Download statistics as CSV

### 5. Data Info Tab
- Data types and structure
- Memory usage
- Download processed data

## Data Format

The app supports CSV files with:
- Date columns (auto-detected)
- Numeric variables
- Index-based time series

## Tips

- Use the sidebar to upload or select files
- Select multiple variables for comparison
- Enable moving averages to smooth time series
- Download processed data and statistics for further analysis

## Troubleshooting

If you encounter issues:
1. Ensure all required packages are installed
2. Check that your CSV file has proper headers
3. Verify date columns are in a recognizable format
4. Check the console for error messages

