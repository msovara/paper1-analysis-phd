# Indian Ocean Dipole (IOD) and African Drought Analysis

Comprehensive analysis of the relationship between the Indian Ocean Dipole (IOD) and drought patterns across Africa (1980-2020).

## 📋 Project Overview

This repository contains code, data, and analysis for investigating:
- IOD-Drought teleconnections across Africa
- ENSO modulation of IOD-drought relationships
- Atmospheric circulation patterns during IOD events
- Statistical and physical mechanisms linking IOD to African hydroclimate

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Anaconda/Miniconda (recommended)
- Access to ERA5 data (for full analysis)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tiny-media-analysis
```

2. Install dependencies:
```bash
# For Streamlit visualization
pip install -r requirements_streamlit.txt

# For full analysis (Anemoi/ML)
pip install -r requirements_anemoi.txt
```

### Interactive Data Visualization

Launch the Streamlit dashboard:
```bash
streamlit run streamlit_data_visualizer.py
```

Or use the provided scripts:
- Windows: `run_streamlit.bat`
- Linux/Mac: `./run_streamlit.sh`

## 📁 Repository Structure

```
tiny-media-analysis/
├── streamlit_data_visualizer.py    # Interactive data visualization dashboard
├── analysis_config.py              # Configuration for analysis workflows
├── comprehensive_iod_drought_statistics.py  # Main analysis script
├── composite_drought_iod_africa.py # Composite analysis
├── extract_*.py                    # Data extraction scripts
├── plot_*.py                       # Visualization scripts
├── data/                           # Data directory (not in repo)
├── output/                         # Analysis outputs (not in repo)
├── configs/                        # Configuration files
├── utils/                          # Utility functions
├── src/                            # Source code modules
├── training/                       # ML training scripts
├── evaluation/                     # Model evaluation
├── inference/                      # Inference scripts
└── requirements_*.txt              # Python dependencies
```

## 🔬 Key Features

### 1. Data Visualization Dashboard
- Interactive time series plots
- Correlation analysis
- Statistical summaries
- Data export capabilities

### 2. IOD-Drought Analysis
- Composite analysis for positive/negative IOD events
- ENSO-stratified composites
- Lag correlation analysis
- Partial correlation (controlling for ENSO)
- Seasonal analysis
- Wavelet coherence

### 3. Atmospheric Circulation Analysis
- ERA5 circulation composites
- MSLP, wind, and geopotential height analysis
- Physical mechanism diagnostics

## 📊 Data

### Input Data
- **DMI (Dipole Mode Index)**: IOD index from multiple sources (ERA5, NOAA, etc.)
- **Drought Indices**: SPI and SPEI at 3- and 6-month accumulation
- **ENSO**: Niño3.4 index
- **ERA5**: Atmospheric reanalysis data (MSLP, winds, geopotential height)

### Sample Data Files
- `nino34.long.anom.csv`: Niño3.4 index
- `dmi_son_top_events.csv`: Top IOD events
- `dmi_son_annual_averages.csv`: Annual DMI averages

**Note**: Large data files (NetCDF, GRIB) are not included in the repository. See data download scripts for obtaining full datasets.

## 🛠️ Usage

### Running Analysis

1. **Basic IOD-Drought Analysis**:
```bash
python simple_iod_drought_analysis.py
```

2. **Comprehensive Statistics**:
```bash
python comprehensive_iod_drought_statistics.py
```

3. **Composite Analysis**:
```bash
python composite_drought_iod_africa.py
```

### Configuration

Edit `analysis_config.py` to customize:
- Analysis periods
- Regional boundaries
- Drought thresholds
- IOD event definitions

## 📈 Visualization

The project includes multiple visualization tools:
- Streamlit interactive dashboard
- Matplotlib/Plotly static plots
- Cartopy maps for spatial analysis

## 🔧 Cluster Computing

For running on CHPC Lengau cluster:
- PBS job scripts: `*.pbs`
- Cluster setup guides: `LENGAU_*.md`
- SSH automation: `ssh_auto.py`, `remote_execute.py`

## 📚 Documentation

- `README_STREAMLIT.md`: Streamlit dashboard guide
- `QUICK_START.md`: Quick start guide
- `LENGAU_RUN_GUIDE.md`: Cluster computing guide
- `DRAFT_PAPER_IOD_DROUGHT.md`: Paper draft
- Various analysis guides in markdown files

## 🤝 Contributing

This is a research project. For questions or collaboration, please contact the repository owner.

## 📝 Citation

If you use this code or analysis, please cite:
```
Sovara, M. (2025). Indian Ocean Dipole and African Drought Analysis.
[Add full citation when published]
```

## ⚠️ Important Notes

- Large data files are excluded from the repository (see `.gitignore`)
- Some scripts require cluster access for full functionality
- Data download scripts may require API keys or data access permissions
- Output directories are not tracked in git

## 📄 License

[Add license information]

## 👤 Author

**Mthetho Sovara**
- Email: [your-email]
- Institution: [your-institution]

---

For detailed analysis workflows, see the individual script documentation and markdown guides in the repository.

