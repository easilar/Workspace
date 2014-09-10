import ROOT
from math import *
#from helpers import getVarValue, deltaPhi, minAbsDeltaPhi,  deltaR, invMass,
from Workspace.HEPHYPythonTools.helpers import getVarValue, getFileList

from stage1Tuples import WJetsHTToLNu, WJetsToLNu25ns
small = True
smallNumber = 50

prefix = 'ht'
cut='Sum$(jetsPt)>=2'
var = 'Sum$(jetsPt*(jetsPt>30))'
binning = [500,0,2500]
startFitRange = 150

#prefix='met'
#var = 'slimmedMETs'
#binning = [250,0,2500]
#startFitRange = 100

binningStr = ','.join([str(x) for x in binning])
 
cInc = ROOT.TChain('Events')
for b in WJetsToLNu25ns['bins']:
  l = getFileList(b['dir'])
  if small:
    l=l[:smallNumber]
  print "Adding ", len(l), "files from", b['dbsName']
  for f in l:
    cInc.Add(f)
for b in WJetsHTToLNu['bins']:
  c = ROOT.TChain('Events')
  l = getFileList(b['dir'])
  if small:
    l=l[:smallNumber]
  print "Adding ", len(l), "files from", b['dbsName']
  for f in l:
    c.Add(f)
  b['chain']=c

c1 = ROOT.TCanvas()
cInc.Draw(var+'>>hTMP('+binningStr+')',cut,'goff')
hTMP = ROOT.gDirectory.Get('hTMP')
hTMP.SetLineColor(ROOT.kRed)
hWJetsInc = hTMP.Clone()
hWJetsInc.Draw()
hWJetsInc.Scale(1./hWJetsInc.Integral())
del hTMP

c1.SetLogy()
wjetHTHistos = ROOT.TObjArray(len(WJetsHTToLNu['bins']))
for b in WJetsHTToLNu['bins']:
  b['chain'].Draw(var+'>>hTMP('+binningStr+')', cut, 'goff')
  hTMP = ROOT.gDirectory.Get('hTMP')
  b['histo'] = hTMP.Clone()
  b['histo'].Scale(1./b['histo'].Integral())
  b['histo'].Draw('same')
  wjetHTHistos.Add(b['histo'])
  del hTMP

c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/'+prefix+'_wjetsHTNormalized.png')

fit = ROOT.TFractionFitter(hWJetsInc, wjetHTHistos)
fit.Constrain(1,0.0,1.0)
fit.Constrain(2,0.0,1.0)
fit.Constrain(3,0.0,1.0)
fit.Constrain(4,0.0,1.0)
fit.SetRangeX(hWJetsInc.FindBin(startFitRange),hWJetsInc.FindBin(binning[-1]))
status = fit.Fit()
print status
if status==0:
  result = fit.GetPlot();
  hWJetsInc.Draw("");
  result.SetLineColor(ROOT.kBlue)
  result.Draw("same")

  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngCSA14/'+prefix+'_wjetsHTNormalized_fitResult.png')