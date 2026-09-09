# Historical processing sequence and reproduction prerequisites

This sequence is reconstructed from numbered shell scripts, task-invocation
messages in retained logs, and Gen2 `repositoryCfg.yaml` parent records. The
archived shell scripts are **historical evidence, not turnkey launch scripts**:
some commands were commented out after earlier runs, some paths refer to a
retired site, and configuration files were changed between invocations.
Do not run these scripts against an existing repository.

## Environment and inputs

1. Install the LSST **19.0.0 Gen2** stack, including the component versions recorded
   under `processing/<field>/butler/<rerun>/config/packages.pickle.json`.
   This is not a Gen3 YAML pipeline. The later v26 QC-reading environment does
   not replace this reduction environment.
2. Set up `lsst_distrib` and the CFHT instrument package. The author's reported
   `obs_cfht` commit is `549c8174caa0f697f3f83d3bd6ff8349d2df08de`; the archived
   mapper file contains `lsst.obs.cfht.MegacamMapper`.
3. Download the 32 CADC **p** products listed in `data/input_exposures.json`.
   Select only the 16 visits of the field being reduced. The historical ingest
   command used `rawData/*.fz` with `--mode=link`; do not mix fields inadvertently.
4. Prepare a **new** field work directory and Gen2 `DATA` repository. Install the
   appropriate HTM-indexed reference catalogs under `DATA/ref_cats`. The surviving
   reference-catalog link points to an unavailable earlier filesystem; precise
   reference-catalog build recipes have not been recovered. The manuscript's
   stated releases are Gaia DR2, PS1 DR1 and SDSS DR12, but the effective per-band
   selections must first be reconciled with the archived configurations.
5. Resolve the items in [KNOWN_GAPS.md](../provenance/KNOWN_GAPS.md). In particular,
   choose the correct historical configuration for each band rather than treating
   the last saved file as the configuration of every exposure.

## Ordered tasks

Paths in this table are relative to `processing/<field>/butler/`. All resolved
configurations are full saved task configurations, not just override fragments.
The retained `*.py~N` files are historical backups and are not independently
verified per-band selections.

| Order | Command/task | Input → output rerun | Saved full configuration |
| --- | --- | --- | --- |
| 1 | `ingestImages.py` | Elixir p files → `DATA/raw` | mapper and input manifest; no complete saved ingest config recovered |
| 2 | `processCcd.py` | `DATA` → `processCcdOutputs_noct` | `processCcdOutputs_noct/config/processCcd.py` and backups |
| 3 | `makeDiscreteSkyMap.py` | `processCcdOutputs_noct` → `coadd` | user override `../overrides/makeDiscreteSkyMapConfig.py`; no complete saved task config recovered |
| 4 | `reportPatches.py` | `coadd` → patch lists | recorded patch lists in `../commands/` |
| 5 | `jointcal.py` | `coadd` → `jointcal` | `jointcal/config/jointcal.py` and backups |
| 6 | `makeCoaddTempExp.py` | `jointcal` → `coadd2` | `coadd2/config/deep_makeCoaddTempExp.py` |
| 7 | `assembleCoadd.py --warpCompare` | `coadd2` → `coadd2` | `coadd2/config/deep_compareWarpAssembleCoadd.py` and backups |
| 8 | `detectCoaddSources.py` | `coadd2` → `coaddMeasure` | `coaddMeasure/config/detect.py` |
| 9 | `mergeCoaddDetections.py` | `coaddMeasure` → same | `coaddMeasure/config/mergeDetect.py` |
| 10 | `deblendCoaddSources.py` | `coaddMeasure` → same | `coaddMeasure/config/deblend.py` |
| 11 | `measureCoaddSources.py` | `coaddMeasure` → `coaddMeasure2` | `coaddMeasure2/config/measureMerged.py` and backups |
| 12 | `mergeCoaddMeasurements.py` | `coaddMeasure2` → same | `coaddMeasure2/config/mergeMeasure.py` |
| 13 | `forcedPhotCoadd.py` | `coaddMeasure2` → `coaddForcedPhot` | `coaddForcedPhot/config/forcedPhotCoadd.py` |

The saved skymap override specifies TAN projection, 4000 × 4000-pixel inner
patches and 0.185 arcsec/pixel. The recorded visit lists and patch lists preserve
the actual selectors. `02_skyMap.sh` calls an external `get_skymap_corner.py`
helper that was not recovered; the resulting patch lists *are* included.

## Command pattern (not an executable recipe until gaps are resolved)

For example, for a single field and band, after preparing a clean work directory
containing that field's selectors and verified configurations:

```bash
source "$LSST_V19_ROOT/loadLSST.bash"
setup lsst_distrib
ingestImages.py DATA rawData/*.fz --mode=link
processCcd.py DATA @list_process_r.list --rerun processCcdOutputs_noct \
    -C verified_configs/processCcd_r.py -j 4
makeDiscreteSkyMap.py DATA @list_process_u.list @list_process_g.list \
    @list_process_r.list @list_process_i.list \
    --rerun processCcdOutputs_noct:coadd -C verified_configs/makeDiscreteSkyMap.py
jointcal.py DATA --rerun coadd:jointcal @list_jc_r.list \
    -C verified_configs/jointcal_r.py -j 4
makeCoaddTempExp.py DATA --rerun jointcal:coadd2 @select_r.list @patches_r.txt \
    -C verified_configs/makeCoaddTempExp.py -j 4
assembleCoadd.py --warpCompare DATA --rerun coadd2 @select_r.list @patches_r.txt \
    -C verified_configs/assembleCoadd.py -j 4
detectCoaddSources.py DATA --rerun coadd2:coaddMeasure @patches_r.txt \
    -C verified_configs/detect.py -j 4
```

`verified_configs/` is deliberately **not supplied as a fabricated per-band
selection**. These files must be assembled from the recovered records after
the unresolved provenance is confirmed. Repeat single-band steps for u2/g2/r2/i3
and then merge detections with `--id filter=u2^g2^r2^i3`. Deblend per band,
measure per band into `coaddMeasure2`, merge measurements across the four filters,
and run forced photometry per band into `coaddForcedPhot`, in the order above.
The original invocations and selectors are preserved in each field's `commands/`
and `log_excerpts.txt`; they provide the remaining task arguments without
pretending that the last edited shell files record every executed run.

The historical scripts contain `--clobber-config`. Do not use that option to
conceal a configuration mismatch or to overwrite an existing science repository.
Reruns such as `coadd2_0325_ugri`, `coadd2_old_r` and `*_0527` are retained as
alternative historical records, not silently selected as final products.

After LSST catalog measurement/extraction, the author applies color-term and
photometric corrections at catalog level following LoVoCCS; see
[catalog calibration](../photometry/README.md) for the coefficients and source
modules. This separate post-processing stage does not change LSST images and
must not be duplicated by enabling LSST color terms. Its exact historical
CFHT invocation is not inferred from upstream DECam defaults.

Visit-level PSF QC reads the single-epoch products independently of this catalog
calibration. Limiting-magnitude analyses require the appropriate calibrated
catalogs. See [QC instructions](../qc/README.md).
Weak-lensing map generation and related downstream analyses are out of scope.
