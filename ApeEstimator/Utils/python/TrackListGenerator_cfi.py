import FWCore.ParameterSet.Config as cms


TrackListGenerator = cms.EDAnalyzer("TrackListGenerator",
    trackSource = cms.InputTag('generalTracks'),
)
