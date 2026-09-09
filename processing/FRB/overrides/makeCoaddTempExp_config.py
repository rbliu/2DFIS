# Apply jointcal WCS and PhotoCalib results to input calexps?
config.doApplyUberCal=True

# Make direct Warp/Coadds
#config.makeDirect=False

# Make Psf-Matched Warp/Coadd?
config.makePsfMatched=True


# Warping kernel
config.warpAndPsfMatch.psfMatch.kernel['AL'].warpingConfig.warpingKernelName='lanczos5'

# Warping kernel
config.warpAndPsfMatch.warp.warpingKernelName='lanczos5'

# Warping kernel for mask (use ``warpingKernelName`` if '')
config.warpAndPsfMatch.warp.maskWarpingKernelName='lanczos5'

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.coaddPsf.warpingKernelName='lanczos5'
