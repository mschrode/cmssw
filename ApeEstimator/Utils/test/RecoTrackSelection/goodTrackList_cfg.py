import os

import FWCore.ParameterSet.Config as cms




##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('sample', 'data2', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Input sample")
options.register('isTest', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Test run")
options.register('useCrab', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Run via CRAB")

# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

print "Input sample: ", options.sample
print "Test run: ", options.isTest
print "Run via CRAB: ", options.useCrab



##
## Process definition
##
process = cms.Process("GoodTrackList")



##
## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('TrackListGenerator')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = -1  # Do not use =0, else all error messages (except those listed below) are supressed
process.MessageLogger.cerr.TrackListGenerator = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 ## really show only every 1000th



##
## Process options
##
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)



##
## Input sample definition
##
isData1 = isData2 = False
isData = False
isQcd = isWlnu = isZmumu1 = isZmumu2 = isZtautau = False
isMc = False
if options.sample == 'data1':
    isData1 = True
    isData = True
elif options.sample == 'data2':
    isData2 = True
    isData = True
elif options.sample == 'qcd':
    isQcd = True
    isMc = True
elif options.sample == 'wlnu':
    isWlnu = True
    isMc = True
elif options.sample == 'zmumu1':
    isZmumu1 = True
    isMc = True
elif options.sample == 'zmumu2':
    isZmumu2 = True
    isMc = True
elif options.sample == 'ztautau':
    isZtautau = True
    isMc = True
else:
    print 'ERROR --- incorrect data sammple: ', options.sample
    exit(8888)



##
## Input Files
##
process.load("ApeEstimator.Utils.samples.data_Run2011A_PromptV4_cff")
#if isData1:
#    pass
#elif isData2:
#    process.load("ApeEstimator.Utils.samples.data_Run2011A_PromptV4_cff")
#elif isQcd:
#    #process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Fall10_QcdMuPt10_cff")
#    #process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Fall10_QcdMuPt10_ApeSkim_cff")
#    process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Spring11_QcdMuPt15_ApeSkim_cff")
#elif isWlnu:
#    #process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Fall10_WToMuNu_cff")
#    #process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Fall10_WToMuNu_ApeSkim_cff")
#    process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Spring11_WJetsToLNu_ApeSkim_cff")
#elif isZmumu:
#    #process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Fall10_DYToMuMu_ApeSkim_cff")
#    process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Spring11_DYToMuMu_ApeSkim_cff")
#elif isZtautau:
#    process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Spring11_DYToTauTau_ApeSkim_cff")
    


##
## Number of Events (should be after input file)
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
if options.isTest: process.maxEvents.input = 1001



##
## Track and event selection
##
process.load("ApeEstimator.ApeEstimator.AlcaRecoSelection_cff")



##
## Track List Generator
##
process.load("ApeEstimator.Utils.TrackListGenerator_cfi")
process.TrackListGenerator.trackSource = 'ALCARECOTkAlMuonIsolated'



##
## Output File Configuration
##
outputName = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/Utils/hists/'
if options.isTest:
    outputName = outputName + 'test_'
outputName = outputName + options.sample + '_goodTrackList.root'

if options.useCrab:
    outputName = 'goodTrackList.root'

process.TFileService = cms.Service("TFileService",
    fileName = cms.string(outputName),
    closeFileFast = cms.untracked.bool(True)
)



##
## Path
##
process.p = cms.Path(
    process.mySeqALCARECOTkAlMuonIsolated*
    process.seqVertexSelection*
    process.TrackListGenerator
)



