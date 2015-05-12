import FWCore.ParameterSet.Config as cms

process = cms.Process("APEtoASCIIDump")

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff') 
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_design', '')

import CalibTracker.Configuration.Common.PoolDBESSource_cfi
process.apeRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
    connect = cms.string("sqlite_file:/afs/cern.ch/user/m/mschrode/APE/APEfromRandomMisalignment/CMSSW_7_4_1/src/Alignment/APEEstimation/test/TkAlignmentApe_test2.db"),
    toGet = cms.VPSet(
        cms.PSet(
            record = cms.string('TrackerAlignmentErrorExtendedRcd'),
            tag = cms.string('testTagAPE')
        )
    )
)
process.prefer_apeRcd = cms.ESPrefer("PoolDBESSource", "apeRcd")


process.load('Configuration.Geometry.GeometryExtended_cff')
process.TrackerTopologyEP = cms.ESProducer("TrackerTopologyEP")

# Alignment producer
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
from Alignment.CommonAlignmentAlgorithm.ApeSettingAlgorithm_cfi import *
process.AlignmentProducer.algoConfig = ApeSettingAlgorithm
process.AlignmentProducer.applyDbAlignment = cms.untracked.bool(True)
process.AlignmentProducer.saveApeToDB = True
process.AlignmentProducer.algoConfig.readApeFromASCII = False
process.AlignmentProducer.algoConfig.setComposites = False
process.AlignmentProducer.algoConfig.readLocalNotGlobal = False
process.AlignmentProducer.algoConfig.readFullLocalMatrix = True
process.AlignmentProducer.algoConfig.apeASCIIReadFile = 'Alignment/APEEstimation/macros/ape.txt'
process.AlignmentProducer.algoConfig.saveApeToASCII = True
process.AlignmentProducer.algoConfig.saveComposites = False
process.AlignmentProducer.algoConfig.saveLocalNotGlobal = cms.untracked.bool(False)
process.AlignmentProducer.algoConfig.apeASCIISaveFile = 'myDump.txt'
        
# to be refined...
process.MessageLogger = cms.Service("MessageLogger",
    statistics = cms.untracked.vstring('cout', 'alignment'),
    categories = cms.untracked.vstring('Alignment'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('DEBUG'),
        noLineBreaks = cms.untracked.bool(True)
    ),
    alignment = cms.untracked.PSet(
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        ),
        noLineBreaks = cms.untracked.bool(True),
        DEBUG = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        ),
        WARNING = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        ),
        ERROR = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        ),
        threshold = cms.untracked.string('INFO'),
        Alignment = cms.untracked.PSet(
            limit = cms.untracked.int32(-1)
        )
    ),
    destinations = cms.untracked.vstring('cout',  ## .log automatically
        'alignment')
)

process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

from CondCore.DBCommon.CondDBSetup_cfi import *
process.PoolDBOutputService = cms.Service(
    "PoolDBOutputService",
    CondDBSetup,
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:TkAlignmentApe.db'),
    toPut = cms.VPSet(
        cms.PSet(
            record = cms.string('TrackerAlignmentErrorExtendedRcd'),
            tag = cms.string('testTagAPE')
        )
    )
)

# We do not even need a path - producer is called anyway...
