# Paper 1 data (kept out of GitHub)

Git ignores `data/`, `output/`, NetCDF, GRIB, and pickle files. Those files are too large for the repository, and they are the copy you need while Lengau is offline (1 December 2026).

## Already on this PC

Copied into this clone (still ignored by git):

| Path | What it is |
| --- | --- |
| `output/comprehensive_iod_statistics/` | Closure-run pickles and figures (~500 MB). This is enough to finish the manuscript and to regenerate plots from saved results. |
| `output/iod_circulation/` | Vertical cross-section figures |
| `data/atmospheric/` | Junction to `tiny-media-analysis\data\atmospheric` (ERA5 GRIB/NetCDF, ~4.4 GB). Same files, no second copy. |

Small index files that **are** in git: `dmi_son_annual_averages.csv`, `dmi_son_top_events.csv`, `nino34.long.anom.csv`.

## Still only on Lengau

SPI/SPEI NetCDF grids are not on this PC. A full rerun of `run_iod_analysis_closure.py` needs them. Pull them before **27 November 2026**:

```powershell
$KEY = "$env:USERPROFILE\.ssh\id_ed25519"
$DEST = "C:\Users\MthethoSovara\paper1-analysis-phd"
scp -i $KEY -r `
  msovara@lengau.chpc.ac.za:/mnt/lustre/users/msovara/DataDownloads/data/output/comprehensive_iod_statistics `
  "$DEST\output\"
scp -i $KEY -r `
  msovara@lengau.chpc.ac.za:/mnt/lustre/users/msovara/DataDownloads/ `
  "$DEST\lengau_DataDownloads\"
```

Use the data-transfer node (`msovara@dtn.chpc.ac.za`) if the login node is slow. After the copy, point `analysis_config.py` paths at `lengau_DataDownloads` only if the scripts do not already find files under `data/`. The statistics script also searches `data/drought_reanalysis` and `data/spi_data`.

`output/` on this PC is the July 2026 closure bundle. Copy the Lengau tree only if that cluster copy is newer than the local one.

## Day-to-day

Write in `manuscript/paper.qmd`. Figures are under `output/comprehensive_iod_statistics/plots/` and `output/iod_circulation/`.

```powershell
python extract_paper_statistics.py
python run_iod_analysis_closure.py --plots-only
```

`--plots-only` rebuilds figures from the pickles. A full `--rerun-all` waits until the SPI/SPEI NetCDFs are in `data/`.
