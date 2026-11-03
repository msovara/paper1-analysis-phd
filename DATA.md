# Paper 1 data (kept out of GitHub)

Git ignores `data/`, `output/`, NetCDF, GRIB, and pickle files. Those files are too large for the repository, and they are the copy you need while Lengau is offline (1 December 2026).

## Already on this PC

Copied into this clone (still ignored by git):

| Path | What it is |
| --- | --- |
| `data/drought_reanalysis/` | SPI3, SPI6, SPEI3, SPEI6 monthly ERA5 NetCDF, 492 files each (1,968 files, 15.3 GiB). Copied from Lengau on 2 November 2026. |
| `data/dmi.had.long.csv`, `data/dmi_era5_1980_2020.csv`, `data/dmi_era5_1980_2020_fixed.csv` | Monthly DMI series |
| `output/comprehensive_iod_statistics/` | Closure-run pickles and figures (~500 MB). |
| `output/iod_circulation/` | Vertical cross-section figures |
| `data/atmospheric/data_stream-moda_stepType-avgua.nc` | Monthly ERA5 atmosphere file (4.3 GB), linked from `tiny-media-analysis` |

Small index files that **are** in git: `dmi_son_annual_averages.csv`, `dmi_son_top_events.csv`, `nino34.long.anom.csv`.

The full `DataDownloads` tree on Lengau is 51 GB. About 20 GB of that is zip archives of the same drought and atmosphere files. This PC has about 14 GB free after the drought copy, so those archives were left on the cluster.

## Still only on Lengau

Pressure-level GRIB used for a fresh vertical cross-section (about 2.5 GB inside `atmospheric/`, plus larger loose GRIB files). The cross-section figures already in `output/iod_circulation/` do not need them. Pull before **27 November 2026** only if you will recompute that figure from raw fields:

```powershell
$KEY = "$env:USERPROFILE\.ssh\id_ed25519"
scp -i $KEY `
  "msovara@lengau.chpc.ac.za:/mnt/lustre/users/msovara/DataDownloads/data/atmospheric/44b356f31168077a5ba0a07bcc0ab547.grib" `
  "C:\Users\MthethoSovara\tiny-media-analysis\data\atmospheric\"
```

## Day-to-day

Write in `manuscript/paper.qmd`. Render with Quarto from `manuscript/`:

```powershell
& "C:\Program Files\Quarto\bin\quarto.exe" render paper.qmd --to docx
```

The Word file is `manuscript/_output/paper.docx` and is not committed. The figures the article embeds are committed under `manuscript/figures/`. Refresh them with:

```powershell
python scripts/build_dmi_figures.py
python scripts/stage_manuscript_figures.py
```

The Southern Africa composite-versus-correlation check is:

```powershell
python scripts/check_southern_africa_sign.py
```

It writes `manuscript/tables/southern_africa_sign_check.csv`. The drought NetCDF files have to be present for a fresh run. A later run reads the monthly cache in that same folder.
