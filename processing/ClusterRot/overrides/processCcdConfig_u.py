# Apply correction for CCD defects, e.g. hot pixels?
config.isr.doDefect=False
# Apply the brighter fatter correction
config.isr.doBrighterFatter=False

config.charImage.repair.cosmicray.nCrPixelMax=1000000

# Useful to get to avoid deblending of satellite tracks
config.calibrate.deblend.maxFootprintSize=2000  # 2200

# Use psfex instead of pca
import lsst.meas.extensions.psfex.psfexPsfDeterminer
config.charImage.measurePsf.psfDeterminer.name='psfex'

# The following should be included for u filter in order to lower the source detection threshold
config.charImage.detection.includeThresholdMultiplier=1.0

# Run CModel
import lsst.meas.modelfit
import lsst.meas.extensions.convolved  # noqa: Load flux.convolved algorithm
config.charImage.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox",
                                               "modelfit_CModel",
                                               "ext_convolved_ConvolvedFlux"]
config.charImage.measurement.slots.modelFlux = "modelfit_CModel"

# Calibrate astrometry and photometry with reference catalogs
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)

config.calibrate.astrometry.wcsFitter.order = 3

config.calibrate.astromRefObjLoader.ref_dataset_name = 'sdss'
config.calibrate.photoRefObjLoader.ref_dataset_name = 'sdss'
config.calibrate.connections.astromRefCat = 'sdss'
config.calibrate.connections.photoRefCat = 'sdss'


# Astrometry with panstarrs
#config.calibrate.astromRefObjLoader.filterMap = {
#    'u':'g',
#    'u2':'g',
#}

# Astrometry with gaia
#config.calibrate.astromRefObjLoader.filterMap = {
#    'u':'phot_g_mean_mag',
#    'u2':'phot_g_mean_mag',
#}

# Photometry with panstarrs
#config.calibrate.photoRefObjLoader.filterMap = {
#        'u':'g',
#        'u2':'g',
#}


# Photometry with sdss
config.calibrate.photoRefObjLoader.filterMap = {
    'u': 'U',
    'u2': 'U',
}

#Astrometry with sdss
config.calibrate.astromRefObjLoader.filterMap = {
    'u': 'U',
    'u2': 'U',
}

config.calibrate.photoCal.applyColorTerms = False

import lsst.pipe.tasks.colorterms
# color term from PS1 to MegaCam
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c3=-1.64
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c2=4.18
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c1=-1.36
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c0=0.823
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].secondary='i'


# use Chebyshev background estimation
config.charImage.background.useApprox=True
config.charImage.detection.background.binSize=128
config.charImage.detection.background.useApprox=True
config.charImage.background.binSize = 128
config.charImage.background.undersampleStyle = 'REDUCE_INTERP_ORDER'
config.charImage.detection.background.binSize = 128
config.charImage.detection.background.undersampleStyle='REDUCE_INTERP_ORDER'
config.charImage.detection.background.binSize = 128
config.charImage.detection.background.undersampleStyle = 'REDUCE_INTERP_ORDER'


# Convolved fluxes can fail for small target seeing if the observation seeing is larger
if "ext_convolved_ConvolvedFlux" in config.charImage.measurement.plugins:
    config.charImage.measurement.plugins["ext_convolved_ConvolvedFlux"].seeing.append(8.0)
    names = config.charImage.measurement.plugins["ext_convolved_ConvolvedFlux"].getAllResultNames()
    config.charImage.measureApCorr.allowFailure += names


# from DECam config
# Kron photometry
import lsst.meas.extensions.photometryKron
config.charImage.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]
config.calibrate.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]

config.calibrate.astrometry.matcher.maxOffsetPix=3000
config.calibrate.astromRefObjLoader.pixelMargin=3000

# trials
config.calibrate.astrometry.wcsFitter.maxScatterArcsec=20.0  #default=10
