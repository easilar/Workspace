import ROOT
import pickle
import os,sys
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getYieldFromChain,getPlotFromChain
from Workspace.RA4Analysis.helpers import nameAndCut, nJetBinName, nBTagBinName, varBinName, varBin, UncertaintyDivision
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_fromArtur import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_25ns_postProcessed_PU_fromArtur import *
from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2_postprocessed import *
from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed import *
#from Workspace.RA4Analysis.cmgTuples_Spring15_MiniAODv2_25ns_postProcessed_1 import *
from Workspace.RA4Analysis.signalRegions import signalRegion3fb
from cutFlow_helper import *
from math import *

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)
lumi = 2200##pb
#SR = signalRegion3fb
signalRegion3fbReduced = {(5, -1):  {(250, -1): {(500, -1):  {'deltaPhi': 1.0}}}}
#signalRegion3fbReduced = {(5, 5):  {(250, 350): {(500, -1):  {'deltaPhi': 1.0}}}}
#                                  (350, 450): {(500, -1):  {'deltaPhi': 1.0}},
#                                  (450, -1):  {(500, -1):  {'deltaPhi': 0.75}}},
#                        (6, 7):  {(250, 350): {(500, 750): {'deltaPhi': 1.0},
#                                               (750, -1):  {'deltaPhi': 1.0}},
#                                  (350, 450): {(500, 750): {'deltaPhi': 1.0},
#                                               (750, -1):  {'deltaPhi': 1.0}},
#                                  (450, -1):  {(500, 750): {'deltaPhi': 0.75},
#                                               (750, -1):  {'deltaPhi': 0.75}}},
#                        (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
#                                               (750, -1):  {'deltaPhi': 1.0}},
#                                 (350, -1):  {(500, -1):  {'deltaPhi': 0.75}}}}
#

SR = signalRegion3fbReduced 
btagVarString = 'nBJetMediumCSV30'
#btagString = 'nBJetMediumCSV30'

lepSels = [
{'cut':'(singleMuonic&&(!isData||(isData&&muonDataSet)))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
 'chain': getChain(single_mu_Run2015D,maxN=maxN,histname="",treeName="Events") ,\
 'trigWeight': "0.942" ,\
  'label':'_mu_', 'str':'1 $\\mu$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#{'cut':'singleElectronic&&(!isData||(isData&&eleDataSet))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
# 'chain': getChain(single_ele_Run2015D,maxN=maxN,histname="",treeName="Events") ,\
# 'trigWeight': "0.949" ,\
#  'label':'_ele_', 'str':'1 $\\e$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'},\
#{'cut':'((!isData&&singleLeptonic)||(isData&&((eleDataSet&&singleElectronic)||(muonDataSet&&singleMuonic))))' , 'veto':'nLooseHardLeptons==1&&nTightHardLeptons==1&&nLooseSoftLeptons==0',\
# 'chain': getChain([single_ele_Run2015D,single_mu_Run2015D],maxN=maxN,histname="",treeName="Events") ,\
# 'trigWeight': "0.945" ,\
#  'label':'_lep_', 'str':'1 $lep$' , 'trigger': '((HLT_EleHT350)||(HLT_MuHT350))'}\
]

bkg_samples=[
{'sample':'TTVH',     "weight":"(1)"            ,"cut":(0,0) , "name":TTV_25ns ,'tex':'t#bar{t}+W/Z/H','color':ROOT.kOrange-3},
{"sample":"QCD",      "weight":"(1)"            ,"cut":(0,0) , "name":QCDHT_25ns, "tex":"QCD","color":ROOT.kCyan-6},
{"sample":"singleTop","weight":"(1)"            ,"cut":(0,0) , "name":singleTop_25ns,"tex":"single top",'color': ROOT.kViolet+5},
{"sample":"DY",       "weight":"(1)"            ,"cut":(0,0) , "name":DY_25ns,"tex":"DY + jets",'color':ROOT.kRed-6},
{"sample":"WJets",    "weight":"weightBTag0_SF" ,"cut":(0,-1) , "name":WJetsHTToLNu_25ns,"tex":"W + jets","color":ROOT.kGreen-2},
{"sample":"ttJets",   "weight":"weightBTag0_SF" ,"cut":(0,-1) , "name":TTJets_combined, "tex":"ttbar + jets",'color':ROOT.kBlue-4},
]
for bkg in bkg_samples:
    bkg['chain'] = getChain(bkg['name'],maxN=maxN,histname="",treeName="Events")

cS1000 = getChain(T5qqqqVV_mGluino_1000To1075_mLSP_1To950[1000][700],histname='')
cS1200 = getChain(T5qqqqVV_mGluino_1200To1275_mLSP_1to1150[1200][800],histname='')
cS1500 = getChain(T5qqqqVV_mGluino_1400To1550_mLSP_1To1275[1500][100],histname='')

signals = [\
{"chain":cS1000,"name":"s1000","color":ROOT.kBlue},\
{"chain":cS1200,"name":"s1200","color":ROOT.kRed},\
{"chain":cS1500,"name":"s1500","color":ROOT.kBlack},\
]

plots =[\
{'ndiv':False,'yaxis':'Events','xaxis':'#Delta#Phi(W,l)','logy':'True' , 'var':'deltaPhi_Wl',                 'varname':'deltaPhi_Wl',       'binlabel':1, 'bin':(30,0,3.141)},\
{'ndiv':True,'yaxis':'Events /','xaxis':'L_{T}','logy':'True' , 'var':  'st',                          'varname':'LT',                  'binlabel':20,  'bin':(45,100,1000)},\
# {'ndiv':True,'yaxis':'Events /','xaxis':'H_{T}','logy':'True' , 'var':'htJet30j',                    'varname':'htJet30j',            'binlabel':50,  'bin':(44,300,2500)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{Jets}','logy':'True' , 'var':'nJet30',                      'varname':'nJet30',                   'binlabel':1,  'bin':(15,0,15)},\
#{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(l)','logy':'True' , 'var':'LepGood_pt[0]',                 'varname':'leptonPt',      'binlabel':15,  'bin':(40,25,625)},\
{'ndiv':False,'yaxis':'Events','xaxis':'N_{bJetsCSV}','logy':'True' , 'var':'nBJetMediumCSV30',           'varname':'nBJetMediumCSV30',      'binlabel':1,  'bin':(8,0,8),       'lowlimit':0,  'limit':8},\
#{'ndiv':True,'yaxis':'Events /','xaxis':'p_{T}(leading jet)','logy':'True' , 'var':'Jet_pt[0]',               'varname':'leading_JetPt',  'binlabel':30,  'bin':(67,0,2010)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'#eta(l)','logy':'True' , 'var':'LepGood_eta[0]',                 'varname':'leptonEta',      'binlabel':25,  'bin':(40,-4,4)},\
#{'ndiv':True,'yaxis':'Events /','xaxis':'#slash{E}_{T}','logy':'True' , 'var':'met_pt',                         'varname':'met',         'binlabel':50,  'bin':(28,0,1400)},\
#{'ndiv':False,'yaxis':'Events /','xaxis':'#slash{E}_{T} #Phi','logy':'True' , 'var':'met_phi',                         'varname':'met_phi',         'binlabel':50,  'bin':(30,-3.14,3.14)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'#phi(l)','logy':'True' , 'var':'LepGood_phi[0]',                 'varname':'leptonPhi',      'binlabel':25,  'bin':(40,-4,4)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'#miniIso(l)','logy':'True' , 'var':'LepGood_miniRelIso[0]',                 'varname':'leptonminiIso',      'binlabel':30,  'bin':(40,0,0.5)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'minDeltaR','logy':'True' , 'var':'Min$(sqrt((abs(Jet_phi-LepGood_phi[0]))**2+(abs(Jet_eta-LepGood_eta[0]))**2))',       'varname':'Min_R_Jet_lepton',      'binlabel':1,  'bin':(50,0,10)},\
#{'ndiv':False,'yaxis':'Events','xaxis':'nVert','logy':'True' , 'var':'nVert',       'varname':'nVert',      'binlabel':1,  'bin':(50,0,50)}
  ]

SBs = [\
     {'nJet':(3,4),'nBJet':(0,0)},\
     #{'nJet':(5,-1),'nBJet':(0,0)},\
     #{'nJet':(4,5),'nBJet':(1,1)},\
      ]

for lepSel in lepSels:
  #path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p1fb/SRplots/tests/"+lepSel['label']
  path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p2fb/Tests/"+lepSel['label']
  #path = "/afs/hephy.at/user/e/easilar/www/data/Run2015D/2p1fb/CRplots/withPU_BtagSF/"+lepSel['label']
  if not os.path.exists(path):
    os.makedirs(path)
  print lepSel['label']
  print "====== "
  for SB in SBs:
    nJet = SB['nJet']
    nbTags = SB['nBJet']
    print "nJet:" , nJet , "nBJet:" , nbTags
    #presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4&&deltaPhi_Wl<0.5"])
    presel = "&&".join([lepSel['cut'],lepSel['veto'],filters,"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
    sig_presel = "&&".join([lepSel['cut'],lepSel['veto'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
    data_presel = "&&".join([lepSel['cut'],lepSel['veto'],lepSel['trigger'],"Jet_pt[1]>80&&abs(LepGood_eta[0])<2.4"])
    bin = {}
    for srNJet in sorted(SR):
      bin[srNJet]={}
      for stb in sorted(SR[srNJet]):
        bin[srNJet][stb] = {}
        for htb in sorted(SR[srNJet][stb]):
          bin[srNJet][stb][htb] = {}
          deltaPhiCut = SR[srNJet][stb][htb]['deltaPhi']
          bla_Name, Cut = nameAndCut(stb, htb, nJet, btb=nbTags, presel=presel, btagVar =  btagVarString)
          print "CUT:" , Cut
          #Name, bla = nameAndCut(stb, htb, srNJet , btb=nbTags, presel=presel, btagVar =  btagVarString)
          Name, bla = nameAndCut(stb, htb, nJet , btb=nbTags, presel=presel, btagVar =  btagVarString)
          print Name
          CR_path = path+'/'+Name+'/' 
          if not os.path.exists(CR_path):
            os.makedirs(CR_path)
          for p in plots:
            bin[srNJet][stb][htb][p['varname']] = {}
            for bkg in bkg_samples:
              print "PRESEL:" , presel
              print "btag Cut:" , bkg['cut']
              bla_Name, Cut = nameAndCut(stb, htb, nJet, btb=bkg['cut'], presel=presel, btagVar =  btagVarString)
              print "CUT:" , Cut
              bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut]), weight = lepSel['trigWeight']+"*"+bkg['weight']+"*lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID*puReweight_true*weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
             # bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut]), weight = bkg['weight']+"*puReweight_true*weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
              #bin[srNJet][stb][htb][p['varname']][bkg['sample']] = getPlotFromChain(bkg['chain'], p['var'], p['bin'], cutString = "&&".join([presel,Cut]), weight = "weight*"+str(lumi)+"/3000", binningIsExplicit=False, addOverFlowBin='both')
            bla_Name, Cut = nameAndCut(stb, htb, nJet, btb=nbTags, presel="(1)", btagVar =  btagVarString)
            bin[srNJet][stb][htb][p['varname']]['signals']
            for sig in signals:
              bin[srNJet][stb][htb][p['varname']]['signals'][sig["name"]] = getPlotFromChain(sig['chain'], p['var'], p['bin'], cutString = "&&".join([sig_presel,Cut]) , weight = "weight", binningIsExplicit=False, addOverFlowBin='both') 
            bin[srNJet][stb][htb][p['varname']]['data'] = getPlotFromChain(lepSel['chain'], p['var'], p['bin'], cutString = "&&".join([data_presel,Cut]) , weight = "(1)", binningIsExplicit=False, addOverFlowBin='both')
            bin[srNJet][stb][htb]['label'] = Name         
            bin[srNJet][stb][htb]['path'] = CR_path        

    for p in plots:
      index = 0
      for srNJet in sorted(SR):
        for stb in sorted(SR[srNJet]):
          for htb in sorted(SR[srNJet][stb]):
            index +=1
            print index
            print bin[srNJet][stb][htb]['label']
            cb = ROOT.TCanvas("cb","cb",800,800)
            cb.cd()
            cb.SetRightMargin(3)
            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.04)
            latex.SetTextAlign(11)
      #      leg = ROOT.TLegend(0.45,0.8,0.65,0.94)
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
            ROOT.gStyle.SetHistMinimumZero()
            h_Stack = ROOT.THStack('h_Stack','h_Stack')
            for bkg in bkg_samples:
              color = bkg['color']
              histo = bin[srNJet][stb][htb][p['varname']][bkg['sample']]
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
              leg.AddEntry(histo, bkg['tex'],"f")
              h_Stack.Add(histo)
              del histo
            h_Stack.Draw("Bar")
            h_Stack.SetMaximum(4000)
            h_Stack.SetMinimum(0.11)
            h_Stack_sig = ROOT.THStack('h_Stack_sig','h_Stack_sig')
            for sig in signals:
              h_sig = bin[srNJet][stb][htb][p['varname']][sig["name"]]
              h_sig.SetLineColor(sig["color"])
              h_sig.SetTitle("")
              h_sig.draw("hist")
              leg.AddEntry(h_sig, sig['name'],"l")
              h_Stack_sig.Add(h_sig)
              del h_sig
            
            color = ROOT.kBlack
            h_data = bin[srNJet][stb][htb][p['varname']]['data']
            h_data.SetMarkerStyle(20)
            h_data.SetMarkerSize(1.8)
            h_data.SetLineColor(color)
            h_data.GetXaxis().SetTitle(p['xaxis'])
            h_data.SetTitle("")
            h_data.GetYaxis().SetTitleSize(0.05)
            h_data.GetYaxis().SetLabelSize(0.05)
            h_data.Draw("E1P")
            h_data.SetMaximum(4000)
            h_data.SetMinimum(0.11)
            h_Stack.Draw("HistoSame")
            h_data.Draw("E1PSame")
            h_Stack_sig.Draw("nostack Same")
            if p['ndiv']:
              h_data.GetXaxis().SetNdivisions(505)
              h_data.GetYaxis().SetTitle(p['yaxis']+str(p['binlabel'])+'GeV')
            if not p['ndiv']:
              h_data.GetYaxis().SetTitle(p['yaxis'])
            stack_hist=ROOT.TH1F("stack_hist","stack_hist",p['bin'][0],p['bin'][1],p['bin'][2])
            stack_hist.Merge(h_Stack.GetHists())
            print "Integral of BKG:" , stack_hist.Integral()
            print "Integral of Data:" , h_data.Integral()
            leg.AddEntry(h_data, "data","PL")
            leg.SetFillColor(0)
            leg.Draw()
            latex.DrawLatex(0.16,0.958,"#font[22]{CMS}"+" #font[12]{Preliminary}")
            #latex.DrawLatex(0.72,0.958,"#bf{L="+str(lumi)+" pb^{-1} (13 TeV)}")
            latex.DrawLatex(0.72,0.958,"#bf{L=2.1 fb^{-1} (13 TeV)}")
            #latex.DrawLatex(0.6,0.8,str(nJet[0])+"#leqN_{Jets}#leq"+str(nJet[1]))
            latex.DrawLatex(0.6,0.8,"N_{Jets}#geq"+str(nJet[0]))
            latex.DrawLatex(0.6,0.75,"#bf{N_{bjets}="+str(nbTags[0])+"}")
            latex.DrawLatex(0.4,0.8,"MC Yield:"+str(format(stack_hist.Integral(),'.2f')) )
            latex.DrawLatex(0.4,0.75,"data Yield:"+str(h_data.Integral()) )
            #latex.DrawLatex(0.6,0.5,"#bf{MC scale=0.71}")
            Pad1.RedrawAxis()
            cb.cd()
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
            h_ratio = h_data.Clone('h_ratio')
            h_ratio.SetMinimum(0.0)
            h_ratio.SetMaximum(1.99)
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
            h_ratio.Draw("E1")
            Func.Draw("same")
            cb.Draw()
            cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.png')
            cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.pdf')
            cb.SaveAs(bin[srNJet][stb][htb]['path']+p['varname']+'.root')
            cb.Clear()
            del h_Stack

