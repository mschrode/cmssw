import FWCore.ParameterSet.Config as cms

# -----------------------------------------------------------------------
# General settings common to all scenarios
MisalignmentScenarioSettings = cms.PSet(
    setRotations = cms.bool(True),
    setTranslations = cms.bool(True),
    seed = cms.int32(1234567),
    distribution = cms.string('gaussian'),
    setError = cms.bool(False)
)


MisalignmentScenario100Mu = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),

    TIBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),

    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),

    TPEEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),

    TIDEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),

    TECEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),
)


MisalignmentScenario200Mu = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01),# shifts in 100mum

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),

    TIBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),

    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),

    TPEEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),

    TIDEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),

    TECEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(2),
            dYlocal = cms.double(2),
            dXlocal = cms.double(2),
        ),
    ),
)


MisalignmentScenario300Mu = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01),# shifts in 100mum

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),

    TIBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),

    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),

    TPEEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),

    TIDEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),

    TECEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(3),
            dYlocal = cms.double(3),
            dXlocal = cms.double(3),
        ),
    ),
)



MisalignmentScenarioBPIX100Mu = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01),# shifts in 100mum

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        ),
    ),
)


MisalignedTPB = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)

MisalignedTPE = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TPEEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)

MisalignedTIB = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TIBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)

MisalignedTOB = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)

MisalignedTID = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TIDEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)

MisalignedTEC = cms.PSet(
    MisalignmentScenarioSettings,
    scale = cms.double(0.01), # shifts in 100um

    TECEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(1),
            dYlocal = cms.double(1),
            dXlocal = cms.double(1),
        )
    )
)


MisalignmentAPEScenarioBase = cms.PSet(
    # Sigma in mum
    #   BPIX:   20
    #   BPIX-y: 10
    #   FPIX:   10
    #   FPIX-y: 20
    #   TEC:    20
    #   TIB:    10
    #   TID:    10
    #   TOB:    10 
    MisalignmentScenarioSettings,
    scale = cms.double(0.0001), # shifts in 1um

    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(20),
            dYlocal = cms.double(10),
            dXlocal = cms.double(20),
        ),
    ),

    TIBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(10),
            dYlocal = cms.double(10),
            dXlocal = cms.double(10),
        ),
    ),

    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(10),
            dYlocal = cms.double(10),
            dXlocal = cms.double(10),
        ),
    ),

    TPEEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(20),
            dYlocal = cms.double(20),
            dXlocal = cms.double(10),
        ),
    ),

    TIDEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(10),
            dYlocal = cms.double(10),
            dXlocal = cms.double(10),
        ),
    ),

    TECEndcaps = cms.PSet(
        DetUnits = cms.PSet(
            dZlocal = cms.double(20),
            dYlocal = cms.double(20),
            dXlocal = cms.double(20),
        ),
    ),
)
