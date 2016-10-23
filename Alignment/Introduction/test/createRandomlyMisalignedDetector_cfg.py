import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import copy, sys, os

process = cms.Process("Misaligner")


###################################################################
# Options
# Can be overwritten via command line
###################################################################
options = VarParsing.VarParsing()
options.register(
    'scenario',
    "PixelMisalignmentScenario1", # default value
    VarParsing.VarParsing.multiplicity.singleton,
    VarParsing.VarParsing.varType.string,
    "scenario to apply"
)
options.parseArguments()


###################################################################
# Message logger service
###################################################################
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('INFO'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(10000000)
    )
)


###################################################################
# Ideal geometry producer and standard includes
###################################################################
process.load('Configuration.Geometry.GeometryRecoDB_cff')


###################################################################
# Just state the Global Tag (and pick some run)
###################################################################
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_design', '') # using ideal geom
print "Using global tag: %s" % process.GlobalTag.globaltag._value


###################################################################
# This uses the object from the tag and applies the misalignment
# scenario on top of that object
###################################################################
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
process.AlignmentProducer.doMisalignmentScenario   = True
process.AlignmentProducer.applyDbAlignment         = True
process.AlignmentProducer.checkDbAlignmentValidity = False #otherwise error thrown for IOV dependent GTs

# import all known misalignment scenarios
from Alignment.Introduction.MisalignmentScenarios_cff import *

# select scenario based on set options
scenarioExists = False
for objname,oid in globals().items():
    if (str(objname) == str(options.scenario)):
        scenarioExists = True
        print "Using scenario:",objname
        process.AlignmentProducer.MisalignmentScenario = oid
if not scenarioExists:
    print "----- Begin Fatal Exception -----------------------------------------------"
    print "Unrecognized",options.scenario,"misalignment scenario !!!!"
    print "Aborting cmsRun now, please check your input"
    print "----- End Fatal Exception -------------------------------------------------"
    os._exit(1)

process.AlignmentProducer.saveToDB    = True
process.AlignmentProducer.saveApeToDB = False


###################################################################
# Output name
###################################################################
outputfilename = "geometry_"+str(options.scenario)+"_from"+process.GlobalTag.globaltag._value.replace('::All','')+".db"


###################################################################
# Source
###################################################################
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)


###################################################################
# Database output service
###################################################################
from CondCore.CondDB.CondDB_cfi import CondDB
process.PoolDBOutputService = cms.Service(
    "PoolDBOutputService",
    CondDB,
    timetype = cms.untracked.string('runnumber'),
    toPut = cms.VPSet(
        cms.PSet(
            record = cms.string('TrackerAlignmentRcd'),
            tag = cms.string('Alignments')
        ), 
    ),
)
process.PoolDBOutputService.connect = cms.string('sqlite_file:'+outputfilename)
process.PoolDBOutputService.DBParameters.messageLevel = 2
