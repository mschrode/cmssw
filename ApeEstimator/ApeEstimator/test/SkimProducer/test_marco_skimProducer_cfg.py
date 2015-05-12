import os

import FWCore.ParameterSet.Config as cms


##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('sample', 'data1', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Input sample")
options.register('atCern', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "At DESY or at CERN")
options.register('useTrackList', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Use list of preselected tracks")
options.register('isTest', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Test run")

# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

print "Input sample: ", options.sample
print "At CERN: ", options.atCern
print "Use list of preselected tracks: ", options.useTrackList
print "Test run: ", options.isTest


isMc = True
isData = False


## Process definition
##
process = cms.Process("ApeSkim")

## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('AlignmentTrackSelector')
process.MessageLogger.categories.append('')
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

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")
process.load("Configuration.StandardSequences.Services_cff")
#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("Configuration.Geometry.GeometryDB_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("CondCore.DBCommon.CondDBCommon_cfi")

###process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#process.GlobalTag.globaltag = 'DESIGN72_V1::All'
###process.GlobalTag.globaltag = 'POSTLS170_V6::All'

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')
##
## Input Files

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                      fileNames=cms.untracked.vstring(
                        '/store/mc/Spring14dr/DYToMuMu_M-15To50_Tune4C_13TeV-pythia8/ALCARECO/TkAlMuonIsolated-castor_PU_S14_POSTLS170_V6-v1/00000/200D2801-7DF1-E311-A513-003048D439BE.root'

#       '/store/mc/Spring14dr/DYToMuMu_M-15To50_Tune4C_13TeV-pythia8/ALCARECO/TkAlMuonIsolated-castor_PU_S14_POSTLS170_V6-v1/00000/200D2801-7DF1-E311-A513-003048D439BE.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/000908F2-FEEF-E311-9E61-E0CB4E29C502.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/000BD08F-91F5-E311-A0D5-E0CB4E5536F2.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/002CF56F-C5F0-E311-826B-E0CB4E29C4F6.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/00BCBD87-39F3-E311-88DE-002590D0B0BE.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/00D86FE5-C4F0-E311-A199-002590D0B0D2.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/024BF211-47F0-E311-A6BA-0025907B5048.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/0261E5F6-A8F5-E311-B5FD-20CF3027A5ED.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/0423DBF9-91F0-E311-9D22-00259073E46C.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/04490513-A8F3-E311-85DA-E0CB4E19F9A6.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/046FB835-B6F3-E311-AABD-001EC9D80270.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/04AD70FA-8EF1-E311-A8D2-00259073E3D2.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/063F2AA7-DBF0-E311-A854-002590D0AFAA.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/0699A13A-BFF3-E311-9D7C-20CF305B04F5.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/06D1A805-8DF3-E311-AD29-00259073E382.root',
#       '/store/mc/Spring14dr/MinBias_TuneZ2star_13TeV_pythia6/ALCARECO/TkAlMinBias-castor_PU_S14_POSTLS170_V6-v1/00000/089A862B-2DF3-E311-95AF-20CF305B058E.root'


                        ),
#                        firstRun = cms.untracked.uint32(2),
#                        firstEvent = cms.untracked.uint32(4)
       )

##
## Check run and event numbers only for real data
##
#process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
#process.source.duplicateCheckMode = cms.untracked.string("checkEachFile")
#process.source.duplicateCheckMode = cms.untracked.string("checkEachRealDataFile")
#process.source.duplicateCheckMode = cms.untracked.string("checkAllFilesOpened")   # default value



##
## Trigger Selection
##
#process.load("ApeEstimator.ApeEstimator.TriggerSelection_cff")
#if isData:
#    process.TriggerFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#if isMc:
#    process.TriggerFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI311X")



##
## Track List Reader
##
import ApeEstimator.Utils.TrackListReader_cfi
process.TrackList = ApeEstimator.Utils.TrackListReader_cfi.TrackListReader
process.TrackList.trackSource = 'ALCARECOTkAlMuonIsolated'
process.TrackList.trackListFileName = '/afs/cern.ch/user/a/ajkumar/scratch0/trackList/goodTrackList_' + '.root'
if options.isTest: process.TrackList.trackListFileName = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/Utils/hists/test_trackList.root'
print process.TrackList.trackListFileName



##
## Skim tracks
##
import ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff
process.MuSkim = ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff.MuSkimSelector
#process.MuSkim = ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff.MinBiasSkimSelector


##
## If preselected track list is used
##
if options.useTrackList:
    process.MuSkim.src = 'TrackList'
    process.TriggerSelectionSequence *= process.TrackList


 ##
 ## Load and Configure TrackRefitter
 ##
#process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")
#process.MeasurementTrackerEvent.pixelClusterProducer = 'ALCARECOTkAlMuonIsolated'
#process.MeasurementTrackerEvent.stripClusterProducer = 'ALCARECOTkAlMuonIsolated'
#process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
#process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag()

process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
import RecoTracker.TrackProducer.TrackRefitters_cff
process.TrackRefitter = RecoTracker.TrackProducer.TrackRefitter_cfi.TrackRefitter.clone()
process.TrackRefitter.src = "ALCARECOTkAlMuonIsolated"
process.TrackRefitter.TrajectoryInEvent = True
process.TrackRefitter.TTRHBuilder = "WithAngleAndTemplate"
process.TrackRefitter.NavigationSchool = ""



##
## Path
##
#process.path = cms.Path(
#    #process.TriggerSelectionSequence*
#    process.MuSkim
#)

process.path = cms.Path(process.offlineBeamSpot*
                      #process.MeasurementTrackerEvent*
                      process.TrackRefitter*
                      #process.MuSkimSelector*
                      process.MuSkim)#*
                      #process.myanalysis)


##
## Define event selection from path
##
EventSelection = cms.PSet(
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('path')
    )
)




## configure output module
##
process.out = cms.OutputModule("PoolOutputModule",
    ## Parameters directly for PoolOutputModule
    fileName = cms.untracked.string('apeSkim.root'),
    #logicalFileName = cms.untracked.string(''),
    #catalog = cms.untracked.string(''),
    # Maximus size per file before a new one is created
    maxSize = cms.untracked.int32(700000),
    #compressionLevel = cms.untracked.int32(0),
    #basketSize = cms.untracked.int32(0),
    #splitLevel = cms.untracked.int32(0),
    #sortBaskets = cms.untracked.string(''),
    #treeMaxVirtualSize =  cms.untracked.int32(0),
    #fastCloning = cms.untracked.bool(False),
    #overrideInputFileSplitLevels = cms.untracked.bool(True),
    dropMetaData = cms.untracked.string("DROPPED"),
    #dataset = cms.untracked.PSet(
    #    filterName = cms.untracked.string('TkAlMuonIsolated'),
    #    dataTier = cms.untracked.string('ALCARECO'),
    #),
    # Not yet implemented
    #eventAutoFlushCompressedSize = cms.untracked.int32(5*1024*1024),
    
    ## Parameters for inherited OutputModule
    SelectEvents = EventSelection.SelectEvents,
    outputCommands = cms.untracked.vstring(
        'keep *',
    ),
)
process.load("ApeEstimator.ApeEstimator.PrivateSkim_EventContent_cff")
process.out.outputCommands.extend(process.ApeSkimEventContent.outputCommands)




##
## Outpath
##
process.outpath = cms.EndPath(process.out)
process.schedule = cms.Schedule(process.path,process.outpath)



