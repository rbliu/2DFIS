# Warp name: one of 'direct' or 'psfMatched'
#config.warpType='psfMatched'

# Template parameter used to format corresponding field template parameter
#config.connections.warpType='psfMatched'

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.coaddPsf.warpingKernelName='lanczos5'

# Name of warping kernel; choices: lanczos3,lanczos4,lanczos5,bilinear,nearest
config.assembleStaticSkyModel.coaddPsf.warpingKernelName='lanczos5'
