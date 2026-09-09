# SPDX-License-Identifier: GPL-3.0-only
"""Reproduce CFHT visit QC from immutable Gen2 src/calexp FITS products.

Run in the supplied LSST v26 environment. Measurements follow the Moffat2D
procedure in lovoccs_pipe/python_scripts/check_visit/check_visit.py, with
CFHT Gen2 FITS input rather than DECam Gen3 Butler collections.
No input products are changed. Failed fits are flagged, never replaced by 10 px.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import time
import warnings

for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"

import numpy as np
from astropy.io import fits
from astropy.modeling import fitting, models
import lsst.afw.table as afw_table

VISITS = {
    "ClusterRot": {"u": list(range(2786404, 2786408)),
                   "g": list(range(2786408, 2786412)),
                   "r": list(range(2786623, 2786627)),
                   "i": list(range(2786627, 2786631))},
    "FRB": {"u": list(range(2785479, 2785483)),
            "g": list(range(2785483, 2785487)),
            "r": list(range(2785487, 2785491)),
            "i": list(range(2785491, 2785495))},
}
BANDS = {"u": "u2", "g": "g2", "r": "r2", "i": "i3"}


def measure(job):
    field, band, visit, sources, images, destination, field_root = job
    start = time.time()
    out = Path(destination) / "measurements"
    out.mkdir(parents=True, exist_ok=True)
    stem = f"{field}_{band}_{visit}"
    target = out / (stem + ".npz")
    if target.exists():
        raise FileExistsError(target)
    rows = []
    detectors = []
    reference = []
    scales = []
    for src in sources:
        ccd = int(Path(src).stem.split("-")[-1])
        calexp = images[ccd]
        catalog = afw_table.SourceCatalog.readFits(src)
        stars = catalog[catalog["calib_psf_used"]].copy(deep=True)
        ra = np.rad2deg(np.asarray(stars["coord_ra"]))
        dec = np.rad2deg(np.asarray(stars["coord_dec"]))
        xx = np.asarray(stars["base_SdssShape_xx"])
        yy = np.asarray(stars["base_SdssShape_yy"])
        xy = np.asarray(stars["base_SdssShape_xy"])
        with np.errstate(divide="ignore", invalid="ignore"):
            e1, e2 = (xx - yy) / (xx + yy), 2 * xy / (xx + yy)
        fwhms = []
        statuses = []
        with fits.open(calexp, memmap=True) as hdul:
            if hdul[0].header.get("FILTER") != BANDS[band]:
                raise ValueError(f"Wrong filter for {calexp}")
            scale = float(hdul[0].header["PIXSCAL1"])
            scales.append(scale)
            data = hdul[1].data
            x0 = -float(hdul[1].header.get("LTV1", 0))
            y0 = -float(hdul[1].header.get("LTV2", 0))
            for sx, sy in zip(stars["slot_Centroid_x"], stars["slot_Centroid_y"]):
                val, status = np.nan, -1
                try:
                    x, y = int(np.round(sx - x0)), int(np.round(sy - y0))
                    stamp = data[y-10:y+11, x-10:x+11]
                    if stamp.shape != (21, 21):
                        raise ValueError("edge stamp")
                    good = np.isfinite(stamp)
                    if good.sum() < 30 or not np.isfinite(stamp[10, 10]):
                        raise ValueError("invalid stamp")
                    gx, gy = np.meshgrid(np.arange(x-10, x+11), np.arange(y-10, y+11))
                    initial = models.Moffat2D(amplitude=stamp[10, 10],
                                              x_0=x, y_0=y, gamma=2., alpha=1.)
                    fitter = fitting.LevMarLSQFitter()
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        model = fitter(initial, gx[good], gy[good], stamp[good])
                        val = float(model.fwhm)
                    status = int(fitter.fit_info.get("ierr", -2))
                    if not np.isfinite(val) or val <= 0 or model.alpha.value <= 0:
                        status = -3
                        val = np.nan
                except (ValueError, RuntimeError, TypeError, IndexError, FloatingPointError):
                    pass
                fwhms.append(val)
                statuses.append(status)
        fw = np.asarray(fwhms)
        status = np.asarray(statuses)
        ellip = np.hypot(e1, e2)
        valid = np.isfinite(fw) & np.isin(status, [1, 2, 3, 4])
        detectors.append({"ccd": ccd, "n_psf_used": len(stars),
                          "n_fit_valid": int(valid.sum()),
                          "fwhm_pix_median_all_finite": float(np.nanmedian(fw)),
                          "fwhm_pix_median": float(np.nanmedian(fw[valid])),
                          "ellipticity_median": float(np.nanmedian(ellip)),
                          "src_path": src, "calexp_path": calexp})
        for j in range(len(stars)):
            rows.append((ccd, ra[j], dec[j], fw[j], fw[j]*scale,
                         e1[j], e2[j], status[j]))
    a = np.asarray(rows, dtype=float)
    if not len(a):
        raise ValueError(f"No PSF stars: {stem}")
    np.savez_compressed(target, ccd=a[:, 0].astype(int), ra=a[:, 1], dec=a[:, 2],
                        fwhm_pix=a[:, 3], fwhm_arcsec=a[:, 4],
                        e1=a[:, 5], e2=a[:, 6], fit_status=a[:, 7].astype(int))
    legacy_dir = "check_visit_output" if field == "ClusterRot" else "a04_check_visit_output"
    legacy = Path(field_root) / legacy_dir / f"v{visit}_med.txt"
    if legacy.exists():
        old = {int(row[0]): row for row in np.loadtxt(legacy)}
        for d in detectors:
            oldrow = old[d["ccd"]]
            reference.append({"ccd": d["ccd"],
                              "n_difference": d["n_psf_used"] - int(oldrow[4]),
                              "ellipticity_difference": d["ellipticity_median"] - oldrow[1],
                              "fwhm_pix_difference": d["fwhm_pix_median_all_finite"] - oldrow[2]})
    good = np.isfinite(a[:, 4]) & np.isin(a[:, 7], [1, 2, 3, 4])
    result = {"field": field, "band": band, "visit": visit,
              "n_ccd": len(detectors), "n_psf_used": len(a),
              "n_fit_valid": int(good.sum()), "n_fit_failed": int((~good).sum()),
              "pixel_scales_arcsec": sorted(set(scales)),
              "fwhm_arcsec_median": float(np.median(a[good, 4])),
              "ellipticity_median": float(np.nanmedian(np.hypot(a[:, 5], a[:, 6]))),
              "detectors": detectors, "legacy_comparison": reference,
              "seconds": time.time()-start}
    (out / (stem + ".json")).write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--cluster-root", type=Path, required=True,
                        help="ClusterRot work directory containing DATA/")
    parser.add_argument("--frb-root", type=Path, required=True,
                        help="FRB work directory containing DATA/")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    roots = {"ClusterRot": args.cluster_root, "FRB": args.frb_root}
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    jobs = []
    for field, byband in VISITS.items():
        repo = roots[field] / "DATA/rerun/processCcdOutputs_noct"
        src_index = {}
        img_index = {}
        wanted = {v for group in byband.values() for v in group}
        for name, prefix, index in [("src", "SRC", src_index), ("calexp", "calexp", img_index)]:
            for p in (repo / name).rglob(prefix + "-*.fits"):
                _, visit, ccd = p.stem.split("-")
                if int(visit) in wanted:
                    key = (int(visit), int(ccd))
                    if key in index:
                        raise ValueError(f"Duplicate product: {p}")
                    index[key] = str(p)
        for band, visits in byband.items():
            for visit in visits:
                ccds = sorted(c for v, c in src_index if v == visit)
                if ccds != list(range(36)):
                    raise ValueError(f"Incomplete CCD coverage: {field}/{visit}: {ccds}")
                sources = [src_index[(visit, c)] for c in ccds]
                images = {c: img_index[(visit, c)] for c in ccds}
                jobs.append((field, band, visit, sources, images, str(output), str(roots[field])))
    print(f"Preflight passed: {len(jobs)} visits, 36 matched CCDs each", flush=True)
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(measure, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(json.dumps({k: result[k] for k in ["field", "band", "visit", "n_psf_used", "n_fit_failed", "fwhm_arcsec_median", "ellipticity_median", "seconds"]}), flush=True)
    manifest = {"method": "21x21-pixel unweighted circular Moffat2D; calib_psf_used; base_SdssShape ellipticity",
                "fit_valid_status": [1, 2, 3, 4],
                "source_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "visits": sorted(results, key=lambda x: (x["field"], "ugri".index(x["band"]), x["visit"]))}
    (output / "qc_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("ALL_VISITS_COMPLETE", flush=True)


if __name__ == "__main__":
    main()
