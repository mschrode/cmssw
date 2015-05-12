# This file is used to misalign a given geometry
# modified version of alignment_forGeomComp_cfg.py

# Config file template to produce a treeFile.root usable as input for
# .../CMSSW/Alignment/MillePedeAlignmentAlgorithm/macros/CompareMillePede.h
# to compare two different geometries.
#
# last update on $Date: 2012/01/23 23:06:15 $ by $Author: hauk $

import FWCore.ParameterSet.Config as cms



##
## Setup command line options
##
import FWCore.ParameterSet.VarParsing as VarParsing
import sys
options = VarParsing.VarParsing ('standard')
options.register('iov', 'A', VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.string, "IOV")
options.register('spread', 5, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, "Spread of misalignment")

# get and parse the command line arguments
if( hasattr(sys, "argv") ):
    for args in sys.argv :
        arg = args.split(',')
        for val in arg:
            val = val.split('=')
            if(len(val)==2):
                setattr(options,val[0], val[1])

print "IOV: ", options.iov
print "Spread of misalignment in micron: ", options.spread
gaussSpread = float(options.spread)/10000.
print "Spread of misalignment in cm: ", gaussSpread




##
## Process
##
process = cms.Process("Alignment")
process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring("ProductNotFound") # do not accept this exception
)



##
##  Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.alignment = cms.untracked.PSet(
    DEBUG = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
    ),
    INFO = cms.untracked.PSet(
        limit = cms.untracked.int32(5),
        reportEvery = cms.untracked.int32(5)
    ),
    WARNING = cms.untracked.PSet(
        limit = cms.untracked.int32(10)
    ),
    ERROR = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
    ),
    Alignment = cms.untracked.PSet(
        limit = cms.untracked.int32(-1),
        reportEvery = cms.untracked.int32(1)
    )
)
process.MessageLogger.cerr.placeholder = cms.untracked.bool(True)
process.MessageLogger.destinations = ['alignment']
process.MessageLogger.statistics = ['alignment']
process.MessageLogger.categories = ['Alignment']



##
## Conditions (Geometry from GlobalTag is used if no other one is specified with a ESPrefer command)
##
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'DESIGN53_V9::All' # take your favourite



##
## If alignment constants not from global tag, add starting geometry here
##
from CondCore.DBCommon.CondDBSetup_cfi import *
process.trackerAlignment = cms.ESSource(
    "PoolDBESSource",
    CondDBSetup,
    connect = cms.string("frontier://FrontierProd/CMS_COND_31X_ALIGNMENT"),
    toGet = cms.VPSet(
        cms.PSet(
	    record = cms.string("TrackerAlignmentRcd"),
            tag = cms.string("TrackerAlignment_GR10_v6_offline"),
        ),
        #cms.PSet(
	#    record = cms.string("TrackerAlignmentErrorRcd"),
        #    tag = cms.string("TrackerIdealGeometryErrors210_mc"),
        #),
    ),
)
process.es_prefer_trackerAlignment = cms.ESPrefer("PoolDBESSource", "trackerAlignment")



##
## Alignment producer (mainly dummy, no alignment algorithm is run)
##
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
process.AlignmentProducer.ParameterBuilder.Selector = cms.PSet(
    alignParams = cms.vstring(
        'TrackerTPBModule,111111',
        'TrackerTPEModule,111111',
        'TrackerTIBModuleUnit,101111',
        'TrackerTIDModuleUnit,101111',
        'TrackerTOBModuleUnit,101111',
        'TrackerTECModuleUnit,101111'
    ),
)
# assign by reference (i.e. could change MillePedeAlignmentAlgorithm as well):
process.AlignmentProducer.algoConfig = process.MillePedeAlignmentAlgorithm
process.AlignmentProducer.algoConfig.mode = 'pedeRead'
process.AlignmentProducer.algoConfig.pedeReader.readFile = 'FILE_MUST_NOT_EXIST.res'
process.AlignmentProducer.algoConfig.treeFile = 'my_treeFile_' + str(options.spread) + '_' + options.iov + '.root'
# Now set the misalignment scenario
process.AlignmentProducer.doMisalignmentScenario = True
process.AlignmentProducer.applyDbAlignment = True # either globalTag or trackerAlignment
process.AlignmentProducer.saveToDB = True # should not be needed, but is: otherwise AlignmentProducer does not  call relevant algorithm part
#process.AlignmentProducer.saveApeToDB = True
from ApeEstimator.ApeEstimator.MisalignedTracker_cff import PixelTob5
PixelTob5.TOBHalfBarrels.DetUnits.dXlocal = gaussSpread
PixelTob5.TPBHalfBarrels.DetUnits.dXlocal = gaussSpread
PixelTob5.TPBHalfBarrels.DetUnits.dYlocal = gaussSpread
PixelTob5.TPEEndcaps.DetUnits.dXlocal = gaussSpread
PixelTob5.TPEEndcaps.DetUnits.dYlocal = gaussSpread
process.AlignmentProducer.MisalignmentScenario = PixelTob5



##
## Empty source, but give run number to have correct geometry corresponding to IOV which contains given run number
##
process.source = cms.Source("EmptySource",
    firstRun = cms.untracked.uint32(170249), # choose your run!
)
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1) )



##
## IOV period
##
if options.iov == 'A':
    process.source.firstRun = 158000
elif options.iov == 'B':
    process.source.firstRun = 160000
elif options.iov == 'C':
    process.source.firstRun = 162000
elif options.iov == 'D':
    process.source.firstRun = 164000
elif options.iov == 'E':
    process.source.firstRun = 165000
elif options.iov == 'F':
    process.source.firstRun = 165500
elif options.iov == 'G':
    process.source.firstRun = 166200
elif options.iov == 'H':
    process.source.firstRun = 167000
elif options.iov == 'I':
    process.source.firstRun = 167050
elif options.iov == 'P1':
    process.source.firstRun = 171000
elif options.iov == 'P2':
    process.source.firstRun = 172000
elif options.iov == 'P3':
    process.source.firstRun = 174000
else:
    print 'ERROR --- incorrect IOV range: ', options.iov
    exit(8888)



##
## Process (needs some analyzer to run)
##
process.dump = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(process.dump)



##
## Output module
##
process.PoolDBOutputService = cms.Service(
    "PoolDBOutputService",
    CondDBSetup,
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:pixelTobMisaligned_' + str(options.spread) + '_' + options.iov + '.db'),
    toPut = cms.VPSet(
      cms.PSet(
        record = cms.string('TrackerAlignmentRcd'),
        tag = cms.string('TrackerScenario'),
      )
    )
)

