import os

import FWCore.ParameterSet.Config as cms




##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('sample', 'data1', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Input sample")
options.register('fileNumber', 1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Input file number")
options.register('iterNumber', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Iteration number")
options.register('lastIter', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Last iteration")
options.register('alignRcd','design', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "AlignmentRcd")



# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

#print "Input sample: ", options.sample
#print "Input file number", options.fileNumber
print "Iteration number: ", options.iterNumber
print "Last iteration: ", options.lastIter
print "AlignmentRcd: ", options.alignRcd
isParticleGun = False
isMc = True

##
## Process definition
##
process = cms.Process("ApeEstimator")

process.load("RecoVertex.BeamSpotProducer.BeamSpot_cff")
process.load("Configuration.StandardSequences.Services_cff")
#process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("CondCore.DBCommon.CondDBCommon_cfi")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#process.GlobalTag.globaltag = ' POSTLS170_V6::All'
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "POSTLS170_V6::All"


##
## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('SectorBuilder')
process.MessageLogger.categories.append('ResidualErrorBinning')
process.MessageLogger.categories.append('HitSelector')
process.MessageLogger.categories.append('CalculateAPE')
process.MessageLogger.categories.append('ApeEstimator')
process.MessageLogger.categories.append('TrackRefitter')
process.MessageLogger.categories.append('AlignmentTrackSelector')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.SectorBuilder = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.HitSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.CalculateAPE = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.ApeEstimator = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.AlignmentTrackSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 10 ## really show only every 1000th



##
## Process options
##
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)

##
## Input Files
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                      fileNames=cms.untracked.vstring(
                        #'root://eoscms//eos/cms/store/caf/user/ajkumar/ApeSkim71/zmumu50/apeSkim1.root'
			#'root://eoscms//eos/store/caf/user/ajkumar/apeSkim_1_1_0X0.root'
			#'file:/afs/cern.ch/work/a/ajkumar/APE_newCPE/CMSSW_7_2_0_pre6/src/apeSkim_1_1_0X0.root'
	'file:/afs/cern.ch/work/a/ajkumar/APE_newCPE_v1/CMSSW_7_2_0_pre6/src/ApeEstimator/ApeEstimator/test/SkimProducer/apeSkim.root'
                        ),
#                        firstRun = cms.untracked.uint32(2),
#                        firstEvent = cms.untracked.uint32(4)
       )

##
#readFiles = cms.untracked.vstring()
#process.source = cms.Source ("PoolSource",
#    fileNames = readFiles
#)
#readFiles.extend( [
#    'file:reco.root',
#] )

## Check run and event numbers for Dublicates --- only for real data
##
#process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")
#process.source.duplicateCheckMode = cms.untracked.string("checkEachFile")
process.source.duplicateCheckMode = cms.untracked.string("checkEachRealDataFile")
#process.source.duplicateCheckMode = cms.untracked.string("checkAllFilesOpened")   # default value

##
## Whole Refitter Sequence


#process.load("RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi")
#process.MeasurementTrackerEvent.pixelClusterProducer = 'MuSkim'
#process.MeasurementTrackerEvent.stripClusterProducer = 'MuSkim'
#process.MeasurementTrackerEvent.inactivePixelDetectorLabels = cms.VInputTag()
#process.MeasurementTrackerEvent.inactiveStripDetectorLabels = cms.VInputTag()


#process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
#from RecoTracker.TrackProducer.TrackRefitters_cff import *

import RecoTracker.TrackProducer.TrackRefitters_cff
process.TrackRefitter = RecoTracker.TrackProducer.TrackRefitter_cfi.TrackRefitter.clone()
process.TrackRefitter.src = "MuSkim"
process.TrackRefitter.TrajectoryInEvent = True
process.TrackRefitter.TTRHBuilder = "WithAngleAndTemplate"
process.TrackRefitter.NavigationSchool = ""

#import RecoTracker.TrackProducer.TrackRefitters_cff
#process.TrackRefitter = TrackRefitter.clone(
#  src = 'MuSKim',
#  TrajectoryInEvent = True,
#  TTRHBuilder = "WithAngleAndTemplate",
#  NavigationSchool = ""
#)

##
process.load("ApeEstimator.ApeEstimator.TrackRefitter_38T_cff")

#if isMc:
#    process.GlobalTag.globaltag = 'DESIGN72_V1::All'
#    elif options.alignRcd=='useStartGlobalTagForAllConditions':
#	process.GlobalTag.globaltag = 'DESIGN72_V1::All'
#else isData:
#    process.GlobalTag.globaltag = 'FT_R_53_V18::All'
#process.FittingSmootherRKP5.EstimateCut = 25.
#process.FittingSmootherRKP5.RejectTracks = True
#process.FittingSmootherRKP5.LogPixelProbabilityCut = -14.
#process.HighPuritySelector.src = 'generalTracks'
process.HighPuritySelector.src = 'MuSkim'


 ##
 ## Load and Configure TrackRefitter
 ##



##
## New pixel templates
#if isData:
#    process.GlobalTag.toGet = cms.VPSet(
#    cms.PSet(
#    record = cms.string("SiPixelTemplateDBObjectRcd"),
#    tag = cms.string("SiPixelTemplateDBObject_38T_v4_offline"),
#    connect = cms.untracked.string("frontier://FrontierArc/CMS_COND_PIXEL_DA14"),
#    )
#)
#else:
##
process.GlobalTag.toGet = cms.VPSet(
   cms.PSet(
    record = cms.string("SiPixelTemplateDBObjectRcd"),
    tag = cms.string("SiPixelTemplateDBObject_38T_v3_mc"),
    connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PIXEL"),
   )
)
## Alignment and APE
##
import CalibTracker.Configuration.Common.PoolDBESSource_cfi
## Choose Alignment (w/o touching APE)
if options.alignRcd=='design':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_31X_FROM21X',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerIdealGeometry210_mc'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'misalTob20':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/work/a/ajkumar/APE_538_patch1_git/CMSSW_5_3_8_patch1/src/ApeEstimator/ApeEstimator/test/Misalignments/AlignmentsTob20.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'idealAligned':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/idealAlignedGeometry/alignments_MP.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('Alignments'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
elif options.alignRcd == 'data_v9a_offline':
  # Recent geometry of data
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierArc/CMS_COND_31X_ALIGNMENT_DA14',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerAlignment_v9a_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierArc/CMS_COND_310X_ALIGN_DA14',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v3_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6':
  # Recent geometry
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_31X_ALIGNMENT',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerAlignment_GR10_v6_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus5':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_5.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus10':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_10.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus15':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_15.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'GR10_v6_plus20':
  process.myTrackerAlignment = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'sqlite_file:/afs/cern.ch/user/h/hauk/scratch0/apeStudies/dataMisalignment/pixelTobMisaligned_20.db',
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
  )
  process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource","myTrackerAlignment")
  # Kinks and bows
  process.myTrackerAlignmentKinksAndBows = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = 'frontier://FrontierProd/CMS_COND_310X_ALIGN',
    toGet = [
      cms.PSet(
        record = cms.string('TrackerSurfaceDeformationRcd'),
        tag = cms.string('TrackerSurfaceDeformations_v1_offline'),
      ),
    ],
  )
  process.es_prefer_trackerAlignmentKinksAndBows = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentKinksAndBows")
elif options.alignRcd == 'globalTag':
  pass
elif options.alignRcd == 'useStartGlobalTagForAllConditions':
  pass
elif options.alignRcd == '':
  pass
else:
  print 'ERROR --- incorrect alignment: ', options.alignRcd
  exit(8888)

## APE
if options.iterNumber==0:
    process.myTrackerAlignmentErr = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
      connect = 'frontier://FrontierProd/CMS_COND_31X_FROM21X',
      toGet = [
        cms.PSet(
          record = cms.string('TrackerAlignmentErrorRcd'),
          tag = cms.string('TrackerIdealGeometryErrors210_mc'),
        ),
      ],
    )
    process.es_prefer_trackerAlignmentErr = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentErr")
else:
    process.myTrackerAlignmentErr = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
      connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/ApeEstimator/ApeEstimator/hists/apeObjects/apeIter'+str(options.iterNumber-1)+'.db',
      toGet = [
        cms.PSet(
          record = cms.string('TrackerAlignmentErrorRcd'),
          tag = cms.string('AlignmentErrors'),
        ),
      ],
    )
    process.es_prefer_trackerAlignmentErr = cms.ESPrefer("PoolDBESSource","myTrackerAlignmentErr")



##
## Beamspot (Use correct Beamspot for simulated Vertex smearing of ParticleGun)
##
if isParticleGun:
    process.load("ApeEstimator.ApeEstimator.BeamspotForParticleGun_cff")


##
## Trigger Selection
##
process.load("ApeEstimator.ApeEstimator.TriggerSelection_cff")


##
## ApeEstimator
##
from ApeEstimator.ApeEstimator.ApeEstimator_cff import *
process.ApeEstimator1 = ApeEstimator.clone(
    tjTkAssociationMapTag = "TrackRefitterHighPurityForApeEstimator",
    analyzerMode = False,
)

process.ApeEstimator2 = ApeAnalyzer.clone()
process.ApeEstimator3 = process.ApeEstimator2.clone(
    zoomHists = False,
)

process.ApeEstimatorSequence = cms.Sequence(process.ApeEstimator1)
if options.iterNumber==0:
  process.ApeEstimatorSequence *= process.ApeEstimator2
  process.ApeEstimatorSequence *= process.ApeEstimator3
elif options.lastIter == True:
  process.ApeEstimatorSequence *= process.ApeEstimator2



##
## Output File Configuration
##
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/workingArea/'+options.sample+str(options.fileNumber)+'.root'),
    #fileName = cms.string("Output_APE.root"),
    closeFileFast = cms.untracked.bool(True)
)



##
## Path
##
process.p = cms.Path(
    process.TriggerSelectionSequence*
    process.offlineBeamSpot*
    #process.MeasurementTrackerEvent*
    process.TrackRefitter*
    process.RefitterHighPuritySequence*
    process.ApeEstimatorSequence
)



