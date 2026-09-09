if hasattr(config.astrometryRefObjLoader, "ref_dataset_name"):
    config.astrometryRefObjLoader.ref_dataset_name = 'sdss'
if hasattr(config.photometryRefObjLoader, "ref_dataset_name"):
    config.photometryRefObjLoader.ref_dataset_name = 'sdss'

config.astrometryRefObjLoader.filterMap = {
        'u2': 'U',
        'g2': 'G',
        'r2': 'R',
        'i2': 'I',
        'i3': 'I',
        'z': 'Z',
}

config.photometryRefObjLoader.filterMap = {
        'u2': 'U',
        'g2': 'G',
        'r2': 'R',
        'i2': 'I',
        'i3': 'I',
        'z': 'Z',
}

config.applyColorTerms = False
#config.photometryVisitOrder = order

# Uncertainty on reference catalog coordinates [mas] to use in place of the `coord_*Err` fields. If None, then raise an exception if the reference catalog is missing coordinate errors. If specified, overrides any existing `coord_*Err` values.
config.astrometryReferenceErr=10.0
