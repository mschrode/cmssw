////////////////////////////////////////////////////////////////////////////////////////
///
///  Write APEs in ASCII-file format
///
///  The ASCII file contains one row per module, where the first column
///  lists the module id and the following 21 columns the diagonal and
///  lower elements x11,x21,x22,x31,x32,x33,0... of the 6x6 covariance
///  matrix, where the upper 3x3 sub-matrix contains the position APEs.
///  The elements are stored in units of cm^2.
///
///  This format is understood as input by
///  Alignment/CommonAlignmentAlgorithm/python/ApeSettingAlgorithm_cfi.py
///
////////////////////////////////////////////////////////////////////////////////////////

#include <exception>
#include <fstream>
#include <iostream>
#include <vector>

#include "TFile.h"
#include "TString.h"
#include "TTree.h"


// APEs in mum, local [x,y,z]
std::vector<double> apesBPX(3,0.);
std::vector<double> apesFPX(3,0.);
std::vector<double> apesTIB(3,0.);
std::vector<double> apesTOB(3,0.);
std::vector<double> apesTID(3,0.);
std::vector<double> apesTEC(3,0.);

const TString trackerTreeFileName = "../../TrackerAlignment/test/TrackerTree.root";


// Transform APE into covariance elements in cm^{2} units
std::vector<double> transformIntoCovarianceMatrixElements(const std::vector<double>& apes) {
  std::vector<double> cov(21,0.);
  cov[0] = apes[0]*apes[0]*1E-8;
  cov[2] = apes[1]*apes[1]*1E-8;
  cov[5] = apes[2]*apes[2]*1E-8;

  return cov;
}


void scaleAPEs(std::vector<double>& apes, const double scale) {
  for(std::vector<double>::iterator it = apes.begin();
      it != apes.end(); ++it) {
    *it = (*it)*scale;
  }
}


void writeAPEsInASCII(const TString& outName="ape.txt") {
  // set APEs (in mum) for different subdetectors
  apesBPX[0] = 20;
  apesBPX[1] = 10;
  apesBPX[2] = 20;
  
  apesFPX[0] = 10;
  apesFPX[1] = 20;
  apesFPX[2] = 20;
  
  apesTIB[0] = 10;
  apesTIB[1] = 10;
  apesTIB[2] = 10;
  
  apesTOB[0] = 10;
  apesTOB[1] = 10;
  apesTOB[2] = 10;
  
  apesTID[0] = 10;
  apesTID[1] = 10;
  apesTID[2] = 10;
  
  apesTEC[0] = 20;
  apesTEC[1] = 20;
  apesTEC[2] = 20;

  // scale APEs by
  const double scale = 2.;
  std::cout << "Scaling APEs by " << scale << std::endl;
  scaleAPEs(apesBPX,scale);
  scaleAPEs(apesFPX,scale);
  scaleAPEs(apesTIB,scale);
  scaleAPEs(apesTOB,scale);
  scaleAPEs(apesTID,scale);
  scaleAPEs(apesTEC,scale);

  // transform into covariance elements
  const std::vector<double> covBPX = transformIntoCovarianceMatrixElements(apesBPX);
  const std::vector<double> covFPX = transformIntoCovarianceMatrixElements(apesFPX);
  const std::vector<double> covTIB = transformIntoCovarianceMatrixElements(apesTIB);
  const std::vector<double> covTOB = transformIntoCovarianceMatrixElements(apesTOB);
  const std::vector<double> covTID = transformIntoCovarianceMatrixElements(apesTID);
  const std::vector<double> covTEC = transformIntoCovarianceMatrixElements(apesTEC);
    
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
    const std::vector<double>* cov = 0;
    if(      theSubdetId == 1 ) cov = &covBPX;
    else if( theSubdetId == 2 ) cov = &covFPX;
    else if( theSubdetId == 3 ) cov = &covTIB;
    else if( theSubdetId == 4 ) cov = &covTID;
    else if( theSubdetId == 5 ) cov = &covTOB;
    else if( theSubdetId == 6 ) cov = &covTEC;
    
    // write APE to ASCII file
    apeSaveFile << theRawId;
    for(std::vector<double>::const_iterator it = cov->begin();
	it != cov->end(); ++it) {
      apeSaveFile << "  " << *it;
    }
    apeSaveFile << std::endl;

  } // end of loop over tree (=modules)

  apeSaveFile.close();
  delete tree;
  file.Close();
  
  std::cout << "Wrote APEs to '" << outName << "'" << std::endl;
}



