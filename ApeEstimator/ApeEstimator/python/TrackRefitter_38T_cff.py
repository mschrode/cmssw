import FWCore.ParameterSet.Config as cms

from Configuration.Geometry.GeometryIdeal_cff import *
from Configuration.StandardSequences.FrontierConditions_GlobalTag_cff import *
from Configuration.StandardSequences.MagneticField_cff import *
from RecoVertex.BeamSpotProducer.BeamSpot_cfi import *

from RecoLocalTracker.SiStripRecHitConverter.StripCPEgeometric_cfi import *
TTRHBuilderGeometricAndTemplate = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
StripCPE = cms.string('StripCPEfromTrackAngle'), # cms.string('StripCPEgeometric'),
#StripCPE = cms.string('StripCPEgeometric'),
ComponentName = cms.string('WithAngleAndTemplate'),
PixelCPE = cms.string('PixelCPEGeneric'),
#PixelCPE = cms.string('PixelCPETemplateReco'),
Matcher = cms.string('StandardMatcher'),
ComputeCoarseLocalPositionFromDisk = cms.bool(False)
)
## TRACK REFITTER (input for Track Selector)
###from RecoTracker.TrackProducer.TrackRefitters_cff import *
# -- Maximal contribution of individual hit to chi2 value of track fit, e.g. = 20. means normalized residual < sqrt(20.)
# not used when < 0.
###FittingSmootherRKP5.EstimateCut = -1.
# -- some cut on pixel hit probability
# not used when < -15.
###FittingSmootherRKP5.LogPixelProbabilityCut = -16.
# -- do not know what exactly this track rejection does
###FittingSmootherRKP5.RejectTracks = False
# -- two track segments if true or only "first" one ???
###FittingSmootherRKP5.BreakTrajWith2ConsecutiveMissing = False
#TrackRefitterForApeEstimator = RecoTracker.TrackProducer.TrackRefitters_cff.TrackRefitterP5.clone(
###TrackRefitterForApeEstimator = RecoTracker.TrackProducer.TrackRefitters_TrackRefitter.clone(

    ###src = 'MuSkim'#ALCARECOTkAlCosmicsCTF0T' #'ALCARECOTkAlCosmicsCosmicTF0T' #'ALCARECOTkAlCosmicsCosmicTF'
          #'ALCARECOTkAlCosmicsCTF' #'ALCARECOTkAlCosmicsRS0T' #'ALCARECOTkAlCosmicsRS'
    ###,TTRHBuilder = 'WithGeometricAndTemplate'     # use StripCPEgeometric instead of standard
    #,TTRHBuilder = 'WithAngleAndTemplate'     # use StripCPEgeometric instead of standard

    #,AlgorithmName = 'ctf'  #'cosmics' #'rs' #'beamhalo'
    #,TrajectoryInEvent = False
    ###,NavigationSchool = ''
###)

###TrackRefitterHighPurityForApeEstimator = TrackRefitterForApeEstimator.clone(
###    src = 'HighPuritySelector'
###)

#from RecoTracker.TrackProducer.TrackRefitters_cff import *
import RecoTracker.TrackProducer.TrackRefitters_cff 
TrackRefitterForApeEstimator = RecoTracker.TrackProducer.TrackRefitter_cfi.TrackRefitter.clone(
	src = "MuSkim",
	TrajectoryInEvent = True,
	TTRHBuilder = "WithAngleAndTemplate",
	NavigationSchool = ''
)

TrackRefitterHighPurityForApeEstimator = TrackRefitterForApeEstimator.clone(
    src = 'HighPuritySelector'
)


## FILTER for high purity tracks
import ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff
HighPuritySelector = ApeEstimator.ApeEstimator.AlignmentTrackSelector_cff.HighPuritySelector



## SEQUENCE
#RefitterSequence = cms.Sequence(offlineBeamSpot
#                                *TrackRefitterForApeEstimator
#)

RefitterHighPuritySequence = cms.Sequence(
    offlineBeamSpot
    #*HighPuritySelector
    *TrackRefitterHighPurityForApeEstimator
)



