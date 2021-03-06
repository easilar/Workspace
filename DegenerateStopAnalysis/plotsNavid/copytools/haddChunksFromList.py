
import os
import glob

## you can get the samples with glob.glob( "/mother_dir/*Spring15*" )


samples=['/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WWTo2L2Nu_13TeV-powheg_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ZJetsToNuNu_HT-600ToInf_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ZJetsToNuNu_HT-400To600_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ZZ_TuneCUETP8M1_13TeV-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_test',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2_MC25ns',
 '/data/nrad/cmgTuples/RunII/Spring15_v1/ZJetsToNuNu_HT-200To400_13TeV-madgraph_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns']


#samples=['/data/nrad/cmgTuples/RunII/Spring15_v1/backup_DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1_MC25ns']

def doHadd():
  for sample in samples:
    #os.system("cd %s"%sample)
    os.chdir(sample)
    #os.system("haddChunks.py -c %s"%sample)
    os.system("heppy_hadd.py -c .")
  
