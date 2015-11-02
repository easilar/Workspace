import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from rCShelpers import *
import math
from Workspace.HEPHYPythonTools.user import username
from Workspace.RA4Analysis.signalRegions import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gStyle.SetOptStat(0)

cWJets  = getChain(WJetsHTToLNu_25ns,histname='')
cTTJets = getChain(TTJets_HTLO_25ns,histname='')
cBkg = getChain([WJetsHTToLNu_25ns,TTJets_HTLO_25ns,singleTop_25ns,TTV_25ns,DY_25ns],histname='')#no QCD
cData = getChain([data_mu_25ns , data_ele_25ns] , histname='')

def getRCS(c, cut, dPhiCut):
  h = getPlotFromChain(c, "deltaPhi_Wl", [0,dPhiCut,pi], cutString=cut, binningIsExplicit=True)
  if h.GetBinContent(1)>0 and h.GetBinContent(2)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
    rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
    del h
    return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
  del h

lumi = 3
weights = [
{'var':'weight','label':'original'},\
]
diLep = "((ngenLep+ngenTau)==2)"
prefix = 'singleLeptonic_Spring15_'
path = '/data/'+username+'/Spring15/25ns/rCS_0b_'+str(lumi)+'_CBID/'+weights[0]['label']+'/'
presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&Jet_pt[1]>80"
data_presel = "singleLeptonic&&nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0&&((HLT_EleHT350)||(HLT_MuHT350))&&Jet_pt[1]>80" 
btagString = 'nBJetMediumCSV30'
weight_str, weight_err_str = makeWeight(lumi, sampleLumi=3.)
lepSel = 'hard'
btagVarString = 'nBJetMediumCSV30'


###### data rCS plots ######
nJet = (4,5)
nbtag = [(1,1),(2,2)]
ht = 500
sideBand3fb =     {(4, 5): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},
                            (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},
                            (450, -1):  {(ht, -1):   {'deltaPhi': 0.75}}}}
bin = {}
for srNJet in sideBand3fb:
  bin[srNJet]={}
  for stb in sideBand3fb[srNJet]:
    bin[srNJet][stb] = {}
    for htb in sideBand3fb[srNJet][stb]:
      bin[srNJet][stb][htb] = {}
      deltaPhiCut = sideBand3fb[srNJet][stb][htb]['deltaPhi']
      rCS_Name_1b, rCS_Cut_1b = nameAndCut(stb, htb, srNJet, btb=(1,1), presel=data_presel, btagVar = btagVarString)
      rCS_Name_2b, rCS_Cut_2b = nameAndCut(stb, htb, srNJet, btb=(2,2), presel=data_presel, btagVar = btagVarString)
      print rCS_Name_1b
      print rCS_Name_2b
      rCS_1b = getRCS(cData, rCS_Cut_1b,  deltaPhiCut)
      rCS_2b = getRCS(cData, rCS_Cut_2b,  deltaPhiCut)
      print "rCS 1b :" , rCS_1b['rCS'] ,"+-" ,rCS_1b['rCSE_sim']
      print "rCS 2b :" , rCS_2b['rCS'] ,"+-" ,rCS_2b['rCSE_sim']
      print "rCS 2b/1b : " , rCS_2b['rCS'] / rCS_1b['rCS']
      bin[srNJet][stb][htb]['rCS_1b'] = rCS_1b
      bin[srNJet][stb][htb]['rCS_2b'] = rCS_2b
      bin[srNJet][stb][htb]['rCS_1b']['label'] = nBTagBinName((1,1))
      bin[srNJet][stb][htb]['rCS_2b']['label'] = nBTagBinName((2,2))
print bin
cb = ROOT.TCanvas("cb","cb",800,800)
cb.cd()
##cb.SetGrid()
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(11)
leg = ROOT.TLegend(0.55,0.65,0.95,0.75)
leg.SetBorderSize(1)
ROOT.gStyle.SetHistMinimumZero()
h0 = ROOT.TH1F("h0","h0",2,0,2)
h1 = ROOT.TH1F("h1","h1",2,0,2)
h2 = ROOT.TH1F("h2","h2",2,0,2)
h0.SetMarkerColor(ROOT.kRed)
h0.SetLineColor(ROOT.kRed)
h0.SetLineWidth(3)
h1.SetMarkerColor(ROOT.kBlue)
h1.SetLineColor(ROOT.kBlue)
h2.SetMarkerColor(ROOT.kBlack)
h2.SetLineColor(ROOT.kBlack)
#h0b.SetMaximum(0.2)
h0.SetMaximum(0.2)
h1.SetMaximum(0.2)
h2.SetMaximum(0.2)
for i , tag in enumerate(('_1b','_2b')):
    h0.SetBinContent(i+1,         bin[nJet][(250,350)][(ht,-1)]['rCS'+tag]['rCS'])
    h0.SetBinError(i+1,           bin[nJet][(250,350)][(ht,-1)]['rCS'+tag]['rCSE_sim'])
    h0.GetXaxis().SetBinLabel(i+1,bin[nJet][(250,350)][(ht,-1)]['rCS'+tag]['label'])
    h1.SetBinContent(i+1,         bin[nJet][(350,450)][(ht,-1)]['rCS'+tag]['rCS'])
    h1.SetBinError(i+1,           bin[nJet][(350,450)][(ht,-1)]['rCS'+tag]['rCSE_sim'])
    h1.GetXaxis().SetBinLabel(i+1,bin[nJet][(350,450)][(ht,-1)]['rCS'+tag]['label'])
    h2.SetBinContent(i+1,         bin[nJet][(450,-1)][(ht,-1)]['rCS'+tag]['rCS'])
    h2.SetBinError(i+1,           bin[nJet][(450,-1)][(ht,-1)]['rCS'+tag]['rCSE_sim'])
    h2.GetXaxis().SetBinLabel(i+1,bin[nJet][(450,-1)][(ht,-1)]['rCS'+tag]['label'])
h0.GetYaxis().SetTitle("R_{CS}")
h1.GetYaxis().SetTitle("R_{CS}")
h2.GetYaxis().SetTitle("R_{CS}")
h0.Draw("EH1")
h1.Draw("EH1 same")
h2.Draw("EH1 same")
leg.AddEntry(h0, "250 #leq L_{T} #leq350" ,"l")
leg.AddEntry(h1, "350 #leq L_{T} #leq450" ,"l")
leg.AddEntry(h2, "450 #leq L_{T}" ,"l")
leg.SetFillColor(0)
leg.SetLineColor(0)
leg.Draw()
latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Pleriminary}")
latex.DrawLatex(0.68,0.958,"#bf{L=1.26 fb^{-1} (13 TeV)}")
latex.DrawLatex(0.6,0.9,"H_{T}>"+str(ht))
latex.DrawLatex(0.6,0.85,"4 #leq N_{Jets} #leq5" )
#latex.DrawLatex(0.6,0.8,"Run 2015D")
#latex.DrawLatex(0.3,0.8,"Semi Lepton")
cb.Draw()
cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cBkg_rCS_HT'+str(ht)+'.png')
cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cBkg_rCS_HT'+str(ht)+'.pdf')
cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/cBkg_rCS_HT'+str(ht)+'.root')



###### WJets rCS Plots ##### 

#ht = 1000
#signalRegion3fb = {(3, 3): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (450, -1):  {(ht, -1):    {'deltaPhi': 0.75}}},\
#                   (4, 4): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (450, -1):  {(ht, -1):    {'deltaPhi': 0.75}}},\
#                   (5, 5): {(250, 350): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (350, 450): {(ht, -1):   {'deltaPhi': 1.0}},\
#                            (450, -1):  {(ht, -1):    {'deltaPhi': 1.0}}},\
#                   (6, 7): {(250, 350): {(ht, -1):  {'deltaPhi': 1.0}},\
#                            (350, 450): {(ht, -1):  {'deltaPhi': 1.0}},\
#                            (450, -1):  {(ht, -1):   {'deltaPhi': 0.75}}},
#                   (8, -1): {(250, 350):{(ht, -1): {'deltaPhi': 1.0}},
#                             (350, 450):{(ht, -1):  {'deltaPhi': 0.75}},
#                             (450, -1): {(ht, -1):   {'deltaPhi': 0.75}}}}
#
#bin = {}
#signalRegions = signalRegion3fb
#for srNJet in signalRegions:
#  bin[srNJet]={}
#  for stb in signalRegions[srNJet]:
#    bin[srNJet][stb] = {}
#    for htb in signalRegions[srNJet][stb]:
#      bin[srNJet][stb][htb] = {}
#      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
#      rCS_Name , rCS_Cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel=presel, btagVar = btagVarString)
#      print rCS_Name
#      rCS = getRCS(cWJets, rCS_Cut ,  deltaPhiCut)
#      print "rCS 0b from function:" , rCS['rCS'] , rCS['rCSE_sim']
#      bin[srNJet][stb][htb]['rCS'] = rCS
#      bin[srNJet][stb][htb]['label'] = nJetBinName(srNJet)
#
#print bin
#cb = ROOT.TCanvas("cb","cb",800,800)
#cb.cd()
###cb.SetGrid()
#latex = ROOT.TLatex()
#latex.SetNDC()
#latex.SetTextSize(0.04)
#latex.SetTextAlign(11)
#leg = ROOT.TLegend(0.6,0.7,0.95,0.8)
#leg.SetBorderSize(1)
#ROOT.gStyle.SetHistMinimumZero()
#h0 = ROOT.TH1F("h0","h0",5,0,5)
#h1 = ROOT.TH1F("h1","h1",5,0,5)
#h2 = ROOT.TH1F("h2","h2",5,0,5)
#h0.SetMarkerColor(ROOT.kRed)
#h0.SetLineColor(ROOT.kRed)
#h1.SetMarkerColor(ROOT.kBlue)
#h1.SetLineColor(ROOT.kBlue)
#h2.SetMarkerColor(ROOT.kBlack)
#h2.SetLineColor(ROOT.kBlack)
##h0b.SetMaximum(0.2)
#h0.SetMaximum(0.1)
#h1.SetMaximum(0.1)
#h2.SetMaximum(0.1)
#for i , srNJet in enumerate(sorted(bin)):
#    h0.SetBinContent(i+1,         bin[srNJet][(250,350)][(ht,-1)]['rCS']['rCS'])
#    h0.SetBinError(i+1,           bin[srNJet][(250,350)][(ht,-1)]['rCS']['rCSE_sim'])
#    h0.GetXaxis().SetBinLabel(i+1,bin[srNJet][(250,350)][(ht,-1)]['label'])
#    h1.SetBinContent(i+1,         bin[srNJet][(350,450)][(ht,-1)]['rCS']['rCS'])
#    h1.SetBinError(i+1,           bin[srNJet][(350,450)][(ht,-1)]['rCS']['rCSE_sim'])
#    h1.GetXaxis().SetBinLabel(i+1,bin[srNJet][(350,450)][(ht,-1)]['label'])
#    h2.SetBinContent(i+1,         bin[srNJet][(450,-1)][(ht,-1)]['rCS']['rCS'])
#    h2.SetBinError(i+1,           bin[srNJet][(450,-1)][(ht,-1)]['rCS']['rCSE_sim'])
#    h2.GetXaxis().SetBinLabel(i+1,bin[srNJet][(450,-1)][(ht,-1)]['label'])
#
#h0.GetYaxis().SetTitle("R_{CS}")
#h1.GetYaxis().SetTitle("R_{CS}")
#h2.GetYaxis().SetTitle("R_{CS}")
#h0.Draw("EH1")
#h1.Draw("EH1 same")
#h2.Draw("EH1 same")
#leg.AddEntry(h0, "250 #leq L_{T} #leq350" ,"l")
#leg.AddEntry(h1, "350 #leq L_{T} #leq450" ,"l")
#leg.AddEntry(h2, "450 #leq L_{T}" ,"l")
#leg.SetFillColor(0)
#leg.SetLineColor(0)
#leg.Draw()
#latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
#latex.DrawLatex(0.68,0.958,"#bf{L=3 fb^{-1} (13 TeV)}")
#latex.DrawLatex(0.6,0.9,"H_{T}>"+str(ht))
#latex.DrawLatex(0.6,0.85,"W+Jets")
##latex.DrawLatex(0.3,0.8,"Semi Lepton")
#cb.Draw()
#cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/WJets_rCS_HT'+str(ht)+'.png')
#cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/WJets_rCS_HT'+str(ht)+'.pdf')
#cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/WJets_rCS_HT'+str(ht)+'.root')

#####TTJets RCS Plots######

#signalRegion3fb = {(5, 5): {(350, 450): {(500, -1):   {'deltaPhi': 1.0}}}}
#                         #   (350, 450): {(500, -1):   {'deltaPhi': 1.0}}}}

##bin = {}
##signalRegions = signalRegion3fb
##for srNJet in signalRegions:
##  for stb in signalRegions[srNJet]:
##    bin[stb] = {}
##    for htb in signalRegions[srNJet][stb]:
##      bin[stb][htb] = {}
##      deltaPhiCut = signalRegions[srNJet][stb][htb]['deltaPhi']
##      for crNJet in [(3,3),(4,4),(5,5),(6,7),(8,-1)]:
##        deltaPhiCut = 1
##        rCS_crLowNJet_Name_1b, rCS_crLowNJet_Cut_1b = nameAndCut(stb, htb, crNJet, btb=(1,1), presel=presel, btagVar = btagVarString)
##        rCS_crLowNJet_Name_0b, rCS_crLowNJet_Cut_0b = nameAndCut(stb, htb, crNJet, btb=(0,0), presel=presel, btagVar = btagVarString)
##        print rCS_crLowNJet_Name_1b
##        rCS_1b = getRCS(cTTJets, rCS_crLowNJet_Cut_1b,  deltaPhiCut)
##        rCS_0b = getRCS(cTTJets, rCS_crLowNJet_Cut_0b,  deltaPhiCut)
##        print "rCS 1b from function:" , rCS_1b['rCS'] , rCS_1b['rCSE_sim']
##        print "rCS 0b from function:" , rCS_0b['rCS'] , rCS_0b['rCSE_sim']
##        bin[stb][htb][crNJet] = {\
##        'label':  nJetBinName(crNJet),\
##        '1b_value': rCS_1b['rCS'],\
##        '1b_error': rCS_1b['rCSE_sim'],\
##        '0b_value': rCS_0b['rCS'],\
##        '0b_error': rCS_0b['rCSE_sim'],\
##        }
##
##print bin
##njet_dict = bin[(350, 450)][(500, -1)]
##cb = ROOT.TCanvas("cb","cb",800,800)
##cb.cd()
####cb.SetGrid()
##latex = ROOT.TLatex()
##latex.SetNDC()
##latex.SetTextSize(0.04)
##latex.SetTextAlign(11)
##leg = ROOT.TLegend(0.6,0.7,0.95,0.8)
##leg.SetBorderSize(1)
##ROOT.gStyle.SetHistMinimumZero()
##h1b = ROOT.TH1F("h1b","h1b",5,0,5)
##h1b.SetMarkerColor(ROOT.kBlue) 
##h1b.SetLineColor(ROOT.kBlue) 
##h1b.SetBarWidth(1)
##h1b.SetBarOffset(0)
##h1b.SetStats(0)
##h1b.SetMinimum(0) 
###h1b.SetMaximum(0.2) 
##h1b.SetMaximum(0.05) 
##for i , crNJet in enumerate([(3,3),(4,4),(5,5),(6,7),(8,-1)]):
##    h1b.SetBinContent(i+1, njet_dict[crNJet]['1b_value']) 
##    h1b.SetBinError(i+1, njet_dict[crNJet]['1b_error']) 
###   h1b.SetBinContent(i+1, d_35_0[i])
##    h1b.GetXaxis().SetBinLabel(i+1,njet_dict[crNJet]['label'])
##leg.AddEntry(h1b, "n_{b_tag} = 1" ,"l") 
##h1b.GetYaxis().SetTitle("R_{CS}")
##h1b.Draw("EH1")
##h0b = ROOT.TH1F("h0b","h0b",5,0,5)
##h0b.SetMarkerColor(ROOT.kRed)
##h0b.SetLineColor(ROOT.kRed)  
##h0b.SetBarWidth(1)
##h0b.SetBarOffset(0)
##h0b.SetStats(0)
##h0b.SetMinimum(0)
###h0b.SetMaximum(0.2)
##h0b.SetMaximum(0.05)
##for i , crNJet in enumerate([(3,3),(4,4),(5,5),(6,7),(8,-1)]):
##    h0b.SetBinContent(i+1, njet_dict[crNJet]['0b_value'])
##    h0b.SetBinError(i+1, njet_dict[crNJet]['0b_error'])
###   h0b.SetBinContent(i+1, d_35_0[i])
##    h0b.GetXaxis().SetBinLabel(i+1,njet_dict[crNJet]['label'])
##leg.AddEntry(h0b, "n_{b_tag} = 0" ,"l")
##h0b.GetYaxis().SetTitle("R_{CS}")
##h0b.Draw("EH1 same")
##leg.SetFillColor(0)
##leg.SetLineColor(0)
##leg.Draw()
##latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Simulation}")
##latex.DrawLatex(0.68,0.958,"#bf{L=3 fb^{-1} (13 TeV)}")
##latex.DrawLatex(0.6,0.9,"H_{T}>500")
##latex.DrawLatex(0.6,0.85,"350<=L_{T}<=450")
##latex.DrawLatex(0.3,0.85,"tt+Jets")
##latex.DrawLatex(0.3,0.8,"Semi Lepton")
##cb.Draw()
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/ttJets_rCS_LT350450_HT500.png')
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/ttJets_rCS_LT350450_HT500.pdf')
##cb.SaveAs('~/www/Spring15/25ns/rCS_Plots/ttJets_rCS_LT350450_HT500.root')


