import lsst.pipe.tasks.mergeMeasurements
assert type(config)==lsst.pipe.tasks.mergeMeasurements.MergeMeasurementsConfig, 'config is of type %s.%s instead of lsst.pipe.tasks.mergeMeasurements.MergeMeasurementsConfig' % (type(config).__module__, type(config).__name__)
import lsst.pipe.base.config
# Names of filters which may have no associated detection
# (N.b. should include MergeDetectionsConfig.skyFilterName)
config.pseudoFilterList=['sky']

# Name of flux measurement for calculating the S/N when choosing the reference band.
config.snName='base_PsfFlux'

# If the S/N from the priority band is below this value (and the S/N is larger than minSNDiff compared to the priority band), use the band with the largest S/N as the reference band.
config.minSN=10.0

# If the difference in S/N between another band and the priority band is larger than this value (and the S/N in the priority band is less than minSN) use the band with the largest S/N as the reference band
config.minSNDiff=3.0

# Require that these flags, if available, are not set
config.flags=['base_PixelFlags_flag_interpolatedCenter', 'base_PsfFlux_flag', 'ext_photometryKron_KronFlux_flag', 'modelfit_CModel_flag']

# Priority-ordered list of bands for the merge.
config.priorityList=['r2', 'i3', 'g2', 'u2']

# Name of coadd
config.coaddName='deep'

# name for connection inputSchema
config.connections.inputSchema='{inputCoaddName}Coadd_meas_schema'

# name for connection outputSchema
config.connections.outputSchema='{outputCoaddName}Coadd_ref_schema'

# name for connection catalogs
config.connections.catalogs='{inputCoaddName}Coadd_meas'

# name for connection mergedCatalog
config.connections.mergedCatalog='{outputCoaddName}Coadd_ref'

# Template parameter used to format corresponding field template parameter
config.connections.inputCoaddName='deep'

# Template parameter used to format corresponding field template parameter
config.connections.outputCoaddName='deep'

