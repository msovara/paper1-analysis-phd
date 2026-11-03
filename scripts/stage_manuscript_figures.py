"""Copy the manuscript figures out of the gitignored output tree.

``output/`` stays untracked. ``manuscript/figures/`` is the small set that
``paper.qmd`` embeds, so a clone can render the article without the NetCDF
files. Each copy is recorded with its source path and SHA-256.

    python scripts/stage_manuscript_figures.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEST = REPO / "manuscript" / "figures"

# Source path relative to the repository, then the name used in paper.qmd.
FIGURES = (
    ("output/comprehensive_iod_statistics/plots/composite_drought_SPI3_SPEI3_maps.png", "composite_drought_SPI3_SPEI3_maps.png"),
    ("output/comprehensive_iod_statistics/plots/composite_drought_SPI6_SPEI6_maps.png", "composite_drought_SPI6_SPEI6_maps.png"),
    ("output/comprehensive_iod_statistics/plots/composite_drought_regional_averages_bars.png", "composite_drought_regional_averages_bars.png"),
    ("output/comprehensive_iod_statistics/plots/enso_stratified_composite_SPI3_SPEI3.png", "enso_stratified_composite_SPI3_SPEI3.png"),
    ("output/comprehensive_iod_statistics/plots/enso_stratified_composite_SPI6_SPEI6.png", "enso_stratified_composite_SPI6_SPEI6.png"),
    ("output/comprehensive_iod_statistics/plots/lag_correlation_analysis.png", "lag_correlation_analysis.png"),
    ("output/comprehensive_iod_statistics/plots/partial_correlation_analysis.png", "partial_correlation_analysis.png"),
    ("output/comprehensive_iod_statistics/plots/seasonal_analysis_SPI3.png", "seasonal_analysis_SPI3.png"),
    ("output/comprehensive_iod_statistics/plots/seasonal_analysis_SPI6.png", "seasonal_analysis_SPI6.png"),
    ("output/comprehensive_iod_statistics/plots/seasonal_analysis_SPEI3.png", "seasonal_analysis_SPEI3.png"),
    ("output/comprehensive_iod_statistics/plots/seasonal_analysis_SPEI6.png", "seasonal_analysis_SPEI6.png"),
    ("output/comprehensive_iod_statistics/plots/atmospheric_circulation_composites.png", "atmospheric_circulation_composites.png"),
    ("output/comprehensive_iod_statistics/plots/atmospheric_circulation_wind_vectors.png", "atmospheric_circulation_wind_vectors.png"),
    ("output/comprehensive_iod_statistics/plots/atmospheric_circulation_geopotential_height_mercator.png", "atmospheric_circulation_geopotential_height_mercator.png"),
    ("output/iod_circulation/iod_circulation_cross_section_positive_negative_iod.png", "iod_circulation_cross_section_positive_negative_iod.png"),
    ("output/iod_circulation/iod_circulation_lonpressure_positive_negative_iod.png", "iod_circulation_lonpressure_positive_negative_iod.png"),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    rows = ["filename,bytes,sha256,source"]
    missing = []
    for source_rel, name in FIGURES:
        source = REPO / source_rel
        if not source.is_file():
            missing.append(source_rel)
            continue
        target = DEST / name
        target.write_bytes(source.read_bytes())
        rows.append(f"{name},{target.stat().st_size},{sha256(target)},{source_rel}")
        print(f"staged {name}")
    copied = {name for _source, name in FIGURES}
    for path in sorted(DEST.glob("*.png")):
        if path.name in copied:
            continue
        rows.append(f"{path.name},{path.stat().st_size},{sha256(path)},scripts/build_dmi_figures.py")
        print(f"recorded generated {path.name}")
    manifest = DEST / "MANIFEST.csv"
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    if missing:
        raise SystemExit("missing source figures:\n" + "\n".join(missing))
    print(f"wrote {manifest}")


if __name__ == "__main__":
    main()
