"""Reconcile the Southern Africa composite sign with the SON correlation.

The July 2026 closure reports a dry positive-IOD composite and a positive
full-series SON correlation for the same region. Those are different estimands:

- composite: mean SON anomaly of the canonical years, minus the SON climatology
  of the other years, then the area-weighted regional mean of that map;
- seasonal correlation: Pearson r of monthly DMI and monthly regional SPI/SPEI
  in September, October, and November, using every year.

This script reads the closure pickles and, when the NetCDF files are present,
rebuilds the Southern Africa SON series so the two signs can be compared on
one table. Raw NetCDF and pickles stay outside git. The written table is the
small derived record cited by the manuscript.

Run from the repository root:

    python scripts/check_southern_africa_sign.py
"""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import pearsonr

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from analysis_config import IOD_COMPOSITE_SON_YEARS  # noqa: E402

OUT_DIR = REPO / "manuscript" / "tables"
PICKLE_DIR = REPO / "output" / "comprehensive_iod_statistics" / "data"
NC_DIR = REPO / "data" / "drought_reanalysis"
DMI_ANNUAL = REPO / "dmi_son_annual_averages.csv"
DMI_MONTHLY = REPO / "data" / "dmi.had.long.csv"

REGION = "Southern Africa"
LAT = (-35.0, -10.0)
LON = (10.0, 40.0)
YEARS = range(1980, 2021)
SON = (9, 10, 11)
POSITIVE = list(IOD_COMPOSITE_SON_YEARS["positive"])
NEGATIVE = list(IOD_COMPOSITE_SON_YEARS["negative"])
EVENTS = set(POSITIVE + NEGATIVE)
INDICES = ("SPI3", "SPEI3")


def _lat_lon(da: xr.DataArray) -> tuple[str, str]:
    lat = "lat" if "lat" in da.coords else "latitude"
    lon = "lon" if "lon" in da.coords else "longitude"
    return lat, lon


def area_weighted_mean(
    da: xr.DataArray,
    lat_bounds: tuple[float, float] = LAT,
    lon_bounds: tuple[float, float] = LON,
) -> float:
    """Match ``_compute_regional_means``: cosine weights, NaNs dropped in the sum.

    Weights are normalised over the whole box, including ocean cells. A constant
    ocean mask therefore scales the mean. The correlation is invariant to that
    scale when the mask does not change with time.
    """
    lat_name, lon_name = _lat_lon(da)
    lat_vals = da[lat_name].values
    lat_min, lat_max = lat_bounds
    lon_min, lon_max = lon_bounds
    if len(lat_vals) > 1 and lat_vals[0] < lat_vals[-1]:
        lat_slice = slice(lat_min, lat_max)
    else:
        lat_slice = slice(lat_max, lat_min)
    region = da.sel({lat_name: lat_slice, lon_name: slice(lon_min, lon_max)})
    if region.size == 0:
        return float("nan")
    lat_2d, _lon_2d = np.meshgrid(
        region[lat_name].values, region[lon_name].values, indexing="ij"
    )
    weights = np.cos(np.radians(lat_2d))
    weights = weights / weights.sum()
    return float(np.nansum(region.values * weights))


def closure_rows() -> list[dict]:
    """Read the seasonal-correlation pickle only.

    The composite pickle still points at Lengau NetCDF paths, so its maps are
    not opened here. The composite anomalies are recomputed from the local files.
    """
    rows = []
    with (PICKLE_DIR / "seasonal_analysis_results.pkl").open("rb") as handle:
        seasonal = pickle.load(handle)
    for index in INDICES:
        corr = seasonal[index]["SON"][REGION]
        rows.append(
            {
                "index": index,
                "estimand": "closure_monthly_SON_correlation",
                "value": float(corr["correlation"]),
                "n": "",
                "p_value": float(corr["p_value"]),
                "source": "seasonal_analysis_results.pkl",
            }
        )
    return rows


def _month_file(index: str, year: int, month: int) -> Path:
    matches = sorted(NC_DIR.glob(f"{index}_*_{year}{month:02d}.nc"))
    if len(matches) != 1:
        raise FileNotFoundError(f"{index} {year}-{month:02d}: found {len(matches)} files")
    return matches[0]


def monthly_regional_means(index: str) -> pd.DataFrame:
    cache = OUT_DIR / f"southern_africa_{index.lower()}_son_months.csv"
    if cache.is_file():
        return pd.read_csv(cache)
    records = []
    for year in YEARS:
        for month in SON:
            path = _month_file(index, year, month)
            with xr.open_dataset(path) as ds:
                var = list(ds.data_vars)[0]
                value = area_weighted_mean(ds[var])
            records.append({"year": year, "month": month, "value": value})
    frame = pd.DataFrame.from_records(records)
    frame.to_csv(cache, index=False)
    return frame


def _monthly_series(frame: pd.DataFrame) -> pd.Series:
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame.loc[frame["dmi"] <= -999, "dmi"] = np.nan
    return frame.set_index("date")["dmi"]


def load_dmi_monthly_sources() -> dict[str, pd.Series]:
    hadisst = pd.read_csv(DMI_MONTHLY)
    hadisst.columns = ["date", "dmi"]
    sources = {"HadISST": _monthly_series(hadisst)}
    for label, path in (
        ("ERA5", REPO / "data" / "dmi_era5_1980_2020.csv"),
        ("ERA5_fixed", REPO / "data" / "dmi_era5_1980_2020_fixed.csv"),
    ):
        frame = pd.read_csv(path)
        date_col = "time" if "time" in frame.columns else "valid_time"
        sources[label] = _monthly_series(
            frame.rename(columns={date_col: "date", "DMI": "dmi"})[["date", "dmi"]]
        )
    return sources


def _corr_row(index: str, estimand: str, x: np.ndarray, y: np.ndarray, source: str) -> dict:
    mask = np.isfinite(x) & np.isfinite(y)
    n = int(mask.sum())
    if n < 3:
        value, p_value = float("nan"), float("nan")
    else:
        value, p_value = pearsonr(x[mask], y[mask])
    return {
        "index": index,
        "estimand": estimand,
        "value": float(value),
        "n": n,
        "p_value": float(p_value),
        "source": source,
    }


def recomputed_rows(
    index: str,
    monthly: pd.DataFrame,
    dmi_monthly: dict[str, pd.Series],
    dmi_annual: pd.DataFrame,
) -> list[dict]:
    rows = []
    stamps = pd.to_datetime(
        {"year": monthly["year"], "month": monthly["month"], "day": 1}
    )
    drought = monthly["value"].to_numpy(dtype=float)
    for label, series in dmi_monthly.items():
        rows.append(
            _corr_row(
                index,
                f"recomputed_monthly_SON_correlation_{label}",
                series.reindex(stamps).to_numpy(dtype=float),
                drought,
                f"monthly regional means correlated with {label}",
            )
        )

    annual = monthly.groupby("year", as_index=False)["value"].mean()
    annual["event"] = annual["year"].map(lambda year: year in EVENTS)
    annual["phase"] = annual["year"].map(
        lambda year: "positive" if year in POSITIVE else "negative" if year in NEGATIVE else "other"
    )
    non_event = annual.loc[~annual["event"], "value"]
    clim = float(non_event.mean())
    for phase in ("positive", "negative"):
        sample = annual.loc[annual["phase"] == phase, "value"]
        rows.append(
            {
                "index": index,
                "estimand": f"recomputed_{phase}_IOD_anomaly",
                "value": float(sample.mean() - clim),
                "n": int(sample.shape[0]),
                "p_value": "",
                "source": "SON mean of monthly regional means minus non-event SON mean",
            }
        )

    annual = annual.merge(dmi_annual, left_on="year", right_index=True, how="left")
    subsets = (
        ("all_years", annual),
        ("canonical_years", annual.loc[annual["event"]]),
        ("other_years", annual.loc[~annual["event"]]),
    )
    dmi_columns = (
        ("HadISST", "DMI_HadISST_SON"),
        ("ERSST", "DMI_ERSST_SON"),
        ("ERA5", "DMI_ERA5_SON"),
    )
    for dmi_label, column in dmi_columns:
        for subset_label, sample in subsets:
            rows.append(
                _corr_row(
                    index,
                    f"recomputed_annual_SON_correlation_{subset_label}_{dmi_label}",
                    sample[column].to_numpy(dtype=float),
                    sample["value"].to_numpy(dtype=float),
                    f"annual SON regional means + {column}",
                )
            )
    annual.to_csv(OUT_DIR / f"southern_africa_{index.lower()}_son_means.csv", index=False)
    return rows


def write_markdown(table: pd.DataFrame) -> None:
    def get(index: str, estimand: str) -> float:
        hit = table[(table["index"] == index) & (table["estimand"] == estimand)]
        return float(hit["value"].iloc[0])

    def cell(index: str, estimand: str) -> str:
        value = get(index, estimand)
        return f"{value:+.3f}"

    lines = [
        "| Estimand | SPI3 | SPEI3 |",
        "|---|---:|---:|",
        f"| Closure monthly SON correlation | {cell('SPI3', 'closure_monthly_SON_correlation')} | {cell('SPEI3', 'closure_monthly_SON_correlation')} |",
        f"| Recomputed positive-IOD anomaly | {cell('SPI3', 'recomputed_positive_IOD_anomaly')} | {cell('SPEI3', 'recomputed_positive_IOD_anomaly')} |",
        f"| Recomputed negative-IOD anomaly | {cell('SPI3', 'recomputed_negative_IOD_anomaly')} | {cell('SPEI3', 'recomputed_negative_IOD_anomaly')} |",
        f"| Recomputed monthly SON correlation, HadISST | {cell('SPI3', 'recomputed_monthly_SON_correlation_HadISST')} | {cell('SPEI3', 'recomputed_monthly_SON_correlation_HadISST')} |",
        f"| Recomputed monthly SON correlation, unfixed ERA5 file | {cell('SPI3', 'recomputed_monthly_SON_correlation_ERA5')} | {cell('SPEI3', 'recomputed_monthly_SON_correlation_ERA5')} |",
        f"| Recomputed monthly SON correlation, ERA5 file matching @fig-dmi | {cell('SPI3', 'recomputed_monthly_SON_correlation_ERA5_fixed')} | {cell('SPEI3', 'recomputed_monthly_SON_correlation_ERA5_fixed')} |",
        f"| Annual SON correlation, HadISST, all years | {cell('SPI3', 'recomputed_annual_SON_correlation_all_years_HadISST')} | {cell('SPEI3', 'recomputed_annual_SON_correlation_all_years_HadISST')} |",
        f"| Annual SON correlation, ERSST, all years | {cell('SPI3', 'recomputed_annual_SON_correlation_all_years_ERSST')} | {cell('SPEI3', 'recomputed_annual_SON_correlation_all_years_ERSST')} |",
        f"| Annual SON correlation, ERA5, all years | {cell('SPI3', 'recomputed_annual_SON_correlation_all_years_ERA5')} | {cell('SPEI3', 'recomputed_annual_SON_correlation_all_years_ERA5')} |",
        f"| Annual SON correlation, HadISST, 12 canonical years | {cell('SPI3', 'recomputed_annual_SON_correlation_canonical_years_HadISST')} | {cell('SPEI3', 'recomputed_annual_SON_correlation_canonical_years_HadISST')} |",
        f"| Annual SON correlation, HadISST, other 29 years | {cell('SPI3', 'recomputed_annual_SON_correlation_other_years_HadISST')} | {cell('SPEI3', 'recomputed_annual_SON_correlation_other_years_HadISST')} |",
        "",
        ": Southern Africa (35°S–10°S, 10°E–40°E). The closure correlation is the July 2026 seasonal pickle. The unfixed ERA5 file is `dmi_era5_1980_2020.csv`; its SON means are not the ERA5 curve in the dataset figure. The matching file is `dmi_era5_1980_2020_fixed.csv`. Anomalies are the canonical-year SON mean minus the other SON seasons. Annual correlations use `dmi_son_annual_averages.csv`, whose ERA5 column matches the fixed file. {#tbl-sa-sign}",
        "",
    ]
    (OUT_DIR / "southern_africa_sign_check.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = closure_rows()
    dmi_annual = pd.read_csv(DMI_ANNUAL).set_index("Year")
    dmi_monthly = load_dmi_monthly_sources()
    for index in INDICES:
        print(f"reading {index} SON files", flush=True)
        monthly = monthly_regional_means(index)
        rows.extend(recomputed_rows(index, monthly, dmi_monthly, dmi_annual))
    table = pd.DataFrame(rows)
    table.to_csv(OUT_DIR / "southern_africa_sign_check.csv", index=False)
    write_markdown(table)
    write_east_africa_check(dmi_monthly)
    print(table.to_string(index=False))


def write_east_africa_check(dmi_monthly: dict[str, pd.Series]) -> None:
    """East Africa is the control for which DMI file the closure correlation used.

    The closure code's East Africa box is 10°S–20°N, 30°E–50°E. This is not one
    of the smaller boxes in ``SOUTHERN_AFRICA_REGIONS``.
    """
    lat_bounds = (-10.0, 20.0)
    lon_bounds = (30.0, 50.0)
    records = []
    for year in YEARS:
        for month in SON:
            path = _month_file("SPI3", year, month)
            with xr.open_dataset(path) as ds:
                var = list(ds.data_vars)[0]
                value = area_weighted_mean(ds[var], lat_bounds, lon_bounds)
            records.append({"year": year, "month": month, "value": value})
    monthly = pd.DataFrame.from_records(records)
    monthly.to_csv(OUT_DIR / "east_africa_spi3_son_months.csv", index=False)
    stamps = pd.to_datetime({"year": monthly["year"], "month": monthly["month"], "day": 1})
    drought = monthly["value"].to_numpy(dtype=float)
    rows = [
        _corr_row(
            "SPI3",
            f"east_africa_monthly_SON_correlation_{label}",
            series.reindex(stamps).to_numpy(dtype=float),
            drought,
            "East Africa 10°S–20°N, 30°E–50°E, monthly SON, " + label,
        )
        for label, series in dmi_monthly.items()
    ]
    frame = pd.DataFrame(rows)
    frame.to_csv(OUT_DIR / "east_africa_spi3_son_dmi_check.csv", index=False)
    print(frame.to_string(index=False))


if __name__ == "__main__":
    main()
