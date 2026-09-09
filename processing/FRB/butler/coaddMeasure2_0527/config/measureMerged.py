import lsst.pipe.tasks.multiBand
assert type(config)==lsst.pipe.tasks.multiBand.MeasureMergedCoaddSourcesConfig, 'config is of type %s.%s instead of lsst.pipe.tasks.multiBand.MeasureMergedCoaddSourcesConfig' % (type(config).__module__, type(config).__name__)
import lsst.meas.base.plugins
import lsst.meas.algorithms.loadIndexedReferenceObjects
import lsst.meas.base.catalogCalculation
import lsst.meas.base.footprintArea
import lsst.meas.base.baseMeasurement
import lsst.meas.astrom.directMatch
import lsst.meas.base.gaussianFlux
import lsst.meas.base.sfm
import lsst.meas.base.scaledApertureFlux
import lsst.meas.base.wrappers
import lsst.meas.base.peakLikelihoodFlux
import lsst.meas.base.noiseReplacer
import lsst.meas.base.pixelFlags
import lsst.meas.base.localBackground
import lsst.meas.base.applyApCorr
import lsst.meas.base.classification
import lsst.pipe.base.config
import lsst.meas.base.naiveCentroid
import lsst.pipe.tasks.setPrimaryFlags
import lsst.meas.base.sdssCentroid
import lsst.meas.base.blendedness
import lsst.meas.base.sdssShape
import lsst.meas.base.apertureFlux
import lsst.meas.algorithms.sourceSelector
import lsst.pipe.tasks.propagateVisitFlags
import lsst.meas.base.psfFlux
# Name of the input catalog to use.If the single band deblender was used this should be 'deblendedFlux.If the multi-band deblender was used this should be 'deblendedModel.If no deblending was performed this should be 'mergeDet'
config.inputCatalog='deblendedFlux'

# the name of the centroiding algorithm used to set source x,y
config.measurement.slots.centroid='base_SdssCentroid'

# the name of the algorithm used to set source moments parameters
config.measurement.slots.shape='base_SdssShape'

# the name of the algorithm used to set PSF moments parameters
config.measurement.slots.psfShape='base_SdssShape_psf'

# the name of the algorithm used to set the source aperture instFlux slot
config.measurement.slots.apFlux='base_CircularApertureFlux_12_0'

# the name of the algorithm used to set the source model instFlux slot
config.measurement.slots.modelFlux='base_GaussianFlux'

# the name of the algorithm used to set the source psf instFlux slot
config.measurement.slots.psfFlux='base_PsfFlux'

# the name of the algorithm used to set the source Gaussian instFlux slot
config.measurement.slots.gaussianFlux='base_GaussianFlux'

# the name of the instFlux measurement algorithm used for calibration
config.measurement.slots.calibFlux='base_CircularApertureFlux_12_0'

# When measuring, replace other detected footprints with noise?
config.measurement.doReplaceWithNoise=True

# How to choose mean and variance of the Gaussian noise we generate?
config.measurement.noiseReplacer.noiseSource='measure'

# Add ann offset to the generated noise.
config.measurement.noiseReplacer.noiseOffset=0.0

# The seed multiplier value to use for random number generation:
# >= 1: set the seed deterministically based on exposureId
# 0: fall back to the afw.math.Random default constructor (which uses a seed value of 1)
config.measurement.noiseReplacer.noiseSeedMultiplier=1

# Prefix to give undeblended plugins
config.measurement.undeblendedPrefix='undeblended_'

# whether to run this plugin in single-object mode
config.measurement.plugins['base_PsfFlux'].doMeasure=True

# Mask planes that indicate pixels that should be excluded from the fit
config.measurement.plugins['base_PsfFlux'].badMaskPlanes=[]

# whether to run this plugin in single-object mode
config.measurement.plugins['base_PeakLikelihoodFlux'].doMeasure=True

# Name of warping kernel (e.g. "lanczos4") used to compute the peak
config.measurement.plugins['base_PeakLikelihoodFlux'].warpingKernelName='lanczos4'

# whether to run this plugin in single-object mode
config.measurement.plugins['base_GaussianFlux'].doMeasure=True

# FIXME! NEVER DOCUMENTED!
config.measurement.plugins['base_GaussianFlux'].background=0.0

# whether to run this plugin in single-object mode
config.measurement.plugins['base_NaiveCentroid'].doMeasure=True

# Value to subtract from the image pixel values
config.measurement.plugins['base_NaiveCentroid'].background=0.0

# Do check that the centroid is contained in footprint.
config.measurement.plugins['base_NaiveCentroid'].doFootprintCheck=True

# If set > 0, Centroid Check also checks distance from footprint peak.
config.measurement.plugins['base_NaiveCentroid'].maxDistToPeak=-1.0

# whether to run this plugin in single-object mode
config.measurement.plugins['base_SdssCentroid'].doMeasure=True

# maximum allowed binning
config.measurement.plugins['base_SdssCentroid'].binmax=16

# Do check that the centroid is contained in footprint.
config.measurement.plugins['base_SdssCentroid'].doFootprintCheck=True

# If set > 0, Centroid Check also checks distance from footprint peak.
config.measurement.plugins['base_SdssCentroid'].maxDistToPeak=-1.0

# if the peak's less than this insist on binning at least once
config.measurement.plugins['base_SdssCentroid'].peakMin=-1.0

# fiddle factor for adjusting the binning
config.measurement.plugins['base_SdssCentroid'].wfac=1.5

# whether to run this plugin in single-object mode
config.measurement.plugins['base_PixelFlags'].doMeasure=True

# List of mask planes to be searched for which occur anywhere within a footprint. If any of the planes are found they will have a corresponding pixel flag set.
config.measurement.plugins['base_PixelFlags'].masksFpAnywhere=['CLIPPED', 'SENSOR_EDGE', 'INEXACT_PSF']

# List of mask planes to be searched for which occur in the center of a footprint. If any of the planes are found they will have a corresponding pixel flag set.
config.measurement.plugins['base_PixelFlags'].masksFpCenter=['CLIPPED', 'SENSOR_EDGE', 'INEXACT_PSF']

# whether to run this plugin in single-object mode
config.measurement.plugins['base_SdssShape'].doMeasure=True

# Additional value to add to background
config.measurement.plugins['base_SdssShape'].background=0.0

# Whether to also compute the shape of the PSF model
config.measurement.plugins['base_SdssShape'].doMeasurePsf=True

# Maximum number of iterations
config.measurement.plugins['base_SdssShape'].maxIter=100

# Maximum centroid shift, limited to 2-10
config.measurement.plugins['base_SdssShape'].maxShift=0.0

# Convergence tolerance for e1,e2
config.measurement.plugins['base_SdssShape'].tol1=9.999999747378752e-06

# Convergence tolerance for FWHM
config.measurement.plugins['base_SdssShape'].tol2=9.999999747378752e-05

# whether to run this plugin in single-object mode
config.measurement.plugins['base_ScaledApertureFlux'].doMeasure=True

# Scaling factor of PSF FWHM for aperture radius.
config.measurement.plugins['base_ScaledApertureFlux'].scale=3.14

# Warping kernel used to shift Sinc photometry coefficients to different center positions
config.measurement.plugins['base_ScaledApertureFlux'].shiftKernel='lanczos5'

# whether to run this plugin in single-object mode
config.measurement.plugins['base_CircularApertureFlux'].doMeasure=True

# Maximum radius (in pixels) for which the sinc algorithm should be used instead of the faster naive algorithm.  For elliptical apertures, this is the minor axis radius.
config.measurement.plugins['base_CircularApertureFlux'].maxSincRadius=10.0

# Radius (in pixels) of apertures.
config.measurement.plugins['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]

# Warping kernel used to shift Sinc photometry coefficients to different center positions
config.measurement.plugins['base_CircularApertureFlux'].shiftKernel='lanczos5'

# whether to run this plugin in single-object mode
config.measurement.plugins['base_Blendedness'].doMeasure=True

# Whether to compute quantities related to the Gaussian-weighted flux
config.measurement.plugins['base_Blendedness'].doFlux=True

# Whether to compute HeavyFootprint dot products (the old deblend.blendedness parameter)
config.measurement.plugins['base_Blendedness'].doOld=True

# Whether to compute quantities related to the Gaussian-weighted shape
config.measurement.plugins['base_Blendedness'].doShape=True

# Radius factor that sets the maximum extent of the weight function (and hence the flux measurements)
config.measurement.plugins['base_Blendedness'].nSigmaWeightMax=3.0

# whether to run this plugin in single-object mode
config.measurement.plugins['base_LocalBackground'].doMeasure=True

# Inner radius for background annulus as a multiple of the PSF sigma
config.measurement.plugins['base_LocalBackground'].annulusInner=7.0

# Outer radius for background annulus as a multiple of the PSF sigma
config.measurement.plugins['base_LocalBackground'].annulusOuter=15.0

# Mask planes that indicate pixels that should be excluded from the measurement
config.measurement.plugins['base_LocalBackground'].badMaskPlanes=['BAD', 'SAT', 'NO_DATA']

# Number of sigma-clipping iterations for background measurement
config.measurement.plugins['base_LocalBackground'].bgIter=3

# Rejection threshold (in standard deviations) for background measurement
config.measurement.plugins['base_LocalBackground'].bgRej=3.0

# whether to run this plugin in single-object mode
config.measurement.plugins['base_FPPosition'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.plugins['base_Jacobian'].doMeasure=True

# Nominal pixel size (arcsec)
config.measurement.plugins['base_Jacobian'].pixelScale=0.5

# whether to run this plugin in single-object mode
config.measurement.plugins['base_Variance'].doMeasure=True

# Scale factor to apply to shape for aperture
config.measurement.plugins['base_Variance'].scale=5.0

# Mask planes to ignore
config.measurement.plugins['base_Variance'].mask=['DETECTED', 'DETECTED_NEGATIVE', 'BAD', 'SAT']

# whether to run this plugin in single-object mode
config.measurement.plugins['base_InputCount'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.plugins['base_PeakCentroid'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.plugins['base_SkyCoord'].doMeasure=True

config.measurement.plugins.names=['base_NaiveCentroid', 'base_LocalBackground', 'base_PsfFlux', 'base_PixelFlags', 'base_GaussianFlux', 'base_CircularApertureFlux', 'base_Blendedness', 'base_SdssShape', 'base_InputCount', 'base_SdssCentroid', 'base_Variance', 'base_SkyCoord']
# whether to run this plugin in single-object mode
config.measurement.undeblended['base_PsfFlux'].doMeasure=True

# Mask planes that indicate pixels that should be excluded from the fit
config.measurement.undeblended['base_PsfFlux'].badMaskPlanes=[]

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_PeakLikelihoodFlux'].doMeasure=True

# Name of warping kernel (e.g. "lanczos4") used to compute the peak
config.measurement.undeblended['base_PeakLikelihoodFlux'].warpingKernelName='lanczos4'

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_GaussianFlux'].doMeasure=True

# FIXME! NEVER DOCUMENTED!
config.measurement.undeblended['base_GaussianFlux'].background=0.0

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_NaiveCentroid'].doMeasure=True

# Value to subtract from the image pixel values
config.measurement.undeblended['base_NaiveCentroid'].background=0.0

# Do check that the centroid is contained in footprint.
config.measurement.undeblended['base_NaiveCentroid'].doFootprintCheck=True

# If set > 0, Centroid Check also checks distance from footprint peak.
config.measurement.undeblended['base_NaiveCentroid'].maxDistToPeak=-1.0

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_SdssCentroid'].doMeasure=True

# maximum allowed binning
config.measurement.undeblended['base_SdssCentroid'].binmax=16

# Do check that the centroid is contained in footprint.
config.measurement.undeblended['base_SdssCentroid'].doFootprintCheck=True

# If set > 0, Centroid Check also checks distance from footprint peak.
config.measurement.undeblended['base_SdssCentroid'].maxDistToPeak=-1.0

# if the peak's less than this insist on binning at least once
config.measurement.undeblended['base_SdssCentroid'].peakMin=-1.0

# fiddle factor for adjusting the binning
config.measurement.undeblended['base_SdssCentroid'].wfac=1.5

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_PixelFlags'].doMeasure=True

# List of mask planes to be searched for which occur anywhere within a footprint. If any of the planes are found they will have a corresponding pixel flag set.
config.measurement.undeblended['base_PixelFlags'].masksFpAnywhere=[]

# List of mask planes to be searched for which occur in the center of a footprint. If any of the planes are found they will have a corresponding pixel flag set.
config.measurement.undeblended['base_PixelFlags'].masksFpCenter=[]

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_SdssShape'].doMeasure=True

# Additional value to add to background
config.measurement.undeblended['base_SdssShape'].background=0.0

# Whether to also compute the shape of the PSF model
config.measurement.undeblended['base_SdssShape'].doMeasurePsf=True

# Maximum number of iterations
config.measurement.undeblended['base_SdssShape'].maxIter=100

# Maximum centroid shift, limited to 2-10
config.measurement.undeblended['base_SdssShape'].maxShift=0.0

# Convergence tolerance for e1,e2
config.measurement.undeblended['base_SdssShape'].tol1=9.999999747378752e-06

# Convergence tolerance for FWHM
config.measurement.undeblended['base_SdssShape'].tol2=9.999999747378752e-05

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_ScaledApertureFlux'].doMeasure=True

# Scaling factor of PSF FWHM for aperture radius.
config.measurement.undeblended['base_ScaledApertureFlux'].scale=3.14

# Warping kernel used to shift Sinc photometry coefficients to different center positions
config.measurement.undeblended['base_ScaledApertureFlux'].shiftKernel='lanczos5'

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_CircularApertureFlux'].doMeasure=True

# Maximum radius (in pixels) for which the sinc algorithm should be used instead of the faster naive algorithm.  For elliptical apertures, this is the minor axis radius.
config.measurement.undeblended['base_CircularApertureFlux'].maxSincRadius=10.0

# Radius (in pixels) of apertures.
config.measurement.undeblended['base_CircularApertureFlux'].radii=[3.0, 4.5, 6.0, 9.0, 12.0, 17.0, 25.0, 35.0, 50.0, 70.0]

# Warping kernel used to shift Sinc photometry coefficients to different center positions
config.measurement.undeblended['base_CircularApertureFlux'].shiftKernel='lanczos5'

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_Blendedness'].doMeasure=True

# Whether to compute quantities related to the Gaussian-weighted flux
config.measurement.undeblended['base_Blendedness'].doFlux=True

# Whether to compute HeavyFootprint dot products (the old deblend.blendedness parameter)
config.measurement.undeblended['base_Blendedness'].doOld=True

# Whether to compute quantities related to the Gaussian-weighted shape
config.measurement.undeblended['base_Blendedness'].doShape=True

# Radius factor that sets the maximum extent of the weight function (and hence the flux measurements)
config.measurement.undeblended['base_Blendedness'].nSigmaWeightMax=3.0

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_LocalBackground'].doMeasure=True

# Inner radius for background annulus as a multiple of the PSF sigma
config.measurement.undeblended['base_LocalBackground'].annulusInner=7.0

# Outer radius for background annulus as a multiple of the PSF sigma
config.measurement.undeblended['base_LocalBackground'].annulusOuter=15.0

# Mask planes that indicate pixels that should be excluded from the measurement
config.measurement.undeblended['base_LocalBackground'].badMaskPlanes=['BAD', 'SAT', 'NO_DATA']

# Number of sigma-clipping iterations for background measurement
config.measurement.undeblended['base_LocalBackground'].bgIter=3

# Rejection threshold (in standard deviations) for background measurement
config.measurement.undeblended['base_LocalBackground'].bgRej=3.0

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_FPPosition'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_Jacobian'].doMeasure=True

# Nominal pixel size (arcsec)
config.measurement.undeblended['base_Jacobian'].pixelScale=0.5

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_Variance'].doMeasure=True

# Scale factor to apply to shape for aperture
config.measurement.undeblended['base_Variance'].scale=5.0

# Mask planes to ignore
config.measurement.undeblended['base_Variance'].mask=['DETECTED', 'DETECTED_NEGATIVE', 'BAD', 'SAT']

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_InputCount'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_PeakCentroid'].doMeasure=True

# whether to run this plugin in single-object mode
config.measurement.undeblended['base_SkyCoord'].doMeasure=True

config.measurement.undeblended.names=[]
# Name of field in schema with number of deblended children
config.setPrimaryFlags.nChildKeyName='deblend_nChild'

# Names of filters which should never be primary
config.setPrimaryFlags.pseudoFilterList=['sky']

# Whether to match sources to CCD catalogs to propagate flags (to e.g. identify PSF stars)
config.doPropagateFlags=True

# Source catalog flags to propagate, with the threshold of relative occurrence (valid range: [0-1], default is 0.2).  Coadd object will have flag set if the fraction of input visits in which it is flagged is greater than the threshold.
config.propagateFlags.flags={'calib_psf_candidate': 0.2, 'calib_psf_used': 0.2, 'calib_psf_reserved': 0.2, 'calib_astrometry_used': 0.2, 'calib_photometry_used': 0.2, 'calib_photometry_reserved': 0.2}

# Source matching radius (arcsec)
config.propagateFlags.matchRadius=0.2

# Name of ccd to give to butler
config.propagateFlags.ccdName='ccd'

# Match sources to reference catalog?
config.doMatchSources=True

# Matching radius, arcsec
config.match.matchRadius=0.25

# Apply flux limit?
config.match.sourceSelection.doFluxLimit=False

# Apply flag limitation?
config.match.sourceSelection.doFlags=False

# Apply unresolved limitation?
config.match.sourceSelection.doUnresolved=False

# Apply signal-to-noise limit?
config.match.sourceSelection.doSignalToNoise=False

# Apply isolated limitation?
config.match.sourceSelection.doIsolated=False

# Select objects with value greater than this
config.match.sourceSelection.fluxLimit.minimum=None

# Select objects with value less than this
config.match.sourceSelection.fluxLimit.maximum=None

# Name of the source flux field to use.
config.match.sourceSelection.fluxLimit.fluxField='slot_CalibFlux_instFlux'

# List of source flag fields that must be set for a source to be used.
config.match.sourceSelection.flags.good=[]

# List of source flag fields that must NOT be set for a source to be used.
config.match.sourceSelection.flags.bad=['base_PixelFlags_flag_edge', 'base_PixelFlags_flag_saturated', 'base_PsfFlux_flags']

# Select objects with value greater than this
config.match.sourceSelection.unresolved.minimum=None

# Select objects with value less than this
config.match.sourceSelection.unresolved.maximum=0.5

# Name of column for star/galaxy separation
config.match.sourceSelection.unresolved.name='base_ClassificationExtendedness_value'

# Select objects with value greater than this
config.match.sourceSelection.signalToNoise.minimum=None

# Select objects with value less than this
config.match.sourceSelection.signalToNoise.maximum=None

# Name of the source flux field to use.
config.match.sourceSelection.signalToNoise.fluxField='base_PsfFlux_instFlux'

# Name of the source flux error field to use.
config.match.sourceSelection.signalToNoise.errField='base_PsfFlux_instFluxErr'

# Name of column for parent
config.match.sourceSelection.isolated.parentName='parent'

# Name of column for nChild
config.match.sourceSelection.isolated.nChildName='deblend_nChild'

# Apply magnitude limit?
config.match.referenceSelection.doMagLimit=False

# Apply flag limitation?
config.match.referenceSelection.doFlags=False

# Apply unresolved limitation?
config.match.referenceSelection.doUnresolved=False

# Apply signal-to-noise limit?
config.match.referenceSelection.doSignalToNoise=False

# Apply magnitude error limit?
config.match.referenceSelection.doMagError=False

# Select objects with value greater than this
config.match.referenceSelection.magLimit.minimum=None

# Select objects with value less than this
config.match.referenceSelection.magLimit.maximum=None

# Name of the source flux field to use.
config.match.referenceSelection.magLimit.fluxField='flux'

# List of source flag fields that must be set for a source to be used.
config.match.referenceSelection.flags.good=[]

# List of source flag fields that must NOT be set for a source to be used.
config.match.referenceSelection.flags.bad=[]

# Select objects with value greater than this
config.match.referenceSelection.unresolved.minimum=None

# Select objects with value less than this
config.match.referenceSelection.unresolved.maximum=0.5

# Name of column for star/galaxy separation
config.match.referenceSelection.unresolved.name='base_ClassificationExtendedness_value'

# Select objects with value greater than this
config.match.referenceSelection.signalToNoise.minimum=None

# Select objects with value less than this
config.match.referenceSelection.signalToNoise.maximum=None

# Name of the source flux field to use.
config.match.referenceSelection.signalToNoise.fluxField='flux'

# Name of the source flux error field to use.
config.match.referenceSelection.signalToNoise.errField='flux_err'

# Select objects with value greater than this
config.match.referenceSelection.magError.minimum=None

# Select objects with value less than this
config.match.referenceSelection.magError.maximum=None

# Name of the source flux error field to use.
config.match.referenceSelection.magError.magErrField='mag_err'

config.match.referenceSelection.colorLimits={}
# Padding to add to 4 all edges of the bounding box (pixels)
config.match.refObjLoader.pixelMargin=300

# Default reference catalog filter to use if filter not specified in exposure; if blank then filter must be specified in exposure
config.match.refObjLoader.defaultFilter=''

# Mapping of camera filter name: reference catalog filter name; each reference filter must exist
config.match.refObjLoader.filterMap={'g2': 'g', 'r2': 'r'}

# Require that the fields needed to correct proper motion (epoch, pm_ra and pm_dec) are present?
config.match.refObjLoader.requireProperMotion=False

# Name of the ingested reference dataset
config.match.refObjLoader.ref_dataset_name='pan-starrs'

# Write reference matches in denormalized format? This format uses more disk space, but is more convenient to read.
config.doWriteMatchesDenormalized=False

# Name of coadd
config.coaddName='deep'

# Size of psfCache
config.psfCache=100

# Strictness of Astropy unit compatibility check, can be 'raise', 'warn' or 'silent'
config.checkUnitsParseStrict='raise'

# Apply aperture corrections
config.doApCorr=True

# flux measurement algorithms in getApCorrNameSet() to ignore; if a name is listed that does not appear in getApCorrNameSet() then a warning is logged
config.applyApCorr.ignoreList=[]

# set the general failure flag for a flux when it cannot be aperture-corrected?
config.applyApCorr.doFlagApCorrFailures=True

# flux measurement algorithms to be aperture-corrected by reference to another algorithm; this is a mapping alg1:alg2, where 'alg1' is the algorithm being corrected, and 'alg2' is the algorithm supplying the corrections
config.applyApCorr.proxies={}

# Run catalogCalculation task
config.doRunCatalogCalculation=True

# critical ratio of model to psf flux
config.catalogCalculation.plugins['base_ClassificationExtendedness'].fluxRatio=0.925

# correction factor for modelFlux error
config.catalogCalculation.plugins['base_ClassificationExtendedness'].modelErrFactor=0.0

# correction factor for psfFlux error
config.catalogCalculation.plugins['base_ClassificationExtendedness'].psfErrFactor=0.0

config.catalogCalculation.plugins.names=['base_ClassificationExtendedness', 'base_FootprintArea']
# Should be set to True if fake sources have been inserted into the input data.
config.hasFakes=False

# name for connection inputSchema
config.connections.inputSchema='{inputCoaddName}Coadd_deblendedFlux_schema'

# name for connection outputSchema
config.connections.outputSchema='{inputCoaddName}Coadd_meas_schema'

# name for connection refCat
config.connections.refCat='pan-starrs'

# name for connection exposure
config.connections.exposure='{inputCoaddName}Coadd_calexp'

# name for connection skyMap
config.connections.skyMap='{inputCoaddName}Coadd_skyMap'

# name for connection visitCatalogs
config.connections.visitCatalogs='src'

# name for connection inputCatalog
config.connections.inputCatalog='{inputCoaddName}Coadd_deblendedFlux'

# name for connection outputSources
config.connections.outputSources='{outputCoaddName}Coadd_meas'

# name for connection matchResult
config.connections.matchResult='{outputCoaddName}Coadd_measMatch'

# name for connection denormMatches
config.connections.denormMatches='{outputCoaddName}Coadd_measMatchFull'

# Template parameter used to format corresponding field template parameter
config.connections.inputCoaddName='deep'

# Template parameter used to format corresponding field template parameter
config.connections.outputCoaddName='deep'

