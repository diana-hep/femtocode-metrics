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

void runfile(const char* fileName) {
  std::cout << fileName << std::endl;

  double total = 0.0;

  TFile *tfile = new TFile(fileName);
  TTree *ttree;
  tfile->GetObject("Events", ttree);

  std::cout << "number of TBaskets ???" << std::endl;

  // get the branch with a full path
  // it's a TBranchElement because recoTracks_generalTracks__RECO.obj is a structure
  // flat ntuples don't have TBranchElements, but we only need TBranchElement::GetBranchCount for structures
  TBranchElement *branch = (TBranchElement*)ttree->GetBranch("recoTracks_generalTracks__RECO.obj.chi2_");

  // essential!!! MakeClass mode lets us view the structure one leaf at a time.
  ttree->SetMakeClass(1);

  // has to be reassigned for each new TFile (we only know the maximum for *this file*)
  int bufferSize = ((TLeaf*)(branch->GetListOfLeaves()->First()))->GetLeafCount()->GetMaximum();

  // allocate a buffer that's just big enough
  Float_t *buffer = new Float_t[bufferSize];

  // have the branch fill this buffer
  ttree->SetBranchAddress("recoTracks_generalTracks__RECO.obj.chi2_", buffer);

  // allocating a place to put the size is also essential
  Int_t size = 0;
  ttree->SetBranchAddress("recoTracks_generalTracks__RECO.obj",&size);

  // clock stuff
  clock_t lastTime = clock();    
  long items = 0L;
  long itemsPerPrint = 100000L;

  // the loop over events
  Long64_t numEvents = ttree->GetEntries();
  for (Long64_t i = 0;  i < numEvents;  i++) {
    // essential! GetEntry from the branch, not the ttree
    branch->GetEntry(i);

    // get the number of elements (tracks in this case)
    int numTracks = branch->GetBranchCount()->GetNdata();

    // and loop over them
    for (int j = 0;  j < numTracks;  ++j) {
      // getting the data does not involve any function calls
      total += buffer[j];

      // clock stuff
      items++;
      if (items % itemsPerPrint == 0) {
        clock_t now = clock();
        std::cout << 1.0 * (now - lastTime) / itemsPerPrint / CLOCKS_PER_SEC * 1e9 << " ns/item" << std::endl;
        lastTime = now;
      }
    }
  }

  // clock and checksum results
  std::cout << "check total " << total << " == 1.55104e+07 (" << (abs(total - 1.55104e+07) < 1e-6*1.55104e+07 ? "true" : "false") << ")" << std::endl;
}

void readOneBranch() {
  runfile("Mu_Run2010B-Apr21ReReco-v1_AOD.root");
  runfile("copy2.root");
  runfile("copy3.root");
  runfile("copy4.root");
  runfile("copy5.root");
  gSystem->Exit(0);
}


// SetMakeClass(1)

// GetLenType() * GetLenStatic() * GetLeafCount()->GetMaximum()

