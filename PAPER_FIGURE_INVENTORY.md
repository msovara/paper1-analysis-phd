# Paper Figure Inventory — IOD–Drought Africa (1980–2020)

**Closure run:** 11 Jul 2026 (Lengau)  
**Local figures:** `output/comprehensive_iod_statistics/plots/` and `output/iod_circulation/`  
**Config source:** `analysis_config.py` (`IOD_COMPOSITE_SON_YEARS`, `AFRICA_ANALYSIS_BOUNDS`, `IOD_CIRCULATION_DIAGNOSTIC_LON`)

---

## Manuscript figure map

| Fig | Title (working) | Local file(s) | Status |
|-----|-----------------|---------------|--------|
| 1 | DMI dataset comparison | *Not in closure bundle* — use `dmi_*.png` from prior DMI analysis | ⚠️ copy separately if needed |
| 2 | Strong SON IOD events | *Not in closure bundle* — `dmi_son_events_analysis.png` | ⚠️ copy separately |
| 3 | IOD-phase drought composites | `composite_drought_SPI3_SPEI3_maps.png`, `composite_drought_SPI6_SPEI6_maps.png`; bars: `composite_drought_SPI3_SPEI3_bars.png`, `composite_drought_SPI6_SPEI6_bars.png` | ✅ |
| 4 | ENSO-stratified composites | `enso_stratified_composite_SPI3_SPEI3.png`, `enso_stratified_composite_SPI6_SPEI6.png`; summary: `enso_stratified_composite_summary_table.png` | ✅ |
| 5 | Lag correlations | `lag_correlation_analysis.png` | ✅ |
| 6 | Partial correlations (ENSO control) | `partial_correlation_analysis.png` | ✅ |
| 7 | Seasonal correlations | `seasonal_analysis_SPI3.png`, `seasonal_analysis_SPI6.png`, `seasonal_analysis_SPEI3.png`, `seasonal_analysis_SPEI6.png` | ✅ |
| 8 | Wavelet coherence | `wavelet_coherence_SPI3.png`, `wavelet_coherence_SPI6.png`, `wavelet_coherence_SPEI3.png`, `wavelet_coherence_SPEI6.png` | ✅ |
| 9 | ERA5 circulation (MSLP / 850 hPa / 500 hPa) | `atmospheric_circulation_composites.png` | ✅ |
| 10 | Geopotential height | `atmospheric_circulation_geopotential_height_mercator.png`, `atmospheric_circulation_geopotential_height_polar_stereographic.png` | ✅ |
| 11 | 850 hPa wind vectors | `atmospheric_circulation_wind_vectors.png` | ✅ |
| 12 | ω + u vertical cross-section (lat–pressure) | `iod_circulation/iod_circulation_cross_section_positive_negative_iod.png` | ✅ |
| 13 | ω + u vertical cross-section (lon–pressure) | `iod_circulation/iod_circulation_lonpressure_positive_negative_iod.png` | ✅ |

### Supplementary / diagnostic (not all required for main text)

| File | Use |
|------|-----|
| `spatial_correlation_*.png` (×4) | Supplement: grid-point correlation maps |
| `multiple_index_comparison.png` | Supplement: index comparison |
| `composite_drought_regional_averages_bars.png` | Alternative to per-index bar panels |
| `atmospheric_circulation_winds_over_geopotential.png` | Alternative circulation layout |
| `atmospheric_composites_negative_iod.png` | Diagnostic |

---

## Canonical IOD SON years (closure config)

| Phase | Years | *n* |
|-------|-------|-----|
| Positive | 1994, 1997, 2006, 2012, 2015, 2018, 2019 | 7 |
| Negative | 1980, 1981, 1992, 1996, 1998 | 5 |

---

## Key numbers verified from closure figures (Jul 2026)

### Composite significance (% land grid points, p < 0.05)

| Index | Positive IOD | Negative IOD |
|-------|-------------|--------------|
| SPI3 | 17.8% | 6.5% |
| SPEI3 | 7.5% | 7.6% |
| SPI6 | 16.8% | 7.9% |
| SPEI6 | 6.6% | 9.2% |

### Lag correlations (max \|r\|, from figure labels)

| Region | SPEI3 | SPEI6 | SPI3 | SPI6 |
|--------|-------|-------|------|------|
| East Africa | 0.161 @ 0 | 0.176 @ 0 | 0.169 @ −1 | 0.226 @ −1 |
| Southern Africa | 0.241 @ −9 | 0.256 @ −8 | 0.209 @ −9 | 0.227 @ −9 |
| West Africa | −0.089 @ −3 | −0.110 @ −3 | −0.156 @ −4 | −0.186 @ −4 |
| Central Africa | 0.053 @ 0 | 0.071 @ −12 | 0.054 @ −12 | 0.095 @ −12 |
| North Africa | 0.125 @ 0 | 0.125 @ −2 | 0.053 @ −7 | 0.049 @ −10 |

### Vertical cross-sections (Fig. 12–13)

- Domain: zonal mean **10°E–50°E**, **35°S–37°N**, African land mask
- **+IOD:** ascent (ω < 0) over Horn (~5–15°N) → wet composites; subsidence over subtropical Southern Africa (~15–35°S) → drought
- **−IOD:** reversed pattern over Horn and southern subtropics

---

## Manuscript gaps to close

1. **Figures 1–2:** DMI validation panels not in current local `output/` — SCP from Lengau or regenerate locally if DMI CSVs exist.
2. **Discussion §4.1 / Conclusions §5.1:** East Africa **+IOD = wetter** (positive SPI/SPEI), not drier — corrected in draft update.
3. **Methods §2.8:** Updated to 7 positive IOD years and separate circulation diagnostic domain.
4. **References:** Placeholder author/email/funding still needed.
