# Reproducibility status and unresolved provenance

This document distinguishes recovered evidence from assumptions. The collection
is not yet a verified, complete end-to-end reproduction package. No settings
were altered to hide disagreement with the manuscript.

## 1. Color terms and reference catalogs

Both fields' current saved `processCcdOutputs_noct/config/processCcd.py` contain
`config.calibrate.photoCal.applyColorTerms=False`; their current saved
`jointcal/config/jointcal.py` also has `config.applyColorTerms=False`.

**Resolved by the author on 2026-09-10:** color terms were applied at catalog
level following the LoVoCCS procedure, using the parameters in the manuscript
Appendix. The disabled LSST switches are therefore consistent with that workflow,
not evidence of a missing color correction. The coefficients have been transcribed
in `photometry/manuscript_color_terms.json`, with their source and sign convention.
The corresponding upstream color-term, zero-point and configuration modules are
now included as method references at the already-identified LoVoCCS commit.

ClusterRot's last saved processCcd and jointcal configurations select `sdss`
for both reference loaders. Its processCcd backups also contain Gaia/PS1 and
Gaia/SDSS variants. FRB's last saved records select `gaia` and `pan-starrs`.
These local dataset labels alone do not prove the reference releases or which
configuration was applied to each exposure. `provenance/calibration_settings.json`
provides an automatically extracted index; the full original settings are retained.

The historical CFHT invocation, input matched-star catalogs, selection cuts,
per-field zero-point offsets and uncertainty handling have not yet been linked
to the exact paper products. The supplied upstream modules contain DECam-specific
defaults, so they are not represented as that historical invocation. In particular,
the upstream zero-point module defaults to a stellar-locus correction in u; the
CFHT u-band choice still requires confirmation. The local Appendix contains PS1
g/r/i/z relations, while the SDSS u relation occurs in Section 3.

The recovered LSST overrides have commented-out cubic coefficients; these do not
establish the subsequent catalog correction. The remaining reference-loader and
per-band history questions are separate from the now-confirmed correction stage.
The manuscript sentences attributing the correction to `processCcd`/`photoCalib`
also need to be updated to the author-confirmed catalog-level description.

## 2. Files changed across runs

Some historical shell scripts refer to files no longer present in the user
configuration directory, including FRB `processCcdConfig_u.py`,
`jointcal_config.py`, `forcedPhotCoaddConfig.py` and merge configuration files.
Logs also mention trial configurations no longer present. Full persisted
configurations and backups are included where available, but a saved rerun
configuration may have been overwritten after multiple band-specific invocations.
Backups cannot be assigned to every visit purely by their `~N` suffix.

The current ClusterRot single-frame shell scripts target `processCcdOutputs`,
while the coadd parent records and historical logged invocations identify
`processCcdOutputs_noct` as the downstream input. Several script lines are
commented out after earlier runs. Hence the latest shell files are archived
as evidence, not represented as a complete batch-launch recipe.

## 3. External inputs and helpers

The original raw-data and `ref_cats` links point to an unavailable previous
storage system. CADC files can be located unambiguously, but historical local
input checksums and the exact HTM reference-catalog preparation/selection recipe
were not recovered. Current CADC checksums must not be called historical hashes.

`get_skymap_corner.py` and the CFHT catalog-extraction helper
`load_dm_output_all_new.py` are referenced by historical scripts but were not
found in the scoped source locations. The resulting visit/patch selectors are
archived. Full saved configurations were not found for ingest and skymap creation;
the command records and available skymap override are included instead.

## 4. LoVoCCS and the QC revision

The supplied server LoVoCCS checkout is a 2025 Gen3/DECam codebase. It cannot
be represented as an untouched 2023 CFHT/Gen2 processing package. Its exact
commit and source subset are archived, together with the CFHT adaptation used
to regenerate all-visit QC in 2026. The moment/Moffat QC measurements were
validated against the eight retained r-band visits; no end-to-end image
reduction was rerun for this archive.

The upstream limiting-magnitude routines are included with their direct config
dependency. Their original CFHT invocation, prior source selections, calibration
corrections, and catalog-extraction path still need to be tied to the final
paper products before this part can be called fully reproducible. DECam defaults
in the upstream module must not be described as measured CFHT choices.

## 5. Publication checklist

- Confirm the final per-band processCcd/jointcal configuration mapping.
- Archive the exact CFHT catalog-correction invocation and offsets; update the
  manuscript's processCcd/photoCalib wording to the confirmed catalog-level stage.
- Supply or document the reference-catalog preparation and catalog extraction.
- Confirm the exact limiting-magnitude input selections and invocation.
- Perform an independent end-to-end run if numerical reproduction is claimed.
- After provenance is resolved, tag a release and optionally archive it with a DOI.

This archive intentionally preserves recoverable information now; an unresolved
item is not silently filled with an invented setting.
