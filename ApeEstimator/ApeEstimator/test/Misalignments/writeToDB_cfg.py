# Config is used to misalign the design geometry

import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")
# Message logger service
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('INFO'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(10000000)
    )
)



# Ideal geometry producer
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Geometry.TrackerNumberingBuilder.trackerNumberingGeometry_cfi")



# Misalignment example scenario producer
process.load("ApeEstimator.ApeEstimator.MisalignedTracker_cff")
process.MisalignedTrackerForApe.scenario = process.Tob20



# data loop
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)



# Database output service
import CondCore.DBCommon.CondDBSetup_cfi
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    CondCore.DBCommon.CondDBSetup_cfi.CondDBSetup,
    # Writing to oracle needs the following shell variable setting (in zsh):
    # export CORAL_AUTH_PATH=/afs/cern.ch/cms/DB/conddb
    # connect = cms.string('oracle://cms_orcoff_prep/CMS_COND_ALIGNMENT'),  # preparation/develop. DB
    timetype = cms.untracked.string('runnumber'),   # runnumber is default
    connect = cms.string('sqlite_file:AlignmentsTob20.db'),
    toPut = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario')
      ), 
      cms.PSet(
        record = cms.string('TrackerAlignmentErrorRcd'),
        tag = cms.string('TrackerScenarioErrors')
      )
    )
)
process.PoolDBOutputService.DBParameters.messageLevel = 2





# execution of one module needed to really start the producer
#process.prod = cms.EDAnalyzer("TestAnalyzer",
#    fileName = cms.untracked.string('misaligned.root')
#)
process.prod = cms.EDAnalyzer("TestTrackerHierarchy",
    dumpAlignments = cms.untracked.bool(False) # (True)
)



process.p1 = cms.Path(process.prod)

