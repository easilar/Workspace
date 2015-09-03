import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
#from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
from Workspace.RA4Analysis.cmgTuples_Data50ns_1l import *
from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *

from cutFlow_helper import *
from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

lumi = 42   ##pb
#weight_str = '((xsec*genWeight)*'+str(lumi)+')'  ##for bkg
lepSels = [
#  {'cut':OneMu , 'veto':OneMu_lepveto, 'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '(HLT_MuHT350MET70 || HLT_Mu50NoIso)'},\
#  {'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '(HLT_EleHT350MET70 || HLT_ElNoIso)'},\
  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350MET70 || HLT_ElNoIso)||(HLT_MuHT350MET70 || HLT_Mu50NoIso))' }\
]
lepSel = lepSels[0]

#path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/"+lepSel['cut'].split('&&')[0]+"/"
#path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/SingleLeptonic_only_promt_zerob/"
#path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/SingleMuonic/"
path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/SingleLeptonic_only_promt_0b/"
if not os.path.exists(path):
  os.makedirs(path)

cut =   {\
#'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters]),\
'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,filters,nbjets_30_cut_zero]),\
#'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80]),\
#,ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters,jets_2_80]),\
'bkgcut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero]),\
#,ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,jets_2_80]),\
'label':'0 b-jets (CSVv2)'}


#samples=[
#  {"sample":"data_mu" ,   "list":data_mu , "tex":"Single_Muon","color":ROOT.kBlack},
#  {"sample":"data_mu_17July" ,   "list":data_mu_17July , "tex":"Single_Muon_17Jul","color":ROOT.kBlack},
#  {"sample":"data_ele",   "list":data_ele, "tex":"Single_Electron", "color":ROOT.kBlack},\
#  {"sample":"data_ele_17July",   "list":data_ele_17July, "tex":"data", "color":ROOT.kBlack}
#]

samples=[
  {"cut":"run>=251643","sample":"data_mu" ,          "list":SingleMuon_Run2015B_PromptReco, "tex":"Single_Muon","color":ROOT.kBlack},
#  {"cut":"run<=251562","sample":"data_mu_17July" ,   "list":SingleMuon_Run2015B_17Jul2015, "tex":"Single_Muon_17Jul","color":ROOT.kBlack},
  {"cut":"run>=251643","sample":"data_ele",          "list":SingleElectron_Run2015B_PromptReco, "tex":"Single_Electron", "color":ROOT.kBlack},\
#  {"cut":"run<=251562","sample":"data_ele_17July",   "list":SingleElectron_Run2015B_17Jul2015, "tex":"data", "color":ROOT.kBlack}
]

for s in samples:
    s['chunk'] , s['norm']  = getChunks(s['list'],maxN=maxN)
    #chain = ROOT.TChain('tree')
    #chain.Add(s['chunk'][0]["file"])
    #s["cpTree"] = chain.CopyTree(s['cut']+'&&'+cut['cut'])  
    #print s["cpTree"].GetEntries()
    print s['chunk']
    print s['norm']

data_chunks = [s['chunk'][0] for s in samples ]
data_chain = getChain(data_chunks,maxN=maxN,histname="",treeName="tree")
print data_chain.GetEntries()
y_data = getYieldFromChain(data_chain, cutString = "(1)", weight = "(1)", returnError=False)
print y_data
cp_data = data_chain.CopyTree(cut['cut'])
print "data cp created with cut :" , cut['cut']

bkg_samples=[
{"sample":"DY",           "name":DY_50ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"singleTop",    "name":singleTop_50ns,"tex":"single top",'color': ROOT.kViolet+5},
{"sample":"QCD",          "name":QCD_HT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"WJets",        "name":WJetsToLNu_50ns,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",       "name":TTJets_50ns, "tex":"ttbar + jets",'color':ROOT.kBlue-4},
]

print "Now this will be slow but It will done once !!!"
for bkg in bkg_samples:
  #bkg['chain'] = []
  #bkg['norm'] = []
  #bkg['chunks'].append(b_chunk[0])
  #bkg['norm'].append(b_norm) 
  bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events") 
  print "I am gonna copy tree now with the cut:" , cut['bkgcut']
  bkg['cpTree'] = bkg['chain'].CopyTree(cut['bkgcut'])
  print "copied....."
  #bkg['sumNorm'] = sum(bkg['norm'])
  #bkg['chain'] = getChain(bkg['chunks'],maxN=maxN,histname="",treeName="tree")
  #print "I am gonna copy tree now with the cut:" , cut['bkgcut']
  #bkg['cpTree'] = bkg['chain'].CopyTree(cut['bkgcut'])
  #print "copied....."

plots =[\
  {'ndiv':True,'yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':ht,                    'varname':'htJet30j',            'binlabel':50,  'bin':(50,0,2500)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':njets_30,                      'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':nbjets_30,           'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
  {'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':dPhi,                 'varname':'deltaPhi_Wl',       'binlabel':1,  'bin':(30,0,3.14)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'S_{T}','logy':'True' , 'var':  "(LepGood_pt[0]+met_pt)",                          'varname':'st',                  'binlabel':50,  'bin':(36,200,2000)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'Jet_pt[0]',  'binlabel':30,  'bin':(67,0,2010)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',                         'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}NoHF','logy':'True' , 'var':'metNoHF_pt',                         'varname':'metNoHF',         'binlabel':50,  'bin':(28,0,1400)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'LepGood_pt[0]',                 'varname':'leptonPt',      'binlabel':25,  'bin':(40,0,1000)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',                 'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',                 'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'#miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',                 'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
  {'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))',       'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)}
]

for p in plots:
  print "Plotting starts.."
  can = ROOT.TCanvas(p['varname'],p['varname'],800,800)
  can.cd()
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextSize(0.05)
  latex.SetTextAlign(11)
  leg = ROOT.TLegend(0.75,0.6,0.9,0.9)
  leg.SetBorderSize(1)
  Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
  Pad1.SetLogy()
  Pad1.SetTopMargin(0.06)
  Pad1.SetBottomMargin(0)
  Pad1.SetLeftMargin(0.16)
  Pad1.SetRightMargin(0.05)
  Pad1.Draw()
  Pad1.cd()
  h_Stack = ROOT.THStack('h_Stack',p['varname'])

  for bkg in bkg_samples:
    color = bkg['color']
    print color
    print bkg['sample']
    chain = bkg['cpTree']
    #weight_str = '((xsec*genWeight/3)*'+str(lumi)+')'
    #weight_str = '(('+str(MC_scale)+'*xsec*genWeight)*'+str(lumi)+')'
    #histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
    #histo = ROOT.TH1F(str(histo) ,str(histo),*p['bin'])
    #chain.Draw('('+p['var']+')>>'+str(histoname),weight_str+"*(1)")
    histo = getPlotFromChain(chain, p['var'], p['bin'], cutString = "(1)", weight = "weight*42/3000", binningIsExplicit=False, addOverFlowBin='')
    print histo
    #histo.Draw("Bar")
    histo.SetFillColor(color)
    histo.SetLineColor(ROOT.kBlack)
    histo.SetLineWidth(2)
    histo.GetXaxis().SetTitle(p['xaxis'])
    histo.SetTitle("")
    histo.GetYaxis().SetTitleSize(2)
    if p['ndiv']:
       histo.GetXaxis().SetNdivisions(505)
       histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
    if not p['ndiv']:
       histo.GetYaxis().SetTitle(p['yaxis'])
    h_Stack.Add(histo)
    leg.AddEntry(histo, bkg['tex'],"f")
  h_Stack.Draw("Bar")
  h_Stack.SetMaximum(500)
  h_Stack.SetMinimum(0.11)
  #h_Stack.GetYaxis().SetTitleSize(2)
  data =  cp_data
  color = ROOT.kBlack
  histo = 'h_data'
  histoname = histo
  print histoname
  #print p['bin'],p['lowlimit'],p['limit']
  histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'][0],p['bin'][1],p['bin'][2])
  data.Draw(p['var']+'>>'+str(histoname))
  print "pass draw : ) "
  histo.SetMarkerStyle(20)
  histo.SetMarkerSize(1.2)
  histo.SetLineColor(color)
  histo.GetXaxis().SetTitle(p['xaxis'])
  histo.SetTitle("")
  histo.GetYaxis().SetTitleSize(0.05)
  histo.GetYaxis().SetLabelSize(0.05)
  #h_Stack.Draw()
  histo.Draw("EP")
  histo.SetMaximum(500)
  histo.SetMinimum(0.11)
  h_Stack.Draw("HistoSame")
  histo.Draw("EPSame")
  #print "data Integral" , histo.Integral()
  #h_Stack.GetXaxis().SetTitle(p['xaxis'])
  if p['ndiv']:
    histo.GetXaxis().SetNdivisions(505)
    histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
  #  h_Stack.GetXaxis().SetNdivisions(505)
  #  h_Stack.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
  if not p['ndiv']:
    histo.GetYaxis().SetTitle(p['yaxis'])
  #  h_Stack.GetYaxis().SetTitle(p['yaxis'])
  stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
  stack_hist.Merge(h_Stack.GetHists())
  print "Integral of BKG:" , stack_hist.Integral()
  print "Integral of Data:" , histo.Integral()
  leg.AddEntry(histo, "data","PL")
  leg.SetFillColor(0)
  leg.Draw()
  latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
  latex.DrawLatex(0.74,0.958,"#bf{L=42 pb^{-1} (13 TeV)}")
  latex.DrawLatex(0.6,0.8,"#bf{H_{T}>500 GeV}")
  latex.DrawLatex(0.6,0.75,"#bf{L_{T}>250 GeV}")
  latex.DrawLatex(0.6,0.7,"#bf{N_{bjets}==0}")
  Pad1.RedrawAxis()
  can.cd()
  Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
  Pad2.SetTopMargin(0)
  Pad2.SetBottomMargin(0.5)
  Pad2.SetLeftMargin(0.16)
  Pad2.SetRightMargin(0.05)
  Pad2.Draw()
  Pad2.cd()
  Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
  Func.SetParameter(0,1)
  Func.SetLineColor(2)
  h_ratio = histo.Clone('h_ratio')
  h_ratio.SetMinimum(0.0)
  h_ratio.SetMaximum(2.9)
  h_ratio.Sumw2()
  h_ratio.SetStats(0)
  h_ratio.Divide(stack_hist)
  h_ratio.SetMarkerStyle(20)
  h_ratio.SetMarkerColor(ROOT.kBlack)
  h_ratio.SetTitle("")
  h_ratio.GetYaxis().SetTitle("Data/Pred. ")
  h_ratio.GetYaxis().SetTitleSize(0.1)
  h_ratio.GetXaxis().SetTitle(p['xaxis'])
  h_ratio.GetYaxis().SetTitleFont(42)
  h_ratio.GetYaxis().SetTitleOffset(0.6)
  h_ratio.GetXaxis().SetTitleOffset(1)
  h_ratio.GetYaxis().SetNdivisions(505)
  h_ratio.GetXaxis().SetTitleSize(0.2)
  h_ratio.GetXaxis().SetLabelSize(0.13)
  h_ratio.GetYaxis().SetLabelSize(0.1)
  h_ratio.Draw("E")
  #h_ratio.Draw()
  Func.Draw("same")
  #Func.Draw()
  can.Draw()
  can.SaveAs(path+p['varname']+'.png')
  can.SaveAs(path+p['varname']+'.pdf')
  can.SaveAs(path+p['varname']+'.root')
  del can
