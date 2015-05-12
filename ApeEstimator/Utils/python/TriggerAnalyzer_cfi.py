import FWCore.ParameterSet.Config as cms

TriggerAnalyzer = cms.EDAnalyzer('TriggerAnalyzer',
    # Trigger results
    triggerResults = cms.InputTag('TriggerResults','','HLT'),
)
