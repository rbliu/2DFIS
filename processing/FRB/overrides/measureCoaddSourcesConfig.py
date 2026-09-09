# HSM and KSB shape measurement
import lsst.meas.extensions.shapeHSM
config.measurement.plugins.names |= ["ext_shapeHSM_HsmShapeKsb",         # KSB
                                     "ext_shapeHSM_HsmShapeRegauss",     # HSM 
                                     "ext_shapeHSM_HsmSourceMoments",    # not PSF correction; for measurements above
                                     "ext_shapeHSM_HsmPsfMoments"]       # moments of PSF; for measurements above
config.measurement.slots.shape = "ext_shapeHSM_HsmSourceMoments"
config.measurement.slots.psfShape = "ext_shapeHSM_HsmPsfMoments"
config.measurement.plugins["ext_shapeHSM_HsmShapeRegauss"].deblendNChild = "deblend_nChild"

# CModel flux for color measurement (Bosch et al. 2017)
import lsst.meas.modelfit
config.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
config.measurement.slots.modelFlux = "modelfit_CModel"

# Kron flux and size
import lsst.meas.extensions.photometryKron
config.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]


# The reference catalogs are only for quality assurance purposes
from lsst.meas.algorithms import LoadIndexedReferenceObjectsTask
config.match.refObjLoader.retarget(LoadIndexedReferenceObjectsTask)
config.match.refObjLoader.ref_dataset_name='pan-starrs'
config.match.refObjLoader.filterMap={
    'g2':'g',
    'r2':'r',
    'i3':'i',
    'u2':'g',
}
config.connections.refCat = 'pan-starrs'
