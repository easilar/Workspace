#!/bin/sh 
########Spring15###############

#python cmgPostProcessing.py --overwrite  --calcbtagweights --skim="HT500ST250"  --samples=TToLeptons_sch
#python cmgPostProcessing.py --overwrite  --calcbtagweights --skim="HT500ST250"  --samples=TToLeptons_tch
#python cmgPostProcessing.py --overwrite  --calcbtagweights --skim="HT500ST250"  --samples=TBar_tWch

#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=ST_tchannel_antitop_4f_leptonDecays
#python cmgPostProcessing.py --overwrite --calcbtagweights --skim="HT500ST250"  --samples=ST_tchannel_antitop_4f_inclusiveDecays
#python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=ST_tW_antitop_5f_inclusiveDecays

#python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DiBoson_WW
#python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DiBoson_WZ
#python cmgPostProcessing.py --overwrite  --skim="HT500ST250"  --samples=DiBoson_ZZ

python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights  --samples=TTWJetsToLNu
python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights  --samples=TTWJetsToQQ
python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights  --samples=TTZToLLNuNu
python cmgPostProcessing.py --overwrite --skim="HT500ST250" --calcbtagweights  --samples=TTZToQQ



