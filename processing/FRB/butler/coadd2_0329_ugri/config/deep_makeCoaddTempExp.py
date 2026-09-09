import lsst.pipe.tasks.makeCoaddTempExp
assert type(config)==lsst.pipe.tasks.makeCoaddTempExp.MakeCoaddTempExpConfig, 'config is of type %s.%s instead of lsst.pipe.tasks.makeCoaddTempExp.MakeCoaddTempExpConfig' % (type(config).__module__, type(config).__name__)
import lsst.meas.algorithms.gaussianPsfFactory
import lsst.afw.math.warper
import lsst.ip.diffim.psfMatch
import lsst.ip.diffim.modelPsfMatch
import lsst.meas.algorithms.coaddPsf.coaddPsf
import lsst.meas.algorithms.subtractBackground
import lsst.pipe.tasks.selectImages
import lsst.pipe.tasks.coaddInputRecorder
import lsst.pipe.tasks.warpAndPsfMatch
import lsst.pex.config.config
# Coadd name: typically one of deep or goodSeeing.
config.coaddName='deep'

# Mask planes that, if set, the associated pixel should not be included in the coaddTempExp.
config.badMaskPlanes=['NO_DATA']

# Add records for CCDs we iterated over but did not add a coaddTempExp due to a lack of unmasked pixels in the coadd footprint.
config.inputRecorder.saveEmptyCcds=False

# Add records for CCDs we iterated over but did not add a coaddTempExp due to an exception (often due to the calexp not being found on disk).
config.inputRecorder.saveErrorCcds=False

# Save the total number of good pixels in each coaddTempExp (redundant with a sum of good pixels in associated CCDs)
config.inputRecorder.saveVisitGoodPix=True

# Save weights in the CCDs table as well as the visits table? (This is necessary for easy construction of CoaddPsf, but otherwise duplicate information.)
config.inputRecorder.saveCcdWeights=True

# Match to modelPsf? Deprecated. Sets makePsfMatched=True, makeDirect=False
config.doPsfMatch=False

# Kernel size (width and height) (pixels); if None then sizeFactor is used
config.modelPsf.size=None

# Kernel size as a factor of fwhm (dimensionless); size = sizeFactor * fwhm; ignored if size is not None
config.modelPsf.sizeFactor=3.0

# Minimum kernel size if using sizeFactor (pixels); ignored if size is not None
config.modelPsf.minSize=5

# Maximum kernel size if using sizeFactor (pixels); ignored if size is not None
config.modelPsf.maxSize=None

# Default FWHM of Gaussian model of core of star (pixels)
config.modelPsf.defaultFwhm=3.0

# Add a Gaussian to represent wings?
config.modelPsf.addWing=True

# wing width, as a multiple of core width (dimensionless); ignored if addWing false
config.modelPsf.wingFwhmFactor=2.5

# wing amplitude, as a multiple of core amplitude (dimensionless); ignored if addWing false
config.modelPsf.wingAmplitude=0.1

# Apply jointcal WCS and PhotoCalib results to input calexps?
config.doApplyUberCal=True

# Use meas_mosaic's applyMosaicResultsExposure() to do the photometric calibration/wcs update (deprecated).
config.useMeasMosaic=False

# Add photometric calibration variance to warp variance plane.
config.includeCalibVar=False

# Size in pixels of matching kernel. Must be odd.
config.matchingKernelSize=21

# Warping kernel
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.warpingKernelName='lanczos5'

# Warping kernel for mask (use ``warpingKernelName`` if '')
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.maskWarpingKernelName='bilinear'

# ``interpLength`` argument to `lsst.afw.math.warpExposure`
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.interpLength=10

# ``cacheSize`` argument to `lsst.afw.math.SeparableKernel.computeCache`
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.cacheSize=1000000

# mask bits to grow to full width of image/variance kernel,
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.growFullMask=16

# Value of footprint detection threshold
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.detThreshold=10.0

# Type of detection threshold
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.detThresholdType='pixel_stdev'

# If true run detection on the template (image to convolve);
#                  if false run detection on the science image
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.detOnTemplate=True

# Mask planes that lead to an invalid detection.
#                  Options: NO_DATA EDGE SAT BAD CR INTRP
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.badMaskPlanes=['NO_DATA', 'EDGE', 'SAT']

# Minimum number of pixels in an acceptable Footprint
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.fpNpixMin=5

# Maximum number of pixels in an acceptable Footprint;
#                  too big and the subsequent convolutions become unwieldy
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.fpNpixMax=500

# If config.scaleByFwhm, grow the footprint based on
#                  the final kernelSize.  Each footprint will be
#                  2*fpGrowKernelScaling*kernelSize x
#                  2*fpGrowKernelScaling*kernelSize.  With the value
#                  of 1.0, the remaining pixels in each KernelCandiate
#                  after convolution by the basis functions will be
#                  equal to the kernel size itself.
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.fpGrowKernelScaling=1.0

# Growing radius (in pixels) for each raw detection
#                  footprint.  The smaller the faster; however the
#                  kernel sum does not converge if the stamp is too
#                  small; and the kernel is not constrained at all if
#                  the stamp is the size of the kernel.  The grown stamp
#                  is 2 * fpGrowPix pixels larger in each dimension.
#                  This is overridden by fpGrowKernelScaling if scaleByFwhm
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.fpGrowPix=30

# Scale fpGrowPix by input Fwhm?
config.warpAndPsfMatch.psfMatch.kernel['AL'].detectionConfig.scaleByFwhm=True

# type of statistic to use for grid points
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.statisticsProperty='MEANCLIP'

# behaviour if there are too few points in grid for requested interpolation style
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.undersampleStyle='REDUCE_INTERP_ORDER'

# how large a region of the sky should be used for each background point
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.binSize=128

# Sky region size to be used for each background point in X direction. If 0, the binSize config is used.
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.binSizeX=0

# Sky region size to be used for each background point in Y direction. If 0, the binSize config is used.
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.binSizeY=0

# how to interpolate the background values. This maps to an enum; see afw::math::Background
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.algorithm='AKIMA_SPLINE'

# Names of mask planes to ignore while estimating the background
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.ignoredPixelMask=['BAD', 'EDGE', 'DETECTED', 'DETECTED_NEGATIVE', 'NO_DATA']

# Ignore NaNs when estimating the background
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.isNanSafe=False

# Use Approximate (Chebyshev) to model background.
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.useApprox=True

# Approximation order in X for background Chebyshev (valid only with useApprox=True)
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.approxOrderX=6

# Approximation order in Y for background Chebyshev (valid only with useApprox=True)
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.approxOrderY=-1

# Use inverse variance weighting in calculation (valid only with useApprox=True)
config.warpAndPsfMatch.psfMatch.kernel['AL'].afwBackgroundConfig.weighting=True

# Use afw background subtraction instead of ip_diffim
config.warpAndPsfMatch.psfMatch.kernel['AL'].useAfwBackground=False

# Include terms (including kernel cross terms) for background in ip_diffim
config.warpAndPsfMatch.psfMatch.kernel['AL'].fitForBackground=False

# Type of basis set for PSF matching kernel.
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelBasisSet='alard-lupton'

# Number of rows/columns in the convolution kernel; should be odd-valued.
#                  Modified by kernelSizeFwhmScaling if scaleByFwhm = true
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelSize=21

# Scale kernelSize, alardGaussians by input Fwhm
config.warpAndPsfMatch.psfMatch.kernel['AL'].scaleByFwhm=False

# Multiplier of the largest AL Gaussian basis sigma to get the kernel bbox (pixel) size.
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelSizeFwhmScaling=6.0

# Minimum kernel bbox (pixel) size.
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelSizeMin=21

# Maximum kernel bbox (pixel) size.
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelSizeMax=35

# Type of spatial functions for kernel and background
config.warpAndPsfMatch.psfMatch.kernel['AL'].spatialModelType='chebyshev1'

# Spatial order of convolution kernel variation
config.warpAndPsfMatch.psfMatch.kernel['AL'].spatialKernelOrder=2

# Spatial order of differential background variation
config.warpAndPsfMatch.psfMatch.kernel['AL'].spatialBgOrder=1

# Size (rows) in pixels of each SpatialCell for spatial modeling
config.warpAndPsfMatch.psfMatch.kernel['AL'].sizeCellX=128

# Size (columns) in pixels of each SpatialCell for spatial modeling
config.warpAndPsfMatch.psfMatch.kernel['AL'].sizeCellY=128

# Number of KernelCandidates in each SpatialCell to use in the spatial fitting
config.warpAndPsfMatch.psfMatch.kernel['AL'].nStarPerCell=3

# Maximum number of iterations for rejecting bad KernelCandidates in spatial fitting
config.warpAndPsfMatch.psfMatch.kernel['AL'].maxSpatialIterations=3

# Use Pca to reduce the dimensionality of the kernel basis sets.
#                  This is particularly useful for delta-function kernels.
#                  Functionally, after all Cells have their raw kernels determined, we run
#                  a Pca on these Kernels, re-fit the Cells using the eigenKernels and then
#                  fit those for spatial variation using the same technique as for Alard-Lupton kernels.
#                  If this option is used, the first term will have no spatial variation and the
#                  kernel sum will be conserved.
config.warpAndPsfMatch.psfMatch.kernel['AL'].usePcaForSpatialKernel=False

# Subtract off the mean feature before doing the Pca
config.warpAndPsfMatch.psfMatch.kernel['AL'].subtractMeanForPca=True

# Number of principal components to use for Pca basis, including the
#                  mean kernel if requested.
config.warpAndPsfMatch.psfMatch.kernel['AL'].numPrincipalComponents=5

# Do sigma clipping on each raw kernel candidate
config.warpAndPsfMatch.psfMatch.kernel['AL'].singleKernelClipping=False

# Do sigma clipping on the ensemble of kernel sums
config.warpAndPsfMatch.psfMatch.kernel['AL'].kernelSumClipping=False

# Do sigma clipping after building the spatial model
config.warpAndPsfMatch.psfMatch.kernel['AL'].spatialKernelClipping=False

# Test for maximum condition number when inverting a kernel matrix.
#                  Anything above maxConditionNumber is not used and the candidate is set as BAD.
#                  Also used to truncate inverse matrix in estimateBiasedRisk.  However,
#                  if you are doing any deconvolution you will want to turn this off, or use
#                  a large maxConditionNumber
config.warpAndPsfMatch.psfMatch.kernel['AL'].checkConditionNumber=False

# Mask planes to ignore when calculating diffim statistics
#                  Options: NO_DATA EDGE SAT BAD CR INTRP
config.warpAndPsfMatch.psfMatch.kernel['AL'].badMaskPlanes=['NO_DATA', 'EDGE', 'SAT']

# Rejects KernelCandidates yielding bad difference image quality.
#                  Used by BuildSingleKernelVisitor, AssessSpatialKernelVisitor.
#                  Represents average over pixels of (image/sqrt(variance)).
config.warpAndPsfMatch.psfMatch.kernel['AL'].candidateResidualMeanMax=0.25

# Rejects KernelCandidates yielding bad difference image quality.
#                  Used by BuildSingleKernelVisitor, AssessSpatialKernelVisitor.
#                  Represents stddev over pixels of (image/sqrt(variance)).
config.warpAndPsfMatch.psfMatch.kernel['AL'].candidateResidualStdMax=1.5

# Use the core of the footprint for the quality statistics, instead of the entire footprint.
#                  WARNING: if there is deconvolution we probably will need to turn this off
config.warpAndPsfMatch.psfMatch.kernel['AL'].useCoreStats=False

# Radius for calculation of stats in 'core' of KernelCandidate diffim.
#                  Total number of pixels used will be (2*radius)**2.
#                  This is used both for 'core' diffim quality as well as ranking of
#                  KernelCandidates by their total flux in this core
config.warpAndPsfMatch.psfMatch.kernel['AL'].candidateCoreRadius=3

# Maximum allowed sigma for outliers from kernel sum distribution.
#                  Used to reject variable objects from the kernel model
config.warpAndPsfMatch.psfMatch.kernel['AL'].maxKsumSigma=3.0

# Maximum condition number for a well conditioned matrix
config.warpAndPsfMatch.psfMatch.kernel['AL'].maxConditionNumber=50000000.0

# Use singular values (SVD) or eigen values (EIGENVALUE) to determine condition number
config.warpAndPsfMatch.psfMatch.kernel['AL'].conditionNumberType='EIGENVALUE'

# Maximum condition number for a well conditioned spatial matrix
config.warpAndPsfMatch.psfMatch.kernel['AL'].maxSpatialConditionNumber=10000000000.0

# Remake KernelCandidate using better variance estimate after first pass?
#                  Primarily useful when convolving a single-depth image, otherwise not necessary.
config.warpAndPsfMatch.psfMatch.kernel['AL'].iterateSingleKernel=False

# Use constant variance weighting in single kernel fitting?
#                  In some cases this is better for bright star residuals.
config.warpAndPsfMatch.psfMatch.kernel['AL'].constantVarianceWeighting=True

# Calculate kernel and background uncertainties for each kernel candidate?
#                  This comes from the inverse of the covariance matrix.
#                  Warning: regularization can cause problems for this step.
config.warpAndPsfMatch.psfMatch.kernel['AL'].calculateKernelUncertainty=False

# Use Bayesian Information Criterion to select the number of bases going into the kernel
config.warpAndPsfMatch.psfMatch.kernel['AL'].useBicForKernelBasis=False

# Number of base Gaussians in alard-lupton kernel basis function generation.
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardNGauss=3

# Polynomial order of spatial modification of base Gaussians. List length must be `alardNGauss`.
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardDegGauss=[4, 2, 2]

# Default sigma values in pixels of base Gaussians. List length must be `alardNGauss`.
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardSigGauss=[0.7, 1.5, 3.0]

# Used if `scaleByFwhm==True`, scaling multiplier of base Gaussian sigmas for automated sigma determination
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardGaussBeta=2.0

# Used if `scaleByFwhm==True`, minimum sigma (pixels) for base Gaussians
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardMinSig=0.7

# Used if `scaleByFwhm==True`, degree of spatial modification of ALL base Gaussians in AL basis during deconvolution
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardDegGaussDeconv=3

# Used if `scaleByFwhm==True`, minimum sigma (pixels) for base Gaussians during deconvolution; make smaller than `alardMinSig` as this is only indirectly used
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardMinSigDeconv=0.4

# Used if `scaleByFwhm==True`, number of base Gaussians in AL basis during deconvolution
config.warpAndPsfMatch.psfMatch.kernel['AL'].alardNGaussDeconv=3

config.warpAndPsfMatch.psfMatch.kernel.name='AL'
# If too small, automatically pad the science Psf? Pad to smallest dimensions appropriate for the matching kernel dimensions, as specified by autoPadPsfTo. If false, pad by the padPsfBy config.
config.warpAndPsfMatch.psfMatch.doAutoPadPsf=True

# Minimum Science Psf dimensions as a fraction of matching kernel dimensions. If the dimensions of the Psf to be matched are less than the matching kernel dimensions * autoPadPsfTo, pad Science Psf to this size. Ignored if doAutoPadPsf=False.
config.warpAndPsfMatch.psfMatch.autoPadPsfTo=1.4

# Pixels (even) to pad Science Psf by before matching. Ignored if doAutoPadPsf=True
config.warpAndPsfMatch.psfMatch.padPsfBy=0

# Warping kernel
config.warpAndPsfMatch.warp.warpingKernelName='lanczos5'

# Warping kernel for mask (use ``warpingKernelName`` if '')
config.warpAndPsfMatch.warp.maskWarpingKernelName='lanczos5'

# ``interpLength`` argument to `lsst.afw.math.warpExposure`
config.warpAndPsfMatch.warp.interpLength=10

# ``cacheSize`` argument to `lsst.afw.math.SeparableKernel.computeCache`
config.warpAndPsfMatch.warp.cacheSize=1000000

# mask bits to grow to full width of image/variance kernel,
config.warpAndPsfMatch.warp.growFullMask=16

# persist <coaddName>Coadd_<warpType>Warp
config.doWrite=True

# Work with a background subtracted calexp?
config.bgSubtracted=True

# Warping kernel cache size
config.coaddPsf.cacheSize=10000

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.coaddPsf.warpingKernelName='lanczos5'

# Make direct Warp/Coadds
config.makeDirect=False

# Make Psf-Matched Warp/Coadd?
config.makePsfMatched=True

# Write out warps even if they are empty
config.doWriteEmptyWarps=False

# Should be set to True if fake sources have been inserted into the input data.
config.hasFakes=False

# Apply sky correction?
config.doApplySkyCorr=False

