import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger = cms.Service("MessageLogger",
       destinations   = cms.untracked.vstring("cerr"),
       cerr           = cms.untracked.PSet(threshold = cms.untracked.string("WARNING"))
)

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring("file:/uscms_data/d2/pivarski/CMSSW_8_0_25/src/TreeMaker/Production/test/RunIISpring16MiniAODv2_SMS-T1tttt_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_MINIAODSIM_PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1.root"))
# process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring("file:/uscms_data/d2/pivarski/CMSSW_8_0_25/src/test_cmssw.root"))

process.CraptasticAnalyzer = cms.EDAnalyzer("CraptasticAnalyzer")

process.p = cms.Path(process.CraptasticAnalyzer)
