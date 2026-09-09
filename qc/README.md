# LoVoCCS quality control and the CFHT revision

## Source identity

`upstream/` preserves the supplied server checkout's relevant source files at
[LoVoCCS commit 132bcb2](https://github.com/astroenglert/lovoccs_pipe/tree/132bcb20c966ef2d0c7b93ce5d46f9a52f3f12c4),
including its GPL-3.0 license. This is a **2025 DECam/Gen3 implementation**,
not the original CFHT/Gen2 reduction source. The upstream README describes that
project as a whole; it must not be read as the procedure applied to 2DFIS.
The check_visit and quality_check modules are preserved as method/source
references. No lensing-map workflow is invoked by this archive.
The author subsequently clarified that LoVoCCS was also used for catalog-level
color corrections. The corresponding `photometric_correction` modules and their
config dependency are included under the same upstream snapshot; see
`../photometry/README.md`. Only site-specific paths in the additional upstream
config were redacted, as recorded in the source inventory.

`adapters/build_visit_qc.py` and `adapters/render_visit_qc_original_style.py`
are the scripts used for the 2026 all-visit QC revision. The archive version adds
command-line field roots to remove private site paths; the measurement algorithm
and plotting settings are unchanged. Original revision-script checksums are in
`../provenance/qc_revision_scripts.json`. These adapters are GPL-3.0; see
`upstream/LICENSE`.

## Reproduce the 32 visit QC figures

The measurement adapter reads **existing** Gen2 products under each field's
`DATA/rerun/processCcdOutputs_noct/src` and `calexp`. It requires a Python
environment with `lsst.afw.table`, NumPy, Astropy and SciPy. The actual revision
used the author's LSST v26 environment **only as a reader**, not for reprocessing
the v19 images. Do not use the DECam Gen3 Butler queries in the upstream module
directly on a CFHT Gen2 repository. No custom `obs_wfst` functionality is invoked
by the adapter; it reads source-catalog and image FITS files directly.

```bash
python qc/adapters/build_visit_qc.py \
    --cluster-root /path/to/cluster/workdir \
    --frb-root /path/to/frb/workdir \
    --output qc_output --workers 8
python qc/adapters/render_visit_qc_original_style.py \
    --data qc_output --output qc_output/figures
```

Use a new measurement output directory: existing per-visit NPZ files are not
overwritten. The rendering step requires NumPy and Matplotlib and overwrites
matching PNG filenames in its explicitly selected output directory.
It produces `fig-qc_cluster_<visit>.png` and `fig-qc_FRB_<visit>.png`.

The measurement method is:

1. Select `calib_psf_used` sources in each of the 36 CCD catalogs.
2. Fit an unweighted circular `Moffat2D` to a 21 × 21-pixel image cutout centered
   on the rounded LSST centroid. The initial amplitude is the central pixel,
   gamma is 2 pixels and alpha is 1; use `LevMarLSQFitter` and mask nonfinite pixels.
3. Retain finite, positive FWHM measurements with positive alpha and optimizer
   status 1, 2, 3 or 4. Failed fits are recorded, not replaced by 10 pixels.
4. Calculate `e1=(xx-yy)/(xx+yy)`, `e2=2xy/(xx+yy)` and `e=hypot(e1,e2)` from
   the `base_SdssShape` moments. This is a stellar-shape QC diagnostic, not a
   measurement of PSF-model residuals or a shear-calibration test.
5. Convert FWHM using the input FITS `PIXSCAL1` header (0.185 arcsec/pixel for the
   checked inputs). Do not silently substitute a different instrument-scale
   value quoted elsewhere.

The revised plots have two spatial panels and two unfilled 50-bin histograms,
with the same blue-green color map for both spatial panels. The FRB declination
display interval is 58.8–60.0 degrees as requested for the revision; it is a
display choice, not a data-selection cut. Cluster spatial axes use equal numeric
degree scales. Plotting preserves the existing RA display convention.

The existing r-band validation covered 8 visits and 288 CCDs. Selected-star
counts agree exactly; maximum differences in median ellipticity and median
Moffat FWHM were 2.78e-17 and 8.32e-6 pixels, respectively. Across all 32 visits,
there are 224,984 selected stars, one excluded failed FWHM fit and one nonfinite
ellipticity. This validation does not establish weak-lensing systematic errors.

## Limiting magnitudes

The archived
`upstream/python_scripts/quality_check/quality_check.py` includes
`plot_snr_mag_hist` and `plot_mag_magerr`; its direct configuration dependency
is `upstream/python_scripts/configs/quality_check_config.py`.

`plot_snr_mag_hist` accepts separate Astropy star/galaxy tables with `x`, `y`
and `<band>_psf_mag`, `<band>_psf_magerr`, `<band>_cmodel_mag`,
`<band>_cmodel_magerr` columns as appropriate. It calculates
`S/N = (2.5 / ln(10)) / magnitude_error`, applies a configurable radial cut,
selects open S/N intervals (defaults 9–11 and 19–21), and reports median and
maximum magnitude in each interval. These statistics are not interchangeable
with an injection/recovery completeness limit. A 5-sigma value must not be
fabricated by relabeling the 10-sigma result.

The file imports TreeCorr, NumPy, SciPy, Matplotlib, Astropy and Astroquery;
it uses the historical SciPy `trapz`/`cumtrapz` names. A compatible historical
environment or a separately documented compatibility adaptation is required.
The upstream CFHT-independent default center/radius and the DECam-specific
quality-cut config are **not** established 2DFIS parameter choices. The source
selection and invocation used for the paper's depth table remain an explicit
provenance gap; see `../provenance/KNOWN_GAPS.md`. Do not run `draw_catalog` or
apply all upstream quality cuts merely to reproduce a magnitude–error plot.
