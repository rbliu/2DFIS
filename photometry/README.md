# Catalog-level color-term correction

## Author-confirmed processing stage

On 2026-09-10 the author clarified that 2DFIS color terms were applied **at
catalog level following the LoVoCCS procedure**, with the coefficients stated in
the manuscript Appendix. This supersedes the earlier description of enabling
the color terms in the LSST `processCcd` configuration.

The stages are distinct:

1. LSST performs the image-level processing and catalog measurements, with
   `applyColorTerms=False` in the recovered processCcd/jointcal configurations.
2. The catalog photometry is subsequently corrected using the LoVoCCS procedure
   and the CFHT-specific color relations.
3. Downstream photometric analyses use the corrected catalogs. The correction
   does not modify LSST-generated images or their archived task configuration.

The disabled LSST switches are thus consistent with the author's clarification.
Do not turn them on merely to make the files appear consistent with an earlier
manuscript sentence: doing so could apply corrections at the wrong stage or twice.

## Coefficients and direction

`manuscript_color_terms.json` transcribes the third-generation CFHT relations
from the current manuscript. This is a transcription for reproducibility, **not
a recovered historical runtime configuration**. In the Appendix's convention,

```
x = g_PS1 - i_PS1
m_CFHT - m_PS1 = a0 + a1*x + a2*x**2 + a3*x**3
```

The JSON explicitly lists each target/reference band, color, coefficient order,
and whether the band is observed in 2DFIS. z2 is reference information only;
there are no z exposures in this work. The SDSS u-to-CFHT u2 relation is transcribed
separately from Section 3, since it is absent from the local Appendix. The exact
CFHT u-band correction route is not inferred from an upstream default.

The above relation predicts a CFHT-system reference-star magnitude. It is not an
instruction to add or subtract the same polynomial from every science object's
magnitude using that object's own noisy color. The calibration implementation
and output magnitude system determine how the residual zero-point shift is used.

## Pinned upstream implementation

These files were retrieved from the exact upstream commit previously verified
for the clean server checkout:

- `../qc/upstream/python_scripts/photometric_correction/color_terms.py`
- `../qc/upstream/python_scripts/photometric_correction/zero_point.py`
- `../qc/upstream/python_scripts/configs/photometric_correction_config.py`

Source: [LoVoCCS 132bcb20c966ef2d0c7b93ce5d46f9a52f3f12c4](https://github.com/astroenglert/lovoccs_pipe/tree/132bcb20c966ef2d0c7b93ce5d46f9a52f3f12c4/python_scripts/photometric_correction).
The source and published SHA-256 hashes are in the provenance inventory.
Only the site-specific config paths have been redacted. GPL-3.0 licensing is
preserved in `../qc/upstream/LICENSE`.

In this upstream version, `color_terms.py` forms residuals of the measured
catalog magnitude against the reference magnitude plus the color polynomial,
then estimates a per-band median bias. `zero_point.py` subtracts the resulting
bias from catalog magnitudes and can propagate its uncertainty into magnitude
errors. The polynomial has four coefficients, including the cubic term, so
LSST's commented-out cubic config entries do not constrain this separate step.

The upstream implementation is **not a ready-to-run CFHT recipe**: its instrument
mapping lacks a CFHT entry, the zero-point script hard-codes `decam`, it applies
specific calibration-star color/magnitude cuts, and its config has
`use_locus=['u']`. These defaults are evidence of the upstream algorithm, not
confirmed parameters of the historical 2DFIS run. No stellar-locus correction,
extinction treatment, or error propagation is newly asserted for 2DFIS here.

## Remaining execution provenance

To reproduce the exact corrected catalog, attach the historical CFHT driver or
equivalent documented invocation, matched-star input/column mapping, selection
criteria, per-field/band residual offsets, affected photometry columns and error
handling. Confirm whether u uses the Section 3 SDSS relation, a stellar-locus
step, or both. These details are distinct from the now-confirmed processing stage
and published polynomial coefficients.

No science catalog was recalibrated as part of this archive update.
