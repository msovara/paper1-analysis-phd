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
### 3.1 DMI dataset characterization and strong IOD events

Before examining drought teleconnections, we first characterize the DMI time series from three datasets (HadISST, ERSST, and ERA5) to assess inter-dataset agreement and identify canonical strong IOD events used in subsequent composite analyses.

**Monthly time series comparison (1980–2020)**: The full monthly DMI time series from all three datasets (HadISST, ERSST, and ERA5) reveal strong interannual variability with generally consistent timing of major events across the 492-month record, though with notable differences in magnitude (Figure 1a). All three series exhibit sharp peaks (positive DMI events) and deep troughs (negative DMI events) throughout the period, frequently crossing the ±0.5°C IOD threshold. HadISST and ERSST DMI values track very closely, showing similar magnitudes and timing for most events, with both series frequently exceeding the positive IOD threshold and occasionally dropping below the negative threshold. The ERA5 DMI series generally follows the same timing for major events as HadISST and ERSST but shows much larger amplitude variations, particularly for negative DMI events. ERA5's troughs are consistently much deeper, often falling below −1.5°C and sometimes below −2.0°C, while HadISST and ERSST rarely drop below −1.0°C. Prominent positive DMI events (exceeding +0.5°C) appear in all three series around 1982–1983, 1986–1987, 1994, 1997–1998 (a very strong event, with ERA5 exceeding 2°C), 2002–2003, 2007, 2011, 2015, and 2019 (another very strong event, with ERA5 exceeding 2°C and HadISST/ERSST reaching above 1.5°C). ERA5 shows numerous and very strong negative events, frequently dropping below −1.5°C (e.g., early 1980s, mid-1980s, early 1990s, late 1990s, mid-2000s, early 2010s, mid-2010s), while HadISST and ERSST show less frequent and less extreme negative excursions.

**SON-averaged time series and correlations**: When focusing on the SON season (when IOD typically peaks), the correlation patterns become clearer. HadISST and ERSST SON-averaged DMI values track closely throughout the period, with correlation coefficient *r* = 0.794 (*p* < 10⁻¹⁰⁸), indicating excellent agreement on both the timing and magnitude of IOD variability (Figure 1d). In contrast, correlations involving ERA5 are weaker but still highly significant: HadISST vs ERA5 (*r* = 0.572, *p* < 10⁻⁴⁴) and ERSST vs ERA5 (*r* = 0.580, *p* < 10⁻⁴⁵). The scatter plot relationships (Figure 1d) confirm these correlation patterns, with HadISST–ERSST showing tight clustering around the 1:1 line, while ERA5 comparisons show greater scatter and systematic biases.

**Distribution characteristics**: Box plot analysis reveals systematic differences in DMI distributions across datasets (Figure 1b). HadISST DMI has a median near zero (−0.05°C) with an interquartile range (IQR) from approximately −0.2°C to 0.05°C, and whiskers extending from −0.7°C to 0.7°C. ERSST DMI shows a similar distribution with median at 0.0°C, IQR from −0.1°C to 0.2°C, and whiskers from −0.5°C to 0.7°C. ERA5 DMI exhibits a notably different distribution with a more negative median (−0.4°C), wider IQR (−0.8°C to −0.05°C), and much broader whiskers extending from approximately −2.2°C to 1.2°C. These differences reflect the reanalysis nature of ERA5, which may capture more extreme variability or incorporate different observational constraints compared to the observational SST products. Monthly box plots for HadISST (Figure 1c) show that DMI variability is relatively uniform across months, with medians near zero and similar IQRs, though some months (e.g., September–November) show slightly wider distributions consistent with IOD peak seasonality.

**Strong IOD events**: The top 5 positive IOD events identified from SON-averaged HadISST DMI are 1994, 1997, 2006, 2018, and 2019 (Figure 2a). The top 5 negative events are 1980, 1981, 1992, 1996, and 1998 (Figure 2b). These canonical events are used for circulation composite analysis (Section 3.8). Comparison across datasets reveals important inter-dataset differences in event magnitude. For positive events, ERA5 consistently shows higher DMI values than HadISST and ERSST, particularly in 1994 (ERA5 ~1.2°C vs HadISST ~0.5°C) and 1997 (ERA5 ~1.7°C vs HadISST ~1.0°C). ERSST often shows the weakest positive signals, with some events (1994, 2006, 2018) falling below the +0.5°C threshold or even negative. For negative events, ERA5 again shows stronger (more negative) values, particularly in 1996 (ERA5 ~−1.2°C vs HadISST ~−0.7°C) and 1992 (ERA5 ~−0.8°C vs HadISST ~−0.6°C). ERSST shows the weakest negative signals, with some events (1980, 1981, 1992) barely exceeding the −0.5°C threshold.

**Inter-dataset scatter relationships**: Scatter plots comparing strong events across datasets (Figure 2c–d) reveal systematic biases. HadISST vs ERSST comparisons show that for positive events, ERSST values are generally lower than HadISST (points below the 1:1 line), while for negative events, ERSST values are less negative than HadISST (points above the 1:1 line). In contrast, HadISST vs ERA5 comparisons show the opposite pattern: ERA5 values are generally higher than HadISST for positive events (points above the 1:1 line) and more negative for negative events (points below the 1:1 line). These biases are consistent with ERA5's tendency to amplify IOD extremes, which may reflect the reanalysis's incorporation of atmospheric observations that respond to SST gradients, or differences in how SST anomalies are represented in reanalysis versus observational products.

**Implications for analysis**: The inter-dataset differences highlight the importance of dataset choice in IOD studies. HadISST serves as the reference dataset for event identification in this study, as it is widely used in IOD research and shows good agreement with ERSST. ERA5's stronger amplitude variations may provide enhanced signal-to-noise for circulation composites, but may also introduce artifacts if the reanalysis over-amplifies extremes. The consistent timing of events across all three datasets provides confidence that the identified canonical years represent genuine IOD variability rather than dataset-specific artifacts.

**Figure 1:** DMI dataset comparison and characterization  
(a) Monthly DMI time series (1980–2020) from HadISST (blue), ERSST (red), and ERA5 (green), with ±0.5°C thresholds (dashed lines), showing the full 492-month record with prominent positive and negative events. (b) Box plots comparing DMI distributions across datasets (all monthly values). (c) Monthly box plots for HadISST DMI showing seasonal variability. (d) Scatter plots with correlation coefficients for SON-averaged values: HadISST vs ERSST (*r* = 0.794, *p* < 10⁻¹⁰⁸), HadISST vs ERA5 (*r* = 0.572, *p* < 10⁻⁴⁴), and ERSST vs ERA5 (*r* = 0.580, *p* < 10⁻⁴⁵).  
`dmi_timeseries_comparison.png`, `dmi_box_plots.png`, `dmi_single_panel_normalized_comparison.png` or correlation scatter plots

**Figure 2:** Strong IOD events analysis  
(a) Top 5 positive IOD events (1994, 1997, 2006, 2018, 2019) compared across datasets. (b) Top 5 negative IOD events (1980, 1981, 1992, 1996, 1998) compared across datasets. (c) Scatter plot: HadISST vs ERSST for strong events. (d) Scatter plot: HadISST vs ERA5 for strong events.  
`dmi_son_events_analysis.png`, `dmi_multipanel_normalized_comparison.png`

### 3.2 Drought composites by IOD phase

Composite drought maps reveal spatially heterogeneous responses across Africa that vary systematically by index type (SPI vs SPEI) and accumulation window (3 vs 6 months). The following subsections provide detailed annotations for each drought index, highlighting both commonalities and distinctions in how IOD phases manifest across different drought metrics.

#### 3.2.1 SPI3 (3-month Standardized Precipitation Index)

SPI3 composites capture short-term precipitation anomalies, reflecting moisture deficits that develop over a 3-month accumulation period. Each composite figure (Figure 3a) contains four panels: (1) positive IOD composite showing average SPI3 anomalies during positive IOD events, (2) negative IOD composite showing average SPI3 anomalies during negative IOD events, (3) difference map (positive minus negative IOD) highlighting regions where IOD phase has the strongest differential impact, and (4) regional averages bar chart comparing the five African regions.

**Positive IOD composite:** During positive IOD events, SPI3 shows spatially heterogeneous patterns with generally wetter-than-normal conditions across most of Africa, except Southern Africa which experiences drier conditions. The spatial pattern reveals enhanced precipitation in East Africa, West Africa, Central Africa, and particularly North Africa, with statistically significant anomalies (p < 0.05, indicated by stippling) covering approximately **16.3%** of grid points. Regional averages from the bar chart indicate: **East Africa +0.574**, **Southern Africa −0.182**, **West Africa +0.487**, **Central Africa +0.278**, and **North Africa +0.869**. The strongest wet signals (positive SPI3 values > +0.5) appear in North Africa, East Africa, and West Africa, indicating enhanced precipitation during positive IOD events. In contrast, Southern Africa shows moderate drought conditions (SPI3 = −0.182), suggesting reduced precipitation in this region during positive IOD phases.

**Negative IOD composite:** Negative IOD events are associated with generally weaker and more spatially variable patterns relative to positive IOD conditions. Statistically significant anomalies cover approximately **12.6%** of grid points, indicating a somewhat weaker signal than positive IOD events. Regional averages indicate: **East Africa +0.163**, **Southern Africa +0.109**, **West Africa +0.191**, **Central Africa +0.474**, and **North Africa −0.152**. Notably, Central Africa shows the strongest positive anomaly (+0.474) during negative IOD events, while North Africa experiences slight drought conditions (SPI3 = −0.152). The difference map (positive minus negative) reveals that North Africa shows the largest differential response (+1.021), indicating strong asymmetry between positive and negative IOD effects, with positive IOD events bringing substantially more precipitation to this region. East Africa also shows a notable difference (+0.411), while Central Africa shows an opposite pattern, with negative IOD events associated with wetter conditions than positive IOD events.

**Key features:**
- Captures short-term (3-month) precipitation deficits
- Most sensitive to seasonal rainfall variations
- Strongest signals in regions with direct Indian Ocean moisture influence
- Anomalies can develop and decay relatively quickly

#### 3.2.2 SPI6 (6-month Standardized Precipitation Index)

SPI6 composites integrate precipitation anomalies over a 6-month accumulation period, providing a measure of more persistent hydrological drought conditions. Compared to SPI3, SPI6 anomalies typically show similar spatial patterns but with slightly enhanced magnitudes in most regions, reflecting the cumulative nature of the 6-month accumulation window. The longer accumulation window means SPI6 reflects cumulative moisture deficits that may persist beyond the immediate IOD forcing period, incorporating lagged responses and soil moisture memory effects. During positive IOD events, SPI6 shows regional averages of: **East Africa +0.668**, **Southern Africa −0.135**, **West Africa +0.374**, **Central Africa +0.249**, and **North Africa +0.878**. Statistically significant anomalies cover approximately **16.1%** of grid points. The 6-month integration means these anomalies may extend beyond the SON season, capturing both direct IOD forcing and subsequent persistence. Notably, East Africa shows a stronger positive signal in SPI6 (+0.668) compared to SPI3 (+0.574), suggesting that positive IOD impacts accumulate over the longer time window. North Africa maintains the strongest positive anomaly (+0.878), similar to SPI3, indicating consistent enhancement of precipitation during positive IOD events. Negative IOD events are associated with regional averages of: **East Africa +0.298**, **Southern Africa −0.165**, **West Africa +0.329**, **Central Africa +0.609**, and **North Africa −0.070**. Statistically significant anomalies cover approximately **11.2%** of grid points. Central Africa shows the strongest positive anomaly (+0.609) during negative IOD events, even stronger than in SPI3, suggesting that negative IOD impacts on Central Africa precipitation accumulate over the 6-month window. The persistence of SPI6 anomalies relative to SPI3 suggests that some IOD-related drought impacts accumulate over time, with the longer window capturing both direct forcing and subsequent persistence mechanisms.

**Key features:**
- Captures medium-term (6-month) precipitation deficits
- Reflects cumulative and persistent hydrological drought
- Incorporates lagged responses and soil moisture memory
- Anomalies may persist beyond immediate IOD forcing period

#### 3.2.3 SPEI3 (3-month Standardized Precipitation Evapotranspiration Index)

SPEI3 composites incorporate both precipitation and evaporative demand, making this index sensitive to temperature-driven drying in addition to precipitation deficits. During positive IOD events, SPEI3 shows regional averages of: **East Africa +0.391**, **Southern Africa −0.293**, **West Africa +0.435**, **Central Africa +0.259**, and **North Africa +0.648**. Statistically significant anomalies cover approximately **6.2%** of grid points, notably lower than SPI3 (16.3%), suggesting that evaporative demand effects may reduce the spatial coherence of the signal. Notable differences from SPI3 appear in several regions: East Africa shows weaker positive anomalies in SPEI3 (+0.391) compared to SPI3 (+0.574), suggesting that increased evaporative demand partially offsets precipitation gains. Southern Africa shows stronger drought conditions in SPEI3 (−0.293) compared to SPI3 (−0.182), indicating that evaporative demand amplifies the precipitation deficit in this region. West Africa shows similar values between SPEI3 (+0.435) and SPI3 (+0.487), suggesting that precipitation effects dominate. North Africa shows weaker positive anomalies in SPEI3 (+0.648) compared to SPI3 (+0.869), indicating that evaporative demand reduces the net water balance benefit despite enhanced precipitation. In semi-arid and arid zones, SPEI3 anomalies are often weaker than SPI3, reflecting the additional contribution of atmospheric evaporative demand that partially offsets precipitation gains. The 3-month accumulation window means SPEI3 captures short-term water balance anomalies, where increased temperature and evaporative demand during IOD events can intensify drought even in the absence of large precipitation deficits. During negative IOD events, SPEI3 shows regional averages of: **East Africa +0.320**, **Southern Africa +0.234**, **West Africa +0.278**, **Central Africa +0.546**, and **North Africa +0.091**. Statistically significant anomalies cover approximately **13.0%** of grid points, higher than for positive IOD events. Patterns differ from SPI3 in several regions: Southern Africa shows positive anomalies in SPEI3 (+0.234) compared to slightly positive in SPI3 (+0.109), suggesting that reduced evaporative demand during negative IOD events enhances water availability. Central Africa shows similar strong positive anomalies in both indices, indicating that precipitation effects dominate. North Africa shows positive anomalies in SPEI3 (+0.091) compared to negative in SPI3 (−0.152), suggesting that reduced evaporative demand during negative IOD events improves water balance despite reduced precipitation.

**Key features:**
- Captures short-term (3-month) water balance (precipitation minus PET)
- Sensitive to both precipitation deficits and temperature-driven evaporative demand
- Shows enhanced drying in semi-arid/arid regions relative to SPI3
- Reflects combined effects of rainfall anomalies and atmospheric moisture demand

#### 3.2.4 SPEI6 (6-month Standardized Precipitation Evapotranspiration Index)

SPEI6 composites integrate water balance anomalies over a 6-month period, providing the most comprehensive measure of persistent drought conditions that account for both precipitation and evaporative demand. Compared to SPEI3, SPEI6 shows generally stronger positive anomalies in most regions, reflecting the cumulative nature of the 6-month accumulation window. The 6-month accumulation window means SPEI6 captures cumulative water balance deficits that incorporate both precipitation anomalies and sustained periods of elevated evaporative demand. During positive IOD events, SPEI6 shows regional averages of: **East Africa +0.524**, **Southern Africa −0.247**, **West Africa +0.354**, **Central Africa +0.234**, and **North Africa +0.579**. Statistically significant anomalies cover approximately **8.4%** of grid points. The anomalies reflect the combined effects of precipitation and evaporative demand over extended periods. Compared to SPI6, SPEI6 shows weaker positive anomalies in all regions except Southern Africa (where both show negative values), indicating that cumulative evaporative demand partially offsets precipitation gains over the 6-month window. East Africa shows stronger positive anomalies in SPEI6 (+0.524) compared to SPEI3 (+0.391), suggesting that positive IOD impacts accumulate over time. Southern Africa shows persistent drought conditions (−0.247), similar to SPEI3, indicating sustained water deficits. Negative IOD events are associated with regional averages of: **East Africa +0.423**, **Southern Africa −0.020**, **West Africa +0.456**, **Central Africa +0.696**, and **North Africa +0.190**. Statistically significant anomalies cover approximately **13.0%** of grid points. Central Africa shows the strongest positive anomaly (+0.696), even stronger than in SPEI3, suggesting that negative IOD impacts on Central Africa water balance accumulate substantially over the 6-month window. Southern Africa shows near-neutral conditions (−0.020) in SPEI6 compared to positive in SPEI3 (+0.234), suggesting that cumulative effects differ from short-term responses. Differences between SPEI6 and SPI6 are most pronounced in regions where temperature anomalies and evaporative demand contribute substantially to drought development. SPEI6 shows weaker positive anomalies than SPI6 in East Africa, West Africa, Central Africa, and North Africa during positive IOD events, indicating that cumulative evaporative demand reduces net water balance benefits. During negative IOD events, SPEI6 shows stronger positive anomalies than SPI6 in Central Africa (+0.696 vs +0.609) and West Africa (+0.456 vs +0.329), suggesting that reduced evaporative demand enhances water availability beyond precipitation effects alone.

**Key features:**
- Captures medium-term (6-month) water balance deficits
- Most comprehensive drought metric (precipitation and PET)
- Reflects cumulative effects of both rainfall and evaporative demand
- Shows strongest divergence from SPI6 in regions with high evaporative demand

#### 3.2.5 Cross-index comparisons and synthesis

**SPI3 vs SPI6:** The comparison reveals that SPI6 generally shows stronger positive anomalies than SPI3 during positive IOD events in East Africa (+0.668 vs +0.574) and North Africa (+0.878 vs +0.869), while showing similar or slightly weaker signals in other regions. During negative IOD events, SPI6 shows stronger positive anomalies than SPI3 in East Africa (+0.298 vs +0.163), West Africa (+0.329 vs +0.191), and particularly Central Africa (+0.609 vs +0.474). SPI3 captures more immediate, short-lived responses to IOD forcing, while SPI6 shows more persistent anomalies that may reflect cumulative effects and soil moisture memory. The enhanced signals in SPI6 for Central Africa during negative IOD events suggest that precipitation impacts accumulate substantially over the 6-month window, indicating persistent hydrological responses.

**SPEI3 vs SPEI6:** Similar to the SPI comparison, SPEI6 shows generally stronger positive anomalies than SPEI3 during both positive and negative IOD events in most regions. During positive IOD events, SPEI6 shows stronger signals in East Africa (+0.524 vs +0.391), West Africa (+0.354 vs +0.435, though West Africa is an exception), and North Africa (+0.579 vs +0.648, though North Africa is an exception). During negative IOD events, SPEI6 shows substantially stronger signals in Central Africa (+0.696 vs +0.546) and West Africa (+0.456 vs +0.278). The comparison highlights how temperature-driven evaporative demand effects accumulate over time, with SPEI6 often showing stronger anomalies than SPEI3 in regions where cumulative water balance effects are important.

**SPI vs SPEI (3-month):** Differences between SPI3 and SPEI3 are most pronounced in East Africa, Southern Africa, and North Africa during positive IOD events, where evaporative demand contributes substantially to drought development. In East Africa, SPEI3 shows weaker positive anomalies (+0.391) than SPI3 (+0.574), reflecting that increased evaporative demand partially offsets precipitation gains. In Southern Africa, SPEI3 shows stronger drought conditions (−0.293) than SPI3 (−0.182), indicating that evaporative demand amplifies precipitation deficits. In North Africa, SPEI3 shows weaker positive anomalies (+0.648) than SPI3 (+0.869), suggesting that evaporative demand reduces net water balance benefits despite enhanced precipitation. West Africa and Central Africa show similar values between SPI3 and SPEI3, suggesting that precipitation effects dominate drought development in these regions, with minimal contribution from evaporative demand.

**SPI vs SPEI (6-month):** The comparison between SPI6 and SPEI6 reveals systematic differences, with SPEI6 showing weaker positive anomalies than SPI6 during positive IOD events in all regions except Southern Africa (where both show negative values). This pattern indicates that cumulative evaporative demand over the 6-month window reduces net water balance benefits relative to precipitation alone. During positive IOD events, the differences are: East Africa (SPEI6 +0.524 vs SPI6 +0.668), West Africa (SPEI6 +0.354 vs SPI6 +0.374), Central Africa (SPEI6 +0.234 vs SPI6 +0.249), and North Africa (SPEI6 +0.579 vs SPI6 +0.878). During negative IOD events, SPEI6 shows stronger positive anomalies than SPI6 in Central Africa (+0.696 vs +0.609) and West Africa (+0.456 vs +0.329), suggesting that reduced evaporative demand during negative IOD events enhances water availability beyond precipitation effects alone. The 6-month accumulation window means that temperature anomalies and elevated PET can have substantial cumulative effects, leading to weaker SPEI6 anomalies relative to SPI6 in most regions during positive IOD events, but stronger anomalies in some regions during negative IOD events.

**Spatial heterogeneity:** Across Africa, the drought response exhibits spatial heterogeneity consistent with differing moisture source regions, topographic effects, and regional circulation regimes. In areas directly influenced by Indian Ocean moisture transport (e.g., East Africa), IOD-related anomalies appear most directly during seasons aligned with IOD peak activity (SON), with positive IOD events bringing enhanced precipitation (SPI3: +0.574, SPI6: +0.668) and negative IOD events showing weaker positive anomalies (SPI3: +0.163, SPI6: +0.298). North Africa shows the strongest positive response to positive IOD events (SPI3: +0.869, SPI6: +0.878), suggesting strong teleconnections, while showing slight drought conditions during negative IOD events (SPI3: −0.152, SPI6: −0.070). Southern Africa shows an opposite pattern, with drought conditions during positive IOD events (SPI3: −0.182, SPI6: −0.135) and near-neutral to slightly positive conditions during negative IOD events (SPI3: +0.109, SPI6: −0.165), indicating complex regional responses. Central Africa shows particularly strong positive responses to negative IOD events (SPI3: +0.474, SPI6: +0.609), suggesting that negative IOD phases enhance precipitation in this region. West Africa shows moderate positive responses to both IOD phases, with stronger signals during positive IOD events. These patterns reflect the indirect nature of teleconnections in some regions and the dominance of other climate modes, while direct Indian Ocean influences are most apparent in East Africa and North Africa.

**Figure 3:** Composite drought anomalies during IOD phases  
(a) SPI3 composites for positive and negative IOD phases. (b) SPI6 composites for positive and negative IOD phases. (c) SPEI3 composites for positive and negative IOD phases. (d) SPEI6 composites for positive and negative IOD phases.  
`composite_drought_SPI3.png`, `composite_drought_SPI6.png`, `composite_drought_SPEI3.png`, `composite_drought_SPEI6.png`

### 3.3 ENSO modulation of IOD–drought relationships

ENSO-stratified composites reveal that IOD–drought relationships are strongly modulated by background ENSO conditions, with both synergistic and competing effects depending on the phase combination. The analysis uses a **3×3 framework** (Figure 4) showing drought composites for each combination of ENSO state (El Niño, La Niña, Neutral) and IOD phase (positive, negative, and their difference). This stratification isolates the "pure" IOD signal under Neutral ENSO conditions and demonstrates how ENSO modifies IOD–drought teleconnections through shared Indo-Pacific circulation pathways.

#### 3.3.1 SPI3 ENSO-stratified composites

The SPI3 ENSO-stratified composites (Figure 4a) reveal distinct patterns for each ENSO×IOD combination, highlighting how background ENSO state alters IOD-related precipitation anomalies.

**El Niño conditions:**
- **Positive IOD + El Niño**: This combination represents a synergistic coupling where both modes enhance Indo-Pacific convection anomalies. The composite shows [**INSERT SPECIFIC PATTERNS**], with enhanced drought conditions in Southern Africa and [**other regions**], while East Africa and North Africa may show [**wetter/drier**] conditions. The synergistic effect amplifies the IOD signal, resulting in stronger anomalies than positive IOD alone. Statistically significant regions (p < 0.05, indicated by stippling) cover approximately [**X%**] of grid points.
- **Negative IOD + El Niño**: This combination shows competing influences, as negative IOD typically enhances eastern Indian Ocean convection while El Niño suppresses it. The composite reveals [**INSERT SPECIFIC PATTERNS**], with generally [**weaker/more variable**] signals compared to negative IOD under Neutral conditions. Some regions may show cancellation effects, while others may show enhanced anomalies where both modes act in concert.
- **Difference (Positive − Negative IOD) during El Niño**: The difference map highlights regions where positive and negative IOD phases have the strongest differential impact under El Niño conditions. Values range from [**min**] to [**max**], with the largest differences typically appearing in [**specific regions**], indicating strong IOD phase dependence even when ENSO is active.

**La Niña conditions:**
- **Positive IOD + La Niña**: This combination shows competing influences, as positive IOD enhances western Indian Ocean convection while La Niña enhances eastern Pacific convection, potentially creating complex circulation patterns. The composite shows [**INSERT SPECIFIC PATTERNS**], with generally [**weaker/stronger**] signals compared to positive IOD under Neutral conditions. Some regions may show cancellation, while others may show enhanced anomalies where both modes reinforce each other.
- **Negative IOD + La Niña**: This combination represents another synergistic coupling, as both modes enhance eastern Indian Ocean and western Pacific convection. The composite reveals [**INSERT SPECIFIC PATTERNS**], with enhanced wet conditions in [**specific regions**] and drought conditions in [**other regions**]. The synergistic effect amplifies the negative IOD signal, resulting in stronger anomalies than negative IOD alone.
- **Difference (Positive − Negative IOD) during La Niña**: The difference map shows [**INSERT SPECIFIC PATTERNS**], with values ranging from [**min**] to [**max**]. The pattern may differ from the El Niño difference map, reflecting how La Niña modifies the IOD phase dependence.

**Neutral ENSO conditions:**
- **Positive IOD + Neutral**: Under Neutral ENSO conditions, the "pure" IOD signal is most clearly visible, as there is minimal interference from ENSO-related circulation anomalies. The composite shows [**INSERT SPECIFIC PATTERNS**], which should align closely with the overall positive IOD composite from Section 3.2.1. Regional patterns include [**East Africa: wetter conditions, Southern Africa: drier conditions, etc.**], with statistically significant anomalies covering approximately [**X%**] of grid points.
- **Negative IOD + Neutral**: Similarly, this composite shows the clearest expression of negative IOD impacts without ENSO interference. The pattern reveals [**INSERT SPECIFIC PATTERNS**], with enhanced precipitation in [**specific regions**] and reduced precipitation in [**other regions**]. This should align with the overall negative IOD composite from Section 3.2.1.
- **Difference (Positive − Negative IOD) during Neutral**: The difference map under Neutral conditions provides the cleanest measure of IOD phase dependence, showing values ranging from [**min**] to [**max**]. The largest differences appear in [**specific regions**], indicating where IOD phase has the strongest independent influence on African drought.

**Cross-ENSO comparisons:** Comparing the same IOD phase across different ENSO states reveals systematic modulation. Positive IOD composites are typically [**stronger/weaker**] during El Niño compared to Neutral, and [**stronger/weaker**] during La Niña compared to Neutral, reflecting the synergistic and competing influences described above. Negative IOD composites show [**similar/different**] patterns of ENSO modulation. The Neutral ENSO composites provide the baseline for assessing ENSO's modifying influence.

#### 3.3.2 SPI6 ENSO-stratified composites

The SPI6 ENSO-stratified composites (Figure 4b) show similar ENSO×IOD interactions as SPI3, but with generally [**stronger/weaker/more persistent**] signals due to the 6-month accumulation window. The longer time scale means that SPI6 composites capture cumulative effects that may extend beyond the immediate SON forcing period, incorporating lagged responses and soil moisture memory.

**El Niño conditions:**
- **Positive IOD + El Niño**: The SPI6 composite shows [**INSERT COMPARISON WITH SPI3**], with [**stronger/weaker/more persistent**] anomalies in [**specific regions**]. The 6-month accumulation means that synergistic effects between positive IOD and El Niño may accumulate over time, resulting in [**enhanced/reduced**] signals compared to SPI3.
- **Negative IOD + El Niño**: The SPI6 composite reveals [**INSERT COMPARISON WITH SPI3**], showing how competing influences between negative IOD and El Niño manifest over the longer accumulation window.
- **Difference during El Niño**: The SPI6 difference map shows [**INSERT COMPARISON WITH SPI3**], with values ranging from [**min**] to [**max**].

**La Niña conditions:**
- **Positive IOD + La Niña**: The SPI6 composite shows [**INSERT COMPARISON WITH SPI3**], reflecting how competing influences evolve over the 6-month window.
- **Negative IOD + La Niña**: The SPI6 composite reveals [**INSERT COMPARISON WITH SPI3**], showing how synergistic effects between negative IOD and La Niña accumulate over time.
- **Difference during La Niña**: The SPI6 difference map shows [**INSERT COMPARISON WITH SPI3**].

**Neutral ENSO conditions:**
- **Positive IOD + Neutral**: The SPI6 composite under Neutral conditions shows the clearest expression of positive IOD impacts, with patterns that should align with the overall positive IOD SPI6 composite from Section 3.2.2. The 6-month accumulation means that IOD-related precipitation anomalies may persist beyond SON, with regional averages showing [**INSERT COMPARISON WITH SPI3**].
- **Negative IOD + Neutral**: Similarly, the SPI6 composite shows clear negative IOD impacts, with patterns aligning with the overall negative IOD SPI6 composite.
- **Difference during Neutral**: The SPI6 difference map provides the cleanest measure of IOD phase dependence, with values ranging from [**min**] to [**max**].

**SPI3 vs SPI6 under different ENSO states:** Comparing SPI3 and SPI6 composites for the same ENSO×IOD combination reveals how accumulation windows affect the expression of ENSO modulation. In general, SPI6 shows [**stronger/weaker**] signals than SPI3 during [**El Niño/La Niña/Neutral**] conditions, reflecting cumulative effects over the longer time window.

#### 3.3.3 SPEI3 ENSO-stratified composites

The SPEI3 ENSO-stratified composites (Figure 4c) incorporate evaporative demand effects in addition to precipitation, revealing how ENSO×IOD interactions affect water balance anomalies. Differences from SPI3 composites are most pronounced in regions where temperature and evaporative demand contribute substantially to drought development.

**El Niño conditions:**
- **Positive IOD + El Niño**: The SPEI3 composite shows [**INSERT COMPARISON WITH SPI3**], with evaporative demand effects [**amplifying/reducing**] the precipitation anomalies. In regions where El Niño is associated with elevated temperatures, SPEI3 may show [**stronger/weaker**] drought conditions than SPI3, reflecting the additional contribution of increased evaporative demand. The composite reveals [**INSERT SPECIFIC REGIONAL PATTERNS**], with statistically significant anomalies covering approximately [**X%**] of grid points.
- **Negative IOD + El Niño**: The SPEI3 composite shows [**INSERT COMPARISON WITH SPI3**], with evaporative demand effects [**amplifying/reducing**] the competing influences between negative IOD and El Niño.
- **Difference during El Niño**: The SPEI3 difference map shows [**INSERT COMPARISON WITH SPI3**], with values ranging from [**min**] to [**max**].

**La Niña conditions:**
- **Positive IOD + La Niña**: The SPEI3 composite shows [**INSERT COMPARISON WITH SPI3**], with evaporative demand effects [**amplifying/reducing**] the competing influences. In regions where La Niña is associated with cooler temperatures, reduced evaporative demand may [**enhance/reduce**] water balance benefits from precipitation anomalies.
- **Negative IOD + La Niña**: The SPEI3 composite reveals [**INSERT COMPARISON WITH SPI3**], showing how synergistic effects between negative IOD and La Niña manifest in water balance terms, incorporating both precipitation and evaporative demand.
- **Difference during La Niña**: The SPEI3 difference map shows [**INSERT COMPARISON WITH SPI3**].

**Neutral ENSO conditions:**
- **Positive IOD + Neutral**: The SPEI3 composite under Neutral conditions shows the clearest expression of positive IOD impacts on water balance, with patterns that should align with the overall positive IOD SPEI3 composite from Section 3.2.3. Evaporative demand effects may [**reduce**] the net water balance benefits compared to SPI3, particularly in [**specific regions**].
- **Negative IOD + Neutral**: Similarly, the SPEI3 composite shows clear negative IOD impacts on water balance, with patterns aligning with the overall negative IOD SPEI3 composite.
- **Difference during Neutral**: The SPEI3 difference map provides the cleanest measure of IOD phase dependence in water balance terms, with values ranging from [**min**] to [**max**].

**SPI3 vs SPEI3 under different ENSO states:** Comparing SPI3 and SPEI3 composites for the same ENSO×IOD combination reveals how evaporative demand modifies ENSO×IOD interactions. In general, SPEI3 shows [**stronger/weaker**] drought conditions than SPI3 during [**El Niño/La Niña**] conditions in [**specific regions**], reflecting temperature-driven evaporative demand effects. Under Neutral conditions, differences between SPI3 and SPEI3 are typically [**smaller/larger**], as there is less ENSO-related temperature influence.

#### 3.3.4 SPEI6 ENSO-stratified composites

The SPEI6 ENSO-stratified composites (Figure 4d) integrate water balance anomalies over a 6-month period, providing the most comprehensive measure of how ENSO×IOD interactions affect persistent drought conditions. The longer accumulation window means that both precipitation and evaporative demand effects accumulate over time, resulting in [**stronger/weaker/more persistent**] signals compared to SPEI3.

**El Niño conditions:**
- **Positive IOD + El Niño**: The SPEI6 composite shows [**INSERT COMPARISON WITH SPEI3**], with cumulative effects of both precipitation deficits and elevated evaporative demand over the 6-month window. The composite reveals [**INSERT SPECIFIC REGIONAL PATTERNS**], with anomalies that may persist beyond the immediate SON forcing period.
- **Negative IOD + El Niño**: The SPEI6 composite shows [**INSERT COMPARISON WITH SPEI3**], reflecting how competing influences between negative IOD and El Niño accumulate over time in water balance terms.
- **Difference during El Niño**: The SPEI6 difference map shows [**INSERT COMPARISON WITH SPEI3**], with values ranging from [**min**] to [**max**].

**La Niña conditions:**
- **Positive IOD + La Niña**: The SPEI6 composite shows [**INSERT COMPARISON WITH SPEI3**], with cumulative effects of competing influences over the 6-month window.
- **Negative IOD + La Niña**: The SPEI6 composite reveals [**INSERT COMPARISON WITH SPEI3**], showing how synergistic effects between negative IOD and La Niña accumulate over time, incorporating both precipitation and reduced evaporative demand benefits.
- **Difference during La Niña**: The SPEI6 difference map shows [**INSERT COMPARISON WITH SPEI3**].

**Neutral ENSO conditions:**
- **Positive IOD + Neutral**: The SPEI6 composite under Neutral conditions shows the clearest expression of positive IOD impacts on cumulative water balance, with patterns that should align with the overall positive IOD SPEI6 composite from Section 3.2.4. The 6-month accumulation means that both precipitation and evaporative demand effects accumulate, with regional averages showing [**INSERT COMPARISON WITH SPEI3**].
- **Negative IOD + Neutral**: Similarly, the SPEI6 composite shows clear negative IOD impacts on cumulative water balance, with patterns aligning with the overall negative IOD SPEI6 composite.
- **Difference during Neutral**: The SPEI6 difference map provides the cleanest measure of IOD phase dependence in cumulative water balance terms, with values ranging from [**min**] to [**max**].

**SPEI3 vs SPEI6 under different ENSO states:** Comparing SPEI3 and SPEI6 composites for the same ENSO×IOD combination reveals how accumulation windows affect the expression of ENSO×IOD interactions in water balance terms. In general, SPEI6 shows [**stronger/weaker**] signals than SPEI3 during [**El Niño/La Niña/Neutral**] conditions, reflecting cumulative effects over the longer time window.

#### 3.3.5 Synthesis and cross-index comparisons

**ENSO modulation patterns:** Across all indices, several consistent patterns emerge regarding ENSO modulation of IOD–drought relationships:

1. **Synergistic effects**: When IOD and ENSO phases align (e.g., positive IOD + El Niño, negative IOD + La Niña), their combined influence typically [**amplifies**] drought anomalies, resulting in [**stronger**] signals than IOD alone. This reflects shared Indo-Pacific circulation pathways where both modes reinforce convection anomalies.

2. **Competing effects**: When IOD and ENSO phases oppose (e.g., positive IOD + La Niña, negative IOD + El Niño), their influences may [**partially cancel**], resulting in [**weaker/more variable**] signals than IOD alone. However, cancellation is not uniform across regions, and some areas may still show strong anomalies where one mode dominates.

3. **Neutral ENSO baseline**: Under Neutral ENSO conditions, the "pure" IOD signal is most clearly visible, providing a baseline for assessing ENSO's modifying influence. Composites under Neutral conditions should align closely with the overall IOD composites from Section 3.2, confirming that the stratification methodology is consistent.

**Index-specific ENSO modulation:**
- **SPI indices**: ENSO modulation primarily affects precipitation anomalies, with El Niño and La Niña modifying IOD-related rainfall patterns through changes in Indo-Pacific convection and the Walker circulation.
- **SPEI indices**: ENSO modulation affects both precipitation and evaporative demand. El Niño conditions, often associated with elevated temperatures, may amplify drought conditions in SPEI relative to SPI, while La Niña conditions, often associated with cooler temperatures, may enhance water balance benefits.

**Accumulation window effects:** Comparing 3-month and 6-month indices under the same ENSO×IOD combination reveals how accumulation windows affect ENSO modulation. In general, 6-month indices show [**stronger/more persistent**] signals, as cumulative effects accumulate over the longer time window. However, the pattern of ENSO modulation (synergistic vs. competing) is generally consistent across accumulation windows.

**Regional heterogeneity:** ENSO modulation of IOD–drought relationships exhibits spatial heterogeneity across Africa. Regions directly influenced by Indian Ocean moisture transport (e.g., East Africa) may show [**stronger/weaker**] ENSO modulation than regions with more indirect teleconnections (e.g., West Africa, Central Africa). This heterogeneity reflects differences in moisture source regions, regional circulation regimes, and the pathways by which ENSO×IOD interactions project onto African hydroclimate.

**Implications for forecasting:** The ENSO-stratified results have important implications for operational drought forecasting. When both IOD and ENSO states are known (e.g., from seasonal climate models), forecasters can use the appropriate ENSO×IOD combination to provide more accurate drought outlooks. The results indicate that IOD impacts cannot be interpreted independently of ENSO state, and forecast systems should consider both modes jointly rather than treating DMI as an isolated predictor.

**Figure 4:** ENSO-stratified drought composites  
(a) SPI3 ENSO-stratified composites showing 3×3 grid (El Niño, La Niña, Neutral × Positive IOD, Negative IOD, Difference). (b) SPI6 ENSO-stratified composites with 6-month accumulation. (c) SPEI3 ENSO-stratified composites incorporating evaporative demand. (d) SPEI6 ENSO-stratified composites with cumulative water balance effects.  
`enso_stratified_composite_SPI3.png`, `enso_stratified_composite_SPI6.png`, `enso_stratified_composite_SPEI3.png`, `enso_stratified_composite_SPEI6.png`

### 3.4 Timing of associations (lag correlations)
Lag correlation analysis indicates that IOD–drought coupling occurs with variable timing across regions and indices. Regions showing peak correlations near zero lag are consistent with concurrent IOD forcing during SON, whereas positive lags (DMI leading drought) suggest delayed hydroclimate impacts consistent with soil-moisture memory, delayed seasonal rainfall responses, or persistence in evaporative demand anomalies (particularly for SPEI). Negative-lag peaks are interpreted cautiously as potential signatures of shared forcing or chance alignment.

**Figure 5:** Lag correlations between DMI and drought indices  
`lag_correlation_analysis.png`

### 3.5 Robustness controlling for ENSO (partial correlations)
Partial correlation patterns indicate which drought teleconnections remain after removing ENSO variability. Where partial correlations remain strong and spatially coherent, the results support an independent IOD association; where partial correlations weaken substantially relative to simple correlations, the apparent IOD signal may reflect ENSO co-variability. This diagnostic provides a stronger basis for causal interpretation than correlations alone, particularly in regions where ENSO and IOD frequently co-occur.

**Figure 6:** Partial correlation maps (IOD controlling for ENSO)  
`partial_correlation_analysis.png`

### 3.6 Seasonal dependence
Seasonal analyses show that drought sensitivity to IOD is not confined strictly to SON. Some regions exhibit consistent anomalies across seasons, whereas others show sign or magnitude changes that likely reflect seasonal migration of convergence zones, regional rainfall regimes, and seasonal evolution of land–atmosphere feedbacks. Differences between SPI and SPEI seasonality provide additional evidence for temperature-driven modulation in some regions.

**Figure 7:** Seasonal diagnostics  
`seasonal_analysis_SPI3.png`, `seasonal_analysis_SPI6.png`, `seasonal_analysis_SPEI3.png`, `seasonal_analysis_SPEI6.png`

### 3.7 Time–frequency dependence (wavelet coherence)
Wavelet coherence reveals intermittency in IOD–drought coupling. Periods of elevated coherence at interannual periodicities suggest that the teleconnection is stronger during epochs with stronger or more frequent IOD/ENSO events, while weaker coherence in other periods suggests non-stationarity. Coherence patterns differ across indices and time scales, indicating that precipitation-driven and evaporative-demand-driven drought responses may be expressed differently in the time–frequency domain.

**Figure 8:** Wavelet coherence diagnostics  
`wavelet_coherence_SPI3.png`, `wavelet_coherence_SPEI3.png`, etc.

### 3.8 Physical consistency from ERA5 circulation composites
ERA5 composites provide mechanistic consistency for the drought teleconnections. MSLP anomalies during IOD events suggest reorganized surface pressure gradients and altered convergence patterns. At 850 hPa, wind anomalies indicate changes in low-level moisture transport into and across Africa, providing a direct pathway linking oceanic forcing to precipitation and drought anomalies. At 500 hPa, geopotential height anomalies reflect ridge/trough structures that influence vertical motion and synoptic-scale flow.

To improve interpretability, geopotential height anomalies and wind vectors are plotted separately, reducing visual clutter compared to overlaid products. Hemispheric and polar-view geopotential height plots support interpretation of broader circulation structures beyond the African continent.

**Figure 9:** Atmospheric circulation composites  
`atmospheric_circulation_composites.png`  
**Figure 10:** Geopotential height anomaly composites  
`atmospheric_circulation_geopotential_height_mercator.png`, `atmospheric_circulation_geopotential_height_polar_stereographic.png`  
**Figure 11:** Wind vector composites  
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


