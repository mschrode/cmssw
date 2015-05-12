import os

import FWCore.ParameterSet.Config as cms




##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('iterNumber', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "Iteration number")
options.register('setBaseline', False, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, "Set baseline")



# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

print "Iteration number: ", options.iterNumber
print "Set baseline: ", options.setBaseline



if options.setBaseline:
    print "Set baseline mode, do not create APE DB-object"
    exit(1)


##
## Process definition
##
process = cms.Process("APE")
# we need conditions
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'IDEAL_V11::All'

# include "Configuration/StandardSequences/data/FakeConditions.cff"
# initialize magnetic field
#process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("Configuration.Geometry.GeometryDB_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = 'POSTLS170_V6::All'
#////////////////////////////////////////////////////////
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')


#///////////////////////////////////
# ideal geometry and interface
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")
process.load("Configuration.Geometry.GeometryDB_cff")

#process.load("Geometry.TrackerNumberingBuilder.trackerNumberingGeometry_cfi")
# for Muon: include "Geometry/MuonNumbering/data/muonNumberingInitialization.cfi"

# track selection for alignment
#process.load("Alignment.CommonAlignmentProducer.AlignmentTrackSelector_cfi")

# Alignment producer
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
from Alignment.CommonAlignmentAlgorithm.ApeSettingAlgorithm_cfi import *
process.AlignmentProducer.algoConfig = ApeSettingAlgorithm
process.AlignmentProducer.saveApeToDB = True
process.AlignmentProducer.algoConfig.readApeFromASCII = True
process.AlignmentProducer.algoConfig.setComposites = False
process.AlignmentProducer.algoConfig.readLocalNotGlobal = True
process.AlignmentProducer.algoConfig.readFullLocalMatrix = True
# CAVEAT: Input file name has to start with a Package name...
process.AlignmentProducer.algoConfig.apeASCIIReadFile = 'ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/allData_apeOutput.txt'
process.AlignmentProducer.algoConfig.saveApeToASCII = True 
process.AlignmentProducer.algoConfig.saveComposites = False
process.AlignmentProducer.algoConfig.apeASCIISaveFile = 'myLocalDump.txt'
        
# replace AlignmentProducer.doMisalignmentScenario = true
# replace AlignmentProducer.applyDbAlignment = true # needs other conditions than fake!
# Track refitter (adapted to alignment needs)
#process.load("RecoTracker.TrackProducer.RefitterWithMaterial_cff")

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
            limit = cms.untracked.int32(0)
        ),
        noLineBreaks = cms.untracked.bool(True),
        DEBUG = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        WARNING = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        ERROR = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

from CondCore.DBCommon.CondDBSetup_cfi import *
process.PoolDBOutputService = cms.Service(
    "PoolDBOutputService",
    CondDBSetup,
    timetype = cms.untracked.string('runnumber'),
    #connect = cms.string('sqlite_file:ape.db'),
    connect = cms.string('sqlite_file:'+os.environ['CMSSW_BASE']+'/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/apeIter'+str(options.iterNumber)+'.db'),
    #toPut = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorRcd'),
    toPut = cms.VPSet(cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
            tag = cms.string('AlignmentErrors')
        )
    )
)



# We do not even need a path - producer is called anyway...
#process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
#process.p = cms.Path(process.offlineBeamSpot)
#process.TrackRefitter.src = 'AlignmentTrackSelector'
#process.TrackRefitter.TrajectoryInEvent = True


