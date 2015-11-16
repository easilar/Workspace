#!/bin/sh 

python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=SingleElectron_Run2015D_v4
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=SingleElectron_Run2015D_05Oct
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=SingleMuon_Run2015D_v4
python cmgPostProcessing.py --overwrite --leptonSelection=hard --skim="HT500ST250"  --samples=SingleMuon_Run2015D_05Oct
