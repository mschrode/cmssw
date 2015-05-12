import os

import FWCore.ParameterSet.Config as cms

from ApeEstimator.ApeEstimator.ApeEstimatorSummary_cfi import *



ApeEstimatorSummaryBaseline = ApeEstimatorSummary.clone(
    setBaseline = True,
    apeWeight = "entriesOverSigmaX2",
    #sigmaFactorFit = 2.5,
    #InputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/inputFile.root',
    #ResultsFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/resultsFile.root',
    #BaselineFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/baselineApe.root',
)



ApeEstimatorSummaryIter = ApeEstimatorSummary.clone(
    #setBaseline = False,
    apeWeight = "entriesOverSigmaX2",
    #sigmaFactorFit = 2.5,
    correctionScaling = 0.6,
    #smoothIteration = True,
    smoothFraction = 0.5,
    #InputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/inputFile.root',
    #ResultsFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/resultsFile.root',
    #BaselineFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/baselineApe.root',
    #IterationFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/iterationApe.root',
    #ApeOutputFile = os.environ['CMSSW_BASE'] + '/src/ApeEstimator/ApeEstimator/hists/apeOutput.txt',
)




