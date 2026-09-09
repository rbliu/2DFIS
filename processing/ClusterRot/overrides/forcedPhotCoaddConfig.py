import lsst.meas.modelfit
import lsst.shapelet
config.measurement.plugins.names |= ["modelfit_DoubleShapeletPsfApprox", "modelfit_CModel"]
config.measurement.slots.modelFlux = "modelfit_CModel"

config.doApCorr=True

# extendedness = mag_PSF - mag_CModel
# ~ 0: star; > 0: galaxy
config.catalogCalculation.plugins.names = ["base_ClassificationExtendedness"]
config.measurement.slots.psfFlux = "base_PsfFlux"

import lsst.meas.extensions.photometryKron
config.measurement.plugins.names |= ["ext_photometryKron_KronFlux"]


#config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('CLIPPED')
# These do not work anymore??
#config.measurement.plugins['base_PixelFlags'].masksFpCenter.append('BRIGHT_OBJECT')
#config.measurement.plugins['base_PixelFlags'].masksFpAnywhere.append('BRIGHT_OBJECT')
