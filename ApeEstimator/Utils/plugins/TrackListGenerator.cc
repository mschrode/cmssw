// -*- C++ -*-
//
// Package:    TrackListGenerator
// Class:      TrackListGenerator
// 
/**\class TrackListGenerator TrackListGenerator.cc ApeEstimator/Utils/plugins/TrackListGenerator.cc

 Description: Creates TTree containing necessary Event and Track information to match tracks in another module

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Johannes Hauk,6 2-039,+41227673512,
//         Created:  Wed Aug 31 12:07:44 CEST 2011
// $Id: TrackListGenerator.cc,v 1.1 2011/08/31 16:31:37 hauk Exp $
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"

#include "TTree.h"

//
// class declaration
//

class TrackListGenerator : public edm::EDAnalyzer {
   public:
      explicit TrackListGenerator(const edm::ParameterSet&);
      ~TrackListGenerator();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      
      struct TrackParams{
        TrackParams(const double eta, const double phi, const double pt):
	  eta_(eta), phi_(phi), pt_(pt){}
	float eta_;
	float phi_;
	float pt_;
      };
      
      // ----------member data ---------------------------
      
      const edm::ParameterSet parameterSet_;
      
      typedef std::map<unsigned int, std::vector<TrackParams> > EventTrackParams;
      typedef std::map<unsigned int, std::map<unsigned int, std::vector<TrackParams> > > RunEventTrackParams;
      RunEventTrackParams m_runEventTrackParams_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
TrackListGenerator::TrackListGenerator(const edm::ParameterSet& iConfig):
parameterSet_(iConfig)
{
}


TrackListGenerator::~TrackListGenerator()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
TrackListGenerator::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  const unsigned int run(iEvent.id().run());
  const unsigned int event(iEvent.id().event());
  
  edm::InputTag trackSource = parameterSet_.getParameter<edm::InputTag>("trackSource");
  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByLabel(trackSource, tracks);
  
  reco::TrackCollection::const_iterator i_track;
  for(i_track = tracks->begin(); i_track != tracks->end(); ++i_track){
    const double eta(i_track->eta());
    const double phi(i_track->phi());
    const double pt(i_track->pt());
    
    TrackParams trackParams(eta, phi, pt);
    m_runEventTrackParams_[run][event].push_back(trackParams);
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
TrackListGenerator::beginJob(){
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TrackListGenerator::endJob(){
  edm::Service<TFileService> fileService;
  //TFileDirectory dir = fileService->mkdir("TrackList");
  
  TTree* tree(0);
  tree = fileService->make<TTree>("t_trackList","Tree containing information about tracks");
  
  unsigned int run(0), event(0);
  float eta(-999.), phi(-999.), pt(-999.);
  tree->Branch("Run", &run, "Run/i");
  tree->Branch("Event", &event, "Event/i");
  tree->Branch("Eta", &eta, "Eta/F");
  tree->Branch("Phi", &phi, "Phi/F");
  tree->Branch("Pt", &pt, "Pt/F");
  
  RunEventTrackParams::iterator i_run;
  for(i_run = m_runEventTrackParams_.begin(); i_run != m_runEventTrackParams_.end(); ++i_run){
    run = i_run->first;
    EventTrackParams& m_eventTrackParams(i_run->second);
    EventTrackParams::iterator i_event;
    for(i_event = m_eventTrackParams.begin(); i_event != m_eventTrackParams.end(); ++i_event){
      event = i_event->first;
      std::vector<TrackParams>& v_trackParams(i_event->second);
      std::vector<TrackParams>::const_iterator i_trackParams;
      for(i_trackParams = v_trackParams.begin(); i_trackParams != v_trackParams.end(); ++i_trackParams){
        eta = i_trackParams->eta_;
        phi = i_trackParams->phi_;
        pt = i_trackParams->pt_;
	
	tree->Fill();
      }
    }
  }
}

// ------------ method called when starting to processes a run  ------------
void 
TrackListGenerator::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TrackListGenerator::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TrackListGenerator::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TrackListGenerator::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TrackListGenerator::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackListGenerator);
