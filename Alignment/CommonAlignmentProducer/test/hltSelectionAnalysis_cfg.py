import FWCore.ParameterSet.Config as cms

process = cms.Process("HLTSelectionAnalysis")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000000)

#process.load('Configuration.StandardSequences.MagneticField_cff')
#process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff') 
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
print "Using global tag: %s" % process.GlobalTag.globaltag

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        "/store/data/Run2015D/Cosmics/ALCARECO/TkAlCosmics0T-PromptReco-v3/000/256/873/00000/14207219-1B61-E511-8BD9-02163E0146F5.root"
    )
)

from Alignment.CommonAlignmentProducer.hltSelectionAnalyzer_cfi import hltSelectionAnalyzer
process.analysis = hltSelectionAnalyzer.clone()

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("HLTSelection.root")
)

process.p = cms.Path(
    process.analysis
)



