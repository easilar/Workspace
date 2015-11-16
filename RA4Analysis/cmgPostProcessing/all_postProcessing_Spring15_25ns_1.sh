#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="LHEHT600"    --samples=TTJets_LO
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250LHE"  --samples=TTJets_LO_HT600to800_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250LHE"  --samples=TTJets_LO_HT800to1200_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250LHE"  --samples=TTJets_LO_HT1200to2500_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250LHE"  --samples=TTJets_LO_HT2500toInf_25ns
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"    --samples=TTJets_LO_pow
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250semiLep"  --samples=TTJets_SingleLeptonFromT_full
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250semiLep"  --samples=TTJets_SingleLeptonFromTbar_full
#python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250diLep"  --samples=TTJets_DiLepton_full
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250FullHadronic"    --samples=TTJets_LO

