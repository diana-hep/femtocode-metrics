// system include files
#include <string>
#include <iostream>
#include <sys/time.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

//
// class declaration
//

class CraptasticAnalyzer: public edm::EDAnalyzer {
public:
  explicit CraptasticAnalyzer(const edm::ParameterSet&);
  ~CraptasticAnalyzer();
  
private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
	
  virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  virtual void endRun(edm::Run const&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  // edm::InputTag tag00; edm::EDGetTokenT<GenEventInfoProduct> token00;
  // edm::InputTag tag01; edm::EDGetTokenT<reco::BeamSpot> token01;
  // edm::InputTag tag02; edm::EDGetTokenT<PileupSummaryInfo> token02;
  // edm::InputTag tag03; edm::EDGetTokenT<pat::ElectronCollection> token03;
  // edm::InputTag tag04; edm::EDGetTokenT<pat::JetCollection> token04;
  // edm::InputTag tag05; edm::EDGetTokenT<pat::JetCollection> token05;
  // edm::InputTag tag06; edm::EDGetTokenT<pat::METCollection> token06;
  edm::InputTag tag07; edm::EDGetTokenT<pat::MuonCollection> token07;
  // edm::InputTag tag08; edm::EDGetTokenT<pat::PackedCandidateCollection> token08;
  // edm::InputTag tag09; edm::EDGetTokenT<pat::PackedGenParticleCollection> token09;
  // edm::InputTag tag10; edm::EDGetTokenT<pat::PhotonCollection> token10;
  // edm::InputTag tag11; edm::EDGetTokenT<pat::TauCollection> token11;
  // edm::InputTag tag12; edm::EDGetTokenT<reco::GenJetCollection> token12;
  // edm::InputTag tag13; edm::EDGetTokenT<reco::GenParticleCollection> token13;
  // edm::InputTag tag14; edm::EDGetTokenT<reco::VertexCollection> token14;

  double gettime();

  int numEvents = 0;
  double startTime = 0.0;
  double endTime = 0.0;
  
  int numValid = 0;
};

double CraptasticAnalyzer::gettime() {
  struct timeval x;
  gettimeofday(&x, NULL);
  return (double)x.tv_sec*1000000 + (double)x.tv_usec;
}

CraptasticAnalyzer::CraptasticAnalyzer(const edm::ParameterSet& iConfig)
  // : tag00(edm::InputTag("generator")), token00(consumes<GenEventInfoProduct>(tag00))                          //    48131  17.9786  22.1468   18.0022
  // : tag01(edm::InputTag("offlineBeamSpot")), token01(consumes<reco::BeamSpot>(tag01))                         //    48131   5.14639  5.24505
  // : tag02(edm::InputTag("slimmedAddPileupInfo")), token02(consumes<PileupSummaryInfo>(tag02))                 //        0   3.36029  3.65678   3.22441
  // : tag03(edm::InputTag("slimmedElectrons")), token03(consumes<pat::ElectronCollection>(tag03))               //   120463  46.9321  47.8609
  // : tag04(edm::InputTag("slimmedJets")), token04(consumes<pat::JetCollection>(tag04))                         //   806177  41.6812  42.1276
  // : tag05(edm::InputTag("slimmedJetsAK8")), token05(consumes<pat::JetCollection>(tag05))                      //    87530  21.3368  23.6459   23.7429
  // : tag06(edm::InputTag("slimmedMETs")), token06(consumes<pat::METCollection>(tag06))                         //    48131  14.9535  14.5592
  : tag07(edm::InputTag("slimmedMuons")), token07(consumes<pat::MuonCollection>(tag07))                       //   132274  47.1641  47.5094
  // : tag08(edm::InputTag("lostTracks")), token08(consumes<pat::PackedCandidateCollection>(tag08))              //    33562   9.49151  9.80951
  // : tag09(edm::InputTag("packedGenParticles")), token09(consumes<pat::PackedGenParticleCollection>(tag09))    // 26422831  37.4702  40.8709   36.8598
  // : tag10(edm::InputTag("slimmedPhotons")), token10(consumes<pat::PhotonCollection>(tag10))                   //   139746  42.882   39.4736   44.5847
  // : tag11(edm::InputTag("slimmedTaus")), token11(consumes<pat::TauCollection>(tag11))                         //   305544  28.1048  32.48     32.8797
  // : tag12(edm::InputTag("slimmedGenJets")), token12(consumes<reco::GenJetCollection>(tag12))                  //   678167  13.149   12.0526   12.995
  // : tag13(edm::InputTag("prunedGenParticles")), token13(consumes<reco::GenParticleCollection>(tag13))         //  8079211  28.7914  28.2984
  // : tag14(edm::InputTag("offlineSlimmedPrimaryVertices")), token14(consumes<reco::VertexCollection>(tag14))   //   826543   8.45638  8.24014
  { }

CraptasticAnalyzer::~CraptasticAnalyzer() { }

// ------------ method called for each event  ------------
void
CraptasticAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (numEvents == 0)
    startTime = gettime();

  // edm::Handle<GenEventInfoProduct> data00; iEvent.getByToken(token00, data00); if (data00.isValid()) numValid += 1;
  // edm::Handle<reco::BeamSpot> data01; iEvent.getByToken(token01, data01); if (data01.isValid()) numValid += 1;
  // edm::Handle<PileupSummaryInfo> data02; iEvent.getByToken(token02, data02); if (data02.isValid()) numValid += 1;
  // edm::Handle<pat::ElectronCollection> data03; iEvent.getByToken(token03, data03); numValid += data03->size();
  // edm::Handle<pat::JetCollection> data04; iEvent.getByToken(token04, data04); numValid += data04->size();
  // edm::Handle<pat::JetCollection> data05; iEvent.getByToken(token05, data05); numValid += data05->size();
  // edm::Handle<pat::METCollection> data06; iEvent.getByToken(token06, data06); numValid += data06->size();
  edm::Handle<pat::MuonCollection> data07; iEvent.getByLabel("slimmedMuons", data07); numValid += data07->size();
  // edm::Handle<pat::PackedCandidateCollection> data08; iEvent.getByToken(token08, data08); numValid += data08->size();
  // edm::Handle<pat::PackedGenParticleCollection> data09; iEvent.getByToken(token09, data09); numValid += data09->size();
  // edm::Handle<pat::PhotonCollection> data10; iEvent.getByToken(token10, data10); numValid += data10->size();
  // edm::Handle<pat::TauCollection> data11; iEvent.getByToken(token11, data11); numValid += data11->size();
  // edm::Handle<reco::GenJetCollection> data12; iEvent.getByToken(token12, data12); numValid += data12->size();
  // edm::Handle<reco::GenParticleCollection> data13; iEvent.getByToken(token13, data13); numValid += data13->size();
  // edm::Handle<reco::VertexCollection> data14; iEvent.getByToken(token14, data14); numValid += data14->size();

  numEvents++;
  endTime = gettime();
}

// ------------ method called once each job just before starting event loop  ------------
void 
CraptasticAnalyzer::beginJob() { }

// ------------ method called once each job just after ending the event loop  ------------
void 
CraptasticAnalyzer::endJob() {
  std::cout << "Crudly Dudley. " << numEvents << " events with " << numValid << " valid objects in " << (endTime - startTime)/1e6 << " sec" << std::endl;
}

// ------------ method called when starting to processes a run  ------------
void 
CraptasticAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&) { }

// ------------ method called when ending the processing of a run  ------------
void 
CraptasticAnalyzer::endRun(edm::Run const&, edm::EventSetup const&) { }

// ------------ method called when starting to processes a luminosity block  ------------
void 
CraptasticAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) { }

// ------------ method called when ending the processing of a luminosity block  ------------
void 
CraptasticAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) { }

//define this as a plug-in
DEFINE_FWK_MODULE(CraptasticAnalyzer);
