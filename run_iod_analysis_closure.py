#!/usr/bin/env python3
"""Run final IOD-drought analysis closure (offline-safe). Use on Lengau or locally."""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], log: Path, cwd: Path) -> int:
    line = f"\n>>> {' '.join(cmd)}\n"
    print(line, end="")
    with log.open("a", encoding="utf-8") as f:
        f.write(line)
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", default=".", help="Project root (data/, output/)")
    parser.add_argument("--plots-only", action="store_true", help="Regenerate plots from pickle only")
    args = parser.parse_args()

    workdir = Path(args.workdir).resolve()
    log = workdir / f"iod_closure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log.write_text(f"=== IOD analysis closure ===\nWorkdir: {workdir}\nStarted: {datetime.now()}\n", encoding="utf-8")

    py = sys.executable

    rc = run([py, "verify_iod_analysis_closure.py", "--data-dir", ".", "--check-inputs"], log, workdir)
    if rc != 0:
        print("INPUT CHECK FAILED — see log:", log)
        return rc

    if args.plots_only:
        rc = run([
            py, "comprehensive_iod_drought_statistics_optimized.py",
            "--regenerate-plots",
            "--analyses", "enso_stratified_composite,lag,partial,seasonal,multiple_index",
        ], log, workdir)
    else:
        print("Full rerun started — may take 30–90+ minutes. Log:", log)
        rc = run([py, "comprehensive_iod_drought_statistics_optimized.py", "--rerun-all"], log, workdir)
    if rc != 0:
        print("Statistics step failed — see log:", log)
        return rc

    circ_rc = run([
        py, "plot_iod_circulation_cross_section.py",
        "--data-dir", ".",
        "--output-dir", "output/iod_circulation",
        "--no-synthetic",
    ], log, workdir)
    if circ_rc != 0:
        print("WARN: circulation step failed (see log); continuing to output check.")

    rc = run([
        py, "verify_iod_analysis_closure.py",
        "--data-dir", ".",
        "--stats-output", "output/comprehensive_iod_statistics",
        "--circ-output", "output/iod_circulation",
        "--check-outputs",
    ], log, workdir)

    if rc == 0:
        print("CLOSURE COMPLETE. Log:", log)
    else:
        print("CLOSURE INCOMPLETE. Log:", log)
    return rc


if __name__ == "__main__":
    sys.exit(main())
