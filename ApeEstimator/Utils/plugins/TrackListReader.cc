// -*- C++ -*-
//
// Package:    TrackListReader
// Class:      TrackListReader
// 
/**\class TrackListReader TrackListReader.cc ApeEstimator/Utils/plugins/TrackListReader.cc

 Description: Produces TrackCollection of tracks matched to those in stored track list

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Johannes Hauk,6 2-039,+41227673512,
//         Created:  Wed Aug 31 15:26:54 CEST 2011
// $Id: TrackListReader.cc,v 1.2 2011/09/30 14:47:35 hauk Exp $
//
//


// system include files
#include <memory>
#include <fstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/EDMException.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "TFile.h"
#include "TDirectory.h"
#include "TString.h"
#include "TTree.h"

//
// class declaration
//

class TrackListReader : public edm::EDProducer {
   public:
      explicit TrackListReader(const edm::ParameterSet&);
      ~TrackListReader();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      virtual void beginRun(edm::Run&, edm::EventSetup const&);
      virtual void endRun(edm::Run&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
      
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
      
      unsigned int counter1;
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
TrackListReader::TrackListReader(const edm::ParameterSet& iConfig):
parameterSet_(iConfig)
{
  produces<reco::TrackCollection>();
  counter1 = 0;
}


TrackListReader::~TrackListReader()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
TrackListReader::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  std::auto_ptr<reco::TrackCollection> outputTrack(new reco::TrackCollection);
  
  const unsigned int run(iEvent.id().run());
  const unsigned int event(iEvent.id().event());
  
  if(m_runEventTrackParams_.count(run)==0){iEvent.put(outputTrack); return;}
  if(m_runEventTrackParams_[run].count(event)==0){iEvent.put(outputTrack); return;}
  std::vector<TrackParams>& v_trackParams(m_runEventTrackParams_[run][event]);
  
  edm::InputTag trackSource = parameterSet_.getParameter<edm::InputTag>("trackSource");
  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByLabel(trackSource, tracks);
  
  reco::TrackCollection::const_iterator i_track;
  for(i_track = tracks->begin(); i_track != tracks->end(); ++i_track){
    const float eta(i_track->eta());
    const float phi(i_track->phi());
    const float pt(i_track->pt());
    
    bool isMatched(false);
    std::vector<TrackParams>::const_iterator i_trackParams;
    for(i_trackParams = v_trackParams.begin(); i_trackParams != v_trackParams.end(); ++i_trackParams){
      
      const float deltaR(reco::deltaR(eta, phi, i_trackParams->eta_, i_trackParams->phi_));
      const float deltaPt(pt - i_trackParams->pt_);
      
      const float maxTrackDeltaR(0.001);
      const float maxTrackDeltaPt(0.1);
      if(deltaR>maxTrackDeltaR)continue;
      if(deltaPt>maxTrackDeltaPt)continue;
      isMatched = true;
      ++counter1;
      break;
    }
    
    if(isMatched)outputTrack->push_back(*i_track);
  }
  
  
  iEvent.put(outputTrack);
}



// ------------ method called once each job just before starting event loop  ------------
void 
TrackListReader::beginJob(){
  
  // Check if input file exists
  TFile* file(0);
  const std::string trackListFileName(parameterSet_.getParameter<std::string>("trackListFileName"));
  ifstream inputStream;
  inputStream.open(trackListFileName.c_str());
  if(inputStream.is_open()){
  inputStream.close();
    file = new TFile(trackListFileName.c_str(),"READ");
  }
  if(file){
    edm::LogInfo("TrackListReader")<<"Input file with TTree opened";
  }
  else{
    edm::LogError("TrackListReader")<<"There is NO input file !!!\n"
                                    <<"...cannot match tracks to selected ones. Please check path in cfg:\n"
				    <<"\t"<<trackListFileName;
    throw edm::Exception( edm::errors::Configuration,
                            "Wrong file name in cfg file" );
  }
  
  // Check if specified plugin exists
  TDirectory* treeDir(0);
  TString inputPluginName(parameterSet_.getParameter<std::string>("inputPluginName"));
  inputPluginName += "/";
  treeDir = (TDirectory*)file->TDirectory::GetDirectory(inputPluginName);
  if(treeDir){
    edm::LogInfo("TrackListReader")<<"Directory with TTree opened";
  }
  else{
    edm::LogError("TrackListReader")<<"There is NO directory !!!\n"
                                    <<"...cannot match tracks to selected ones. Please check path in cfg:\n"
				    <<"\t"<<inputPluginName;
    throw edm::Exception( edm::errors::Configuration,
                            "Wrong plugin name in cfg file" );
  }
  
  // Get input TTree
  unsigned int run(0), event(0);
  float eta(-999.), phi(-999.), pt(-999.);
  TTree* tree(0);
  treeDir->GetObject("t_trackList", tree);
  if(tree){
    //edm::LogInfo("TrackListReader")<<"TTree opened";
    tree->SetBranchAddress("Run", &run);
    tree->SetBranchAddress("Event", &event);
    tree->SetBranchAddress("Eta", &eta);
    tree->SetBranchAddress("Phi", &phi);
    tree->SetBranchAddress("Pt", &pt);
  }
  else{
    edm::LogError("TrackListReader")<<"There is NO TTree !!!\n"
                                    <<"...cannot match tracks to selected ones.";
    throw edm::Exception( edm::errors::Configuration,
                            "No TTree in file" );
  }
  
  const unsigned int nEvent(tree->GetEntries());
  for(UInt_t iEvent=0; iEvent<nEvent; ++iEvent){
    tree->GetEntry(iEvent);
    TrackParams trackParams(eta, phi, pt);
    m_runEventTrackParams_[run][event].push_back(trackParams);
  }
  
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TrackListReader::endJob() {
  std::cout<<"\n\tNumber of matched tracks: "<<counter1<<"\n";
}

// ------------ method called when starting to processes a run  ------------
void 
TrackListReader::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TrackListReader::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TrackListReader::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TrackListReader::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TrackListReader::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackListReader);
