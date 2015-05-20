########################################################################################
###
###  Read and write APEs to and from database and ASCII files
###
###  The ASCII file contains one row per module, where the first column
###  lists the module id and the following 21 columns the diagonal and
###  lower elements x11,x21,x22,x31,x32,x33,0... of the 6x6 covariance
###  matrix, where the upper 3x3 sub-matrix contains the position APEs.
###  The elements are stored in units of cm^2.
###
########################################################################################



###### Steering parameters #############################################################

### specify the input APE
#
# GT
GT = "auto:run2_design"
#
# read the APE from database or from ASCII
# True: from database, False: from ASCII
readAPEFromDB = True

### specify APE input from database (only relevant if 'readAPEFromDB=True')
#
# specify run (to get proper IOV in IOV dependent databases)
# for data payload only, "1" for MC
readDBRun = 1
#
# True: APE from GT, False: APE from es_prefer statement
readDBOverwriteGT = True 
#
# info for es_prefer to overwrite APE info in GT
# (only relevant if 'readDBOverwriteGT=True')
readDBConnect = "frontier://FrontierProd/CMS_CONDITIONS"
readDBTag     = "TrackerAlignmentExtendedErrors_v4_offline_IOVs"

### specify APE input from ASCII (only relevant if 'readAPEFromDB=False')
#
# file name (relative to $CMSSW_BASE/src)
readASCIIFile = "Alignment/APEEstimation/macros/apes_startup_pessimistic.txt"
#

### specify APE output to ASCII file
#
saveAPEtoASCII = True
saveASCIIFile = "myDump.txt"

### specify APE output to database file
#
saveAPEtoDB = True
saveAPEFile = "TkAlignmentApe.db"
saveAPETag  = "testTagAPE"



###### Main script #####################################################################

import FWCore.ParameterSet.Config as cms
process = cms.Process("APEtoASCIIDump")


### load the conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff') 
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag,GT,"")
print "Using global tag: %s" % process.GlobalTag.globaltag._value

if readAPEFromDB and readDBOverwriteGT:
    import CalibTracker.Configuration.Common.PoolDBESSource_cfi
    process.apeRcd = CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone(
        connect = cms.string(readDBConnect),
        toGet = cms.VPSet(
            cms.PSet(
                record = cms.string("TrackerAlignmentErrorExtendedRcd"),
                tag = cms.string(readDBTag)
            )
        )
    )
    process.prefer_apeRcd = cms.ESPrefer("PoolDBESSource", "apeRcd")


### load the ideal geometry
### (in 7_4_X, need to construct the TrackerTopology on the fly)
process.load('Configuration.Geometry.GeometryExtended_cff')
process.TrackerTopologyEP = cms.ESProducer("TrackerTopologyEP")


### setup the alignmnet producer to read the APEs and dump them
process.load("Alignment.CommonAlignmentProducer.AlignmentProducer_cff")
from Alignment.CommonAlignmentAlgorithm.ApeSettingAlgorithm_cfi import ApeSettingAlgorithm
#
# general settings
process.AlignmentProducer.algoConfig = ApeSettingAlgorithm.clone()
process.AlignmentProducer.algoConfig.setComposites       = cms.bool(False)
process.AlignmentProducer.algoConfig.saveComposites      = cms.untracked.bool(False)
process.AlignmentProducer.algoConfig.readLocalNotGlobal  = cms.bool(False)
process.AlignmentProducer.algoConfig.readFullLocalMatrix = cms.bool(True)
process.AlignmentProducer.algoConfig.saveLocalNotGlobal  = cms.untracked.bool(False)
#
# define how APEs are read: either from DB or from ASCII
process.AlignmentProducer.applyDbAlignment            = cms.untracked.bool(readAPEFromDB)
process.AlignmentProducer.checkDbAlignmentValidity    = cms.untracked.bool(False) # enable reading from tags with several IOVs
process.AlignmentProducer.algoConfig.readApeFromASCII = cms.bool(not readAPEFromDB)
process.AlignmentProducer.algoConfig.apeASCIIReadFile = cms.FileInPath(readASCIIFile)
#
# define how APEs are written
process.AlignmentProducer.saveApeToDB                 = cms.bool(saveAPEtoDB)
process.AlignmentProducer.algoConfig.saveApeToASCII   = cms.untracked.bool(saveAPEtoASCII)
process.AlignmentProducer.algoConfig.apeASCIISaveFile = cms.untracked.string(saveASCIIFile)


### specify the output database file
from CondCore.DBCommon.CondDBSetup_cfi import *
process.PoolDBOutputService = cms.Service(
    "PoolDBOutputService",
    CondDBSetup,
    timetype = cms.untracked.string("runnumber"),
    connect = cms.string("sqlite_file:"+saveAPEFile),
    toPut = cms.VPSet(
        cms.PSet(
            record = cms.string("TrackerAlignmentErrorExtendedRcd"),
            tag = cms.string(saveAPETag)
        )
    )
)
     
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


### speficy the source
# 
# process an empty source
process.source = cms.Source(
    "EmptySource",
    firstRun = cms.untracked.uint32(readDBRun)
)
#
# need to run over 1 event
# NB: will print an "MSG-e" saying no events to process. This can be ignored.
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# We do not even need a path - producer is called anyway...
