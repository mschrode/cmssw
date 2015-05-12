{



gROOT->ProcessLine(".L tdrstyle.C");
setTDRStyle();
gStyle->SetErrorX(0.5);

gStyle->SetPadLeftMargin(0.15);
gStyle->SetPadRightMargin(0.10);
//gStyle->SetPadTopMargin(0.10);
//gStyle->SetPadBottomMargin(0.10);
gStyle->SetTitleOffset(1.0,"Y");






//----------------------------------------------------------------------------------------------------------------------------





gROOT->ProcessLine(".L DrawIteration.C+");




DrawIteration drawIteration1(14, true);

//drawIteration1.outputDirectory("$CMSSW_BASE/src/ApeEstimator/ApeEstimator/hists/comparison/");  // default

//drawIteration1.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/MC_start/workingArea/iter14/allData_iterationApe.root","MC start");
drawIteration1.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/GlobalTag_final/workingArea/iter14/allData_iterationApe.root","Prompt");
drawIteration1.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/GR10_v6_final/workingArea/iter14/allData_iterationApe.root","Reprocessing");
//drawIteration1.addInputFile("","");

//drawIteration1.addCmsText("CMS Preliminary");
drawIteration1.drawResult();



/*

DrawIteration drawIteration2(14, true);

drawIteration2.outputDirectory("$CMSSW_BASE/src/ApeEstimator/ApeEstimator/hists/comparison/systematics/");

//drawIteration2.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/GR10_v6_newPixelTemplate/workingArea/iter14/allData_iterationApe.root","plus0");
drawIteration2.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/GR10_v6_newPixelTemplate_plus5/workingArea/iter14/allData_iterationApe.root","  5 #mum");
drawIteration2.addInputFile("/afs/cern.ch/user/h/hauk/private/rootFilesApe/GR10_v6_newPixelTemplate_plus10/workingArea/iter14/allData_iterationApe.root","10 #mum");
drawIteration2.addInputFile("/afs/cern.ch/user/h/hauk/scratch0/apeStudies/rootFiles/GR10_v6_newPixelTemplate_plus15/workingArea/iter14/allData_iterationApe.root","15 #mum");
drawIteration2.addInputFile("/afs/cern.ch/user/h/hauk/private/rootFilesApe/GR10_v6_newPixelTemplate_plus20/workingArea/iter14/allData_iterationApe.root","20 #mum");
//drawIteration2.addInputFile("","");

drawIteration2.drawResult();

*/



gROOT->ProcessLine(".q");


}
