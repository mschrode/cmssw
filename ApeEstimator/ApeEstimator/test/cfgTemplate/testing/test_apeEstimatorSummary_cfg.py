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



##
## Process definition
##
process = cms.Process("ApeEstimatorSummary")



##
## Message Logger
##
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories.append('CalculateAPE')
process.MessageLogger.cerr.INFO.limit = 0
process.MessageLogger.cerr.default.limit = 0
process.MessageLogger.cerr.CalculateAPE = cms.untracked.PSet(limit = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000 ## really show only every 1000th



##
## Process options
##
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
)



##
## Input Files
##
process.source = cms.Source("EmptySource")



##
## Number of Events
##
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )



##
## ApeEstimatorSummary
##
from ApeEstimator.ApeEstimator.ApeEstimatorSummary_cff import *
process.ApeEstimatorSummarySequence = cms.Sequence()
if options.setBaseline:
  process.ApeEstimatorSummary1 = ApeEstimatorSummaryBaseline.clone(
    # baseline will be set
    BaselineFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_baselineApe.root',
    InputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_desing.root',
    ResultsFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_resultsFile.root',
  )
  process.ApeEstimatorSummary2 = ApeEstimatorSummaryIter.clone(
    BaselineFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_baselineApe.root',
    InputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_desing.root',
    ResultsFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_resultsFile.root',
    # files are not in use in baseline mode
    IterationFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_iterationApe.root',
    ApeOutputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_apeOutput.txt',
  )
  process.ApeEstimatorSummarySequence *= process.ApeEstimatorSummary1
  process.ApeEstimatorSummarySequence *= process.ApeEstimatorSummary2
else:
  process.ApeEstimatorSummary1 = ApeEstimatorSummaryIter.clone(
    # keep the same for all jobs
    BaselineFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/allData_baselineApe.root',
    # keep the first one on misaligned geometry for iterations on same geometry (or better use copy of it)
    IterationFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/allData_iterationApe.root',
    # change iteration number for these
    InputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/allData.root',
    ResultsFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/allData_resultsFile.root',
    ApeOutputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/test/cfgTemplate/testing/iter'+str(options.iterNumber)+'/allData_apeOutput.txt',
  )
  process.ApeEstimatorSummarySequence *= process.ApeEstimatorSummary1



##
## Path
##
process.p = cms.Path(
    process.ApeEstimatorSummarySequence
)






