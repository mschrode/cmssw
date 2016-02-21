// -*- C++ -*-
//
// Package:    Alignment/
// Class:      HLTSelectionAnalyzer
//
// Original Author:  Matthias Schroeder
//         Created:  Sat, 20 Feb 2016 18:57:23 GMT
//
//

#include <iostream>
#include <map>
#include <memory>
#include <vector>

#include "TRegexp.h"
#include "TString.h"
#include "TTree.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"


class HLTSelectionAnalyzer : public edm::EDAnalyzer {
public:
  explicit HLTSelectionAnalyzer(const edm::ParameterSet&);
  ~HLTSelectionAnalyzer() {}
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
  
private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  typedef std::map< TString, std::vector<Int_t> > Triggers;
  typedef std::map< TString, std::vector<Int_t> >::iterator TriggersIt;

  TString treeName_;
  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  std::vector<UInt_t> runNums_;
  std::vector<UInt_t> lumNums_;
  std::vector<UInt_t> evtNums_;
  Triggers triggers_;
};


HLTSelectionAnalyzer::HLTSelectionAnalyzer(const edm::ParameterSet& iConfig) {
  treeName_ = iConfig.getParameter<std::string>("OutTreeName").c_str();
  triggerResultsToken_ = consumes< edm::TriggerResults>(edm::InputTag("TriggerResults","","HLT"));
}


void HLTSelectionAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // store event information
  const edm::EventAuxiliary& aux = iEvent.eventAuxiliary();
  runNums_.push_back( aux.run() );
  lumNums_.push_back( aux.luminosityBlock() );
  evtNums_.push_back( aux.event() );
  const size_t numEvtsProcessed = evtNums_.size();

  // get trigger decisions
  edm::Handle<edm::TriggerResults> hTriggerResults;
  iEvent.getByToken(triggerResultsToken_,hTriggerResults);

  // store trigger decisions
  //std::cout << runNums_.back() << ":" << lumNums_.back() << ":" << evtNums_.back() << std::endl;
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(*hTriggerResults);
  for(size_t iTrig = 0; iTrig < hTriggerResults->size(); ++iTrig) {
    TString triggerName = triggerNames.triggerName(iTrig).c_str();
    // count all "_v*" as same name
    const int pos = triggerName.Index(TRegexp("_v[0-9]"));
    if( pos > 0 ) triggerName.Resize(pos);
    const UInt_t accept = hTriggerResults->accept(iTrig) ? 1 : 0;
    //std::cout << "  " << triggerName << " : " << accept << std::endl;
    TriggersIt trigIt = triggers_.find(triggerName);
    if( trigIt != triggers_.end() ) {
      // this trigger is already known. Store decision
      trigIt->second.push_back(accept);
    } else {
      // this trigger is not yet known.
      // first, add to list of know triggers and fill up
      // with '-1' for 'unknown' for all the previous events
      std::vector<Int_t> tmp( numEvtsProcessed-1, -1 );
      tmp.push_back(accept);
      triggers_[triggerName] = tmp;
    }
  }

  // check if there are any triggers in the list of known triggers
  // that are not in the triggerNames list (do not apply to this event)
  for(TriggersIt it = triggers_.begin(); it != triggers_.end(); ++it) {
    if( it->second.size() == numEvtsProcessed-1 ) {
      it->second.push_back(-1);	// indicate that trigger does not exist in this event
    } else if( it->second.size() < numEvtsProcessed-1 ) {
      throw cms::Exception("BadEventCount") << "Trigger path bookkeeping failed";
    }
  }
}


void HLTSelectionAnalyzer::beginJob() {}


void HLTSelectionAnalyzer::endJob() {
  // sanity check
  const size_t numEvtsProcessed = evtNums_.size();
  for(TriggersIt it = triggers_.begin(); it != triggers_.end(); ++it) {
    if( it->second.size() != numEvtsProcessed ) {
      throw cms::Exception("BadEventCount")
	<< "Trigger path bookkeeping failed:\n"
	<< "There are " << it->second.size() << " decisions stored for '" << it->first << "'\n" 
	<< "but should be " << numEvtsProcessed;
    }
  }

  // write results to tree
  edm::Service<TFileService> fs;
  if( !fs ) {
    throw edm::Exception(edm::errors::Configuration,"TFile Service is not registered in cfg file");
  }
  TTree* tree = fs->make<TTree>(treeName_,treeName_);
  tree->SetAutoSave(10000000000);
  tree->SetAutoFlush(1000000);

  // prepare temporary variables, needed to store
  // trigger decisions in tree
  UInt_t runNum = 0;
  UInt_t lumNum = 0;
  UInt_t evtNum = 0;
  std::vector<Int_t> decisions(triggers_.size(),-2);
  tree->Branch("RunNum",&runNum,"RunNum/i");
  tree->Branch("LumNum",&lumNum,"LumNum/i");
  tree->Branch("EvtNum",&evtNum,"EvtNum/i");
  size_t trigIdx = 0;
  for(TriggersIt it = triggers_.begin(); it != triggers_.end(); ++it, ++trigIdx) {
    tree->Branch(it->first,&(decisions.at(trigIdx)),(it->first)+"/I");
  }  

  // now, loop over events and store trigger decisions in tree
  for(size_t iEvt = 0; iEvt < evtNums_.size(); ++iEvt) {

    // reset temporary variables
    runNum = 0;
    lumNum = 0;
    evtNum = 0;
    for(size_t i = 0; i < decisions.size(); ++i) {
      decisions.at(i) = 0;
    }

    // store values of current event in temporary variables
    // and write to tree
    runNum = runNums_.at(iEvt);
    lumNum = lumNums_.at(iEvt);
    evtNum = evtNums_.at(iEvt);
    size_t trigIdx = 0;
    for(TriggersIt it = triggers_.begin(); it != triggers_.end(); ++it, ++trigIdx) {
      decisions.at(trigIdx) = it->second.at(iEvt);
    }
    tree->Fill();
  }
}


void HLTSelectionAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HLTSelectionAnalyzer);

