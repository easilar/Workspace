import copy, os, sys
###dir = '/data/easilar/cmgTuples/postProcessed_Spring15_MC_from_Artur_CBID/hard/' 
dir = '/data/easilar/cmgTuples/postProcessed_Spring15_MC_from_Artur/hard/' 
data_dir = '/data/easilar/cmgTuples/postProcessed_Spring15_Data_from_Artur_CBID/hard/'

data_mu_25ns={\
"name": "SingleMuon_Run2015D",
"bins": [
"SingleMuon_Run2015D_v4",
"SingleMuon_Run2015D_05Oct"
],
"dir": data_dir,
}

data_ele_25ns={\
"name": "SingleElectron_Run2015D",
"bins": [
"SingleElectron_Run2015D_v4",
"SingleElectron_Run2015D_05Oct"
],
"dir": data_dir,
}

TTJets_HTLO_25ns={\
"name" : "tt+Jets_LO",
"bins" : [
#"TTJets_HT-0to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2",
"TTJets_LO_25ns",
"TTJets_HT600to800",
"TTJets_HT800to1200",
"TTJets_HT1200to2500",
"TTJets_HT2500toInf",
],
#'dir' : '/data/easilar/cmgTuples/postProcessed_Spring15_MC_from_Artur_CBID/HT400/hard/',
'dir' : dir,
}

WJetsHTToLNu_25ns={\
"name" : "W+Jets",
"bins" : [
"WJetsToLNu_HT100to200",
"WJetsToLNu_HT200to400",
"WJetsToLNu_HT400to600",
#"WJetsToLNu_HT600toInf",
"WJetsToLNu_HT600to800",
"WJetsToLNu_HT800to1200",
"WJetsToLNu_HT1200to2500",
"WJetsToLNu_HT2500toInf",
],
'dir' : dir,
}


singleTop_25ns={\
"name" : "singleTop",
"bins" : [
"TBar_tWch",
"TToLeptons_sch",
"TToLeptons_tch",
"T_tWch",
],
'dir' : dir,
}

DY_25ns={\
"name" : "DY",
"bins" : [
"DYJetsToLL_M50_HT100to200",
"DYJetsToLL_M50_HT200to400",
"DYJetsToLL_M50_HT400to600",
"DYJetsToLL_M50_HT600toInf",
],
'dir' : dir,
}


QCDHT_25ns = {
"name":"QCD",
"bins":[
"QCD_HT1000to1500",
"QCD_HT1500to2000",
"QCD_HT2000toInf",
"QCD_HT200to300",
"QCD_HT300to500",
"QCD_HT500to700",
"QCD_HT700to1000",
],
'dir' : dir,
}

TTV_25ns = {
"name":"TTVH_HT",
"bins":[
"TTWJetsToLNu_25ns",
"TTWJetsToQQ_25ns",
"TTZToLLNuNu_25ns",
"TTZToQQ_25ns",
],
'dir' : dir,
}



