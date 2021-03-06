import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)
#lumi = 2250##pb
#path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p3fb/diLep_syst_study_results/"
#path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p25fb/diLep_syst_study_results/"
path = "/afs/hephy.at/user/e/easilar/www/data/Run2016B/4fb/diLep_syst_study_results/"
#path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p25fb/diLep_syst_study_results_nJet_Fix/"
#data_mean = pickle.load(file('/data/easilar/Spring15/25ns/data_mean_25Feb_0p75_pkl'))
data_mean = pickle.load(file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/data_mean_4fb_0b_pkl'))
#SR = signalRegion3fb
SR = {(3,-1):{(250,-1):{(500,-1):{"deltaPhi":1}}}}

btagVarString = 'nBJetMediumCSV30'
p = {'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':False , 'var':'nJet30','varname':'nJet30', 'binlabel':1,  'bin':(6,4,9)}

bin = {}
for srNJet in sorted(SR):
  bin[srNJet]={}
  for stb in sorted(SR[srNJet]):
    bin[srNJet][stb] = {}
    for htb in sorted(SR[srNJet][stb]):
      bin[srNJet][stb][htb] = {}
      Name, bla_Cut = nameAndCut(stb, htb, srNJet, btb=(0,0), presel="(1)", btagVar =  btagVarString)
      print Name
      fratio_diLep = ROOT.TFile(path+'st250_ht500_njet3_nbtagEq0_nJet30_allWeights_diLep_Ratio_eq0b.root')
      fratio_oneLep = ROOT.TFile(path+'st250_ht500_njet3_nbtagEq0_nJet30_eq0b_Ratio.root')
      cb = ROOT.TCanvas("cb","cb",800,800)
      cb.cd()
      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextSize(0.04)
      latex.SetTextAlign(11) 
      hint1 = ROOT.TH1F("hint1", "1 sigma", 100, 3, 9)
      hint2 = ROOT.TH1F("hint2", "2 sigma", 100, 3, 9)
      hint1.SetMarkerSize(0)
      hint2.SetMarkerSize(0)
      h_ratio_diLep = fratio_diLep.Get("h_ratio")
      h_ratio_oneLep = fratio_oneLep.Get("h_ratio")
      h_double_ratio = h_ratio_diLep.Clone("h_double_ratio")
      h_double_ratio.Divide(h_ratio_oneLep)
      h_double_ratio.GetXaxis().SetLabelSize(0.05)
      h_double_ratio.GetYaxis().SetLabelSize(0.05)
      h_double_ratio.GetYaxis().SetTitleSize(0.05)
      h_double_ratio.Sumw2()
      h_double_ratio.Draw()
      bin[srNJet][stb][htb]["nJetMean"] = data_mean[srNJet][stb][htb]["data_mean"]
      func = ROOT.TF1("my","[0] + [1] * (x-"+str(format(bin[srNJet][stb][htb]["nJetMean"],'.3f'))+")",3,9)
      h_double_ratio.Fit(func)
      FitFunc     = h_double_ratio.GetFunction('my')
      latex.DrawLatex(0.6,0.85,"Fit:")
      latex.DrawLatex(0.6,0.8,"Constant:"+str(format(FitFunc.GetParameter(0),'.3f'))+"+-"+str(format(FitFunc.GetParError(0),'.3f')))
      latex.DrawLatex(0.6,0.75,"Slope:"+str(format(FitFunc.GetParameter(1),'.3f'))+"+-"+str(format(FitFunc.GetParError(1),'.3f')))
      #latex.DrawLatex(0.6,0.7, "mean:"+str(format(h_ratio3.GetMean(),'.3f')))
      latex.DrawLatex(0.2,0.85,"(nJet+add lost)/(nJet)")
      bin[srNJet][stb][htb]["constant"] = sqrt(abs(1-FitFunc.GetParameter(0))**2+abs(FitFunc.GetParError(0))**2)
      bin[srNJet][stb][htb]["slope"] = sqrt(abs(0-abs(FitFunc.GetParameter(1)))**2+abs(FitFunc.GetParError(1))**2)
      print "mean:" , bin[srNJet][stb][htb]["nJetMean"]
      print "constant",abs(1-FitFunc.GetParameter(0)) ,"error", abs(FitFunc.GetParError(0)),"quad sum of constant:" , bin[srNJet][stb][htb]["constant"]
      print "slope",abs(0-abs(FitFunc.GetParameter(1))) ,"error", abs(FitFunc.GetParError(1)),"quad sum of constant:" , bin[srNJet][stb][htb]["slope"]
      ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint1, 0.68)
      ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(hint2, 0.95)
      hint1.SetFillColorAlpha(ROOT.kGreen, 0.45)
      hint2.SetFillColorAlpha(ROOT.kYellow, 0.45)
      hint2.Draw("e3 same")
      hint1.Draw("e3 same")
      h_double_ratio.Draw("same")
      cb.SaveAs(path+Name+'_'+p['varname']+'_double_Ratio_1b.root')
      cb.SaveAs(path+Name+'_'+p['varname']+'_double_Ratio_1b.png')
      cb.SaveAs(path+Name+'_'+p['varname']+'_double_Ratio_1b.pdf')
      #for f_ratio in [{'name':'diLep' , 'file':fratio_diLep} , {'name':'oneLep' , 'file':fratio_oneLep}]:
      #  cb = ROOT.TCanvas("cb","cb",800,800)
      #  cb.cd()
      #  latex = ROOT.TLatex()
      #  latex.SetNDC()
      #  latex.SetTextSize(0.04)
      #  latex.SetTextAlign(11)
      #  h_ratio = f_ratio['file'].Get("h_ratio")
      #  h_ratio.GetXaxis().SetLabelSize(0.1)
      #  h_ratio.GetXaxis().SetLabelSize(0.05)
      #  h_ratio.GetYaxis().SetLabelSize(0.05)
      #  h_ratio.GetYaxis().SetTitleSize(0.1)
      #  h_ratio.GetYaxis().SetTitleSize(0.05)
      #  h_ratio.GetXaxis().SetTitle("nJets")
      #  h_ratio.GetYaxis().SetNdivisions(510)
      #  h_ratio.Draw()
      #  func = ROOT.TF1("my","[0] + [1] * (x-"+str(format(h_ratio.GetMean(),'.3f'))+")",4,9)
      #  h_ratio.Fit('my')
      #  FitFunc     = h_ratio.GetFunction('my')
      #  latex.DrawLatex(0.6,0.85,"Fit:")
      #  latex.DrawLatex(0.6,0.8,"Constant:"+str(format(FitFunc.GetParameter(0),'.3f'))+"+-"+str(format(FitFunc.GetParError(0),'.3f')))
      #  latex.DrawLatex(0.6,0.75,"Slope:"+str(format(FitFunc.GetParameter(1),'.3f'))+"+-"+str(format(FitFunc.GetParError(1),'.3f')))
      #  latex.DrawLatex(0.6,0.7, "mean:"+str(format(h_ratio.GetMean(),'.3f')))
      #  latex.DrawLatex(0.3,0.85,"nJet")
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.root')
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.png')
      #  cb.SaveAs(path+Name+'_'+p['varname']+'_allWeights_'+f_ratio['name']+'_Ratio.pdf')



pickle.dump(bin,file('/data/easilar/Results2016/ICHEP/DiLep_SYS/V1/DL_syst_eq0b_V2_pkl','w'))
