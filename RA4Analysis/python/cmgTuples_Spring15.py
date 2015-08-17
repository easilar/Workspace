import copy, os, sys


#artur_path = "/afs/cern.ch/work/e/easilar/Aug06_GoldenJSON/"
artur_path = "/afs/cern.ch/work/e/easilar/data/data_from_Artur_newMET_13Aug/Aug12_GoldenJson_METnoHF/"


data_ele={\
"name" : "SingleElectron_Run2015B",
"chunkString" : "SingleElectron_Run2015B",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}

data_mu={\
"name" : "SingleMuon_Run2015B",
"chunkString" : "SingleMuon_Run2015B",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}


data_ele_17July={\
"name" : "SingleElectron_Run2015B_17Jul",
"chunkString" : "SingleElectron_Run2015B_17Jul",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}

data_mu_17July={\
"name" : "SingleMuon_Run2015B_17Jul",
"chunkString" : "SingleMuon_Run2015B_17Jul",
"rootFileLocation":"/treeProducerSusySingleLepton/tree.root",
"skimAnalyzerDir":"skimAnalyzerCount",
"treeName":"tree",
'isData':True,
'dir' : artur_path+"/"
}

################

TTJets={\
#"name" : "TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

DY={\
#"name" : "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
#'dir' : "/tmp/easilar/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx/", 
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8//", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

T_tWch={\
#"name" : "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TBar_tWch={\
#"name" : "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

TToLeptons_tch={\
#"name" : "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/", 
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

WJets={\
#"name" : "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8",
"chunkString" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx",
#'dir' : "/tmp/easilar/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/",
#'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_plzworkheplx/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#QCD_HT100to200={\
#"name" : "QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
#"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
#'dir' : "/tmp/easilar/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx/",
#"rootFileLocation":"tree.root",
#"treeName":"tree",
#'isData':False
#}

QCD_HT200to300={\
#"name" : "QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT300to500={\
#"name" : "QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT500to700={\
#"name" : "/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT700to1000={\
#"name" : "/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1000to1500={\
#"name" : "/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT1500to2000={\
#"name" : "/QCD_HT1000to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

QCD_HT2000toInf={\
#"name" : "/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"chunkString" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
"name" : "RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_plzworkheplx",
'dir' : "/afs/hephy.at/work/e/easilar/MC_Spring15_Samples/hadded_samples/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/",
"rootFileLocation":"tree.root",
"treeName":"tree",
'isData':False
}

#print QCD_HT500to700


