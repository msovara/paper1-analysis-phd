# Draft Manuscript (Working) — Indian Ocean Dipole Teleconnections and African Drought

**Project:** IOD–drought relationships in Africa (1980–2020)  
**Data:** ERA5 (atmospheric circulation), drought indices (SPI/SPEI; multiple accumulation windows), DMI (IOD), Niño3.4 (ENSO)  
**Status:** Draft for internal review (placeholders remain; update with your preferred journal format and exact numeric results).

---

## Title (working)
**Indian Ocean Dipole influence on African drought variability (1980–2020): composite, ENSO-stratified, and atmospheric circulation evidence**

## Author list (placeholder)
M. Sovara\*, Co-authors…  
\*Corresponding author: (email)

## Abstract (draft)
Understanding the drivers of African drought is critical for seasonal forecasting and climate risk management. We quantify relationships between the Indian Ocean Dipole (IOD) and drought conditions across Africa for 1980–2020 using standardized drought indices (SPI and SPEI at 3- and 6‑month accumulation) and multiple statistical lenses, including event composites, ENSO-stratified composites, lag correlations, partial correlations, seasonal diagnostics, and wavelet coherence. We further assess physical consistency using ERA5 atmospheric circulation composites (MSLP, 850‑hPa winds, 500‑hPa geopotential height) during canonical positive and negative IOD events in SON. Results indicate regionally heterogeneous IOD–drought teleconnections, modulation by ENSO state, and circulation anomalies consistent with dynamically forced moisture transport changes. This framework links statistical associations to plausible mechanisms and provides guidance for incorporating IOD information into drought early warning over Africa.

**Keywords:** Indian Ocean Dipole; drought; Africa; SPI; SPEI; ENSO; ERA5; teleconnections; composites

---

## 1. Introduction
### 1.1 Motivation
- African drought impacts agriculture, water security, ecosystems, and energy systems.
- Seasonal drought predictability is partly driven by large-scale modes such as IOD and ENSO.

### 1.2 Background
- IOD: zonal SST gradient across the tropical Indian Ocean; peaks during SON.
- Known impacts on East Africa “short rains,” southern African rainfall variability, and broader Indo-Pacific circulation.
- ENSO–IOD interactions can amplify or suppress hydroclimate responses.

### 1.3 Study objectives (edit as needed)
1. Quantify the spatial patterns of drought anomalies during positive/negative IOD events across Africa using SPI/SPEI.
2. Evaluate how ENSO state conditions (El Niño/La Niña/Neutral) modulate IOD–drought composites.
3. Characterize timing (lags) and robustness (partial correlations, seasonal analysis, coherence).
4. Diagnose physically consistent atmospheric circulation patterns from ERA5 during IOD events.

---

## 2. Data and Methods
### 2.1 Study domain and period
- Domain: Africa and adjacent oceans (analysis maps produced over Africa; circulation plots also produced in hemispheric views).
- Period: **1980–2020** (492 months).

### 2.2 Climate indices
- **DMI (IOD index):** monthly values; IOD events defined using SON-season criteria.
- **Niño3.4:** used for ENSO classification (El Niño, La Niña, Neutral).

### 2.3 Drought indices
- **SPI** and **SPEI** at **3- and 6‑month** accumulation (SPI3, SPI6, SPEI3, SPEI6).
- Gridded drought fields analyzed via composites, correlation, and coherence diagnostics.

### 2.4 Event selection and compositing
- Canonical SON IOD event years used in atmospheric composites:
  - **Positive IOD:** 1994, 1997, 2006, 2018, 2019
  - **Negative IOD:** 1980, 1981, 1992, 1996, 1998
- Composite drought anomalies computed as event mean minus climatology (climatology computed over non‑event SON months; exact definition to confirm in final run).
- Significance: gridpoint tests and/or resampling as implemented; stippling indicates significant regions where available.

### 2.5 ENSO-stratified composites
- 3×3 composite design: ENSO state (El Niño/La Niña/Neutral) × IOD phase (positive/negative/difference).
- Some combinations may be absent or low-sample; panels indicate insufficient data where applicable.

### 2.6 Lagged and partial correlation analysis
- Lag correlations computed for multiple lags (e.g., −12…+12 months).
- Partial correlations evaluate IOD–drought association controlling for confounders (e.g., ENSO).

### 2.7 Wavelet coherence
- Time–frequency coherence between drought indices and IOD (and/or ENSO), highlighting intermittency and scale dependence.

### 2.8 Atmospheric circulation diagnostics (ERA5)
- ERA5 variables:
  - **MSLP**
  - **850‑hPa winds** (u850, v850)
  - **500‑hPa geopotential height** (z500; converted to geopotential height in meters)
- Circulation composites evaluated for SON IOD years relative to climatology.
- Visualization outputs:
  - Multi-variable atmospheric composite panels.
  - Separate plots for **geopotential height anomalies** and **wind vectors** (to reduce clutter).
  - Additional variants for Mercator / polar stereographic views, with hemispheric extents.

---

## 3. Results
### 3.1 Composite drought response to IOD phase
Describe spatial patterns for SPI3/SPI6/SPEI3/SPEI6:
- East Africa (short rains) vs southern Africa (austral rainfall regimes).
- Differences between SPI and SPEI (temperature/evaporative demand sensitivity).

**Figure 1 (suggested):** `composite_drought_SPI3.png`, `composite_drought_SPI6.png`, `composite_drought_SPEI3.png`, `composite_drought_SPEI6.png`

### 3.2 ENSO modulation of IOD–drought teleconnections
- Compare IOD composites under El Niño/La Niña/Neutral conditions.
- Highlight strengthening/weakening of anomalies and shifts in spatial footprint.

**Figure 2 (suggested):** ENSO-stratified composites  
`enso_stratified_composite_SPI3.png`, `enso_stratified_composite_SPI6.png`, `enso_stratified_composite_SPEI3.png`, `enso_stratified_composite_SPEI6.png`

### 3.3 Timing and persistence (lag correlations)
- Identify whether drought response is concurrent with SON IOD or lags/leads by months.
- Summarize key lags per region and index.

**Figure 3 (suggested):** `lag_correlation_analysis.png`

### 3.4 Robustness controlling for ENSO (partial correlations)
- Compare correlation vs partial correlation patterns.
- Indicate regions where IOD signal remains after removing ENSO influence.

**Figure 4 (suggested):** `partial_correlation_analysis.png`

### 3.5 Seasonality
- Seasonal contrasts across African subregions; note any shifts in sign/magnitude across seasons.

**Figure 5 (suggested):** `seasonal_analysis_SPI3.png`, `seasonal_analysis_SPI6.png`, `seasonal_analysis_SPEI3.png`, `seasonal_analysis_SPEI6.png`

### 3.6 Time–frequency dependence (wavelet coherence)
- Report dominant timescales (e.g., 2–7 years) and periods of stronger coupling.

**Figure 6 (suggested):** `wavelet_coherence_SPI3.png`, `wavelet_coherence_SPEI3.png`, etc.

### 3.7 Physical consistency: atmospheric circulation composites
Interpret ERA5 composites in SON:
- **MSLP:** anomalous pressure patterns consistent with altered convergence/subsidence.
- **850‑hPa winds:** moisture transport anomalies into/out of drought-prone regions.
- **Z500:** mid‑tropospheric height anomalies consistent with ridge/trough structures.

**Figure 7 (suggested):** `atmospheric_circulation_composites.png`  
**Figure 8a (suggested):** `atmospheric_circulation_geopotential_height_mercator.png` (or `_platecarree` if Mercator fallback used)  
**Figure 8b (suggested):** `atmospheric_circulation_geopotential_height_polar_stereographic.png`  
**Figure 9 (suggested):** `atmospheric_circulation_wind_vectors.png`

---

## 4. Discussion
### 4.1 Mechanistic interpretation
- Link drought anomalies to circulation: low-level wind anomalies, pressure patterns, and mid-level geopotential height structure.
- Discuss regional differences and seasonal dependence.

### 4.2 ENSO–IOD interactions
- Explain how ENSO state could shift Walker circulation and influence Indian Ocean convection, modifying African rainfall teleconnections.

### 4.3 SPI vs SPEI differences
- SPEI includes temperature-driven evaporative demand; interpret divergence from SPI in warming-sensitive regions.

### 4.4 Uncertainty and limitations
- Event sample size (particularly ENSO×IOD combinations).
- Significance testing assumptions (spatial autocorrelation, multiple testing).
- Index definitions (thresholds; season selection).
- Potential data/version issues for reproducibility (e.g., dask/xarray compatibility for older pickle files).

---

## 5. Conclusions
1. IOD phase is associated with statistically and physically coherent drought anomalies across Africa, but with strong regional heterogeneity.
2. ENSO state modulates the IOD–drought relationship, affecting both magnitude and spatial structure.
3. ERA5 circulation composites provide physically consistent mechanisms linking IOD to moisture transport and pressure/height anomalies during SON.
4. The combined statistical–physical framework supports use of IOD information in drought early warning and seasonal outlooks.

---

## Data and code availability (draft)
- Outputs stored at: `output/comprehensive_iod_statistics/`  
  - `data/`: pickle results  
  - `plots/`: figures used in this manuscript

---

## Acknowledgements (placeholder)
Compute resources provided by CHPC Lengau. Funding sources… Collaborators…

---

## References (placeholder)
Add journal-formatted references for: Saji et al. (IOD), ENSO–IOD literature, SPI/SPEI methods, ERA5, African rainfall teleconnections, wavelet coherence methods.


