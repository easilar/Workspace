#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_sch
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TToLeptons_tch
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TBar_tWch
python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=T_tWch

#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTWJetsToLNu_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTWJetsToQQ_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTZToLLNuNu_25ns
#python cmgPostProcessing.py --leptonSelection=hard --skim=""  --samples=TTZToQQ_25ns



