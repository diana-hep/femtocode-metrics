#include <iostream>
#include <time.h>

#include "TFile.h"
#include "TTree.h"
#include "TLeaf.h"
#include "TBranch.h"
#include "TClass.h"
#include "TBranchElement.h"
#include "TCollection.h"
#include "TSystem.h"

void quickread() {
  std::cout << "start" << std::endl;

  double total = 0.0;

  TFile *tfile = new TFile("/uscms_data/d2/pivarski/CMSSW_8_0_25/src/TreeMaker/Production/test/RunIISpring16MiniAODv2_SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MINIAODSIM_PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1.root");
  TTree *ttree;
  tfile->GetObject("Events", ttree);

  TBranchElement *branch = (TBranchElement*)ttree->GetBranch("recoVertexs_offlineSlimmedPrimaryVertices__PAT.obj.position_.fCoordinates.fZ");

  ttree->SetMakeClass(1);

  int bufferSize = ((TLeaf*)(branch->GetListOfLeaves()->First()))->GetLeafCount()->GetMaximum();

  Double_t *buffer = new Double_t[bufferSize];

  ttree->SetBranchAddress("recoVertexs_offlineSlimmedPrimaryVertices__PAT.obj.position_.fCoordinates.fZ", buffer);

  Int_t size = 0;
  ttree->SetBranchAddress("recoBeamSpot_offlineBeamSpot__HLT.obj", &size);

  clock_t startTime = clock();
  clock_t lastTime = clock();
  long items = 0L;
  long itemsPerPrint = 100000L;

  Long64_t numEvents = ttree->GetEntries();

  for (int times = 0;  times < 5;  times++) {
    for (Long64_t i = 0;  i < numEvents;  i++) {
      branch->GetEntry(i);

      int numMuons = branch->GetBranchCount()->GetNdata();

      for (int j = 0;  j < numMuons;  ++j) {
        total += buffer[j];

        items++;
        // if (items % itemsPerPrint == 0) {
        //   clock_t now = clock();
        //   std::cout << 1.0 * (now - lastTime) / itemsPerPrint / CLOCKS_PER_SEC * 1e9 << " ns/item" << std::endl;
        //   lastTime = now;
        // }
      }
    }
  }

  clock_t now = clock();

  std::cout << "numEvents: " << numEvents << std::endl;
  std::cout << "numMuons: " << items << std::endl;
  std::cout << "total: " << total << std::endl;

  std::cout << "time: " << 1.0 * (now - startTime) / CLOCKS_PER_SEC / 5.0 << " sec" << std::endl;
}
