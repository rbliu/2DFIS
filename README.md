# 2DFIS: input data and processing provenance

Supporting material for the 2DFIS overview paper: the CFHT input-exposure
manifest, recovered LSST Gen2 configuration files and commands, and LoVoCCS
quality-control source code. This is a **provenance archive**, not a new science
data release or a claim that an end-to-end reprocessing has been validated.

## Contents

| Location | Contents |
| --- | --- |
| [data/input_exposures.json](data/input_exposures.json) | 32 visits, filters, proposal IDs, 36 CCDs per visit, CADC file IDs, direct links and current archive checksums |
| [data/download_urls.txt](data/download_urls.txt) | Direct downloads of the 32 Elixir-preprocessed input FITS files |
| [processing/](processing/) | Recovered user overrides, full persisted task configurations and backups, historical commands, visit/patch lists, Butler parent records and package versions |
| [workflow/README.md](workflow/README.md) | Processing order, task-to-config mapping, setup and reproduction prerequisites |
| [qc/README.md](qc/README.md) | LoVoCCS source snapshot and the CFHT all-visit QC revision adapters |
| [provenance/KNOWN_GAPS.md](provenance/KNOWN_GAPS.md) | Unresolved historical configuration and calibration provenance |
| [provenance/source_inventory.json](provenance/source_inventory.json) | SHA-256 checksums of collected source files and published copies |

Read the known gaps **before using this archive to reproduce photometric
calibration**. In particular, surviving configurations contain
`applyColorTerms=False`, and the exact per-band configuration history and any
subsequent catalog-level corrections have not yet been established. The archive
preserves these records rather than changing them to match a manuscript claim.

## Input data

The two public CFHT programs are
[22BD07 (ClusterRot / RXCJ0110.0+1358)](https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?Observation.collection=CFHT&Observation.proposal.id=22BD07)
and
[22BS10 (FRB190417)](https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/search/?Observation.collection=CFHT&Observation.proposal.id=22BS10).
Each field has four visits in each of u, g, r and i. The actual inputs were
Elixir-preprocessed `p` products. They are called `raw` only by the LSST Gen2
Butler dataset type and `ingestImages.py`; they are not the unprocessed CADC
`o` products. Both product identifiers are recorded in the manifest.

The manifest was cross-checked against the two original Butler SQLite registries
and CADC CAOM2 metadata. The original data links refer to an earlier storage
system and are broken in the migrated repositories. CADC checksums therefore
describe the **currently available compressed archive files**, not a verified
byte-for-byte match to the historical local uncompressed inputs.

Download only if needed (approximately the sum of `cadc_current_bytes` in the
manifest); no large FITS files or final coadd catalogs are included in this Git
repository. See [CADC's direct-data service documentation](https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/doc/data/).

```bash
mkdir -p rawData
cd rawData
wget --input-file=/path/to/2DFIS/data/download_urls.txt
```

## Versions and scope

The historical reduction used LSST Science Pipelines **19.0.0 / Gen2**. Persisted
`packages.pickle` records were decoded with a restricted class whitelist and
archived as readable JSON; these contain more precise component versions.
The author-reported `obs_cfht` revision is
[`549c8174caa0f697f3f83d3bd6ff8349d2df08de`](https://github.com/lsst/obs_cfht/commit/549c8174caa0f697f3f83d3bd6ff8349d2df08de).
The mapper is `lsst.obs.cfht.MegacamMapper`.

LoVoCCS was used for subsequent QC and limiting-magnitude diagnostics, not as
a replacement for the LSST image processing. The available upstream checkout
is newer than the historical reduction; its identity and the 2026 QC adaptations
are explicitly distinguished in [qc/README.md](qc/README.md).

This repository does not distribute weak-lensing maps, shear catalogs,
photometric-redshift products, or accompanying science-analysis code. Coadds and
catalogs are not made public merely by the presence of this repository.
No input data or original server configuration was modified during collection.
Site-specific absolute paths in archived text are replaced by angle-bracket
placeholders; configuration values unrelated to those paths are preserved.

## Local integrity check

```bash
python tools/validate_archive.py
```

This checks manifest coverage, CADC identifiers, archived source hashes and
Python syntax. It does **not** run LSST or establish scientific reproducibility.

## Citation and licensing

Please cite the 2DFIS paper and the relevant LSST/LoVoCCS publications when using
this material. No dataset DOI or software DOI has been minted for this archive.
A Git commit identifies a fixed repository version; a mutable branch URL does
not replace an archival DOI.

The repository's existing GPL-2.0 license is retained. Third-party LoVoCCS code
and its derived QC adapters have separate GPL-3.0 terms; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). An existing root license does
not relicense the vendored sources.
