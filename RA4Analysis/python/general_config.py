import ROOT

##General

sample_lumi = 3000##pb
lumi = 40000 #2300##pb
lumi_label = 12.88
scale = '(1)'
btagVarString = 'nBJetMediumCSV30'

##For Data Only

#filters = "(Flag_goodVertices && Flag_HBHENoiseFilter_fix && Flag_eeBadScFilter && Flag_HBHENoiseIsoFilter)" # && veto_evt_list)"
filters = "(Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_goodVertices && Flag_eeBadScFilter &&  Flag_globalTightHalo2016Filter && Flag_badChargedHadronFilter && Flag_badMuonFilter)"
trigger = "((HLT_EleHT350||HLT_EleHT400||HLT_Ele105)||(HLT_MuHT350||HLT_MuHT400))"

##Common for Background and Signal
#trigger_scale = '((singleElectronic&&0.963)||(singleMuonic&&0.926))'
trigger_scale = '(singleMuonic*0.926+singleElectronic*0.963)'
reweight      = '(weight*'+str(lumi)+')/'+str(sample_lumi)
weight_0b     = 'weightBTag0_SF'
weight_1b     = 'weightBTag1_SF'

##For MC only
bkg_filters = "(Flag_badChargedHadronFilter && Flag_badMuonFilter)"
#lepton_Scale  = 'lepton_eleSF_miniIso01*lepton_eleSF_cutbasedID*lepton_muSF_sip3d*lepton_muSF_miniIso02*lepton_muSF_mediumID'
#lepton_Scale  = 'lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'
lepton_Scale  = 'leptonSF'
topPt         = 'TopPtWeight'
PU            = 'puReweight_true_max4'
#weight_str_plot = '*'.join([reweight,topPt,trigger_scale,PU])
weight_str_plot = '*'.join([trigger_scale,lepton_Scale,topPt,PU,reweight])
#weight_str_CV   = '*'.join([trigger_scale,lepton_Scale,topPt,reweight])
weight_str_CV   = reweight

##For Signal Only
lepton_Scale_signal_fast = 'reweightLeptonFastSimSF'
ISR_weight = 'weight_ISR_new' ##use with a normalisation constant
lepton_Scale_signal  = 'lepton_muSF_HIP*lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01*lepton_eleSF_gsf'
weight_str_signal_plot = '*'.join([trigger_scale,lepton_Scale_signal_fast,lepton_Scale_signal,PU,ISR_weight,reweight])
weight_str_signal_CV = '*'.join([trigger_scale,lepton_Scale_signal,reweight])


def Draw_CMS_header(lumi_label=12.88):
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextAlign(31)
   tex.SetTextFont(42)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.96,0.96,str(lumi_label)+" fb^{-1} (13 TeV)")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(61)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.18,0.96,"CMS")
   tex = ROOT.TLatex()
   tex.SetNDC()
   tex.SetTextFont(52)
   tex.SetTextSize(0.05)
   tex.SetLineWidth(2)
   tex.DrawLatex(0.26,0.96,"Preliminary")
   return

def Set_axis_pad2(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.11)
   histo.GetXaxis().SetTitleSize(0.14)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetTitle("Data/Pred.")
   histo.GetYaxis().SetDecimals()
   histo.GetYaxis().SetNdivisions(505)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.11)
   histo.GetYaxis().SetTitleSize(0.14)
   histo.GetYaxis().SetTitleOffset(0.52)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

def Set_axis_pad1(histo):
   histo.GetXaxis().SetLabelFont(42)
   histo.GetXaxis().SetLabelOffset(0.007)
   histo.GetXaxis().SetLabelSize(0.05)
   histo.GetXaxis().SetTitleSize(0.06)
   histo.GetXaxis().SetTitleOffset(0.9)
   histo.GetXaxis().SetTitleFont(42)
   histo.GetYaxis().SetLabelFont(42)
   histo.GetYaxis().SetLabelOffset(0.007)
   histo.GetYaxis().SetLabelSize(0.05)
   histo.GetYaxis().SetTitleSize(0.06)
   histo.GetYaxis().SetTitleOffset(1.35)
   histo.GetYaxis().SetTitleFont(42)
   histo.GetZaxis().SetLabelFont(42)
   histo.GetZaxis().SetLabelOffset(0.007)
   histo.GetZaxis().SetLabelSize(0.05)
   histo.GetZaxis().SetTitleSize(0.06)
   histo.GetZaxis().SetTitleFont(42)
   return

ROOT.gROOT.LoadMacro("../../HEPHYPythonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
maxN = -1
ROOT.gStyle.SetOptStat(0)


