import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
#import Workspace.HEPHYPythonTools.xsec as xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
#from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns import *
##from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns import *
from cutFlow_helper import *


path = "/afs/hephy.at/user/e/easilar/www/MC/Spring15/25ns_fromArtur/Cut_Flow/"
if not os.path.exists(path):
  os.makedirs(path)

maxN = 1
small = False
if not small : maxN = -1

lumi = 2100.0 #pb-1

lepSels = [
#  {'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '(HLT_MuHT350MET70 || HLT_Mu50)'},\
#  {'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '(HLT_EleHT350MET70 || HLT_Ele105)'},\
{'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))' },\
#{'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#{'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
]


samples=[
{"sample":"DY",           "list":[DYJetsToLL_M_50_HT100to200_25ns,DYJetsToLL_M_50_HT200to400_25ns,DYJetsToLL_M_50_HT400to600_25ns,DYJetsToLL_M_50_HT600toInf_25ns],"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",    "list":[TToLeptons_sch,TToLeptons_tch,TBar_tWch,T_tWch],"tex":"single top",'color': ROOT.kViolet+5},
{"sample":"QCD",          "list":[QCD_HT300to500_25ns,QCD_HT500to700_25ns,QCD_HT700to1000_25ns,QCD_HT1000to1500_25ns,QCD_HT1500to2000_25ns,QCD_HT2000toInf_25ns], "tex":"QCD","color":ROOT.kCyan-6},        
{"sample":"TTVH",          "list":[TTZToQQ_25ns , TTZToLLNuNu_25ns , TTWJetsToQQ_25ns, TTWJetsToLNu_25ns], "tex":"TTVH","color":ROOT.kCyan-6},        
{"sample":"WJets",        "list":[WJetsToLNu_HT100to200_25ns,WJetsToLNu_HT200to400_25ns,WJetsToLNu_HT400to600_25ns,WJetsToLNu_HT600to800_25ns,WJetsToLNu_HT800to1200_25ns,WJetsToLNu_HT1200to2500_25ns,WJetsToLNu_HT2500toInf_25ns],"tex":"W + jets","color":ROOT.kGreen-2},
#{"sample":"ttJets",       "list":[TTJets], "tex":"ttbar + jets",'color':ROOT.kBlue-4},
#{"sample":"ttJets",       "list":[TTJets_LO_25ns,TTJets_LO_HT600to800_25ns,TTJets_LO_HT800to1200_25ns,TTJets_LO_HT1200to2500_25ns,TTJets_LO_HT2500toInf_25ns], "tex":"ttbar + jets",'color':ROOT.kBlue-4},
##{"sample":"ttJets",       "list":[TTJets_LO], "tex":"ttbar + jets",'color':ROOT.kBlue-4},
]

for lepSel in lepSels:
  cuts = [
 #{'cut':'(1)', 'label':'no cut'},\
 #{'cut':'(1)', 'label':'HT Skim'},\
 #{'cut':"&&".join([lepSel['cut']]), 'label': lepSel['str']},\
 #{'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label': lepSel['str']+' veto'},\
 # {'cut':"&&".join([lepSel['cut'],OneLepAnti]), 'label': lepSel['str']+' Anti + veto'},\
 # {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",lep_hard]), 'label': 'nJet $\\geq$ 5'},\
 # {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",jets_2_80,jets_2_80]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
 # {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",jets_2_80,jets_2_80,ht_cut]), 'label':'$H_T >$ 500 GeV'},\
 # {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",jets_2_80,ht_cut,st,jets_2_80]), 'label':'$L_T >$ 250 GeV'},\
 # {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80]), 'label': '0 b-jets (CSVM)' },\
  {'cut':"&&".join([lepSel['cut'],lepSel['veto'],njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_multi,jets_2_80]), 'label': '$>=1 b-jets (CSVM)$' },\
  ###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,njets_30+"==5",jets_2_80]), 'label': 'SR 1 $nJet = 5$'},\
  ###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,njets_30+"==5",'(LepGood_pt[0]+met_pt)>250&&(LepGood_pt[0]+met_pt)<350',jets_2_80]), 'label': 'SR 1 $LT 250-350$'},\
  ###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,njets_30+"==5",'(LepGood_pt[0]+met_pt)>250&&(LepGood_pt[0]+met_pt)<350',ht_cut,jets_2_80]), 'label': 'SR 1 $HT > 500$'},\
  ###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,njets_30+"==5",'(LepGood_pt[0]+met_pt)>250&&(LepGood_pt[0]+met_pt)<350',ht_cut,dPhi_cut]), 'label': 'SR 1 $deltaPhi>1$'},\
  # {'cut':"&&".join([lepSel['cut'],lep_hard,lepSel['veto'],lep_hard]), 'label': lepSel['str']+'_veto'},\
  #{'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard]), 'label': lepSel['str']+'_hard'},\
  #{'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5"]), 'label': 'nJet $\\geq$ 5'},\
  #{'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,jets_2_80]), 'label': '2. jets ($\\geq$ 80 GeV)'},\
  #{'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,st,jets_2_80]), 'label': '$L_T >$ 250 GeV'},\
  #{'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,st,nbjets_30_cut_zero,jets_2_80]), 'label': '0 b-jets (CSVv2)'},\
  #{'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,st,nbjets_30_cut_multi,jets_2_80]), 'label': '$>=1 b-jets (CSVv2)$'},\
#   {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,'(LepGood_pt[0]+met_pt)>=250&&(LepGood_pt[0]+met_pt)<350']), 'label': '$TEST$'},\
#   {'cut':"&&".join([lepSel['cut'],lepSel['veto'],lep_hard,njets_30+">=5",jets_2_80,ht_cut,st,nbjets_30_cut_zero,jets_2_80,'(LepGood_pt[0]+met_pt)>=250&&(LepGood_pt[0]+met_pt)<350',dPhi_cut]), 'label': '$deltaPhi>1$'},\
    
###{'cut':'(1)', 'label':'no cut'},\
###{'cut':lepSel['cut'], 'label':lepSel['str']},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto']]), 'label':'lepton veto'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut]), 'label':'$H_T >$ 500 GeV'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st]), 'label':'$L_T >$ 250 GeV'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut]), 'label':'4 jets ($\\geq$ 30 GeV)'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80]), 'label':'2. jets ($\\geq$ 80 GeV)'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero]), 'label':'0 b-jets (CSVv2)'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,dPhi_cut]), 'label':'$\\Delta\\Phi > 1$'},\
####{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters]), 'label':'Filters'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi]), 'label':'$>=1 b-jets (CSVv2)$'},\
###{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi,dPhi_cut]), 'label':'$\\Delta\\Phi > 1$'},\
####{'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi,filters]), 'label':'Filters'},\
  ]
  ofile = file(path+'cut_flow_'+str(lumi)+'pb_'+lepSel['label']+'_MiniAODv2_.tex','w')
  #ofile = file(path+'cut_flow_'+str(lumi)+'pb_'+lepSel['label']+'_TEST_.tex','w')
  doc_header = '\\documentclass{article}\\usepackage[english]{babel}\\usepackage{graphicx}\\usepackage[margin=0.5in]{geometry}\\begin{document}'
  ofile.write(doc_header)
  ofile.write("\n")
  #table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c | c | c | c}'
  table_header = '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{c | c | c | c | c | c | c }'
  ofile.write(table_header)
  ofile.write("\n")
  for s in samples:
    line = '&' + s['tex'] 
    ofile.write(line)
    ofile.write("\n")
  line_end = '\\\ \\hline'
  ofile.write(line_end)
  ofile.write("\n")
  for cut in cuts:
    print cut['label']
    print cut['cut']
    ofile.write(cut['label'])
    for s in samples:
      tot_yields = 0
      for b in s['list']:
        #print b
        #chunk = getChunks(b, treeName="treeProducerSusySingleLepton",maxN=maxN)
        chunk = getChunks(b,maxN=maxN)
        chain = getChain(chunk[0],maxN=maxN,histname="",treeName="tree")
        #nEntry = chain.GetEntries()
        nEntry = float(chunk[1])
        #print nEntry 
        #weight = lumi*xsec.xsec[b['dbsName']]/nEntry
        #weight = 1 ##count the MC events
        print "MC Events:" , chain.GetEntries(cut['cut'])
        mc_yield = chain.GetEntries(cut['cut'])
        #y_remain = chain.GetEntries(cut['cut'])
        
        y_remain = getYieldFromChain(chain,cutString = cut['cut'],weight = "(((xsec*genWeight)*"+str(lumi)+")/"+str(nEntry)+")")
        #y_remain = getYieldFromChain(chain,cutString = cut['cut'],weight = "(1)")
        #y_remain = getYieldFromChain(chain,cutString = cut['cut'],weight = "(((xsec)*"+str(lumi)+")/"+str(nEntry)+")")
        tot_yields += y_remain
        #tot_yields += mc_yield
      print tot_yields
      line_yield = '&' + str(format(tot_yields, '.1f'))
      ofile.write(line_yield)
    ofile.write('\\\\')
    ofile.write('\n')

  table_end = '\end{tabular}}\end{center}\caption{CutFlow}\label{tab:CutFlow}\end{table}'
  ofile.write(table_end)
  ofile.write("\n")
  doc_end = '\\end{document}'
  ofile.write(doc_end)
  ofile.close()
  print "Written", ofile.name


