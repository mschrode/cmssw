import os

import FWCore.ParameterSet.Config as cms



process = cms.Process("MyAlcareco")



##
## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('AlignmentTrackSelector')
#process.MessageLogger.categories.append('')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.AlignmentTrackSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1))

process.MessageLogger.cerr.FwkReport.reportEvery = 1000 ## really show only every 1000th



##
## Process options
##
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)



##
## Input Files
##
## --- Particle Gun ---
#process.load("ApeEstimator.ApeEstimator.samples.Mc_QcdMuEnriched_desy_cff")
process.load("ApeEstimator.Utils.samples.data_Run2011A_PromptV4_cff")



##
## Number of Events (should be after input file)
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1001) )



##
## ALCARECOTkAlMuonIsolated and additional selection
##
process.load("ApeEstimator.ApeEstimator.AlcaRecoSelection_cff")



##
## Path
##
process.path = cms.Path(
    process.mySeqALCARECOTkAlMuonIsolated*
    process.seqVertexSelection
)



##
## Define event selection from path
##
EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('path')
    )
)



##
## configure output module
##
process.out = cms.OutputModule("PoolOutputModule",
    ## Parameters directly for PoolOutputModule
    #fileName = cms.untracked.string(os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/test.root'),
    fileName = cms.untracked.string('alcarecoMuonIsolated.root'),
    # Maximum size per file before a new one is created
    #maxSize = cms.untracked.int32(500000),
    dropMetaData = cms.untracked.string("DROPPED"),
    #dataset = cms.untracked.PSet(
    #    filterName = cms.untracked.string('TkAlMuonIsolated'),
    #    dataTier = cms.untracked.string('ALCARECO'),
    #),
    
    ## Parameters for inherited OutputModule
    SelectEvents = EventSelection.SelectEvents,
    outputCommands = cms.untracked.vstring(
        'drop *',
	'keep *_ALCARECOTkAlMuonIsolated_*_*', 
        'keep L1AcceptBunchCrossings_*_*_*',
        'keep L1GlobalTriggerReadoutRecord_gtDigis_*_*',
        'keep *_TriggerResults_*_*',
    ),
)



##
## Outpath
##
process.outpath = cms.EndPath(process.out)




