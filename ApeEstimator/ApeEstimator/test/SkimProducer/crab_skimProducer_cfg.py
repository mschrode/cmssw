import os

import FWCore.ParameterSet.Config as cms



##
## Setup command line options
##
###import FWCore.ParameterSet.VarParsing as VarParsing
##import sys
###options = VarParsing.VarParsing ('standard')
###options.register('sample', 'data1', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Input sample")
###options.register('atCern', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "At DESY or at CERN")
###options.register('useTrackList', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Use list of preselected tracks")
###options.register('isTest', True, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Test run")

# get and parse the command line arguments
###if( hasattr(sys, "argv") ):
###    for args in sys.argv :
###        arg = args.split(',')
###        for val in arg:
###            val = val.split('=')
###            if(len(val)==2):
###                setattr(options,val[0], val[1])

###print "Input sample: ", options.sample
###print "At CERN: ", options.atCern
###print "Use list of preselected tracks: ", options.useTrackList
###print "Test run: ", options.isTest



##
## Process definition
##
process = cms.Process("ApeSkim")



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



###isData1 = isData2 = isData3 = isData4 = False
###isData = False
###isQcd = isWlnu = isZmumu = isZtautau = isZmumu10 = isZmumu20 = False
###isMc = False
###if options.sample == 'data1':
###    isData1 = True
    isData = True
elif options.sample == 'data2':
    isData2 = True
    isData = True
elif options.sample == 'data3':
    isData3 = True
    isData = True
elif options.sample == 'data4':
    isData4 = True
    isData = True
elif options.sample == 'qcd':
    isQcd = True
    isMc = True
elif options.sample == 'wlnu':
    isWlnu = True
    isMc = True
elif options.sample == 'zmumu':
    isZmumu = True
    isMc = True
elif options.sample == 'ztautau':
    isZtautau = True
    isMc = True
elif options.sample == 'zmumu10':
    isZmumu10 = True
    isMc = True
elif options.sample == 'zmumu20':
    isZmumu20 = True
    isMc = True
else:
    print 'ERROR --- incorrect data sammple: ', options.sample
    exit(8888)



##
## Input Files
##
#if isData: process.load("ApeEstimator.ApeEstimator.samples.alcareco.data_TkAlMuonIsolated_Run2010B_Dec22ReReco_cff")
#if isQcd: process.load("ApeEstimator.ApeEstimator.samples.alcareco.mc_TkAlMuonIsolated_Spring11_qcdMuEnriched_cff")
#if isWlnu: process.load("ApeEstimator.ApeEstimator.samples.alcareco.mc_TkAlMuonIsolated_Spring11_wlnu_cff")
#if isZmumu: process.load("ApeEstimator.ApeEstimator.samples.alcareco.mc_TkAlMuonIsolated_Spring11_zmumu_cff")
#if isZtautau: process.load("ApeEstimator.ApeEstimator.samples.alcareco.mc_TkAlMuonIsolated_Spring11_ztautau_cff")

if isData1: process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_22Jan2013A_v1_cff")
if isData2: process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_22Jan2013B_v1_cff")
if isData3: process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_22Jan2013C_v1_cff")
if isData4: process.load("ApeEstimator.ApeEstimator.samples.Data_TkAlMuonIsolated_22Jan2013D_v1_cff")
if isQcd: process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer12_qcd_cff")
if isWlnu: process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer12_wlnu_cff")
if isZmumu10: process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer12_zmumu10_cff")
if isZmumu20: process.load("ApeEstimator.ApeEstimator.samples.Mc_TkAlMuonIsolated_Summer12_zmumu20_cff")




##
## Number of Events (should be after input file)
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
if options.isTest: process.maxEvents.input = 1001



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
process.TrackList.trackListFileName = '/afs/cern.ch/user/a/ajkumar/scratch0/trackList/goodTrackList_' + options.sample + '.root'
#if options.isTest: process.TrackList.trackListFileName = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/Utils/hists/test_trackList.root'
#print process.TrackList.trackListFileName



##
## Skim tracks
##
import ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff
process.MuSkim = ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff.MuSkimSelector



##
## If preselected track list is used
##
if options.useTrackList:
    process.MuSkim.src = 'TrackList'
    #process.TriggerSelectionSequence *= process.TrackList



##
## Path
##
process.path = cms.Path(
    #process.TriggerSelectionSequence*
    process.MuSkim
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
        'drop *',
    ),
)
process.load("ApeEstimator.ApeEstimator.PrivateSkim_EventContent_cff")
process.out.outputCommands.extend(process.ApeSkimEventContent.outputCommands)

#if isData1:
#  if options.atCern:
#    process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/data/DoubleMu/Run2011A_May10ReReco/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/data/apeSkim.root'
#elif isData2:
#  if options.atCern:
#    #process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/data/DoubleMu/Run2011A_PromptV4/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#    process.out.fileName = 'apeSkim.root'
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/data/apeSkim.root'
#if isQcd:
#  if options.atCern:
#    process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/mc/Summer11/qcd/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/qcd/apeSkim.root'
#elif isWlnu:
#  if options.atCern:
#    process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/mc/Summer11/wlnu/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/wlnu/apeSkim.root'
#elif isZmumu:
#  if options.atCern:
#    process.out.fileName = ''
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/zmumu/apeSkim.root'
#elif isZtautau:
#  if options.atCern:
#    process.out.fileName = ''
#  else:
#    process.out.fileName = '/scratch/hh/current/cms/user/ajkumar/data/alcareco/ztautau/apeSkim.root'
#elif isZmumu10:
#  if options.atCern:
#    process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/mc/Summer11/zmumu10/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#  else:
#    process.out.fileName = ''
#elif isZmumu20:
#  if options.atCern:
#    process.out.fileName = 'root://eoscms//eos/cms/store/caf/user/ajkumar/mc/Summer11/zmumu20/apeSkim.root?svcClass=cmscafuser&stageHost=castorcms'
#  else:
#    process.out.fileName = ''
if options.isTest:
  process.out.fileName = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/test_apeSkim.root'





##
## Outpath
##
process.outpath = cms.EndPath(process.out)




