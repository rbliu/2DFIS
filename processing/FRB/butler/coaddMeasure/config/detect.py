import lsst.pipe.tasks.multiBand
assert type(config)==lsst.pipe.tasks.multiBand.DetectCoaddSourcesConfig, 'config is of type %s.%s instead of lsst.pipe.tasks.multiBand.DetectCoaddSourcesConfig' % (type(config).__module__, type(config).__name__)
import lsst.pipe.tasks.fakes
import lsst.meas.algorithms.dynamicDetection
import lsst.pipe.base.config
import lsst.meas.algorithms.subtractBackground
import lsst.pipe.tasks.scaleVariance
import lsst.meas.algorithms.skyObjects
# Scale variance plane using empirical noise?
config.doScaleVariance=True

# type of statistic to use for grid points
config.scaleVariance.background.statisticsProperty='MEANCLIP'

# behaviour if there are too few points in grid for requested interpolation style
config.scaleVariance.background.undersampleStyle='REDUCE_INTERP_ORDER'

# how large a region of the sky should be used for each background point
config.scaleVariance.background.binSize=32

# Sky region size to be used for each background point in X direction. If 0, the binSize config is used.
config.scaleVariance.background.binSizeX=0

# Sky region size to be used for each background point in Y direction. If 0, the binSize config is used.
config.scaleVariance.background.binSizeY=0

# how to interpolate the background values. This maps to an enum; see afw::math::Background
config.scaleVariance.background.algorithm='AKIMA_SPLINE'

# Names of mask planes to ignore while estimating the background
config.scaleVariance.background.ignoredPixelMask=['DETECTED', 'DETECTED_NEGATIVE', 'BAD', 'SAT', 'NO_DATA', 'INTRP']

# Ignore NaNs when estimating the background
config.scaleVariance.background.isNanSafe=False

# Use Approximate (Chebyshev) to model background.
config.scaleVariance.background.useApprox=False

# Approximation order in X for background Chebyshev (valid only with useApprox=True)
config.scaleVariance.background.approxOrderX=6

# Approximation order in Y for background Chebyshev (valid only with useApprox=True)
config.scaleVariance.background.approxOrderY=-1

# Use inverse variance weighting in calculation (valid only with useApprox=True)
config.scaleVariance.background.weighting=True

# Mask planes for pixels to ignore when scaling variance
config.scaleVariance.maskPlanes=['DETECTED', 'DETECTED_NEGATIVE', 'BAD', 'SAT', 'NO_DATA', 'INTRP']

# Maximum variance scaling value to permit
config.scaleVariance.limit=10.0

# detected sources with fewer than the specified number of pixels will be ignored
config.detection.minPixels=1

# Pixels should be grown as isotropically as possible (slower)
config.detection.isotropicGrow=True

# Grow all footprints at the same time? This allows disconnected footprints to merge.
config.detection.combinedGrow=True

# Grow detections by nSigmaToGrow * [PSF RMS width]; if 0 then do not grow
config.detection.nSigmaToGrow=2.4

# Grow detections to set the image mask bits, but return the original (not-grown) footprints
config.detection.returnOriginalFootprints=False

# Threshold for footprints; exact meaning and units depend on thresholdType.
config.detection.thresholdValue=5.0

# Include threshold relative to thresholdValue
config.detection.includeThresholdMultiplier=1.0

# specifies the desired flavor of Threshold
config.detection.thresholdType='pixel_stdev'

# specifies whether to detect positive, or negative sources, or both
config.detection.thresholdPolarity='positive'

# Fiddle factor to add to the background; debugging only
config.detection.adjustBackground=0.0

# Estimate the background again after final source detection?
config.detection.reEstimateBackground=False

# type of statistic to use for grid points
config.detection.background.statisticsProperty='MEANCLIP'

# behaviour if there are too few points in grid for requested interpolation style
config.detection.background.undersampleStyle='REDUCE_INTERP_ORDER'

# how large a region of the sky should be used for each background point
config.detection.background.binSize=4096

# Sky region size to be used for each background point in X direction. If 0, the binSize config is used.
config.detection.background.binSizeX=0

# Sky region size to be used for each background point in Y direction. If 0, the binSize config is used.
config.detection.background.binSizeY=0

# how to interpolate the background values. This maps to an enum; see afw::math::Background
config.detection.background.algorithm='AKIMA_SPLINE'

# Names of mask planes to ignore while estimating the background
config.detection.background.ignoredPixelMask=['BAD', 'EDGE', 'DETECTED', 'DETECTED_NEGATIVE', 'NO_DATA']

# Ignore NaNs when estimating the background
config.detection.background.isNanSafe=False

# Use Approximate (Chebyshev) to model background.
config.detection.background.useApprox=False

# Approximation order in X for background Chebyshev (valid only with useApprox=True)
config.detection.background.approxOrderX=6

# Approximation order in Y for background Chebyshev (valid only with useApprox=True)
config.detection.background.approxOrderY=-1

# Use inverse variance weighting in calculation (valid only with useApprox=True)
config.detection.background.weighting=True

# type of statistic to use for grid points
config.detection.tempLocalBackground.statisticsProperty='MEANCLIP'

# behaviour if there are too few points in grid for requested interpolation style
config.detection.tempLocalBackground.undersampleStyle='REDUCE_INTERP_ORDER'

# how large a region of the sky should be used for each background point
config.detection.tempLocalBackground.binSize=64

# Sky region size to be used for each background point in X direction. If 0, the binSize config is used.
config.detection.tempLocalBackground.binSizeX=0

# Sky region size to be used for each background point in Y direction. If 0, the binSize config is used.
config.detection.tempLocalBackground.binSizeY=0

# how to interpolate the background values. This maps to an enum; see afw::math::Background
config.detection.tempLocalBackground.algorithm='AKIMA_SPLINE'

# Names of mask planes to ignore while estimating the background
config.detection.tempLocalBackground.ignoredPixelMask=['BAD', 'EDGE', 'DETECTED', 'DETECTED_NEGATIVE', 'NO_DATA']

# Ignore NaNs when estimating the background
config.detection.tempLocalBackground.isNanSafe=False

# Use Approximate (Chebyshev) to model background.
config.detection.tempLocalBackground.useApprox=False

# Approximation order in X for background Chebyshev (valid only with useApprox=True)
config.detection.tempLocalBackground.approxOrderX=6

# Approximation order in Y for background Chebyshev (valid only with useApprox=True)
config.detection.tempLocalBackground.approxOrderY=-1

# Use inverse variance weighting in calculation (valid only with useApprox=True)
config.detection.tempLocalBackground.weighting=True

# Enable temporary local background subtraction? (see tempLocalBackground)
config.detection.doTempLocalBackground=True

# type of statistic to use for grid points
config.detection.tempWideBackground.statisticsProperty='MEANCLIP'

# behaviour if there are too few points in grid for requested interpolation style
config.detection.tempWideBackground.undersampleStyle='REDUCE_INTERP_ORDER'

# how large a region of the sky should be used for each background point
config.detection.tempWideBackground.binSize=512

# Sky region size to be used for each background point in X direction. If 0, the binSize config is used.
config.detection.tempWideBackground.binSizeX=0

# Sky region size to be used for each background point in Y direction. If 0, the binSize config is used.
config.detection.tempWideBackground.binSizeY=0

# how to interpolate the background values. This maps to an enum; see afw::math::Background
config.detection.tempWideBackground.algorithm='AKIMA_SPLINE'

# Names of mask planes to ignore while estimating the background
config.detection.tempWideBackground.ignoredPixelMask=['BAD', 'EDGE', 'NO_DATA']

# Ignore NaNs when estimating the background
config.detection.tempWideBackground.isNanSafe=False

# Use Approximate (Chebyshev) to model background.
config.detection.tempWideBackground.useApprox=False

# Approximation order in X for background Chebyshev (valid only with useApprox=True)
config.detection.tempWideBackground.approxOrderX=6

# Approximation order in Y for background Chebyshev (valid only with useApprox=True)
config.detection.tempWideBackground.approxOrderY=-1

# Use inverse variance weighting in calculation (valid only with useApprox=True)
config.detection.tempWideBackground.weighting=True

# Do temporary wide (large-scale) background subtraction before footprint detection?
config.detection.doTempWideBackground=True

# The maximum number of peaks in a Footprint before trying to replace its peaks using the temporary local background
config.detection.nPeaksMaxSimple=1

# Multiple of PSF RMS size to use for convolution kernel bounding box size; note that this is not a half-size. The size will be rounded up to the nearest odd integer
config.detection.nSigmaForKernel=7.0

# Mask planes to ignore when calculating statistics of image (for thresholdType=stdev)
config.detection.statsMask=['BAD', 'SAT', 'EDGE', 'NO_DATA']

# Fraction of the threshold to use for first pass (to find sky objects)
config.detection.prelimThresholdFactor=0.5

# Avoid pixels masked with these mask planes
config.detection.skyObjects.avoidMask=['DETECTED', 'DETECTED_NEGATIVE', 'BAD', 'NO_DATA']

# Number of pixels to grow the masked pixels when adding sky objects
config.detection.skyObjects.growMask=0

# Radius, in pixels, of sky objects
config.detection.skyObjects.sourceRadius=8.0

# Try to add this many sky objects
config.detection.skyObjects.nSources=1000

# Maximum number of trial sky object positions
# (default: nSkySources*nTrialSkySourcesMultiplier)
config.detection.skyObjects.nTrialSources=None

# Set nTrialSkySources to
#     nSkySources*nTrialSkySourcesMultiplier
# if nTrialSkySources is None
config.detection.skyObjects.nTrialSourcesMultiplier=5

# Tweak background level so median PSF flux of sky objects is zero?
config.detection.doBackgroundTweak=True

# Minimum number of sky sources in statistical sample; if below this number, we refuse to modify the threshold.
config.detection.minNumSources=10

# Name of coadd
config.coaddName='deep'

# Run fake sources injection task
config.doInsertFakes=False

# Mask plane to set on pixels affected by fakes.  Will be added if not already present.
config.insertFakes.maskPlaneName='FAKE'

# Should be set to True if fake sources have been inserted into the input data.
config.hasFakes=False

# name for connection detectionSchema
config.connections.detectionSchema='{outputCoaddName}Coadd_det_schema'

# name for connection exposure
config.connections.exposure='{inputCoaddName}Coadd'

# name for connection outputBackgrounds
config.connections.outputBackgrounds='{outputCoaddName}Coadd_calexp_background'

# name for connection outputSources
config.connections.outputSources='{outputCoaddName}Coadd_det'

# name for connection outputExposure
config.connections.outputExposure='{outputCoaddName}Coadd_calexp'

# Template parameter used to format corresponding field template parameter
config.connections.inputCoaddName='deep'

# Template parameter used to format corresponding field template parameter
config.connections.outputCoaddName='deep'

