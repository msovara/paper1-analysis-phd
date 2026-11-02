#!/usr/bin/env python3
"""Extract key statistics from closure-run pickles for paper draft."""

import pickle
from pathlib import Path

import numpy as np

DATA = Path("output/comprehensive_iod_statistics/data")

REGIONS = {
    "East Africa": {"lat": (-10, 20), "lon": (30, 50)},
    "Southern Africa": {"lat": (-35, -10), "lon": (10, 40)},
    "West Africa": {"lat": (-5, 20), "lon": (-20, 20)},
    "Central Africa": {"lat": (-10, 15), "lon": (5, 30)},
    "North Africa": {"lat": (15, 37), "lon": (-20, 55)},
}


def _coords(da):
    lat = "lat" if "lat" in da.coords else "latitude"
    lon = "lon" if "lon" in da.coords else "longitude"
    return lat, lon


def regional_mean(da, lat_bounds, lon_bounds):
    lat, lon = _coords(da)
    lat_min, lat_max = lat_bounds
    lon_min, lon_max = lon_bounds
    if lat_min < lat_max:
        sub = da.sel({lat: slice(lat_min, lat_max), lon: slice(lon_min, lon_max)})
    else:
        sub = da.sel({lat: slice(lat_max, lat_min), lon: slice(lon_min, lon_max)})
    return float(sub.mean().values)


def sig_pct(da):
    if "significant" in da.coords or hasattr(da, "name") and da.name == "significant":
        pass
    # significance often stored separately
    return None


def main():
    with open(DATA / "composite_drought_results.pkl", "rb") as f:
        comp = pickle.load(f)

    print("=" * 72)
    print("COMPOSITE DROUGHT REGIONAL AVERAGES")
    print("=" * 72)
    for idx in ["SPI3", "SPI6", "SPEI3", "SPEI6"]:
        if idx not in comp:
            continue
        d = comp[idx]
        print(f"\n{idx}:")
        for phase in ["positive_composite", "negative_composite"]:
            da = d.get(phase)
            if da is None:
                continue
            print(f"  {phase}:")
            for rname, rb in REGIONS.items():
                print(f"    {rname:18s}: {regional_mean(da, rb['lat'], rb['lon']):+.3f}")
        sig_pos = d.get("positive_significance")
        sig_neg = d.get("negative_significance")
        if sig_pos is not None:
            print(f"  positive sig %: {100 * float(sig_pos.mean().values):.1f}")
        if sig_neg is not None:
            print(f"  negative sig %: {100 * float(sig_neg.mean().values):.1f}")

    with open(DATA / "lag_correlation_results.pkl", "rb") as f:
        lag = pickle.load(f)
    print("\n" + "=" * 72)
    print("LAG CORRELATIONS (regional means, key lags)")
    print("=" * 72)
    for key, val in sorted(lag.items()):
        if isinstance(val, dict) and "correlations" in str(type(val)):
            pass

    # inspect structure
    if isinstance(lag, dict):
        for idx in lag:
            print(f"\n{idx} keys: {list(lag[idx].keys()) if isinstance(lag[idx], dict) else type(lag[idx])}")

    with open(DATA / "partial_correlation_results.pkl", "rb") as f:
        partial = pickle.load(f)
    print("\n" + "=" * 72)
    print("PARTIAL CORRELATION STRUCTURE")
    print("=" * 72)
    if isinstance(partial, dict):
        print(list(partial.keys())[:20])
        for k, v in partial.items():
            if isinstance(v, dict):
                print(f"  {k}: {list(v.keys())}")

    with open(DATA / "seasonal_analysis_results.pkl", "rb") as f:
        seasonal = pickle.load(f)
    print("\nSEASONAL keys:", list(seasonal.keys()) if isinstance(seasonal, dict) else type(seasonal))

    csv = DATA / "enso_stratified_composite_summary_table.csv"
    if csv.exists():
        print("\n" + "=" * 72)
        print("ENSO STRATIFIED SUMMARY (first 30 lines)")
        print("=" * 72)
        print(csv.read_text(encoding="utf-8")[:4000])


if __name__ == "__main__":
    main()
