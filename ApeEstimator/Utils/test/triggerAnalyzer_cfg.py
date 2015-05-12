import os

import FWCore.ParameterSet.Config as cms


process = cms.Process("TriggerAnalyzer")



## Message logger
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 ## really show only every 1000th



process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)



## Input Source
#process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_Run2011A_May10ReReco_cff")
#process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_Run2011A_PromptV4_cff")
#process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer11_qcd_cff")
#process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer11_wlnu_cff")
process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer11_zmumu10_cff")
#process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer11_zmumu20_cff")



process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )



## Analyzer under test
process.load("ApeEstimator.Utils.TriggerAnalyzer_cfi")
process.TriggerAnalyzer1 = process.TriggerAnalyzer.clone(
    #triggerResults = cms.InputTag('TriggerResults','','REDIGI311X'),
)



## Path
process.p = cms.Path(
    process.TriggerAnalyzer1
)
