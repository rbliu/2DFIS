# Third-party source and licensing

The initial repository supplied by the author contained the root GPL version 2
license. It has not been replaced.

## LoVoCCS

`qc/upstream/` is a source subset from
https://github.com/astroenglert/lovoccs_pipe at commit
`132bcb20c966ef2d0c7b93ce5d46f9a52f3f12c4`.
The source checkout was clean when collected. Its GPL version 3 license is
preserved in `qc/upstream/LICENSE`; its README and source attribution are retained.
This directory is not covered by a conflicting interpretation of the root
GPL-2.0 file.

The scripts in `qc/adapters/` were prepared for the 2026 2DFIS revision. They
implement the LoVoCCS QC method with CFHT Gen2 FITS input and are distributed
under GPL-3.0 (see `qc/upstream/LICENSE`). Modifications and validation are
described in `qc/README.md`. They are not claimed to be historical LoVoCCS source.

## LSST

`processing/` contains generated LSST configuration records and research-team
configuration/command files, not a distribution of the LSST software stack.
Preserved import names refer to separately installed LSST packages. Their own
licenses and acknowledgements continue to apply. Software versions and the
author-reported instrument-package revision are recorded in `provenance/`.
