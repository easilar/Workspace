import FWCore.ParameterSet.Config as cms

TauTupelizer = cms.EDProducer ( "TauTupelizer",
    verbose      = cms.untracked.bool(False),
    input        = cms.untracked.InputTag("slimmedTaus"),
    ptThreshold = cms.untracked.double(18.),


    tauIDs = cms.untracked.VPSet(
        cms.untracked.PSet(accessTag = cms.untracked.string("againstElectronLoose"),
                           storeTag = cms.untracked.string("AgainstElectronLoose")),
        cms.untracked.PSet(accessTag = cms.untracked.string("againstElectronLooseMVA5"),
                           storeTag = cms.untracked.string("AgainstElectronLooseMVA5")),
        cms.untracked.PSet(accessTag = cms.untracked.string("againstMuonLoose3"),
                           storeTag = cms.untracked.string("AgainstMuonLoose3")),
        cms.untracked.PSet(accessTag = cms.untracked.string("againstMuonLooseMVA"),
                           storeTag = cms.untracked.string("AgainstMuonLooseMVA")),
        cms.untracked.PSet(accessTag = cms.untracked.string("byLooseCombinedIsolationDeltaBetaCorr3Hits"),
                           storeTag = cms.untracked.string("ByLooseCombinedIsolationDeltaBetaCorr3Hits")),
        cms.untracked.PSet(accessTag = cms.untracked.string("decayModeFinding"),
                           storeTag = cms.untracked.string("DecayModeFinding")),
        cms.untracked.PSet(accessTag = cms.untracked.string("puCorrPtSum"),
                           storeTag = cms.untracked.string("PuCorrPtSum"))
    ),


    useForDefaultAlias = cms.untracked.bool(False)

) 


#'againstElectronLoose'
#'againstElectronLooseMVA5'
#'againstElectronMVA5category'
#'againstElectronMVA5raw'
#'againstElectronMedium'
#'againstElectronMediumMVA5'
#'againstElectronTight'
#'againstElectronTightMVA5'
#'againstElectronVLooseMVA5'
#'againstElectronVTightMVA5'
#'againstMuonLoose'
#'againstMuonLoose2'
#'againstMuonLoose3'
#'againstMuonLooseMVA'
#'againstMuonMVAraw'
#'againstMuonMedium'
#'againstMuonMedium2'
#'againstMuonMediumMVA'
#'againstMuonTight'
#'againstMuonTight2'
#'againstMuonTight3'
#'againstMuonTightMVA'
#'byCombinedIsolationDeltaBetaCorrRaw3Hits'
#'byIsolationMVA3newDMwLTraw'
#'byIsolationMVA3newDMwoLTraw'
#'byIsolationMVA3oldDMwLTraw'
#'byIsolationMVA3oldDMwoLTraw'
#'byLooseCombinedIsolationDeltaBetaCorr3Hits'
#'byLooseIsolationMVA3newDMwLT'
#'byLooseIsolationMVA3newDMwoLT'
#'byLooseIsolationMVA3oldDMwLT'
#'byLooseIsolationMVA3oldDMwoLT'
#'byMediumCombinedIsolationDeltaBetaCorr3Hits'
#'byMediumIsolationMVA3newDMwLT'
#'byMediumIsolationMVA3newDMwoLT'
#'byMediumIsolationMVA3oldDMwLT'
#'byMediumIsolationMVA3oldDMwoLT'
#'byTightCombinedIsolationDeltaBetaCorr3Hits'
#'byTightIsolationMVA3newDMwLT'
#'byTightIsolationMVA3newDMwoLT'
#'byTightIsolationMVA3oldDMwLT'
#'byTightIsolationMVA3oldDMwoLT'
#'byVLooseIsolationMVA3newDMwLT'
#'byVLooseIsolationMVA3newDMwoLT'
#'byVLooseIsolationMVA3oldDMwLT'
#'byVLooseIsolationMVA3oldDMwoLT'
#'byVTightIsolationMVA3newDMwLT'
#'byVTightIsolationMVA3newDMwoLT'
#'byVTightIsolationMVA3oldDMwLT'
#'byVTightIsolationMVA3oldDMwoLT'
#'byVVTightIsolationMVA3newDMwLT'
#'byVVTightIsolationMVA3newDMwoLT'
#'byVVTightIsolationMVA3oldDMwLT'
#'byVVTightIsolationMVA3oldDMwoLT'
#'chargedIsoPtSum'
#'decayModeFinding'
#'decayModeFindingNewDMs'
#'neutralIsoPtSum'
#'puCorrPtSum'
