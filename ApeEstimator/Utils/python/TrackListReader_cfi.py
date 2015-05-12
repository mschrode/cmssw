import FWCore.ParameterSet.Config as cms


TrackListReader = cms.EDProducer("TrackListReader",
    ## Tracks to check for match
    trackSource = cms.InputTag('generalTracks'),
    
    ## Selected tracks for matching
    trackListFileName = cms.string('trackList.root'),
    ## Name of corresponding plugin
    inputPluginName = cms.string('TrackListGenerator'),
)
