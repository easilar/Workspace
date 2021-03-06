import os, sys, ROOT
from math import cos, sin, sqrt, asinh, acosh, sinh

def getValue(chain, varname):
  # can treat scalars or arrays with a numeric index
  #   default index (for a scalar) is 0
  vn = varname
  idx = 0
  # try to find index
  iidx = varname.find('[')
  if iidx>-1:
    assert varname[-1] == ']'
    vn = varname[:iidx]
    idx = int(varname[iidx+1:-1])
    
  alias = chain.GetAlias(vn)
  if alias!="":
    return chain.GetLeaf( alias ).GetValue(idx)
  else:
    return chain.GetLeaf( vn ).GetValue(idx)

def softIsolatedMT(chain):
  lepton_pt   = getValue(chain, "softIsolatedMuPt")
  lepton_phi  = getValue(chain, "softIsolatedMuPhi")
  metphi      = getValue(chain, "type1phiMetphi")
  met         = getValue(chain, "type1phiMet")
  return ROOT.sqrt(2*lepton_pt*met*(1.-cos(lepton_phi - metphi)))

def cosDeltaPhiLepW(chain):
  lPt = getValue(chain, "softIsolatedMuPt")
  lPhi = getValue(chain, "softIsolatedMuPhi")
  metphi = getValue(chain, "type1phiMetphi")
  met = getValue(chain, "type1phiMet")
  cosLepPhi = cos(lPhi)
  sinLepPhi = sin(lPhi)
  mpx = met*cos(metphi)
  mpy = met*sin(metphi)
  pW = sqrt((lPt*cosLepPhi + mpx)**2 + (lPt*sinLepPhi + mpy)**2)

  return ((lPt*cosLepPhi + mpx)*cosLepPhi + (lPt*sinLepPhi + mpy)*sinLepPhi )/pW


def pmuboost3d(jets, met, lep):
    mw = 80.385
    wwwtlv = ROOT.TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    mettlv = ROOT.TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    leptlv = ROOT.TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    for jet in jets:
#        if(e.jetPt[ij] > 30.):
            tlvaux = ROOT.TLorentzVector(1e-9,1e-9,1e-9,1e-9)
            tlvaux.SetPtEtaPhiM(jet['pt'],0.,jet['phi'],0.)
            wwwtlv -= tlvaux
    mettlv.SetPtEtaPhiM(met['pt'],0.,met['phi'],0.)
    leptlv.SetPtEtaPhiM(lep['pt'],lep['eta'],lep['phi'], 0.)
#    leptlv.SetPtEtaPhiM(e.muPt[0],e.muEta[0],e.muPhi[0],0.)
# calculate eta(W) estimate; take the + solution
    ptl = (wwwtlv - mettlv).Pt()
    ptn = mettlv.Pt()
    ptw = wwwtlv.Pt()
    etal = leptlv.Eta()
    A = (mw*mw + ptw*ptw - ptl*ptl - ptn*ptn) / (2.*ptl*ptn)
    if(A<1.): A=1.
    etaw = asinh((ptl*sinh(etal)+ptn*sinh(etal+acosh(A)))/ptw)
    if(abs(etaw)>10.): etaw=10*etaw/abs(etaw) # avoid too large values
    wwwtlv.SetPtEtaPhiM(wwwtlv.Pt(),etaw,wwwtlv.Phi(),mw)
# calulate boosted lepton momentum
    beta = wwwtlv.BoostVector()
    leptlv.Boost(-beta)
    return leptlv.P()


