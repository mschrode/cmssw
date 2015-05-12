// -*- C++ -*-
//
// Package:    TriggerAnalyzer
// Class:      TriggerAnalyzer
// 
/**\class TriggerAnalyzer TriggerAnalyzer.cc ApeEstimator/Utils/plugins/TriggerAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Johannes Hauk,6 2-039,+41227673512,
//         Created:  Fri Sep 30 12:54:58 CEST 2011
// $Id: TriggerAnalyzer.cc,v 1.1 2011/09/30 14:48:20 hauk Exp $
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

#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
//
// class declaration
//

class TriggerAnalyzer : public edm::EDAnalyzer {
   public:
      explicit TriggerAnalyzer(const edm::ParameterSet&);
      ~TriggerAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
      
      const edm::ParameterSet parameterSet_;
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
TriggerAnalyzer::TriggerAnalyzer(const edm::ParameterSet& iConfig):
parameterSet_(iConfig)
{
}


TriggerAnalyzer::~TriggerAnalyzer()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
TriggerAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // get handle on collections
  const edm::InputTag triggerResults(parameterSet_.getParameter<edm::InputTag>("triggerResults"));
  edm::Handle<edm::TriggerResults> trigResults;
  iEvent.getByLabel(triggerResults, trigResults);
  if(trigResults.failedToGet()){
    edm::LogError("Problematic Product")<<"Failed to get trigger results, check InputTag in cfg file"
                                        <<"\n...skip event in Analyzer";
    return;
  }
  
  const unsigned int nTrig(trigResults->size());
  const edm::TriggerNames trigNames = iEvent.triggerNames(*trigResults);
  for(size_t iTrig=0; iTrig<nTrig; ++iTrig){
    std::cout<<"Trigger name: "<<trigNames.triggerName(iTrig)<<"\n";
  }
}


// ------------ method called once each job just before starting event loop  ------------
void 
TriggerAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TriggerAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
TriggerAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TriggerAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TriggerAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TriggerAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TriggerAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TriggerAnalyzer);
