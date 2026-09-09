import lsst.pipe.tasks.mergeDetections
assert type(config)==lsst.pipe.tasks.mergeDetections.MergeDetectionsConfig, 'config is of type %s.%s instead of lsst.pipe.tasks.mergeDetections.MergeDetectionsConfig' % (type(config).__module__, type(config).__name__)
import lsst.pipe.tasks.multiBandUtils
import lsst.meas.algorithms.skyObjects
import lsst.pipe.base.config
# Minimum distance from closest peak to create a new one (in arcsec).
config.minNewPeak=1.0

# When adding new catalogs to the merge, all peaks less than this distance  (in arcsec) to an existing peak will be flagged as detected in that catalog.
config.maxSamePeak=0.3

# Always keep peaks detected in this many bands
config.cullPeaks.nBandsSufficient=2

# Always keep this many peaks in each family
config.cullPeaks.rankSufficient=20

# Keep peaks with less than this rank that also match the rankNormalizedConsidered condition.
config.cullPeaks.rankConsidered=30

# Keep peaks with less than this normalized rank that also match the rankConsidered condition.
config.cullPeaks.rankNormalizedConsidered=0.7

# Name of `filter' used to label sky objects (e.g. flag merge_peak_sky is set)
# (N.b. should be in MergeMeasurementsConfig.pseudoFilterList)
config.skyFilterName='sky'

# Avoid pixels masked with these mask planes
config.skyObjects.avoidMask=['DETECTED']

# Number of pixels to grow the masked pixels when adding sky objects
config.skyObjects.growMask=0

# Radius, in pixels, of sky objects
config.skyObjects.sourceRadius=8.0

# Try to add this many sky objects
config.skyObjects.nSources=100

# Maximum number of trial sky object positions
# (default: nSkySources*nTrialSkySourcesMultiplier)
config.skyObjects.nTrialSources=None

# Set nTrialSkySources to
#     nSkySources*nTrialSkySourcesMultiplier
# if nTrialSkySources is None
config.skyObjects.nTrialSourcesMultiplier=5

# Priority-ordered list of bands for the merge.
config.priorityList=['i3', 'r2', 'g2', 'u2']

# Name of coadd
config.coaddName='deep'

# name for connection schema
config.connections.schema='{inputCoaddName}Coadd_det_schema'

# name for connection outputSchema
config.connections.outputSchema='{outputCoaddName}Coadd_mergeDet_schema'

# name for connection outputPeakSchema
config.connections.outputPeakSchema='{outputCoaddName}Coadd_peak_schema'

# name for connection catalogs
config.connections.catalogs='{inputCoaddName}Coadd_det'

# name for connection skyMap
config.connections.skyMap='{inputCoaddName}Coadd_skyMap'

# name for connection outputCatalog
config.connections.outputCatalog='{outputCoaddName}Coadd_mergeDet'

# Template parameter used to format corresponding field template parameter
config.connections.inputCoaddName='deep'

# Template parameter used to format corresponding field template parameter
config.connections.outputCoaddName='deep'

