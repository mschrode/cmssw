#include <exception>
#include <iostream>
#include <vector>

#include "TCanvas.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "TH1D.h"
#include "TLeaf.h"
#include "TObjArray.h"
#include "TString.h"
#include "TStyle.h"
#include "TTree.h"


class Trigger {
public:
  Trigger() : name_(""), nFired_(0) {}
  Trigger(const TString& triggerName, const size_t iEvtOffset);

  void addEvent(const int decision) { 
    decisions_.push_back(decision);
    if( decision > 0 ) ++nFired_;
  }

  TString name() const { return name_; }
  size_t nEvts() const { return decisions_.size(); }
  bool inMenu(const size_t iEvt) const { return decisions_.at(iEvt) != -1; }
  bool fired(const size_t iEvt) const { return decisions_.at(iEvt) == 1; }
  bool fired() const { return nFired_ > 0; }
  size_t nFired() const { return nFired_; }

private:
  TString name_;
  std::vector<int> decisions_;
  size_t nFired_;
};

Trigger::Trigger(const TString& triggerName, const size_t iEvtOffset)
  : name_(triggerName), nFired_(0) {
  decisions_ = std::vector<int>(iEvtOffset,-1);
}



std::vector<Trigger> readTriggers(const std::vector<TString>& fileNames, const TString& treeName) {
  std::map<TString,Trigger> triggers;
  size_t nEvts = 0;

  for( auto& fileName: fileNames ) {

    // get tree from file
    TFile file(fileName,"READ");
    TTree* tree = 0;
    file.GetObject(treeName,tree);
    if( tree == 0 ) {
      std::cerr << "\n\nERROR no tree '" << treeName << "' in file '" << fileName << "'\n" << std::endl;
      throw std::exception();
    }

    // get trigger names (leaf names)
    std::vector<TString> trigNames;
    const TObjArray* leafs = tree->GetListOfLeaves();
    for(int iLeaf = 0; iLeaf < leafs->GetSize(); ++iLeaf) {
      const TString trigName = (*leafs)[iLeaf]->GetName();
      if( !( trigName=="RunNum" || trigName=="LumNum" || trigName=="EvtNum" ) ) {
	trigNames.push_back(trigName);
      }
    }

    // set branch addresses
    std::vector<Int_t> trigDecisions(trigNames.size(),-1);
    for(size_t i = 0; i < trigNames.size(); ++i) {
      tree->SetBranchAddress(trigNames.at(i),&(trigDecisions.at(i)));
    }

    for(int iEvt = 0; iEvt < tree->GetEntries(); ++iEvt, ++nEvts) {
      tree->GetEntry(iEvt);

      for(size_t iTrig = 0; iTrig < trigNames.size(); ++iTrig) {
	const TString name = trigNames.at(iTrig);
	std::map<TString,Trigger>::iterator trigIt = triggers.find(name);
	const int decision = trigDecisions.at(iTrig);
	if( trigIt != triggers.end() ) {
	  trigIt->second.addEvent(decision);
	} else {
	  Trigger trigger(name,nEvts);
	  trigger.addEvent(decision);
	  triggers[name] = trigger;
	}
      }
      for( auto& it: triggers ) {
	if( it.second.nEvts() == nEvts ) {
	  it.second.addEvent(-1);
	}
      }

      if( iEvt>0 && iEvt%10000==0 ) std::cout << "read " << iEvt << " events" << std::endl;
    }

    file.Close();

  } // end of loop over file names

  std::vector<Trigger> vec;
  for( auto& it: triggers ) {
    vec.push_back( it.second );
  }

  // sanity check
  const size_t refNEvts = vec.front().nEvts();
  for( auto& trigger: vec ) {
    if( trigger.nEvts() != refNEvts ) {
      std::cerr << "\n\nERROR different number of events for '" << trigger.name() << "'\n" << std::endl;
      throw std::exception();
    }
  }
    
  return vec;
}


void plotNFired(const std::vector<Trigger>& triggers) {
  gStyle->SetOptStat(0);
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetPadBottomMargin(0.45);
  gStyle->SetPadLeftMargin(0.1);

  size_t nFiredTriggers = 0;
  TH1* h = new TH1D("hNFired",";;N(events)",triggers.size()+1,0,triggers.size()+1);
  h->GetXaxis()->SetBinLabel(1,"total");
  h->SetBinContent(1,triggers.front().nEvts());
  for(size_t i = 0; i < triggers.size(); ++i) {
    const Trigger& trigger = triggers.at(i);
    size_t nFired = 0;
    if( trigger.fired() ) {
      ++nFiredTriggers;
      for(size_t iEvt = 0; iEvt < trigger.nEvts(); ++iEvt) {
	if( trigger.fired(iEvt) ) ++nFired;
      }
    }
    h->GetXaxis()->SetBinLabel(i+2,trigger.name());
    h->SetBinContent(i+2,nFired);
  }
  h->GetXaxis()->LabelsOption("v");
  h->SetLabelSize(0.03,"X");

  TCanvas* can = new TCanvas("can","N(fired)",1000,750);
  can->cd();
  h->Draw("HIST");
  can->SetGridy();
  can->SaveAs("NFired.pdf");
  delete can;

  // for busy plots: only those triggers, which fired more than 10% of the events
  std::vector<TString> importantTriggersNames(1,h->GetXaxis()->GetBinLabel(1));
  std::vector<double> importantTriggersNFired(1,h->GetBinContent(1));
  for(int bin = 2; bin <= h->GetNbinsX(); ++bin) {
    const double num = h->GetBinContent(bin);
    if( num/importantTriggersNFired.front() > 0.1 ) {
      importantTriggersNames.push_back(h->GetXaxis()->GetBinLabel(bin));
      importantTriggersNFired.push_back(h->GetBinContent(bin));
    }
  }
  delete h;

  h = new TH1D("hNFiredImportant",";;N(events)",importantTriggersNames.size(),0,importantTriggersNames.size());
  for(int bin = 1; bin <= h->GetNbinsX(); ++bin) {
    h->GetXaxis()->SetBinLabel(bin,importantTriggersNames.at(bin-1));
    h->SetBinContent(bin,importantTriggersNFired.at(bin-1));
  }
  can = new TCanvas("can","important N(fired)",1000,750);
  can->cd();
  h->Draw("HIST");
  can->SetGridy();
  can->SaveAs("NFiredImportant.pdf");
  delete h;
  delete can;


  // plot overlap (only for triggers which fired at least once)
  for( auto& trigger: triggers ) {
    if( trigger.fired() ) {
      TH1* h = new TH1D("hOverlap",";;Overlap with "+trigger.name()+" [%]",nFiredTriggers,0,nFiredTriggers);
      int bin = 1;
      h->GetXaxis()->SetBinLabel(bin,trigger.name());
      h->SetBinContent(bin,trigger.nFired());
      for( auto& other: triggers ) {
	if( other.fired() && other.name()!=trigger.name() ) {
	  ++bin;
	  size_t nOverlaps = 0;
	  for(size_t iEvt = 0; iEvt < trigger.nEvts(); ++iEvt) {
	    if( trigger.fired(iEvt) && other.fired(iEvt) ) ++nOverlaps;
	  }
	  h->GetXaxis()->SetBinLabel(bin,other.name());
	  h->SetBinContent(bin,nOverlaps);
	}
      }
      h->GetXaxis()->LabelsOption("v");
      h->SetLabelSize(0.03,"X");

      const double tot = h->GetBinContent(1);
      h->Scale(100./tot);
    
      TCanvas* can = new TCanvas("can","N(overlaps)",1000,750);
      can->cd();
      h->Draw("HIST");
      can->SetGridy();
      can->SaveAs("Overlaps_"+trigger.name()+".pdf");

      delete h;
      delete can;
    }
  }
}


void hltSelectionAnalysis() {
  gErrorIgnoreLevel = 1001;  // Suppress message when canvas has been saved

  std::vector<TString> fileNames { 
    "HLTSelection_HLTPhysics-TkAlMinBias_Run2015D-PromptReco-v4.root"
  };
  std::vector<Trigger> triggers = readTriggers(fileNames,"analysis/TriggerResults");
  plotNFired(triggers);
}
