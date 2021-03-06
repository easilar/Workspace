# deltaR_fakes.py
# Script to plot the deltaR and pT ratio distributions between generated and reconstructed electrons
# Author: Mateusz Zarucki

import ROOT
import os, sys
import argparse
import Workspace.DegenerateStopAnalysis.toolsMateusz.ROOToptions
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.pythonFunctions import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.eleWPs import *
from Workspace.DegenerateStopAnalysis.toolsMateusz.regions import *
from Workspace.DegenerateStopAnalysis.tools.degTools import *
from Workspace.DegenerateStopAnalysis.tools.getSamples_8012 import getSamples
from Workspace.DegenerateStopAnalysis.samples.cmgTuples_postProcessed.cmgTuplesPostProcessed_mAODv2_2016 import cmgTuplesPostProcessed
from array import array
from math import pi, sqrt #cos, sin, sinh, log

#Input options
parser = argparse.ArgumentParser(description="Input options")
parser.add_argument("--presel", dest="presel",  help="Add Preselection", type=int, default=1) # applies preselection
parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="tt")
parser.add_argument("--mvaWPs", dest="mvaWPs",  help="Add MVA WPs", type=int, default=1) # includes MVA WPs
parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
#parser.add_argument("--zoom", dest="zoom",  help="Toggle zoom", type=int, default=1)
#parser.add_argument("--id", dest="ID",  help="Electron ID type", type=str, default="standard") # "standard" "noIso" "iso"
#parser.add_argument("--iso", dest="iso",  help="Isolation", type=str, default="relIso03") #"relIso03" "relIso04" "miniRelIso" "relIsoAn04"
args = parser.parse_args()
if not len(sys.argv) > 1:
   print makeLine()
   print "No arguments given. Using default settings."
   print makeLine()
   #exit()

#Arguments 
sample = args.sample 
presel = args.presel 
mvaWPs = args.mvaWPs
save = args.save
#zoom = args.zoom
#ID = args.ID 
#if ID == "iso": isolation = args.iso
#nEles = "01" # 01,01tau,1,2 #Number of electrons in event

#Samples
privateSignals = ["s10FS", "s30", "s30FS", "s60FS", "t2tt30FS"]
backgrounds=["w","tt", "z","qcd"]

samplesList = backgrounds # + privateSignals

cmgPP = cmgTuplesPostProcessed()
samples = getSamples(cmgPP = cmgPP, skim = 'preIncLep', sampleList = samplesList, scan = False, useHT = True, getData = False)

officialSignals = ["s300_290", "s300_270", "s300_240"] #FIXME: crosscheck if these are in allOfficialSignals

allOfficialSignals = samples.massScanList()
#allOfficialSignals = [s for s in samples if samples[s]['isSignal'] and not samples[s]['isData'] and s not in privateSignals and s not in backgrounds] 
allSignals = privateSignals + allOfficialSignals
allSamples = allSignals + backgrounds

print makeLine()
print "Samples:"
newLine()
for s in sorted(samples.keys()):
   print samples[s].name,":",s
print makeLine()
if sample in samples.keys(): print "Using", samples[sample].name, "sample."
else:
   print "!!! Sample " + sample + " unavailable."
   sys.exit(0)
print makeLine()

#Write to file
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   tag = samples[samples.keys()[0]].dir.split('/')[7] + "/" + samples[samples.keys()[0]].dir.split('/')[8]
   savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/%s/electronID/fakes/deltaR"%tag
   
   makeDir(savedir + "/root")
   makeDir(savedir + "/pdf")

#Geometric divisions
ebSplit = 0.8 #barrel is split into two regions
ebeeSplit = 1.479 #division between barrel and endcap
#etaAcc = 2.5 #eta acceptance

#Pt division for MVA ID
ptSplit = 10 #we have above and below 10 GeV categories 

#DeltaR cut for matching
#deltaRcut = 0.3

#Bin size 
#nbins = 100
xmin = 0.0001
#xmax = 1000

#Selection criteria
#intLum = 10.0 #fb-1
weight = samples[sample].weight

#Gets all cuts (electron, SR, CR) for given electron ID
eleIDsel = electronIDs(ID = "standard", removedCut = "None", iso = False)
allCuts = cutClasses(eleIDsel, ID = "standard")

#Preselection
preSel1 = "(met_pt > 200)" #MET
preSel2 = "(Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 4.5 && Jet_id)) > 200)" #HT = Sum of Jets > 30GeV
preSel3 = "(Max$(Jet_pt*(abs(Jet_eta) < " + str(etaAcc) + ") > 100))" #ISR

if presel: preSel = preSel1 + "&&" + preSel2 + "&&" + preSel3
else: preSel = "1"

#single-lepton (semileptonic) events
#if nEles == "01":
#Generated electron selection
#nSel = "ngenLep == 1" 
genSel = "(abs(genLep_pdgId[0]) == 11 && abs(genLep_eta[0]) < " + str(etaAcc) + ")" #electron selection #index [0] ok since (only element)
#genSel = nSel + "&&" + genSel1

#Reconstructed electron selection
etaAcc = 1.4442

fakeEleSel = "(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel['Loose'] + " && LepAll_relIso03 < 0.2 && LepAll_miniRelIso < 0.1 && LepAll_mcMatchId == 0)"
#fakeEleSel2 = "abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + " && " + eleIDsel['Veto'] + " && LepAll_miniRelIso < 0.5 && LepAll_mcMatchId == 0"

fakeMt = "Max$(LepAll_mt*(" + fakeEleSel + "))"
fakePt = "Max$(LepAll_pt*(" + fakeEleSel + "))"
deltaR = "(sqrt((genLep_eta[0] - LepAll_eta)^2 + (genLep_phi[0] - LepAll_phi)^2)*" + fakeEleSel + ")" 
ptRatio = "((LepAll_pt/genLep_pt[0])*" + fakeEleSel + ")"
#deltaRjet = "Min$(sqrt((LepAll_eta[0] - Jet_eta)^2 + (LepAll_phi[0] - Jet_phi)^2))"

fakes = CutClass("fakes", [
   ["MET200","met > 200"],
   ["HT200","ht_basJet > 200"],
   ["dPhi(j1234, MET)>0.3", "Min$(acos(cos(Jet_phi - met_phi)) > 0.3)"],
   #["dPhi(j1234, MET)>0.3", "Min$(" + minAngle("Jet_phi", "met_phi") + " > 0.3)"],
   ["Jets>=1","nBasJet >= 1"], #nJet60
   ["fake", "Sum$(" + fakeEleSel + ") >= 1"],
   ["Mt>20", fakeMt + " > 20"],
   ["Pt<20", fakePt + " < 20"],
   #["anti-QCD2", "abs(mhtJet40 - met_pt)/met < 0.5"] #mhtJet40 not a vector
   #["BJets>=0","nSoftBJetsCSV >= 0 && nHardBJetsCSV >= 0"],
   ], baseCut = None) #allCuts['None']['presel'])

   #["AntiQCD", " (deltaPhi_j12 < 2.5)"], # monojet
   #["ISR110","nJet110 >= 1" ],
   #["TauElVeto","(Sum$(TauGood_idMVA) == 0) && (Sum$(abs(LepAll_pdgId) == 11 && abs(LepAll_eta) < " + str(etaAcc) + "&& LepAll_SPRING15_25ns_v1 == 1) == 0)"],
   #["1Mu-2ndMu20Veto", "(nlep==1 || (nlep ==2 && LepAll_pt[looseMuonIndex2] < 20) )"],
   #["No3rdJet60","nJet60 <= 2"],

##################################################################################Canvas 1#############################################################################################
c1 = ROOT.TCanvas("c1", "Canvas 1", 1200, 1200)
c1.Divide(1,2)

#Electron Cut IDs
hists = {'deltaR':{}, 'ptRatio':{}}#, 'deltaRjet':{}}

#IDs: 0 - none, 1 - veto (~95% eff), 2 - loose (~90% eff), 3 - medium (~80% eff), 4 - tight (~70% eff)
#WPs = ['Veto', 'Loose', 'Medium', 'Tight']

#cutSel = {}

#for i,iWP in enumerate(WPs):
#   cutSel[iWP] = "LepAll_SPRING15_25ns_v1 >= " + str(i+1)

variables = {'deltaR':deltaR, 'ptRatio':ptRatio}#, 'deltaRjet':deltaRjet} # 

for i,var in enumerate(variables.items()):
   c1.cd(i+1)
   
   if var[0] == 'deltaR':
      xmax = 7.0001
      nbins = 70
   elif var[0] == 'ptRatio':
      xmax = 2.0001
      nbins = 100
   #elif var[0] == 'deltaRjet':
   #   xmax = 7
   
   hists[var[0]]['None'] = makeHist(samples[sample].tree, var[1], weight + "*(" + genSel + "&&" + fakes.combined + ")", nbins, xmin, xmax)
   
   if var[0] == 'deltaR': 
      hists[var[0]]['None'].SetName("DeltaR")
      hists[var[0]]['None'].SetTitle("#DeltaR between Leading Generated Electron and Reconstructed Fake Electron (" + samples[sample].name + " Sample)")
      hists[var[0]]['None'].GetXaxis().SetTitle("#DeltaR of GenEle and RecoEle")
   
   elif var[0] == 'ptRatio':
      hists[var[0]]['None'].SetName("RatioPt")
      hists[var[0]]['None'].SetTitle("p_{T} Ratio of Reconstructed Fake Electron and Leading Generated Electron (" + samples[sample].name + " Sample)")
      hists[var[0]]['None'].GetXaxis().SetTitle("Reconstructed Electron p_{T} / Generated Electron p_{T}")
   
   #elif var[0] == 'deltaRjet':
   #   hists[var[0]]['None'].SetName("DeltaRjet")
   #   hists[var[0]]['None'].SetTitle("Minimum DeltaR between Electron and Jet Distributions for Various IDs (" + samples[sample].name + " Sample)")
   #   hists[var[0]]['None'].GetXaxis().SetTitle("Min(dR) of Electron and Jet")
   
   hists[var[0]]['None'].Draw("hist")
   
   #for iWP in WPs:
   #   hists[var[0]][iWP] = makeHist(samples[sample].tree, var[1], weight + "*(" + fakes.combined + "&&" + cutSel[iWP] + ")", nbins, xmin, xmax)
   #   hists[var[0]][iWP].SetName(var[0] + "_" + iWP)
   #   hists[var[0]][iWP].SetFillColor(0)
   #   hists[var[0]][iWP].Draw("histsame")
   
   #ROOT.gPad.SetLogy()
   
   alignStats(hists[var[0]]['None'])
   
   #Colours
   #hists[var[0]]['Veto'].SetLineColor(ROOT.kGreen+3)
   #hists[var[0]]['Loose'].SetLineColor(ROOT.kBlue+1)
   #hists[var[0]]['Medium'].SetLineColor(ROOT.kOrange-2)
   #hists[var[0]]['Tight'].SetLineColor(ROOT.kRed+1)
   
   ROOT.gPad.Modified()
   ROOT.gPad.Update()
   
   #l1.Draw()

c1.Modified()
c1.Update()

#Save
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs(savedir + "/deltaR_%s.png"%(samples[sample].name))
   c1.SaveAs(savedir + "/pdf/deltaR_%s.pdf"%(samples[sample].name))
   c1.SaveAs(savedir + "/root/deltaR_%s.root"%(samples[sample].name))
