
# Full-text Draft Manuscript — Indian Ocean Dipole Teleconnections and African Drought

**Project:** IOD–drought relationships in Africa (1980–2020)  
**Data:** ERA5 circulation (MSLP, u850/v850, z500), drought indices (SPI/SPEI at 3- and 6‑month accumulation), DMI (IOD), Niño3.4 (ENSO)  
**Outputs (figures):** stored under `output/comprehensive_iod_statistics/plots/` on the cluster and selectively downloaded locally.  
**Note:** This is a full prose draft intended for refinement. Items in **[BRACKETS]** are placeholders to be filled with final numbers, thresholds, and references.

---

## Title (working)
**Indian Ocean Dipole modulation of African drought variability (1980–2020): evidence from drought indices and ERA5 circulation composites**

## Authors (placeholder)
M. Sovara\*, Co-authors…  
\*Corresponding author: [email]

---

## Abstract
African drought is a major climate hazard with severe societal and ecological impacts, yet its variability remains difficult to attribute and predict at regional scales. We investigate the influence of the Indian Ocean Dipole (IOD) on African drought variability during 1980–2020 using standardized drought indices (SPI and SPEI at 3‑ and 6‑month accumulation) and a suite of diagnostics including event composites, ENSO-stratified composites, lag correlations, partial correlations, seasonal contrasts, and wavelet coherence. To connect statistical associations to plausible mechanisms, we analyze ERA5 atmospheric circulation composites during SON for canonical positive and negative IOD event years, evaluating mean sea-level pressure, 850‑hPa winds, and 500‑hPa geopotential height anomalies. Across Africa, drought responses to IOD phase are spatially heterogeneous and vary with drought metric and time scale, while ENSO state modulates both the magnitude and footprint of anomalies. Circulation composites reveal patterns consistent with dynamically driven changes in low-level moisture transport and mid‑tropospheric height anomalies during IOD events. Together, these results provide a physically coherent framework for incorporating IOD information into drought early warning and seasonal outlook guidance over Africa.

**Keywords:** Indian Ocean Dipole; drought; Africa; SPI; SPEI; ENSO; ERA5; teleconnections; composites

---

## 1. Introduction
Drought is among the most consequential climate hazards across Africa, affecting agriculture, food systems, water resources, health outcomes, and economic stability. The impacts of drought are often amplified by high climate sensitivity, limited adaptive capacity, and strong dependence on rain‑fed production. Improving drought attribution and predictability is therefore of high scientific and societal value. While local land–atmosphere feedbacks and regional circulation features shape drought development, large-scale ocean–atmosphere modes can impose predictable signals on rainfall and hydroclimate variability across wide regions.

The Indian Ocean Dipole (IOD) is a key mode of coupled variability in the Indian Ocean, commonly quantified by the Dipole Mode Index (DMI), which measures the SST anomaly gradient between the western and eastern equatorial Indian Ocean. The IOD exhibits strong seasonal phase‑locking, typically peaking during boreal autumn (September–November; SON). During positive IOD events, enhanced convection in the western Indian Ocean and suppressed convection in the eastern Indian Ocean reorganize tropical circulation, potentially altering moisture fluxes and rainfall across East Africa and beyond. Conversely, negative IOD events reverse this pattern, with associated changes in convection, low-level winds, and pressure fields. However, the influence of IOD on African hydroclimate is not uniform; responses depend on region, season, and interactions with other modes such as ENSO.

ENSO and IOD can occur independently but often interact through shared Indo-Pacific circulation pathways. ENSO can influence the mean state and variability of the Indian Ocean and can amplify or suppress IOD-related convection anomalies. Consequently, statistical associations between DMI and drought indices may reflect direct IOD influence, ENSO co-variability, or state-dependent modulation. Furthermore, drought metrics differ: SPI reflects precipitation anomalies alone, while SPEI incorporates evaporative demand and can therefore express temperature-driven drying more strongly—an increasingly relevant distinction under warming.

This study combines multiple statistical perspectives and physically interpretable circulation diagnostics to evaluate IOD–drought relationships across Africa for 1980–2020. Specifically, we (i) quantify drought anomalies during IOD phases using SPI and SPEI at 3‑ and 6‑month time scales; (ii) assess ENSO modulation via stratified composites; (iii) examine timing and robustness using lag and partial correlations and wavelet coherence; and (iv) diagnose physically consistent circulation anomalies in ERA5 during canonical IOD events in SON using MSLP, 850‑hPa winds, and 500‑hPa geopotential height. The aim is to provide both statistical and mechanistic evidence supporting how IOD contributes to African drought variability and how that contribution is conditioned by ENSO and drought time scale.

---

## 2. Data and Methods
### 2.1 Study domain and analysis period
Analyses are conducted over Africa and adjacent oceans that influence African moisture pathways. The analysis period is **1980–2020**, corresponding to **492 monthly values** for each index time series. Circulation composites focus on SON, consistent with the IOD seasonal maximum.

### 2.2 Climate indices (IOD and ENSO)
IOD variability is represented by monthly DMI values. ENSO variability is represented by the Niño3.4 index. Months (or seasons) are classified into El Niño, La Niña, or Neutral conditions using a standard thresholding approach **[INSERT thresholds and any smoothing (e.g., 3‑month mean) used in the workflow]**. Where relevant, analyses use these classifications to stratify IOD composites by ENSO state.

### 2.3 Drought indices (SPI and SPEI)
We use SPI and SPEI as standardized drought metrics. SPI is computed from precipitation anomalies at specified accumulation windows; SPEI is computed from a climatic water balance (precipitation minus evaporative demand), and thus can capture temperature-driven drying. We analyze accumulation windows of **3 months (SPI3/SPEI3)** and **6 months (SPI6/SPEI6)**. These capture shorter-term moisture deficits and more persistent hydrological drought conditions, respectively.

### 2.4 Composite analysis
Composite drought anomalies are computed for positive and negative IOD phases by averaging drought index anomalies over the months associated with IOD events and comparing to a climatological baseline. For circulation composites, canonical SON IOD event years are used (Section 2.8). Significance is assessed using the implemented gridpoint method **[INSERT: t-test / bootstrap / permutation; multiple testing handling if any]**, and stippling indicates significant regions where plotted.

### 2.5 ENSO-stratified composites
To evaluate state dependence, we compute composites conditional on ENSO state. A 3×3 framework summarizes drought anomalies for each combination of ENSO phase (El Niño, La Niña, Neutral) and IOD phase (positive, negative, and difference). Where combinations have insufficient sample size, panels indicate low-data conditions rather than over-interpreting noisy composites.

### 2.6 Lag and partial correlation analysis
Lag correlations are computed between DMI and drought indices across multiple lags **[INSERT lag range; repository indicates e.g., −12…+12 months]** to evaluate whether drought responses are concurrent, leading, or lagging relative to IOD variability. Partial correlations quantify the association between DMI and drought indices while controlling for ENSO (Niño3.4), providing a robustness check against ENSO confounding.

### 2.7 Wavelet coherence
Wavelet coherence is computed between DMI and drought indices to assess time–frequency dependence. This reveals whether coupling is persistent over the full record or concentrated in particular epochs and at particular periodicities (e.g., interannual 2–7‑year bands).

### 2.8 Atmospheric circulation composites (ERA5)
We use ERA5 to compute SON circulation anomalies during canonical IOD event years. Variables include:
- MSLP (mean sea-level pressure)
- 850‑hPa winds (u850, v850)
- 500‑hPa geopotential height (z500, converted to meters)

Canonical IOD event years used in the circulation composite workflow are:
- Positive IOD: **1994, 1997, 2006, 2018, 2019**
- Negative IOD: **1980, 1981, 1992, 1996, 1998**

Circulation anomalies are computed relative to SON climatology (excluding event years). For interpretability, geopotential height anomalies and wind vectors are plotted separately, in addition to multi-variable circulation composite panels. Projection variants include Mercator and polar stereographic views, with hemispheric extents.

---

## 3. Results
### 3.1 Drought composites by IOD phase
Composite drought maps indicate that IOD phase is associated with regionally varying drought responses across Africa, with notable differences by index type (SPI vs SPEI) and accumulation window (3 vs 6 months). In general, SPI composites highlight precipitation-driven anomalies, while SPEI composites can show enhanced drying in regions where evaporative demand contributes substantially to water deficits. Differences between SPI3 and SPI6 suggest that some IOD-related signals manifest as shorter-lived anomalies, whereas others accumulate into more persistent deficits.

Across Africa, the drought response exhibits spatial heterogeneity consistent with differing moisture source regions, topographic effects, and regional circulation regimes. In areas influenced by Indian Ocean moisture transport, IOD-related anomalies are expected to appear most directly in seasons aligned with IOD peak activity (SON), while in other regions lagged responses may reflect the propagation of circulation anomalies or persistence mechanisms.

**Figure 1:** Composite drought anomalies during IOD phases  
`composite_drought_SPI3.png`, `composite_drought_SPI6.png`, `composite_drought_SPEI3.png`, `composite_drought_SPEI6.png`

### 3.2 ENSO modulation of IOD–drought relationships
ENSO-stratified composites suggest that the IOD–drought relationship depends on background ENSO conditions. Under El Niño, IOD-related drought anomalies may be amplified or spatially reorganized as ENSO modifies Indo-Pacific convection and the Walker circulation. Under La Niña, IOD-associated anomalies may weaken or shift, and under Neutral ENSO conditions, the “pure” IOD signal may be more apparent in some regions. Because some combinations of ENSO×IOD phase are rare, interpretation focuses on patterns that are consistent across SPI/SPEI and across time scales and that align with circulation diagnostics.

**Figure 2:** ENSO-stratified drought composites  
`enso_stratified_composite_SPI3.png`, `enso_stratified_composite_SPI6.png`, `enso_stratified_composite_SPEI3.png`, `enso_stratified_composite_SPEI6.png`

### 3.3 Timing of associations (lag correlations)
Lag correlation analysis indicates that IOD–drought coupling occurs with variable timing across regions and indices. Regions showing peak correlations near zero lag are consistent with concurrent IOD forcing during SON, whereas positive lags (DMI leading drought) suggest delayed hydroclimate impacts consistent with soil-moisture memory, delayed seasonal rainfall responses, or persistence in evaporative demand anomalies (particularly for SPEI). Negative-lag peaks are interpreted cautiously as potential signatures of shared forcing or chance alignment.

**Figure 3:** Lag correlations between DMI and drought indices  
`lag_correlation_analysis.png`

### 3.4 Robustness controlling for ENSO (partial correlations)
Partial correlation patterns indicate which drought teleconnections remain after removing ENSO variability. Where partial correlations remain strong and spatially coherent, the results support an independent IOD association; where partial correlations weaken substantially relative to simple correlations, the apparent IOD signal may reflect ENSO co-variability. This diagnostic provides a stronger basis for causal interpretation than correlations alone, particularly in regions where ENSO and IOD frequently co-occur.

**Figure 4:** Partial correlation maps (IOD controlling for ENSO)  
`partial_correlation_analysis.png`

### 3.5 Seasonal dependence
Seasonal analyses show that drought sensitivity to IOD is not confined strictly to SON. Some regions exhibit consistent anomalies across seasons, whereas others show sign or magnitude changes that likely reflect seasonal migration of convergence zones, regional rainfall regimes, and seasonal evolution of land–atmosphere feedbacks. Differences between SPI and SPEI seasonality provide additional evidence for temperature-driven modulation in some regions.

**Figure 5:** Seasonal diagnostics  
`seasonal_analysis_SPI3.png`, `seasonal_analysis_SPI6.png`, `seasonal_analysis_SPEI3.png`, `seasonal_analysis_SPEI6.png`

### 3.6 Time–frequency dependence (wavelet coherence)
Wavelet coherence reveals intermittency in IOD–drought coupling. Periods of elevated coherence at interannual periodicities suggest that the teleconnection is stronger during epochs with stronger or more frequent IOD/ENSO events, while weaker coherence in other periods suggests non-stationarity. Coherence patterns differ across indices and time scales, indicating that precipitation-driven and evaporative-demand-driven drought responses may be expressed differently in the time–frequency domain.

**Figure 6:** Wavelet coherence diagnostics  
`wavelet_coherence_SPI3.png`, `wavelet_coherence_SPEI3.png`, etc.

### 3.7 Physical consistency from ERA5 circulation composites
ERA5 composites provide mechanistic consistency for the drought teleconnections. MSLP anomalies during IOD events suggest reorganized surface pressure gradients and altered convergence patterns. At 850 hPa, wind anomalies indicate changes in low-level moisture transport into and across Africa, providing a direct pathway linking oceanic forcing to precipitation and drought anomalies. At 500 hPa, geopotential height anomalies reflect ridge/trough structures that influence vertical motion and synoptic-scale flow.

To improve interpretability, geopotential height anomalies and wind vectors are plotted separately, reducing visual clutter compared to overlaid products. Hemispheric and polar-view geopotential height plots support interpretation of broader circulation structures beyond the African continent.

**Figure 7:** Atmospheric circulation composites  
`atmospheric_circulation_composites.png`  
**Figure 8:** Geopotential height anomaly composites  
`atmospheric_circulation_geopotential_height_mercator.png`, `atmospheric_circulation_geopotential_height_polar_stereographic.png`  
**Figure 9:** Wind vector composites  
`atmospheric_circulation_wind_vectors.png`

---

## 4. Discussion
### 4.1 Interpreting regional heterogeneity
The spatial heterogeneity of IOD–drought responses across Africa likely reflects differences in moisture source regions, the seasonal timing of rainfall, and the pathways by which Indian Ocean convection anomalies project onto African circulation. Regions directly influenced by Indian Ocean moisture transport are expected to show stronger sensitivity during seasons aligned with IOD peak activity. Elsewhere, teleconnections may arise through broader circulation shifts at mid‑levels, changes in subtropical highs, or synoptic-scale steering effects.

### 4.2 ENSO–IOD interaction and conditional effects
ENSO-stratified results indicate that IOD impacts cannot be interpreted independently of the Indo-Pacific background state. ENSO can alter convection over the Maritime Continent and Indian Ocean, shifting the Walker circulation and therefore modulating IOD-related anomalies. This conditional dependence implies that forecast systems and attribution studies should consider both modes jointly rather than treating DMI as an isolated predictor.

### 4.3 SPI vs SPEI and the role of evaporative demand
Differences between SPI and SPEI composites suggest that evaporative demand (and temperature anomalies) can amplify drought signals in some regions and seasons. As warming intensifies, SPEI may increasingly diverge from SPI, particularly in semi‑arid zones where evaporative demand contributes strongly to water deficits. Future work should examine whether the observed differences strengthen over time and how they relate to long‑term trends in temperature and potential evapotranspiration.

### 4.4 Uncertainty and limitations
Key limitations include limited event counts for certain ENSO×IOD combinations, spatial autocorrelation affecting significance interpretation, and sensitivity to thresholds used for event selection and ENSO classification. Additionally, reproducibility may depend on consistent scientific Python environments (e.g., xarray/dask version compatibility for older serialized outputs). These limitations can be addressed through expanded sensitivity analysis (varying thresholds), spatial multiple-testing correction, and replication across alternate datasets and reanalyses.

---

## 5. Conclusions
Across 1980–2020, IOD phase is associated with spatially heterogeneous drought anomalies across Africa, with responses that vary by drought metric (SPI vs SPEI), accumulation window, and season. ENSO significantly modulates IOD–drought relationships, underscoring the need for conditional or multivariate frameworks. ERA5 circulation composites support mechanistic consistency, indicating that IOD events are associated with changes in low-level wind anomalies and mid‑tropospheric height patterns that plausibly influence moisture transport and rainfall. Collectively, the results provide a coherent statistical–physical basis for incorporating IOD information into drought early warning and seasonal outlook guidance over Africa.

---

## Data and code availability (draft)
Outputs used here are stored under `output/comprehensive_iod_statistics/` on the cluster:
- `output/comprehensive_iod_statistics/data/`: serialized results (pickle)
- `output/comprehensive_iod_statistics/plots/`: figures referenced in the manuscript

---

## Acknowledgements (placeholder)
Compute resources provided by CHPC Lengau. [Funding sources]. [Collaborators].

---

## References (placeholder)
[Insert references for IOD definition, ENSO–IOD interaction, SPI/SPEI methodology, ERA5, and teleconnection literature.]


