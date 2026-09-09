# Archive validation

Prepared and checked on 2026-09-10 (Asia/Shanghai).

- 32 unique visits: four visits in each of four filters for each field.
- 1,152 registry CCD entries, with CCD IDs 0–35 and FITS extensions 1–36 per visit.
- Input state `p`, field/proposal/filter assignments and observation IDs checked
  against the author list, original read-only registries and public CADC records.
- 32 direct input URLs agree with the manifest. CADC returned the exact FITS
  artifact names, sizes and MD5 checksums; the images themselves were not downloaded.
- 272 source-file checksum records verified after site-path redaction.
- 137 Python files (including saved task-config backups) passed syntax parsing.
  Syntax parsing does not import LSST or evaluate the saved configuration.
- The published plotting adapter successfully regenerated the FRB visit 2785487
  four-panel PNG from existing local revision measurements; its layout was checked.
- Archived text was scanned for private source storage roots, private keys and
  common GitHub token formats. No server password, authentication token, private
  key, raw FITS image, coadd, or full science catalog was included.
- The original root license was retained; LoVoCCS's GPL-3.0 license is preserved
  separately, and source-derived QC adapters identify their license.

The archived configuration files were not changed to resolve scientific
disagreements. No raw-to-coadd reduction was rerun, no per-band configuration
mapping was inferred solely from backup suffixes, and no missing reference
catalog recipe or color-correction stage was fabricated.

Run `python tools/validate_archive.py` to repeat the offline integrity checks.
Read `KNOWN_GAPS.md` for the outstanding scientific-provenance requirements.
