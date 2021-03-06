# ZinvEstimation_MuMu_loop.py
# Zinv estimation using the Z->mumu channel.
# Mateusz Zarucki 2016

import ROOT
import os, sys
import argparse
import pickle
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import CutClass, Plots, getPlots, drawPlots, Yields, setEventListToChains, makeDir, setup_style
from Workspace.DegenerateStopAnalysis.tools.bTagWeights import bTagWeights
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from Workspace.HEPHYPythonTools import u_float
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Sets TDR style
setup_style()

#Input options
parser = argparse.ArgumentParser(description = "Input options")
parser.add_argument("--SR", dest = "SR",  help = "SR", type = str, default = "SR1") # 'SR1', 'SR1a', 'SR1b', 'SR1c', 'SRL1', 'SRH1', 'SRV1', 'SRL1a', 'SRH1a', 'SRV1a', 'SRL1b', 'SRH1b', 'SRV1b', 'SRL1c', 'SRH1c', 'SRV1c'
parser.add_argument("--CT2", dest = "CT2",  help = "CT2 Cut", type = str, default = "75")
parser.add_argument("--lepEta", dest = "lepEta",  help = "Extra soft lepton eta", type = str, default = "2.5")
#parser.add_argument("--MET", dest = "MET",  help = "MET Cut", type = str, default = "200")
#parser.add_argument("--HT", dest = "HT",  help = "HT Cut", type = str, default = "200")
parser.add_argument("--beforeEmul", dest = "beforeEmul",  help = "beforeEmul plot", type = int, default = 0)
parser.add_argument("--afterEmul", dest = "afterEmul",  help = "afterEmul plot", type = int, default = 1)
parser.add_argument("--leptons", dest = "leptons",  help = "Extra lepton distributions", type = int, default = 1)
parser.add_argument("--peak", dest = "peak",  help = "Z-peak selection", type = int, default = 1)
parser.add_argument("--doYields", dest = "doYields",  help = "Calulate yields", type = int, default = 1)
parser.add_argument("--btag", dest = "btag",  help = "B-tagging option", type = str, default = "sf")
parser.add_argument("--getData", dest = "getData",  help = "Get data samples", type = int, default = 1)
parser.add_argument("--plot", dest = "plot",  help = "Toggle plot", type = int, default = 0)
parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
parser.add_argument("--save", dest = "save",  help = "Toggle save", type = int, default = 1)
parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
parser.add_argument("-b", dest = "batch",  help = "Batch mode", action = "store_true", default = False)
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments
SR = args.SR
CT2cut = args.CT2
lepEta = args.lepEta
beforeEmul = args.beforeEmul
afterEmul = args.afterEmul
leptons = args.leptons
peak = args.peak
#METcut = args.MET
#HTcut = args.HT
doYields = args.doYields
btag = args.btag
getData = args.getData
plot = args.plot
logy = args.logy
save = args.save
verbose = args.verbose

print makeDoubleLine()
print "Performing Zinv estimation."
print makeDoubleLine()

#Samples
cmgPP = cmgTuplesPostProcessed()
samplesList = ["vv", "tt", "dy5to50", "dy"] #"qcd", "w", "z", "st" 
if getData: samplesList.append("d1muBlind")

samples = getSamples(cmgPP = cmgPP, skim = 'oneLep', sampleList = samplesList, scan = False, useHT = True, getData = getData) 

if verbose:
   print makeLine()
   print "Using samples:"
   newLine()
   for s in samplesList:
      if s: print samples[s].name,":",s
      else: 
         print "!!! Sample " + sample + " unavailable."
         sys.exit(0)
#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/Zinv/MuMu"
   
   savedir += "/lepEta" + lepEta
   savedir += "/" + SR
   #savedir += "/bTagWeight_" + btag
   
   savedir1 = savedir + "/beforeEmul"
   savedir2 = savedir + "/afterEmul/CT" + CT2cut
   savedir3 = savedir + "/pickle"
   
   suffix1 = "_" + SR
   suffix2 = suffix1 + "_" + CT2cut

   if peak: 
      suffix1 = "_peak"
      suffix2 = "_peak"
      savedir1 += "/peak"
      savedir2 += "/peak"

   makeDir("%s/root"%(savedir1))
   makeDir("%s/pdf"%(savedir1))
   makeDir("%s/root"%(savedir2))
   makeDir("%s/pdf"%(savedir2))
   makeDir(savedir3)

#Geometric cuts
#etaAcc = 2.1
#ebSplit = 0.8 #barrel is split into two regions
#ebeeSplit = 1.479 #division between barrel and endcap

#Indicies of leading muons
ind1 = "IndexLepAll_mu[0]"
ind2 = "IndexLepAll_mu[1]"

dimuon_mass = "sqrt(2*(LepAll_pt[" + ind1 + "] * LepAll_pt[" + ind2 + "]*(cosh(LepAll_eta[" + ind1 + "] - LepAll_eta[" + ind2 + "]) - cos(LepAll_phi[" + ind1 + "] - LepAll_phi[" + ind2 + "]))))"

dimuon_pt = "sqrt(LepAll_pt[" + ind1 + "]*LepAll_pt[" + ind1 + "] + LepAll_pt[" + ind2 + "]*LepAll_pt[" + ind2 + "] + 2*LepAll_pt[" + ind1 + "]*LepAll_pt[" + ind2 + "]*cos(LepAll_phi[" + ind1 + "] - LepAll_phi[" + ind2 + "]))"

dimuon_phi = "atan(\
((LepAll_pt[" + ind1 + "]*sin(LepAll_phi[" + ind1 + "])) + (LepAll_pt[" + ind2 + "]*sin(LepAll_phi[" + ind2 + "])))/\
((LepAll_pt[" + ind1 + "]*cos(LepAll_phi[" + ind1 + "])) + (LepAll_pt[" + ind2 + "]*cos(LepAll_phi[" + ind2 + "]))))"

met2 = "sqrt(met*met + dimuon_pt*dimuon_pt + 2*met*dimuon_pt*cos(met_phi - dimuon_phi))"
met2_phi = "atan((met*sin(met_phi) + dimuon_pt*sin(dimuon_phi))/(met*cos(met_phi) + dimuon_pt*cos(dimuon_phi)))"

electron_mt_2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_el[0]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_el[0]])))"
muon_mt_2 = "sqrt(2*met2*LepAll_pt[IndexLepAll_mu[2]]*(1 - cos(met2_phi - LepAll_phi[IndexLepAll_mu[2]])))"

for s in samplesList: 
   samples[s].tree.SetAlias("dimuon_mass", dimuon_mass)
   samples[s].tree.SetAlias("dimuon_pt", dimuon_pt)
   samples[s].tree.SetAlias("dimuon_phi", dimuon_phi)
   samples[s].tree.SetAlias("met2", met2)
   samples[s].tree.SetAlias("met2_phi", met2_phi)
   samples[s].tree.SetAlias("electron_mt_2", electron_mt_2)
   samples[s].tree.SetAlias("muon_mt_2", muon_mt_2)

#SRs
def regions(lepton):
   if lepton == "electron":
      pdgId = "11"
      ind = "IndexLepAll_el[0]"
      mt_2 = "electron_mt_2"
   elif lepton == "muon":
      pdgId = "13"
      ind = "IndexLepAll_mu[2]"
      mt_2 = "muon_mt_2"
   else:
      assert False
    
   SRs = {\
      #'SR1':["SR1","LepAll_pt[" + ind + "] < 30"],
      'SR1a':["SR1a",   combineCuts(mt_2 + " < 60", "LepAll_pt[" + ind + "] < 30", "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SR1b':["SR1b",   combineCuts(btw(mt_2, 60, 95), "LepAll_pt[" + ind + "] < 30", "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SR1c':["SR1c",   combineCuts(mt_2 + " > 95", "LepAll_pt[" + ind + "] < 30")],
      
      'SRL1a':["SRL1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 5, 12), "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SRH1a':["SRH1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 12, 20), "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SRV1a':["SRV1a", combineCuts(mt_2 + " < 60", btw("LepAll_pt[" + ind + "]", 20, 30), "LepAll_pdgId[" + ind + "] == " + pdgId)],
   
      'SRL1b':["SRL1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 5, 12), "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SRH1b':["SRH1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 12, 20), "LepAll_pdgId[" + ind + "] == " + pdgId)],
      'SRV1b':["SRV1b", combineCuts(btw(mt_2, 60, 95), btw("LepAll_pt[" + ind + "]", 20, 30), "LepAll_pdgId[" + ind + "] == " + pdgId)],
   
      'SRL1c':["SRL1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 5, 12))],
      'SRH1c':["SRH1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 12, 20))],
      'SRV1c':["SRV1c", combineCuts(mt_2 + " > 95", btw("LepAll_pt[" + ind + "]", 20, 30))]}
   
   SRs['SR1'] =  ["SR1", "((" + SRs['SR1a'][1] + ") || (" + SRs['SR1b'][1] + ") || (" + SRs['SR1c'][1] + "))"]
   SRs['SRL1'] = ["SRL1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 5, 12))]
   SRs['SRH1'] = ["SRH1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 12, 20))]
   SRs['SRV1'] = ["SRV1", combineCuts(SRs['SR1'][1], btw("LepAll_pt[" + ind + "]", 20, 30))]
   
   return SRs

SRs_el = regions('electron')
SRs_mu = regions('muon')

#btag weights
bWeightDict = bTagWeights(btag)
bTagString = bWeightDict['sr1_bjet']
#bTagString = "nBJet == 0" 

#selection on Z-peak
if peak:
   peakCutString = "abs(dimuon_mass - 91.1876) < 15"   
else:
   peakCutString = "1"   

#Preselection & selection of Z->mumu events
dimuon = CutClass("dimuon", [
   ["ISR100", "nIsrJet >= 1"],
   ["TauVeto","Sum$(TauGood_idMVANewDM && TauGood_pt > 20) == 0"],
   ["BVeto", bTagString],
   ["No3rdJet60","nVetoJet <= 2"],
   ["2mu", "nLepAll_mu >= 2"], 
    
   ["muon1", "abs(LepAll_pdgId[" + ind1 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind1 + "] < 0.12"],
   ["pt25", "LepAll_pt[" + ind1 + "] > 25"],
    
   ["muon2", "abs(LepAll_pdgId[" + ind2 + "]) == 13"], #redundant
   ["relIso", "LepAll_relIso03[" + ind2 + "] < 0.12"],
   ["pt20", "LepAll_pt[" + ind2 + "] > 20"],
   
   ["OS", "LepAll_pdgId[" + ind1 + "] == -LepAll_pdgId[" + ind2 + "]"],
   ], baseCut = None)

emulated = CutClass("emulated", [
   ["peak", peakCutString],
   ["dimuon_mass","dimuon_mass > 55"],
   #["dimuon_pt","dimuon_pt > 75"],
   ["met2", "met2 > 75"], #instead of cut on dimuon pt
   ["CT2","min(met2, ht_basJet - 100) >" + CT2cut],
   ], baseCut = dimuon)

electrons = CutClass("electrons", [
   #["ele","nLepAll_el >= 1"], #redundant
   ["2mu-el30Veto-2el20Veto", "((nLepAll_el == 1 && LepAll_pt[IndexLepAll_el[0]] < 30) ||" +\
                               "(nLepAll_el == 2 && LepAll_pt[IndexLepAll_el[0]] < 30 && LepAll_pt[IndexLepAll_el[1]] < 20))"],
   ["muVeto", "(nLepAll_mu == 2 || (nLepAll_mu == 3 && LepAll_pt[IndexLepAll_mu[2]] < 20))"],
   ["eta1.5", "abs(LepAll_eta[IndexLepAll_el[0]]) < " + lepEta],
   SRs_el[SR]
   ], baseCut = emulated)

muons = CutClass("muons", [
   #["mu","nLepAll_mu >= 3"], #redundant
   ["2mu-mu30Veto-2mu20Veto", "((nLepAll_mu == 3 && LepAll_pt[IndexLepAll_mu[2]] < 30) ||" +\
                               "(nLepAll_mu == 4 && LepAll_pt[IndexLepAll_mu[2]] < 30 && LepAll_pt[IndexLepAll_mu[3]] < 20))"],
   ["elVeto", "(nLepAll_el == 0 || (nLepAll_el == 1 && LepAll_pt[IndexLepAll_el[0]] < 20))"],
   ["eta1.5", "abs(LepAll_eta[IndexLepAll_mu[2]]) < " + lepEta],
   SRs_mu[SR]
   ], baseCut = emulated)

#Sets event list      
setEventListToChains(samples, samplesList, dimuon)

if doYields and peak:

   yields = {}
   ZinvRatios = {}
   ZinvYields = {}
   ZinvYields['Zpeak'] = {}
   ZinvYields['Nel'] = {}
   ZinvYields['Nmu'] = {}

   yields['Zpeak'] = Yields(samples, samplesList, emulated, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['Nel'] = Yields(samples, samplesList, electrons, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)
   yields['Nmu'] = Yields(samples, samplesList, muons, cutOpt = "combinedList", pklOpt = False, nDigits = 2, err = True, verbose = True, nSpaces = 10)

   ZinvYields['Zpeak']['data'] = yields['Zpeak'].yieldDictFull['d1muBlind']['emulated']
   ZinvYields['Zpeak']['dy'] =  (yields['Zpeak'].yieldDictFull['dy']['emulated'] + yields['Zpeak'].yieldDictFull['dy5to50']['emulated'])
   ZinvYields['Zpeak']['tt'] =   yields['Zpeak'].yieldDictFull['tt']['emulated']
   ZinvYields['Zpeak']['vv'] =   yields['Zpeak'].yieldDictFull['vv']['emulated']
   ZinvYields['Nel']['data'] =   yields['Nel'].yieldDictFull['d1muBlind']['electrons']
   ZinvYields['Nel']['dy'] =    (yields['Nel'].yieldDictFull['dy']['electrons'] + yields['Nel'].yieldDictFull['dy5to50']['electrons'])
   ZinvYields['Nel']['tt'] =     yields['Nel'].yieldDictFull['tt']['electrons']
   ZinvYields['Nel']['vv'] =     yields['Nel'].yieldDictFull['vv']['electrons']
   ZinvYields['Nmu']['data'] =   yields['Nmu'].yieldDictFull['d1muBlind']['muons']
   ZinvYields['Nmu']['dy'] =    (yields['Nmu'].yieldDictFull['dy']['muons'] + yields['Nmu'].yieldDictFull['dy5to50']['muons'])
   ZinvYields['Nmu']['tt'] =     yields['Nmu'].yieldDictFull['tt']['muons']
   ZinvYields['Nmu']['vv'] =     yields['Nmu'].yieldDictFull['vv']['muons']

   if not os.path.isfile("%s/ZinvYields%s.txt"%(savedir, suffix1)):
      outfile = open("%s/ZinvYields%s.txt"%(savedir, suffix1), "w")
      outfile.write("Zinv Estimation Yields\n")
      outfile.write("CT       Zpeak_data          Zpeak_DY           Zpeak_TT           Zpeak_VV           Nel_data           Nel_DY           Nel_TT           Nel_VV           Nmu_data           Nmu_DY            Nmu_TT          Nmu_VV\n")  
 
   with open("%s/ZinvYields%s.txt"%(savedir, suffix1), "a") as outfile:
      outfile.write(CT2cut.ljust(7) +\
      str(ZinvYields['Zpeak']['data'].round(2)).ljust(18) +\
      str(ZinvYields['Zpeak']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['Zpeak']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Zpeak']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['data'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Nel']['vv'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['data'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['dy'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['tt'].round(2)).ljust(18) +\
      str(ZinvYields['Nmu']['vv'].round(2)) + "\n")

   #Z xsec
   ZinvRatios['Zpeak_dataMC'] = (ZinvYields['Zpeak']['data']/(ZinvYields['Zpeak']['dy'] + ZinvYields['Zpeak']['tt'] + ZinvYields['Zpeak']['vv']))
   
   #probability of extra leptons
   if ZinvYields['Zpeak']['data'].val:
      ZinvRatios['prob_el_data'] = (ZinvYields['Nel']['data']/ZinvYields['Zpeak']['data'])
      ZinvRatios['prob_mu_data'] = (ZinvYields['Nmu']['data']/ZinvYields['Zpeak']['data'])
   
   #probability of observing electron
   ZinvRatios['prob_el_MC'] = ((ZinvYields['Nel']['dy'] + ZinvYields['Nel']['tt'] + ZinvYields['Nel']['vv'])/
                               (ZinvYields['Zpeak']['dy'] + ZinvYields['Zpeak']['tt'] + ZinvYields['Zpeak']['vv']))
   
   if ZinvRatios['prob_el_MC'].val:
      ZinvRatios['prob_el_dataMC'] = ZinvRatios['prob_el_data']/ZinvRatios['prob_el_MC']
   else:
      ZinvRatios['prob_el_dataMC'] = u_float.u_float(0,0)

   #probability of observing muon
   ZinvRatios['prob_mu_MC'] = ((ZinvYields['Nmu']['dy'] + ZinvYields['Nmu']['tt'] + ZinvYields['Nmu']['vv'])/
                                              (ZinvYields['Zpeak']['dy'] + ZinvYields['Zpeak']['tt'] + ZinvYields['Zpeak']['vv']))

   if ZinvRatios['prob_mu_MC'].val:
      ZinvRatios['prob_mu_dataMC'] = ZinvRatios['prob_mu_data']/ZinvRatios['prob_mu_MC']
   else:
      ZinvRatios['prob_mu_dataMC'] = u_float.u_float(0,0)

   #double ratios
   ZinvRatios['ratio_el'] = (ZinvRatios['Zpeak_dataMC']*ZinvRatios['prob_el_dataMC'])
   ZinvRatios['ratio_mu'] = (ZinvRatios['Zpeak_dataMC']*ZinvRatios['prob_mu_dataMC'])

   #Pickle results 
   pickleFile1 = open("%s/ZinvYields%s_CT%s.pkl"%(savedir3,suffix1,CT2cut), "w")
   pickle.dump(ZinvYields, pickleFile1)
   pickleFile1.close()

   pickleFile2 = open("%s/ZinvRatios%s_CT%s.pkl"%(savedir3,suffix1,CT2cut), "w")
   pickle.dump(ZinvRatios, pickleFile2)
   pickleFile2.close()

   pickleFile3 = open("%s/rawZinvYields%s_CT%s.pkl"%(savedir3,suffix1,CT2cut), "w")
   pickle.dump(yields, pickleFile3)
   pickleFile3.close()

   if not os.path.isfile("%s/ZinvRatios%s.txt"%(savedir, suffix1)):
      outfile = open("%s/ZinvRatios%s.txt"%(savedir, suffix1), "w")
      outfile.write("Zinv Estimation Ratios using " + Zchannel + " channel\n")
      outfile.write("CT        Zpeak_data_MC           prob_el_data            prob_el_MC           prob_el_data_MC           prob_mu_data          prob_mu_MC          prob_mu_data_MC           Ratio_el          Ratio_mu\n")

   with open("%s/ZinvRatios%s.txt"%(savedir, suffix1), "a") as outfile:
      outfile.write(CT2cut.ljust(10) +\
      str(ZinvRatios['Zpeak_dataMC'].round(3)).ljust(23) +\
      str(ZinvRatios['prob_el_data'].round(4)).ljust(23) +\
      str(ZinvRatios['prob_el_MC'].round(4)).ljust(24) +\
      str(ZinvRatios['prob_el_dataMC'].round(3)).ljust(25) +\
      str(ZinvRatios['prob_mu_data'].round(4)).ljust(22) +\
      str(ZinvRatios['prob_mu_MC'].round(4)).ljust(22) +\
      str(ZinvRatios['prob_mu_dataMC'].round(3)).ljust(22) +\
      str(ZinvRatios['ratio_el'].round(3)).ljust(21) +\
      str(ZinvRatios['ratio_mu'].round(3)).ljust(21)+ "\n")

if plot:

   plotDict = {\
      "dimuon_mass":{'var':"dimuon_mass",                'bins':[50,5,255],      'decor':{'title':"Di-muon System Invariant Mass Distribution" ,     'x':"M_{#mu#mu} / GeV" ,                 'y':"Events", 'log':[0,logy,0]}},
      "dimuon_pt":{  'var':"dimuon_pt",                  'bins':[50,0,250],      'decor':{'title':"Di-muon System Transverse Momentum Distribution", 'x':"p_{T_{#mu#mu}} / GeV" ,             'y':"Events", 'log':[0,logy,0]}},
      "MET":{        'var':"met",                        'bins':[50,0,500],      'decor':{'title':"MET Distribution" ,                               'x':"Missing E_{T} / GeV" ,              'y':"Events", 'log':[0,logy,0]}},
      "MET2":{       'var':"met2",                       'bins':[50,0,500],      'decor':{'title':"Emulated MET Distribution" ,                      'x':"Emulated Missing E_{T} / GeV" ,     'y':"Events", 'log':[0,logy,0]}},
      "MET2_phi":{   'var':"met2_phi",                   'bins':[20,-3.15,3.15], 'decor':{'title':"Emulated MET Phi Distribution" ,                  'x':"Emulated MET Phi" ,                 'y':"Events", 'log':[0,logy,0]}},
      "HT":{         'var':"ht_basJet",                  'bins':[50,0,500],      'decor':{'title':"H_{{T}} Distribution",                            'x':"H_{T} / GeV" ,                      'y':"Events", 'log':[0,logy,0]}},
      "nJets30":{    'var':"nBasJet",                    'bins':[10,0,10],       'decor':{'title':"Number of Jets with p_{{T}} > 30GeV",             'x':"Number of Jets with p_{T} > 30GeV", 'y':"Events", 'log':[0,logy,0]}},
      "nJets60":{    'var':"nVetoJet",                   'bins':[10,0,10],       'decor':{'title':"Number of Jets with p_{{T}} > 60GeV",             'x':"Number of Jets with p_{T} > 60GeV", 'y':"Events", 'log':[0,logy,0]}},
      "ISRpt":{      'var':"Jet_pt[IndexJet_basJet[0]]", 'bins':[45,100,1000],   'decor':{'title':"Leading Jet p_{{T}}",                             'x':"ISR Jet p_{T}",                     'y':"Events", 'log':[0,logy,0]}},
   }

   plotDict2 = {\
      "elePt":{        'var':"LepAll_pt[IndexLepAll_el[0]]", 'bins':[10,5,30],  'decor':{'title': "Electron pT Distribution" ,          'x':"Electron p_{T} / GeV" ,          'y':"Events", 'log':[0,logy,0]}},
      "muPt":{         'var':"LepAll_pt[IndexLepAll_mu[2]]", 'bins':[10,5,30],  'decor':{'title': "Muon pT Distribution" ,              'x':"Muon p_{T} / GeV" ,              'y':"Events", 'log':[0,logy,0]}},
      "electron_mt_2":{'var':"electron_mt_2",                'bins':[10,0,100], 'decor':{'title': "Emulated Electron mT Distribution" , 'x':"Emulated Electron m_{T} / GeV" , 'y':"Events", 'log':[0,logy,0]}},
      "muon_mt_2":{    'var':"muon_mt_2",                    'bins':[10,0,100], 'decor':{'title': "Emulated Muon mT Distribution" ,     'x':"Emulated Muon m_{T} / GeV" ,     'y':"Events", 'log':[0,logy,0]}},
   }

   plotsList = ["dimuon_mass", "dimuon_pt", "MET", "MET2", "MET2_phi", "HT", "nJets30", "nJets60", "ISRpt"]
   
   plotsDict = Plots(**plotDict)
   plotsDict2 = Plots(**plotDict2)
   
   if beforeEmul:
      #setEventListToChains(samples, samplesList, dimuon)
      dimuonPlots = getPlots(samples, plotsDict, dimuon, samplesList, plotList = plotsList, addOverFlowBin='upper')
      dimuonPlots2 = drawPlots(samples, plotsDict, dimuon, samplesList, plotList = plotsList, plotLimits = [10, 100], denoms=["bkg"], noms = ["d1muBlind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 0.01, normalize = False, save=False)
 
   if afterEmul:
      #setEventListToChains(samples, samplesList, emulated)
      emulatedPlots = getPlots(samples, plotsDict, emulated, samplesList, plotList = plotsList, addOverFlowBin='upper')
      emulatedPlots2 = drawPlots(samples, plotsDict, emulated, samplesList, plotList = plotsList, plotLimits = [10, 100], denoms=["bkg"], noms = ["d1muBlind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 0.01, normalize = False, save=False)
   
   if leptons:
      #setEventListToChains(samples, samplesList, electrons)
      elePlots = getPlots(samples, plotsDict2, electrons, samplesList, plotList = ["elePt", "electron_mt_2"], addOverFlowBin='upper')
      elePlots2 = drawPlots(samples, plotsDict2, electrons, samplesList, plotList = ["elePt", "electron_mt_2"], plotLimits = [10, 100], denoms=["bkg"], noms = ["d1muBlind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 0.01, normalize = False, save=False)
      
      #setEventListToChains(samples, samplesList, muons)
      muPlots = getPlots(samples, plotsDict2, muons, samplesList, plotList = ["muPt", "muon_mt_2"], addOverFlowBin='upper')
      muPlots2 = drawPlots(samples, plotsDict2, muons, samplesList, plotList = ["muPt", "muon_mt_2"], plotLimits = [10, 100], denoms=["bkg"], noms = ["d1muBlind"], fom="RATIO", fomLimits=[0,1.8], plotMin = 0.01, normalize = False, save=False)
   
   #Save canvas
   if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
      if beforeEmul:
         for canv in dimuonPlots2['canvs']:
            #if plot['canvs'][canv][0]:
            dimuonPlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir1, canv, suffix1))
            dimuonPlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir1, canv, suffix1))
            dimuonPlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir1, canv, suffix1))
      if afterEmul:   
         for canv in emulatedPlots2['canvs']:
            #if plot['canvs'][canv][0]:
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix2))
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix2))
            emulatedPlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix2))
      if leptons:   
         for canv in elePlots2['canvs']:
            #if plot['canvs'][canv][0]:
            elePlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix2))
            elePlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix2))
            elePlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix2))
         for canv in muPlots2['canvs']:
            #if plot['canvs'][canv][0]:
            muPlots2['canvs'][canv][0].SaveAs("%s/%s%s.png"%(savedir2, canv, suffix2))
            muPlots2['canvs'][canv][0].SaveAs("%s/root/%s%s.root"%(savedir2, canv, suffix2))
            muPlots2['canvs'][canv][0].SaveAs("%s/pdf/%s%s.pdf"%(savedir2, canv, suffix2))
