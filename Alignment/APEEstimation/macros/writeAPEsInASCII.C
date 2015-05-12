// output format:
// moduleId x11 x21 x22 x31 x32 x33 followed by 15 columns with 0

#include <exception>
#include <fstream>
#include <iostream>
#include <vector>

#include "TFile.h"
#include "TString.h"
#include "TTree.h"


// APEs in mum
const double apeBPX = 5.;
const double apeFPX = 30.;
const double apeTIB = 15.;
const double apeTOB = 15.;
const double apeTID = 50.;
const double apeTEC = 50.;

const TString trackerTreeFileName = "../../TrackerAlignment/test/TrackerTree.root";


void writeAPEsInASCII(const TString& outName="ape.txt") {
    
  // open file with tracker-geometry info
  TFile file(trackerTreeFileName,"READ");
  if( !file.IsOpen() ) {
    std::cerr << "\n\nERROR opening file '" << trackerTreeFileName << "'\n" << std::endl;
    throw std::exception();
  }

  // get tree with geometry info
  TTree* tree = 0;
  const TString treeName = "TrackerTreeGenerator/TrackerTree/TrackerTree";
  file.GetObject(treeName,tree);
  if( tree == 0 ) {
    std::cerr << "\n\nERROR reading tree '" << treeName << "' from file '" << trackerTreeFileName << "'\n" << std::endl;
    throw std::exception();
  }
  
  // tree variables
  unsigned int theRawId = 0;
  unsigned int theSubdetId = 0;
  tree->SetBranchAddress("RawId",&theRawId);
  tree->SetBranchAddress("SubdetId",&theSubdetId);

  // open the output file
  std::ofstream apeSaveFile(outName.Data());

  // tmp vector storing APEs
  std::vector<double> apes(21,0.);

  for(int iE = 0; iE < tree->GetEntries(); ++iE) {
    tree->GetEntry(iE);
    
    // Set the APE according to the subdetector.
    // The subdetector encoding in tree
    // BPIX: 1
    // FPIX: 2
    // TIB:  3
    // TID:  4
    // TOB:  5
    // TEC:  6
    double ape = 0.;
    if(      theSubdetId == 1 ) ape = apeBPX;
    else if( theSubdetId == 2 ) ape = apeFPX;
    else if( theSubdetId == 3 ) ape = apeTIB;
    else if( theSubdetId == 4 ) ape = apeTID;
    else if( theSubdetId == 5 ) ape = apeTOB;
    else if( theSubdetId == 6 ) ape = apeTEC;

    // put APE for current module into tmp vector
    // for the first three diagonal elements
    apes[0] = ape;
    apes[2] = ape;
    apes[5] = ape;
    
    // write APE to ASCII file
    apeSaveFile << theRawId;
    for(std::vector<double>::const_iterator it = apes.begin();
	it != apes.end(); ++it) {
      apeSaveFile << "  " << *it;
    }
    apeSaveFile << std::endl;

  } // end of loop over tree (=modules)

  apeSaveFile.close();
  delete tree;
  file.Close();
  
  std::cout << "Wrote APEs to '" << outName << "'" << std::endl;
}



