import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
#from Workspace.RA4Analysis.cmgTuples_Spring15_v2 import *
#from Workspace.RA4Analysis.cmgTuples_Data25ns_0l import *
from Workspace.RA4Analysis.cmgTuples_data_25ns_fromArtur import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_50ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed import *
##from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed  import *

from cutFlow_helper import *
from math import *
ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)

#lumi = 204.2  ##pb
#lumi = 133  ##pb
lumi =3000 ##fb
#weight_str = '((xsec*genWeight)*'+str(lumi)+')'  ##for bkg
lepSels = [
#######{'cut':OneMu , 'veto':OneMu_lepveto, 'chain': data_mu_25ns ,'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#########{'cut':OneMu ,'veto':OneMu_lepveto, 'chunk':SingleMuon_Run2015D_133 ,'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#####'sample' : [\
#####   {"sample":"data_mu",   "list":SingleMuon_Run2015D_v4     , "tex":"Single_Muon", "color":ROOT.kBlack},\
#####   {"sample":"data_mu",   "list":SingleMuon_Run2015D_05Oct  , "tex":"Single_Muon", "color":ROOT.kBlack},\
#####]\
#####},\
#####{'cut':OneE ,  'veto':OneE_lepveto, 'chain':data_ele_25ns ,'label':'_ele_','str':'1 $e$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
####{'cut':OneE ,  'veto':OneE_lepveto, 'chunk':SingleElectron_Run2015D_133 ,'label':'_ele_','str':'1 $e$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
######{'cut':OneE ,  'veto':OneE_lepveto,  'label':'_ele_','str':'1 $e$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))',\
######'sample' : [\
###### #  {"sample":"data_ele",   "list":SingleElectron_Run2015D_v4  , "tex":"Single_Electron", "color":ROOT.kBlack},\
###### #  {"sample":"data_ele",   "list":SingleElectron_Run2015D_05Oct  , "tex":"Single_Electron", "color":ROOT.kBlack},\
######]\
######},\
#   {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350MET70 || HLT_ElNoIso)||(HLT_MuHT350MET70 || HLT_Mu50NoIso))' }\
  #{'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_ElNoIso||HLT_EleHT350)||(HLT_MuHT350||HLT_Mu50NoIso))' }\
  {'cut':OneLep ,'veto':OneLep_lepveto,'label':'_lep_','str':'1 $lepton$', 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))' }\
]
#lepSel = lepSels[0]
for lepSel in lepSels:
  #path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/"+lepSel['cut'].split('&&')[0]+"/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/SingleLeptonic_only_promt_zerob/"
  ###path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/133pb/zeroB/"+lepSel['label']+"/"
  #######path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/1p2fb/fix/zeroB_0p5_CR/"+lepSel['label']+"/"
  ####path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/1p2fb/fix/1B_4_5jets_CR/"+lepSel['label']+"/"
  path = "/afs/hephy.at/user/e/easilar/www/MC/3fb/"+lepSel['label']+"/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/incB_Muonic_MCScaled/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/incB/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/25ns/4_Sep_2015_Json/SingleLeptonic_incb_MetNoHF_MCscaledtoData/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/25ns/4_Sep_2015_Json/SingleLeptonic_incb_MetNoHF_/"
  #path = "/afs/hephy.at/user/e/easilar/www/data/golden_Json/SingleLeptonic_only_promt_0b/"
  if not os.path.exists(path):
    os.makedirs(path)
  #daniels_cut = "Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)||(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.5&&LepGood_miniRelIso<0.1&&((abs(LepGood_eta)<0.8&&LepGood_mvaIdPhys14>0.73)||((abs(LepGood_eta)>=0.8&&abs(LepGood_eta)<1.44)&&LepGood_mvaIdPhys14>0.57)||((abs(LepGood_eta)>=1.57)&&LepGood_mvaIdPhys14>0.05))&&LepGood_lostHits==0&&LepGood_convVeto&&LepGood_sip3d<4.0))==1&&((abs(LepGood_pdgId)==11&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==0&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.5))==1))             ||(abs(LepGood_pdgId)==13&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==1&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.5))==0)))"
  cut =   {\
  #'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters]),\
  #'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,filters,nbjets_30_cut_zero]),\
  #'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,filters,nbjets_30_cut_zero]),\
  #########'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,lepSel['trigger'],"("+njets_30+">2&&"+njets_30+"<5)",jets_2_80,st,filters,nbjets_30+"==0",jets_2_80]),\
  ##########'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,lepSel['trigger'],"("+njets_30+">3&&"+njets_30+"<6)",jets_2_80,st,filters,nbjets_30+"==1",jets_2_80]),\
  #########'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lepSel['trigger'],"("+njets_30+">=5)",jets_2_80,st,filters,nbjets_30+"==0","("+dPhi+"<0.5)",jets_2_80]),\
  'cut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lepSel['trigger'],"("+njets_30+">=5)",jets_2_80,st,filters,nbjets_30+"==0",jets_2_80]),\
  #####'cut':"&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],ht_cut,st,njets_30_cut,jets_2_80,filters,nbjets_30_cut_multi]),\
  #'cut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,filters]),\
  #,ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,filters,jets_2_80]),\
  #######'bkgcut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,"("+njets_30+">2&&"+njets_30+"<5)",jets_2_80,st,nbjets_30+"==0",jets_2_80]),\
  ###########'bkgcut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],lep_hard,"("+njets_30+">3&&"+njets_30+"<6)",jets_2_80,st,nbjets_30+"==1",jets_2_80]),\
  #######'bkgcut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],"("+njets_30+">=5)",jets_2_80,st,nbjets_30+"==0","("+dPhi+"<0.5)",jets_2_80,]),\
  'bkgcut':"&&".join([ht_cut,lepSel['cut'],lepSel['veto'],"("+njets_30+">=5)",jets_2_80,st,nbjets_30+"==0",jets_2_80,]),\
  #####'bkgcut':"&&".join([lepSel['cut'],lepSel['veto'],ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_multi]),\
  #'bkgcut':"&&".join(['singleLeptonic','nLooseHardLeptons==1&&nTightHardLeptons==1',ht_cut,st,njets_30_cut,jets_2_80]),\
  #,ht_cut,st,njets_30_cut,jets_2_80,nbjets_30_cut_zero,jets_2_80]),\
  'label':'0 b-jets (CSVv2)'}
  #####samples = lepSel['sample']
  ##samples=[
  ###### {"sample":"data_mu" ,   "list":SingleMuon_Run2015D_v4, "tex":"Single_Muon","color":ROOT.kBlack},
  ###### {"sample":"data_mu" ,   "list":SingleMuon_Run2015D_05Oct , "tex":"Single_Muon","color":ROOT.kBlack},
  ##  #{"sample":"data_mu" ,   "list":data_mu , "tex":"Single_Muon","color":ROOT.kBlack},
  ##  #{"sample":"data_mu_17July" ,   "list":data_mu_17July , "tex":"Single_Muon_17Jul","color":ROOT.kBlack},
  ## {"sample":"data_ele",   "list":SingleElectron_Run2015D_v4  , "tex":"Single_Electron", "color":ROOT.kBlack},\
  ## {"sample":"data_ele",   "list":SingleElectron_Run2015D_05Oct  , "tex":"Single_Electron", "color":ROOT.kBlack},\
  ##  #{"sample":"data_ele",   "list":data_ele, "tex":"Single_Electron", "color":ROOT.kBlack},\
  ##  #{"sample":"data_ele_17July",   "list":data_ele_17July, "tex":"data", "color":ROOT.kBlack}
  ##]

  #samples=[
  #  {"cut":"run>=251643","sample":"data_mu" ,          "list":SingleMuon_Run2015B_PromptReco, "tex":"Single_Muon","color":ROOT.kBlack},
  #  {"cut":"run<=251562","sample":"data_mu_17July" ,   "list":SingleMuon_Run2015B_17Jul2015, "tex":"Single_Muon_17Jul","color":ROOT.kBlack},
  #  {"cut":"run>=251643","sample":"data_ele",          "list":SingleElectron_Run2015B_PromptReco, "tex":"Single_Electron", "color":ROOT.kBlack},\
  #  {"cut":"run<=251562","sample":"data_ele_17July",   "list":SingleElectron_Run2015B_17Jul2015, "tex":"data", "color":ROOT.kBlack}
  #]

  #for s in samples:
  #    s['chunk'] , s['norm']  = getChunks(s['list'],maxN=maxN)
  #    #chain = ROOT.TChain('tree')
  #    #chain.Add(s['chunk'][0]["file"])
  #    #s["cpTree"] = chain.CopyTree(s['cut']+'&&'+cut['cut'])  
  #    #print s["cpTree"].GetEntries()
  #    print s['chunk']
  #    print s['norm']

  ####d_chunk , d_norm = getChunks(lepSel['chunk'],maxN=maxN)
  #data_chunks = [s['chunk'][0] for s in samples ]
  #data_chunks = [s['chunk'] for s in samples ]
  #data_chain = getChain(data_chunks,maxN=maxN,histname="",treeName="tree")
  ####data_chain = getChain(samples[1]['chunk']+samples[0]['chunk'],maxN=maxN,histname="",treeName="tree")
  ####data_chain = getChain(lepSel['chain'],maxN=maxN,histname="",treeName="Events")
  ######data_chain = getChain(d_chunk,maxN=maxN,histname="",treeName="tree")
  #######print data_chain.GetEntries()
  #######y_data = getYieldFromChain(data_chain, cutString = cut['cut'], weight = "(1)", returnError=False)
  #########print "data yield after cut:" , y_data
  #cp_data = data_chain.CopyTree(cut['cut'])
  #print "data cp created with cut :" , cut['cut']

  bkg_samples=[
  {"sample":"DY",           "name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
  {"sample":"singleTop",    "name":singleTop_25ns,"tex":"single top",'color': ROOT.kViolet+5},
  {"sample":"QCD",          "name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
  {'sample':'TTVH',          "name":TTV_25ns ,'tex':'t#bar{t}+W/Z/H','color':ROOT.kOrange-3}, 
  #{"sample":"WJets",        "name":WJetsToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
  {"sample":"WJets",        "name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
  #{"sample":"ttJets",       "name":TTJets_25ns, "tex":"ttbar + jets",'color':ROOT.kBlue-4},
  {"sample":"ttJets",       "name":TTJets_HTLO_25ns, "tex":"ttbar + jets",'color':ROOT.kBlue-4},
  ]

  print "Now this will be slow but It will done once !!!"
  y_bkg_list = []
  for bkg in bkg_samples:
    #bkg['chain'] = []
    #bkg['norm'] = []
    #bkg['chunks'].append(b_chunk[0])
    #bkg['norm'].append(b_norm) 
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events") 
    ###print "I am gonna copy tree now with the cut:" , cut['bkgcut']
    ##bkg['cpTree'] = bkg['chain'].CopyTree(cut['bkgcut'])
    ##print "copied....."
    #bkg['sumNorm'] = sum(bkg['norm'])
    #bkg['chain'] = getChain(bkg['chunks'],maxN=maxN,histname="",treeName="tree")
    #print "I am gonna copy tree now with the cut:" , cut['bkgcut']
    #bkg['cpTree'] = bkg['chain'].CopyTree(cut['bkgcut'])
    #print "copied....."
   ##### y_bkg = getYieldFromChain(bkg['chain'], cutString = cut['bkgcut'], weight = "weight", returnError=False)
   ##### y_bkg_list.append(y_bkg)
  ######sum_bkg =  sum(y_bkg_list)
  ######print "sum bkg:" , sum_bkg  ,"ratio:" , y_data/sum_bkg
  from array import array
  dPhiBins  = array('d', [float(x)/1000. for x in range(0,200,100)+range(200,400,200)+range(400,700,300)+range(700,1000,300)+range(1000,2000,1000)+range(2000,3141,1141)+range(3141,4141,1000)])
  plots =[\
  #{'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':dPhi,                 'varname':'deltaPhi_Wl',       'binlabel':1, 'bin': (len(dPhiBins)-1,dPhiBins)},\
  # 'bin':(30,0,3.141)},\
  ##{'ndiv':True,'yaxis':'Events /','xaxis':'L_{T}','logy':'True' , 'var':  "(LepGood_pt[0]+met_pt)",                          'varname':'st',                  'binlabel':20,  'bin':(50,0,1000)},\
  {'ndiv':True,'yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':ht,                    'varname':'htJet30j',            'binlabel':40,  'bin':(50,0,2000)},\
  ##{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':njets_30,                      'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
  ###{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':'nJet',                      'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
  ##{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'LepGood_pt[0]',                 'varname':'leptonPt',      'binlabel':15,  'bin':(40,25,625)},\
  ##{'ndiv':False,'yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':nbjets_30,           'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
  ###{'ndiv':True,'yaxis':'Events /','xaxis':'L_{T}','logy':'True' , 'var':  "(LepGood_pt[0]+metNoHF_pt)",                          'varname':'st_metnohf',                  'binlabel':50,  'bin':(36,200,2000)},\
  ##{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'Jet_pt[0]',  'binlabel':30,  'bin':(67,0,2010)},\
  ##{'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',                 'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
  ##{'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',                         'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
  ##{'ndiv':False,'yaxis':'Events /','xaxis':'#slash{E}_{T} #Phi','logy':'True' , 'var':'met_phi',                         'varname':'met_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
  ###{'ndiv':False,'yaxis':'Events /','xaxis':'#slash{E}_{T}NoHF #Phi','logy':'True' , 'var':'metNoHF_phi',                         'varname':'metNoHF_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
  ###{'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}NoHF','logy':'True' , 'var':'metNoHF_pt',                         'varname':'metNoHF_pt',         'binlabel':50,  'bin':(28,0,1400)},\
  ##{'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',                 'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
  ###{'ndiv':False,'yaxis':'Events','xaxis':'#miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',                 'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
  ###{'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))',       'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)},\
  ##{'ndiv':False,'yaxis':'Events','xaxis':'nVert','logy':'True' , 'var':'nVert',       'varname':'nVert',      'binlabel':1,  'bin':(50,0,50)}
  ###{'ndiv':False,'yaxis':'Events','xaxis':'nVert_withpuWeight','logy':'True' , 'var':'nVert',       'varname':'nVert_puWeight',      'binlabel':1,  'bin':(50,0,50)}
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
   ##Pad1 = ROOT.TPad("Pad1", "Pad1", 0, 0.35, 1, 0.9)
   ##Pad1.SetLogy()
   ##Pad1.SetTopMargin(0.06)
   ##Pad1.SetBottomMargin(0)
   ##Pad1.SetLeftMargin(0.16)
   ##Pad1.SetRightMargin(0.05)
   ##Pad1.Draw()
   ##Pad1.cd()
    h_Stack = ROOT.THStack('h_Stack',p['varname'])

    for bkg in bkg_samples:
      color = bkg['color']
      print color
      print bkg['sample']
      ##chain = bkg['cpTree']
      chain = bkg['chain']
      #weight_str = '((xsec*genWeight/3)*'+str(lumi)+')'
      #weight_str = '(('+str(MC_scale)+'*xsec*genWeight)*'+str(lumi)+')'
      #histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'],p['lowlimit'],p['limit'])
      #histo = ROOT.TH1F(str(histo) ,str(histo),*p['bin'])
      #chain.Draw('('+p['var']+')>>'+str(histoname),weight_str+"*(1)")
      #histo = getPlotFromChain(chain, p['var'], p['bin'], cutString = "(1)", weight = "weight*0.64*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='')
      histo = getPlotFromChain(chain, p['var'], p['bin'], cutString = cut['bkgcut'], weight = "weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
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
    h_Stack.SetMaximum(2000)
    h_Stack.SetMinimum(0.11)
    #h_Stack.GetYaxis().SetTitleSize(2)
    #data =  cp_data
    #data =  data_chain
    color = ROOT.kBlack
    histo = 'h_data'
    histoname = histo
    print histoname
    #print p['bin'],p['lowlimit'],p['limit']
    #histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'][0],p['bin'][1],p['bin'][2])
    #histo = ROOT.TH1F(str(histo) ,str(histo),p['bin'][0],p['bin'][1])
    #data.Draw(p['var']+'>>'+str(histoname),cut['cut'])
    print "pass draw : ) "
    #histo.SetMarkerStyle(20)
    #histo.SetMarkerSize(1.8)
    #histo.SetLineColor(color)
    #histo.GetXaxis().SetTitle(p['xaxis'])
    #histo.SetTitle("")
    #histo.GetYaxis().SetTitleSize(0.05)
    #histo.GetYaxis().SetLabelSize(0.05)
    #h_Stack.Draw()
    #histo.Draw("E1P")
    #histo.SetMaximum(2000)
    #histo.SetMinimum(0.11)
    h_Stack.Draw("Histo")
    #histo.Draw("E1PSame")
    #print "data Integral" , histo.Integral()
    #h_Stack.GetXaxis().SetTitle(p['xaxis'])
    #if p['ndiv']:
    #  histo.GetXaxis().SetNdivisions(505)
    #  histo.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
    #  h_Stack.GetXaxis().SetNdivisions(505)
    #  h_Stack.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
    #if not p['ndiv']:
    #  histo.GetYaxis().SetTitle(p['yaxis'])
    #  h_Stack.GetYaxis().SetTitle(p['yaxis'])
    stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
    #stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1])
    stack_hist.Merge(h_Stack.GetHists())
    print "Integral of BKG:" , stack_hist.Integral()
    #print "Integral of Data:" , histo.Integral()
    #leg.AddEntry(histo, "data","PL")
    leg.SetFillColor(0)
    leg.Draw()
    latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
    latex.DrawLatex(0.72,0.958,"#bf{L="+str(lumi)+" pb^{-1} (13 TeV)}")
    #latex.DrawLatex(0.72,0.958,"#bf{L=1.26 fb^{-1} (13 TeV)}")
    latex.DrawLatex(0.6,0.8,"#bf{H_{T}>500 GeV}")
    latex.DrawLatex(0.6,0.75,"#bf{L_{T}>250 GeV}")
    latex.DrawLatex(0.6,0.7,"#bf{N_{bjets}==0}")
    latex.DrawLatex(0.6,0.5,"#bf{MC scale=0.71}")
   ## Pad1.RedrawAxis()
   ##can.cd()
   ##Pad2 = ROOT.TPad("Pad2", "Pad2",  0, 0.04, 1, 0.35)
   ##Pad2.SetTopMargin(0)
   ##Pad2.SetBottomMargin(0.5)
   ##Pad2.SetLeftMargin(0.16)
   ##Pad2.SetRightMargin(0.05)
   ##Pad2.Draw()
   ##Pad2.cd()
   ###Func = ROOT.TF1('Func',"[0]",p['bin'][1],p['bin'][2])
   ##Func = ROOT.TF1('Func',"[0]",0,3.141)
   ##Func.SetParameter(0,1)
   ##Func.SetLineColor(2)
   ##h_ratio = histo.Clone('h_ratio')
   ##h_ratio.SetMinimum(0.0)
   ##h_ratio.SetMaximum(1.99)
   ##h_ratio.Sumw2()
   ##h_ratio.SetStats(0)
   ##h_ratio.Divide(stack_hist)
   ##h_ratio.SetMarkerStyle(20)
   ##h_ratio.SetMarkerColor(ROOT.kBlack)
   ##h_ratio.SetTitle("")
   ##h_ratio.GetYaxis().SetTitle("Data/Pred. ")
   ##h_ratio.GetYaxis().SetTitleSize(0.1)
   ##h_ratio.GetXaxis().SetTitle(p['xaxis'])
   ##h_ratio.GetYaxis().SetTitleFont(42)
   ##h_ratio.GetYaxis().SetTitleOffset(0.6)
   ##h_ratio.GetXaxis().SetTitleOffset(1)
   ##h_ratio.GetYaxis().SetNdivisions(505)
   ##h_ratio.GetXaxis().SetTitleSize(0.2)
   ##h_ratio.GetXaxis().SetLabelSize(0.13)
   ##h_ratio.GetYaxis().SetLabelSize(0.1)
   ##h_ratio.Draw("E1")
   ###h_ratio.Draw()
   ##Func.Draw("same")
   ###Func.Draw()
    can.SetLogy()
    can.Draw()
    can.SaveAs(path+p['varname']+'.png')
    can.SaveAs(path+p['varname']+'.pdf')
    can.SaveAs(path+p['varname']+'.root')
    can.Clear()
