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

# Astrometry with gaia
#config.calibrate.astromRefObjLoader.filterMap = {
#    'u2':'phot_g_mean_mag',
#    'g2':'phot_g_mean_mag',
#    'r2':'phot_g_mean_mag',
#    'i2':'phot_g_mean_mag',
#    'i3':'phot_g_mean_mag',
#    'z2':'phot_g_mean_mag',
#}

# Photometry with pan-starrs
#config.calibrate.photoRefObjLoader.filterMap = {
#        'u2':'g',
#        'g2':'g',
#        'r2':'r',
#        'i2':'i',
#        'i3':'i',
#        'z2':'z',
#}

#Astrometry with sdss
config.calibrate.astromRefObjLoader.filterMap = {
    'u2': 'U',
    'g2': 'G',
    'r2': 'R',
    'i2': 'I',
    'i3': 'I',
    'z': 'Z',
}

# Photometry with sdss
config.calibrate.photoRefObjLoader.filterMap = {
    'u2': 'U',
    'g2': 'G',
    'r2': 'R',
    'i2': 'I',
    'i3': 'I',
    'z': 'Z',
}


config.calibrate.photoCal.applyColorTerms = True
import lsst.pipe.tasks.colorterms
config.calibrate.photoCal.colorterms.data['e2v'].data['u2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['u2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['u2'].c1=0.036
config.calibrate.photoCal.colorterms.data['e2v'].data['u2'].c0=-0.165
config.calibrate.photoCal.colorterms.data['e2v'].data['u2'].primary='u'
config.calibrate.photoCal.colorterms.data['e2v'].data['u2'].secondary='g'
config.calibrate.photoCal.colorterms.data['e2v'].data['g2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['g2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['g2'].c1=-0.067
config.calibrate.photoCal.colorterms.data['e2v'].data['g2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['g2'].primary='g'
config.calibrate.photoCal.colorterms.data['e2v'].data['g2'].secondary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['r2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c1=0.087
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].primary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].secondary='g'
config.calibrate.photoCal.colorterms.data['e2v'].data['i3']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c1=0.089
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].primary='i'
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].secondary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['z2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['z2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['z2'].c1=0.045
config.calibrate.photoCal.colorterms.data['e2v'].data['z2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['z2'].primary='z'
config.calibrate.photoCal.colorterms.data['e2v'].data['z2'].secondary='i'


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
#config.calibrate.requirePhotoCal=False
#config.calibrate.requireAstrometry=False
