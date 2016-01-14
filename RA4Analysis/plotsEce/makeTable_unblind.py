import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_Unblinding import *
from Workspace.RA4Analysis.signalRegions import *
from cutFlow_helper import *
from math import *

def getNumString(n,ne, acc=2):    ##For printing table 
  if type(n) is float and type(ne) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  else:
    return n +'&$\pm$&'+ ne

weight_str = "(2.1*(weight/3))"
weight_str_var = weight_str+"*"+weight_str 


path = "/afs/hephy.at/user/e/easilar/www/MC/Spring15/25ns_fromArtur/Tables/"
if not os.path.exists(path):
  os.makedirs(path)

bkg_samples=[
{"sample":"DY",           "name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",    "name":singleTop_25ns,"tex":"single top",'color': ROOT.kViolet+5},
{"sample":"QCD",          "name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"TTVH",          "name":TTV_25ns, "tex":"TTVH","color":ROOT.kCyan-6},
{"sample":"WJets",        "name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
]

s_tt = {"sample":"ttJets",       "name":TTJets_combined, "tex":"ttbar + jets",'color':ROOT.kBlue-4}
s_tt['chain'] = getChain(s_tt['name'],histname='')

for b in bkg_samples:
  b['chain'] = getChain(b['name'],histname='')

lepSels = [
{'cut':'singleMuonic' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0', 'label':'_mu_', 'str':'1 $\\mu$' },\
{'cut':'singleElectronic' ,  'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',  'label':'_ele_','str':'1 $e$'},\
{'cut':'singleLeptonic' ,'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0','label':'_lep_','str':'1 $lepton$' }\
]
for lepSel in lepSels:

  print "====" , lepSel['label'] , "====="

  presel = "&&".join([lepSel['cut'],lepSel['veto'],jets_2_80])
  btagString = "nBJetMediumCSV30"
  signalRegions = signalRegion3fb

  rowsNJet = {}
  rowsSt = {}
  for srNJet in sorted(signalRegions):
    rowsNJet[srNJet] = {}
    rowsSt[srNJet] = {}
    rows = 0
    for stb in sorted(signalRegions[srNJet]):
      rows += len(signalRegions[srNJet][stb])
      rowsSt[srNJet][stb] = {'n':len(signalRegions[srNJet][stb])}
    rowsNJet[srNJet] = {'nST':len(signalRegions[srNJet]), 'n':rows}



  pred = {}
  for srNJet in sorted(signalRegions):
    pred[srNJet] = {}
    for stb in sorted(signalRegions[srNJet]):
      pred[srNJet][stb] = {}
      for htb in sorted(signalRegions[srNJet][stb]):
        pred[srNJet][stb][htb] = {}
        deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
        name, cut =  nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagString)
        for b in bkg_samples:
          b['yield'] = getYieldFromChain(b['chain'], cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str)
          b['yield_Var'] = getYieldFromChain(b['chain'], cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str_var)
          print cut ,"    : " , b['yield'] 
          pred[srNJet][stb][htb].update({\
                      b['sample']+'_yield':b['yield'],\
                      b['sample']+'_yield_Var':b['yield_Var'],\
                    })
        s_tt['yield_diLep'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str) 
        s_tt['yield_diLep_Var'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==2&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str_var) 
        s_tt['yield_1Lep'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==1&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str) 
        s_tt['yield_1Lep_Var'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==1&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str_var) 
        s_tt['yield_rest'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==0&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str ) 
        s_tt['yield_rest_Var'] = getYieldFromChain(s_tt['chain'], "(ngenLep+ngenTau)==0&&"+cut+"&&deltaPhi_Wl<"+str(deltaPhiCut), weight = weight_str_var) 
        pred[srNJet][stb][htb].update({\
                                      s_tt['sample']+'_yield_diLep':s_tt['yield_diLep'],\
                                      s_tt['sample']+'_yield_diLep_Var':s_tt['yield_diLep_Var'],\
                                      s_tt['sample']+'_yield_1Lep':s_tt['yield_1Lep'],\
                                      s_tt['sample']+'_yield_1Lep_Var':s_tt['yield_1Lep_Var'],\
                                      s_tt['sample']+'_yield_rest':s_tt['yield_rest'],\
                                      s_tt['sample']+'_yield_rest_Var':s_tt['yield_rest_Var'],\
                                      })

  print 
  print
  print '\\begin{table}[ht]\\begin{center}\\resizebox{\\textwidth}{!}{\\begin{tabular}{|c|c|c|rrr|rrr|rrr|rrr|rrr|rrr|rrr|rrr|c|}\\hline'
  print ' \\njet     & \ST & \HT     &\multicolumn{3}{c|}{$t\\bar{t}$+Jets diLep}&\multicolumn{3}{c|}{$t\\bar{t}$+Jets semiLep}&\multicolumn{3}{c|}{$t\\bar{t}$+Jets had}&\multicolumn{3}{c|}{W+Jets}&\multicolumn{3}{c|}{QCD}&\multicolumn{3}{c|}{TTVH}&\multicolumn{3}{c|}{DY + Jets}&\multicolumn{3}{c|}{Single Top}&\\DF\\\%\hline'
  print '& $[$GeV$]$ &$[$GeV$]$&\multicolumn{3}{c|}{}  &\multicolumn{3}{c|}{}                     &\multicolumn{3}{c|}{}                    &\multicolumn{3}{c|}{}      &\multicolumn{3}{c|}{}   &\multicolumn{3}{c|}{}    &\multicolumn{3}{c|}{}         &\multicolumn{3}{c|}{}          &\multicolumn{1}{c|}{} \\\\\hline'


  secondLine = False
  for srNJet in sorted(signalRegions):
    print '\\hline'
    if secondLine: print '\\hline'
    secondLine = True
    print '\multirow{'+str(rowsNJet[srNJet]['n'])+'}{*}{\\begin{sideways}$'+varBin(srNJet)+'$\end{sideways}}'
    for stb in sorted(signalRegions[srNJet]):
      print '&\multirow{'+str(rowsSt[srNJet][stb]['n'])+'}{*}{$'+varBin(stb)+'$}'
      first = True
      for htb in sorted(signalRegions[srNJet][stb]):
        deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
        if not first: print '&'
        first = False
        print '&$'+varBin(htb)+'$'
        print ' & '+getNumString(pred[srNJet][stb][htb]['ttJets_yield_diLep'],    sqrt(pred[srNJet][stb][htb]['ttJets_yield_diLep_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['ttJets_yield_1Lep'],    sqrt(pred[srNJet][stb][htb]['ttJets_yield_1Lep_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['ttJets_yield_rest'],    sqrt(pred[srNJet][stb][htb]['ttJets_yield_rest_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['WJets_yield'],     sqrt(pred[srNJet][stb][htb]['WJets_yield_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['QCD_yield'],       sqrt(pred[srNJet][stb][htb]['QCD_yield_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['TTVH_yield'],       sqrt(pred[srNJet][stb][htb]['TTVH_yield_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['DY_yield'],        sqrt(pred[srNJet][stb][htb]['DY_yield_Var']))\
             +' & '+getNumString(pred[srNJet][stb][htb]['singleTop_yield'], sqrt(pred[srNJet][stb][htb]['singleTop_yield_Var']))\
             +' & '+str(deltaPhiCut)\
             +'\\\\'
        if htb[1] == -1 : print '\\cline{2-28}'
  print '\\hline\end{tabular}}\end{center}\caption{Background yields for the 0-tag CR regions, 2.1 $fb^{-1}$}\label{tab:0b_yield_table}\end{table}'


  print
