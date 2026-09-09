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
#config.charImage.detection.includeThresholdMultiplier=1.0

# Run CModel
import lsst.meas.modelfit
import lsst.meas.extensions.convolved  # noqa: Load flux.convolved algorithm
config.charImage.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox",
                                               "modelfit_CModel",
                                               "ext_convolved_ConvolvedFlux"]

# Run astrometry using the new htm reference catalog format
# The following retargets are necessary until the new scheme becomes standard
#from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
#config.calibrate.astromRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)
#config.calibrate.photoRefObjLoader.retarget(LoadIndexedReferenceObjectsTask)

# Use new astrometry fitter
#from lsst.meas.astrom import FitSipDistortionTask
#config.calibrate.astrometry.wcsFitter.retarget(FitSipDistortionTask)

config.calibrate.astrometry.wcsFitter.order = 3
#config.calibrate.astrometry.matcher.maxMatchDistArcSec=5


# Select external catalogs for Astrometry and Photometry
#config.calibrate.photoRefObjLoader.ref_dataset_name='sdss'
config.calibrate.photoRefObjLoader.ref_dataset_name='pan-starrs'

#config.calibrate.astromRefObjLoader.ref_dataset_name='gaia'
config.calibrate.astromRefObjLoader.ref_dataset_name='gaia'
#config.calibrate.astromRefObjLoader.ref_dataset_name='sdss'

config.calibrate.connections.astromRefCat = 'gaia'
config.calibrate.connections.photoRefCat = 'pan-starrs'
#config.calibrate.connections.astromRefCat = 'gaia_dr2_A2420'
#config.calibrate.connections.photoRefCat = 'ps1_dr1_A2420'


# Astrometry with panstarrs
#config.calibrate.astromRefObjLoader.filterMap = {
#    'u':'g',
#    'g':'g',
#    'r':'r',
#    'r2':'r',
#    'i':'i',
#    'i2': 'i',
#    'i3': 'i',
#    'z':'z',
#    'y':'y',
#}
# Astrometry with gaia
config.calibrate.astromRefObjLoader.filterMap = {
    'u':'phot_g_mean_mag',
    'u2':'phot_g_mean_mag',
    'g':'phot_g_mean_mag',
    'g2':'phot_g_mean_mag',
    'r':'phot_g_mean_mag',
    'r2':'phot_g_mean_mag',
    'i':'phot_g_mean_mag',
    'i2':'phot_g_mean_mag',
    'i3':'phot_g_mean_mag',
    'z':'phot_g_mean_mag',
    'z2':'phot_g_mean_mag',
    'y':'phot_g_mean_mag',
}

# Photometry with panstarrs
config.calibrate.photoRefObjLoader.filterMap = {
	'u':'g',
        'u2':'g',
	'g':'g',
	'g2':'g',
	'r':'r',
	'r2':'r',
	'i':'i',
	'i2':'i',
	'i3':'i',
	'z':'z',
        'z2':'z',
	'y':'y',
}

# Photometry with sdss
#config.calibrate.photoRefObjLoader.filterMap = {
#    'u': 'U',
#    'g': 'G',
#    'r': 'R',
#    'r2': 'R',
#    'i': 'I',
#    'i2': 'I',
#    'i3': 'I',
#    'z': 'Z',
#    'y': 'Z',
#}

#Astrometry with sdss
#config.calibrate.astromRefObjLoader.filterMap = {
#    'u': 'U',
#    'g': 'G',
#    'r': 'R',
#    'i': 'I',
#    'z': 'Z',
#    'y': 'Z',
#}


config.calibrate.photoCal.applyColorTerms = False

import lsst.pipe.tasks.colorterms
config.calibrate.photoCal.colorterms.data['e2v'].data['i2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c1=0.003
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].primary='i'
config.calibrate.photoCal.colorterms.data['e2v'].data['i2'].secondary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['i3']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c1=0.003
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].primary='i'
config.calibrate.photoCal.colorterms.data['e2v'].data['i3'].secondary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['r2']=lsst.pipe.tasks.colorterms.Colorterm()
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c2=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c1=0.024
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].c0=0.0
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].primary='r'
config.calibrate.photoCal.colorterms.data['e2v'].data['r2'].secondary='g'

# color term from PS1 to MegaCam
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c3=-1.64
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c2=4.18
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c1=-1.36
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].c0=0.823
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['u2'].secondary='i'
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].c3=-0.00178
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].c2=-0.00313
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].c1=0.059
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].c0=0.014
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['g2'].secondary='i'
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].c3=-0.00699
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].c2=0.0125
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].c1=-0.05
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].c0=0.003
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['r2'].secondary='i'
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].c3=-0.0048
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].c2=0.0124
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].c1=0.004
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].c0=-0.005
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['i2'].secondary='i'
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].c3=-0.00523
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].c2=0.00627
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].c1=-0.024
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].c0=0.006
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['i3'].secondary='i'
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2']=lsst.pipe.tasks.colorterms.Colorterm()
#config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].c3=-0.0056
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].c2=0.0239
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].c1=-0.069
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].c0=-0.016
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].primary='g'
config.calibrate.photoCal.colorterms.data['ps1*'].data['z2'].secondary='i'


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
