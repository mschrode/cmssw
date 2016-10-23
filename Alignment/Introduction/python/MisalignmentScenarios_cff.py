import FWCore.ParameterSet.Config as cms

# Defines several misalignment scenarios
#
# Shifts are in [cm]
#
# Further information on syntax and options at
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMisalignmentTools

# -----------------------------------------------------------------------
# General settings common to all scenarios
GlobalSettings = cms.PSet(
    setRotations    = cms.bool(True),
    setTranslations = cms.bool(True),
    seed            = cms.int32(1234567),
    distribution    = cms.string('gaussian'),
    setError        = cms.bool(False),
    scale           = cms.double(0.0001), # --> all shifts to be defined in 1mum
)


# -----------------------------------------------------------------------
# The scenarios:
PixelMisalignmentScenario1 = cms.PSet(
    GlobalSettings,
    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dY = cms.double(50),
            dX = cms.double(50),
        ),
    ),
)

PixelMisalignmentScenario2 = cms.PSet(
    GlobalSettings,
    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZ = cms.double(50),
        ),
    ),
)
