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

The Indian Ocean Dipole (IOD) is a key mode of coupled variability in the Indian Ocean, commonly quantified by the Dipole Mode Index (DMI), which measures the SST anomaly gradient between the western and eastern equatorial Indian Ocean (Saji et al., 1999; Webster et al., 1999). The IOD exhibits strong seasonal phase‑locking, typically peaking during boreal autumn (September–November; SON) (Saji et al., 1999; Cai et al., 2013). During positive IOD events, enhanced convection in the western Indian Ocean and suppressed convection in the eastern Indian Ocean reorganize tropical circulation, potentially altering moisture fluxes and rainfall across East Africa and beyond (Saji et al., 1999; Black et al., 2003). Conversely, negative IOD events reverse this pattern, with associated changes in convection, low-level winds, and pressure fields (Saji et al., 1999). However, the influence of IOD on African hydroclimate is not uniform; responses depend on region, season, and interactions with other modes such as ENSO (Black et al., 2003; Marchant et al., 2007).

ENSO and IOD can occur independently but often interact through shared Indo-Pacific circulation pathways (Webster et al., 1999; Cai et al., 2013). ENSO can influence the mean state and variability of the Indian Ocean and can amplify or suppress IOD-related convection anomalies (Cai et al., 2013). Consequently, statistical associations between DMI and drought indices may reflect direct IOD influence, ENSO co-variability, or state-dependent modulation. Furthermore, drought metrics differ: SPI reflects precipitation anomalies alone (McKee et al., 1993), while SPEI incorporates evaporative demand and can therefore express temperature-driven drying more strongly—an increasingly relevant distinction under warming (Vicente-Serrano et al., 2010; Dai, 2013).

This study combines multiple statistical perspectives and physically interpretable circulation diagnostics to evaluate IOD–drought relationships across Africa for 1980–2020. Specifically, we (i) quantify drought anomalies during IOD phases using SPI and SPEI at 3‑ and 6‑month time scales; (ii) assess ENSO modulation via stratified composites; (iii) examine timing and robustness using lag and partial correlations and wavelet coherence; and (iv) diagnose physically consistent circulation anomalies in ERA5 during canonical IOD events in SON using MSLP, 850‑hPa winds, and 500‑hPa geopotential height. The aim is to provide both statistical and mechanistic evidence supporting how IOD contributes to African drought variability and how that contribution is conditioned by ENSO and drought time scale.

---

## 2. Data and Methods
### 2.1 Study domain and analysis period
The analyses focus on Africa and the surrounding ocean regions that play an important role in supplying moisture to the continent. The study covers the period **1980–2020**, providing **492 monthly data points** for each climate index. To align with the time of year when the Indian Ocean Dipole is strongest, circulation patterns are examined primarily during the **September–October–November (SON) season**. The analysis spans the entire African continent (**35°S–37°N, 20°W–55°E**), and to better capture regional differences, the domain is subdivided into five regions: East Africa (10°S–20°N, 30°E–50°E), Southern Africa (35°S–10°S, 10°E–40°E), West Africa (5°S–20°N, 20°W–20°E), Central Africa (10°S–15°N, 5°E–30°E), and North Africa (15°N–37°N, 20°W–55°E).

### 2.2 Climate indices (IOD and ENSO)
IOD variability is represented by monthly DMI values (Saji et al., 1999). The Niño3.4 index represents ENSO variability. Months (or seasons) are classified into El Niño, La Niña, or Neutral conditions using a standard thresholding approach. **IOD events are identified when monthly DMI exceeds ±0.5°C, with positive IOD events defined as DMI > 0.5°C and negative IOD events as DMI < −0.5°C** (Saji et al., 1999). For ENSO classification, years are categorized based on SON-averaged Niño3.4 values: **El Niño when Niño3.4 ≥ +0.5°C, La Niña when Niño3.4 ≤ −0.5°C, and Neutral when −0.5°C < Niño3.4 < +0.5°C** (Trenberth, 1997). This seasonal averaging aligns with the IOD peak season and ensures consistency with the circulation composite analysis. Where relevant, analyses use these classifications to stratify IOD composites by ENSO state.

### 2.3 Drought indices (SPI and SPEI)
We use the Standardized Precipitation Index (SPI) and the Standardized Precipitation Evapotranspiration Index (SPEI) as standardised drought metrics. The SPI captures anomalies in rainfall alone (McKee et al., 1993), whereas the SPEI also accounts for atmospheric evaporative demand, making it more sensitive to temperature-driven drying (Vicente-Serrano et al., 2010). The SPI and SPEI indices are computed from precipitation and evapotranspiration anomalies at **3 and 6-month accumulation windows**. 

**SPI calculation**: For each grid point, precipitation is accumulated over the specified time window (3 or 6 months). The accumulated precipitation is then fitted to a **gamma distribution using the method of moments** (shape parameter α = μ²/σ², scale parameter β = σ²/μ, where μ is the mean and σ² is the variance). The cumulative probability from the fitted gamma distribution is transformed to a standard normal distribution to obtain SPI values (McKee et al., 1993). A minimum of 30 valid data points is required for reliable distribution fitting.

**SPEI calculation**: SPEI is computed from a climatic water balance (precipitation minus potential evapotranspiration, PET). PET is calculated using the **Thornthwaite method** (Thornthwaite, 1948) or similar temperature-based approach. The water balance (P − PET) is accumulated over the specified time window, and the accumulated values are fitted to a **log-logistic distribution** (Vicente-Serrano et al., 2010). The cumulative probability is then transformed to a standard normal distribution to obtain SPEI values. This approach allows SPEI to capture temperature-driven drying, as increased PET during warm periods can intensify drought even without precipitation deficits.

We analyse accumulation windows of **3 months (SPI3/SPEI3)** and **6 months (SPI6/SPEI6)**. These capture shorter-term moisture deficits and more persistent hydrological drought conditions, respectively. This distinction is increasingly important in a warming climate, where rising temperatures can intensify drought impacts even in the absence of large precipitation deficits (Dai, 2013).

### 2.4 Composite analysis
Composite drought anomalies are computed for positive and negative IOD phases by averaging drought index anomalies over the months associated with IOD events and comparing them to a climatological baseline. The climatology is calculated as the long-term mean (1980–2020) for the corresponding month or season, excluding the event years themselves to avoid circularity. For circulation composites, canonical SON IOD event years are used (Section 2.8). 

**Significance testing**: Statistical significance is assessed using a **two-tailed Student's t-test** at each grid point, comparing the composite mean (averaged across event years) to the climatological mean. The test statistic is calculated as *t* = (event_mean − climatology) / SE, where SE is the standard error of the mean (SE = event_std / √n_events, with ddof=1 for sample standard deviation). The degrees of freedom are *df* = n_events − 1. **Regions with p < 0.05 are considered statistically significant** and are indicated by stippling on composite maps. For circulation variables (e.g., MSLP), an additional practical significance threshold is applied (e.g., |anomaly| ≥ 0.5 hPa for MSLP) to filter out small but statistically significant anomalies that may not be meteorologically meaningful. No explicit multiple testing correction is applied, as the focus is on identifying coherent spatial patterns rather than individual grid-point significance.

### 2.5 ENSO-stratified composites
To evaluate state dependence, we compute composites conditional on ENSO state. A **3×3 framework** summarises drought anomalies for each combination of ENSO phase (El Niño, La Niña, Neutral) and IOD phase (positive, negative, and difference). This approach allows us to isolate the "pure" IOD signal under Neutral ENSO conditions and assess how ENSO modulates IOD–drought relationships. Where combinations have insufficient sample size (typically < 3 events), panels indicate low-data conditions rather than over-interpreting noisy composites. The stratification uses SON-averaged Niño3.4 values to classify each year's ENSO state, ensuring temporal alignment with the IOD peak season.

### 2.6 Lag and partial correlation analysis
Lag correlations are computed between DMI and drought indices across multiple lags from **−12 to +12 months** (25 total lags) to evaluate whether drought responses are concurrent, leading, or lagging relative to IOD variability. For each lag, Pearson correlation coefficients are calculated between the time-shifted DMI and drought index time series at each grid point or regional average. **Positive lags indicate DMI leading drought** (IOD forcing drought), while **negative lags indicate drought leading DMI** (interpreted cautiously as potential reverse causality or shared forcing). The analysis requires a minimum of 10 valid data pairs for each lag to ensure statistical reliability. The lag with the maximum absolute correlation is identified for each region/index combination to determine optimal lead times for prediction.

**Partial correlations** quantify the association between DMI and drought indices while controlling for ENSO (Niño3.4), providing a robustness check against ENSO confounding. The partial correlation *r*DMI,drought|ENSO is calculated as:

*r*DMI,drought|ENSO = (*r*DMI,drought − *r*DMI,ENSO × *r*drought,ENSO) / √[(1 − *r*²DMI,ENSO)(1 − *r*²drought,ENSO)]

where *r*DMI,drought, *r*DMI,ENSO, and *r*drought,ENSO are the pairwise Pearson correlations. This removes the linear influence of ENSO, allowing assessment of the independent IOD contribution to drought variability.

### 2.7 Wavelet coherence
Wavelet coherence is computed between DMI and drought indices to assess time–frequency dependence. This reveals whether coupling is persistent over the full record or concentrated in particular epochs and at particular periodicities (e.g., interannual 2–7‑year bands) (Torrence and Compo, 1998; Grinsted et al., 2004).

### 2.8 Atmospheric circulation composites (ERA5)
We use ERA5 to compute SON circulation anomalies during canonical IOD event years. Variables include:
- **MSLP (mean sea-level pressure)**: Surface pressure field indicating convergence/divergence patterns and pressure gradients
- **850‑hPa winds (u850, v850)**: Low-level horizontal wind components representing moisture transport pathways
- **500‑hPa geopotential height (z500, converted to meters)**: Mid-tropospheric height field indicating ridge/trough structures and vertical motion patterns

**Canonical IOD event years** used in the circulation composite workflow are selected based on SON-averaged DMI magnitude from HadISST data:
- **Positive IOD**: **1994, 1997, 2006, 2018, 2019** (n = 5 events)
- **Negative IOD**: **1980, 1981, 1992, 1996, 1998** (n = 5 events)

These years represent the strongest IOD events during the analysis period, ensuring robust composite signals. The selection prioritizes events with DMI magnitude > 0.5°C during SON, with the top 5 events chosen for each phase to balance signal strength and sample size.

**Composite methodology**: For each variable, SON-averaged values are extracted for each canonical event year. The climatology is calculated as the SON mean over all years in the period (1980–2020), **excluding the event years themselves** to prevent circularity. Anomalies are computed as the difference between the event-year composite mean and the climatology. The composite mean is the simple average across all events within each IOD phase (positive or negative). Statistical significance is assessed using the same t-test approach as for drought composites (Section 2.4), with p < 0.05 indicating significant anomalies.

**Visualization**: For interpretability, geopotential height anomalies and wind vectors are plotted separately, in addition to multi-variable circulation composite panels. This separation reduces visual clutter and allows clearer interpretation of each field. **Projection variants include Mercator** (suitable for equatorial and mid-latitude regions, extent: 180°W–180°E, 90°S–15°N) **and polar stereographic** (suitable for Southern Hemisphere focus, extent: 180°W–180°E, 90°S–0°N), with hemispheric extents to capture large-scale circulation patterns beyond the African continent.

ERA5 is the fifth-generation ECMWF atmospheric reanalysis, providing physically consistent fields at 0.25° × 0.25° horizontal resolution suitable for diagnosing circulation mechanisms (Hersbach et al., 2020).

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
Black, E., Slingo, J., and Sperber, K. R. (2003). An observational study of the relationship between excessively strong short rains in coastal East Africa and Indian Ocean SST. *Monthly Weather Review*, **131**, 74–94. **[VERIFY details]**

Cai, W., Santoso, A., Wang, G., et al. (2013). Projected response of the Indian Ocean Dipole to greenhouse warming. *Nature Geoscience*, **6**, 999–1007. **[VERIFY page numbers / author list]**

Dai, A. (2013). Increasing drought under global warming in observations and models. *Nature Climate Change*, **3**, 52–58.

Grinsted, A., Moore, J. C., and Jevrejeva, S. (2004). Application of the cross wavelet transform and wavelet coherence to geophysical time series. *Nonlinear Processes in Geophysics*, **11**, 561–566.

Hersbach, H., Bell, B., Berrisford, P., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, **146**, 1999–2049.

Marchant, R., Mumbi, C., Behera, S., and Yamagata, T. (2007). The Indian Ocean Dipole—the unsung driver of climatic variability in East Africa. *African Journal of Ecology*, **45**, 4–16. **[VERIFY details]**

McKee, T. B., Doesken, N. J., and Kleist, J. (1993). The relationship of drought frequency and duration to time scales. *Proceedings of the 8th Conference on Applied Climatology*, 179–184.

Saji, N. H., Goswami, B. N., Vinayachandran, P. N., and Yamagata, T. (1999). A dipole mode in the tropical Indian Ocean. *Nature*, **401**, 360–363.

Torrence, C., and Compo, G. P. (1998). A practical guide to wavelet analysis. *Bulletin of the American Meteorological Society*, **79**, 61–78.

Thornthwaite, C. W. (1948). An approach toward a rational classification of climate. *Geographical Review*, **38**, 55–94.

Trenberth, K. E. (1997). The definition of El Niño. *Bulletin of the American Meteorological Society*, **78**, 2771–2777.

Vicente-Serrano, S. M., Beguería, S., and López-Moreno, J. I. (2010). A multiscalar drought index sensitive to global warming: the Standardized Precipitation Evapotranspiration Index. *Journal of Climate*, **23**, 1696–1718.

Webster, P. J., Moore, A. M., Loschnigg, J. P., and Leben, R. R. (1999). Coupled ocean–atmosphere dynamics in the Indian Ocean during 1997–98. *Nature*, **401**, 356–360.


