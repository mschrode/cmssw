import FWCore.ParameterSet.Config as cms

import Alignment.TrackerAlignment.Scenarios_cff as Scenarios

TibTob20 = cms.PSet(
    Scenarios.MisalignmentScenarioSettings,
    TOBHalfBarrels = cms.PSet(
      TOBLayer3_4_5_6 = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
      TOBLayer1_2 = cms.PSet(
	DetUnits = cms.PSet(
	#Dets = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
    ),
    TIBHalfBarrels = cms.PSet(
      TIBLayer3_4 = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
      TIBLayer1_2 = cms.PSet(
        DetUnits = cms.PSet(
	#Dets = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
    ),
)



Tib20 = cms.PSet(
    Scenarios.MisalignmentScenarioSettings,
    TIBHalfBarrels = cms.PSet(
      TIBLayers = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
    ),
)



Tob20 = cms.PSet(
    Scenarios.MisalignmentScenarioSettings,
    TOBHalfBarrels = cms.PSet(
      TOBLayers = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.002),
	),
      ),
    ),
)



PixelTob5 = cms.PSet(
    Scenarios.MisalignmentScenarioSettings,
    TOBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.0005),
	),
    ),
    TPBHalfBarrels = cms.PSet(
        DetUnits = cms.PSet(
	  dXlocal = cms.double(0.0005),
	  dYlocal = cms.double(0.0005),
	),
    ),
    TPEEndcaps = cms.PSet(
      DetUnits = cms.PSet(
	  dXlocal = cms.double(0.0005),
	  dYlocal = cms.double(0.0005),
      ),
    ),
)



import Alignment.TrackerAlignment.MisalignedTracker_cfi


MisalignedTrackerForApe = Alignment.TrackerAlignment.MisalignedTracker_cfi.MisalignedTracker.clone(
    saveToDbase = True,
    scenario = TibTob20,
)

