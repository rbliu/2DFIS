# Warp name: one of 'direct' or 'psfMatched'
#config.warpType='psfMatched'

# Template parameter used to format corresponding field template parameter
#config.connections.warpType='psfMatched'

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.coaddPsf.warpingKernelName='lanczos5'

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.assembleStaticSkyModel.coaddPsf.warpingKernelName='lanczos5'


# Main stacking statistic for aggregating over the epochs.
config.statistic='MEDIAN'

# Perform sigma clipped outlier rejection with MEANCLIP statistic? (DEPRECATED)
config.doSigmaClip=True

# Sigma for outlier rejection; ignored if non-clipping statistic selected.
config.sigmaClip=2.0

# Main stacking statistic for aggregating over the epochs.
config.assembleStaticSkyModel.statistic='MEDIAN'

config.detect.statsMask=['BAD', 'SAT', 'EDGE', 'NO_DATA', 'CLIPPED'] 

