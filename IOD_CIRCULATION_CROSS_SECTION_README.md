# IOD Circulation Vertical Cross-Section

## Overview

Creates the diagnostic figure requested by your supervisor: a **vertical cross-section** showing atmospheric circulation during **positive and negative** IOD events. This bridges your statistical (Paper 1) and dynamical (Paper 2) understanding.

**Uses real ERA5 data** (omega and u-wind on pressure levels). No synthetic data when files are present.

### What the Figure Shows (2-panel layout)

- **(a) Positive IOD**: Subsidence over Central Africa → drought; Ascent over Horn → rainfall
- **(b) Negative IOD**: Opposite pattern (ascent over Central Africa → rainfall; subsidence over Horn)
- **Omega (vertical velocity, Pa/s)**: Color shading (Red = subsidence, Blue = ascent)
- **Zonal wind (u)**: Contours
- **Domain**: 35°S–37°N, zonal mean over 10°E–60°E (Southern to Northern Africa)
- **Vertical**: 1000–100 hPa

### Physical Interpretation

- **Positive IOD**: Central Africa subsidence → drought; Horn ascent → rainfall
- **Negative IOD**: Central Africa ascent → rainfall; Horn subsidence → drought
- The opposite patterns validate the IOD-driven circulation mechanism

---

## Where to Put the Downloaded Files

After downloading, place the NetCDF files in one of these locations (the script checks in order):

| Option | Path | Use case |
|--------|------|----------|
| **1 (recommended)** | `{data_dir}/atmospheric/` | Same as your other ERA5 atmospheric data |
| 2 | `{data_dir}/era5/` | Dedicated ERA5 folder |
| 3 | `{data_dir}/` | Root of your data directory |

**On the cluster (Lengau):**
```
/home/msovara/lustre/DataDownloads/data/atmospheric/
├── era5_omega_pressure_levels_1980-2020.nc   (or .grib from CDS)
├── era5_u_pressure_levels_1980-2020.nc       (or .grib)
└── 44b356f31168077a5ba0a07bcc0ab547.grib    (CDS hash-named GRIB also supported)
```

**Supported formats:** NetCDF (`.nc`) and GRIB (`.grib`, `.grb`, `.grib2`). GRIB requires `cfgrib` (`pip install cfgrib`).

**Locally:**
```
./atmospheric/
├── era5_omega_pressure_levels_1980-2020.nc
└── era5_u_pressure_levels_1980-2020.nc
```

Then run with `--data-dir` pointing to the **parent** of `atmospheric/`:
- Cluster: `--data-dir /home/msovara/lustre/DataDownloads/data`
- Local: `--data-dir .` (if `atmospheric/` is in current directory)

---

## Quick Start

### 1. Download ERA5 data (required for real analysis)

```bash
# Install CDS API
pip install cdsapi

# Register at https://cds.climate.copernicus.eu/ and set up ~/.cdsapirc

# Download omega and u on pressure levels (SON months, 1980–2020)
# Saves to ./atmospheric/ by default
python download_era5_omega_u.py --output-dir atmospheric --years 1980 2020
```

### 2. Run with ERA5 data

```bash
# If atmospheric/ is in current directory
python plot_iod_circulation_cross_section.py --data-dir . --output-dir output/iod_circulation

# On cluster (data in /home/msovara/lustre/DataDownloads/data/atmospheric/)
python plot_iod_circulation_cross_section.py --data-dir /home/msovara/lustre/DataDownloads/data --output-dir output/iod_circulation
```

### 3. Require real data only (no synthetic fallback)

```bash
python plot_iod_circulation_cross_section.py --data-dir . --no-synthetic
```

If omega/u files are not found, the script exits with an error instead of using synthetic data.

---

## Data Requirements

| Variable | ERA5 name | Pressure levels |
|----------|-----------|-----------------|
| Omega | `vertical_velocity` | 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100 hPa |
| U-wind | `u_component_of_wind` | Same |

**Domain**: 35°S to 37°N, 10°E to 60°E  
**Months**: September, October, November (SON)  
**Years**: 1980–2020 (or your analysis period)

---

## Command-Line Options

```
--data-dir PATH              Path to ERA5 atmospheric data (default: . or cluster path)
--output-dir PATH            Output directory (default: output/iod_circulation)
--lat-south, --lat-north     Latitude bounds (default: -30, 30)
--lon-west, --lon-east       Longitude bounds for zonal mean (default: 10, 60)
--download                   Download ERA5 via CDS API before plotting
--positive-iod-years Y1 Y2   Positive IOD years (default: 1994 1997 2006 2012 2015 2018 2019)
--negative-iod-years Y1 Y2   Negative IOD years (default: 1980 1981 1992 1996 1998)
--single-panel               Plot only positive IOD (legacy single-panel figure)
--no-synthetic               Exit with error if ERA5 data not found (do not use synthetic demo)
```

---

## For Paper 2 (ICON/MPAS Validation)

Create two panels:
- **Left**: Model composite (ICON or MPAS)
- **Right**: ERA5 composite

Use the same composite logic (positive IOD years, SON, zonal mean) for both. Compare to validate that the model captures the observed circulation.

---

## Caption Example

> "Zonal-mean vertical velocity (omega) and zonal wind during (a) positive and (b) negative IOD events. Positive IOD: subsidence over Central Africa (red) suppresses convection and causes drought; ascent over the Horn (blue) enhances rainfall. Negative IOD: opposite pattern—ascent over Central Africa favors rainfall. The dipole response validates the IOD-driven circulation mechanism. Contours show zonal wind (m/s)."
