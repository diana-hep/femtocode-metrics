#include <iostream>
#include <string>
#include <ctime>
#include <sys/time.h>

#include "TROOT.h"
#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include "TBranch.h"
#include "TClass.h"
#include "TBranchElement.h"
#include "TCollection.h"
#include "TSystem.h"
#include "TH1F.h"

double diff(struct timeval endTime, struct timeval startTime) {
  return (1000L * 1000L * (endTime.tv_sec - startTime.tv_sec) + (endTime.tv_usec - startTime.tv_usec)) / 1000.0 / 1000.0;
}

void drawread() {
  gROOT->SetBatch(kTRUE);

  TFile *tfile = new TFile("/uscms_data/d2/pivarski/CMSSW_8_0_25/src/TreeMaker/Production/test/RunIISpring16MiniAODv2_SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MINIAODSIM_PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1.root");
  TTree *ttree;
  tfile->GetObject("Events", ttree);

  TH1F *h = new TH1F("h", "h", 1, -1000.0, 1000.0);

  std::string branchName;
  struct timeval startTime, endTime;

  int n = 0;

  n++;
  branchName = "patJets_slimmedJetsAK8__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

  n++;
  branchName = "patTaus_slimmedTaus__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

  n++;
  branchName = "patJets_slimmedJets__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

  n++;
  branchName = "patPhotons_slimmedPhotons__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

  n++;
  branchName = "patMuons_slimmedMuons__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

  n++;
  branchName = "patElectrons_slimmedElectrons__PAT.obj.m_state.p4Polar_.fCoordinates.fPt";
  gettimeofday(&startTime, 0);
  ttree->Draw((branchName + " >> h").c_str());
  gettimeofday(&endTime, 0);
  std::cout << branchName << " " << n << " " << diff(endTime, startTime) << " sec" << std::endl;

}
