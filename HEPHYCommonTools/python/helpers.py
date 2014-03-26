import ROOT
from math import pi, sqrt, cos, sin, sinh

def test():
  return 1

def getObjFromFile(fname, hname):
  f = ROOT.TFile(fname)
  assert not f.IsZombie()
  f.cd()
  htmp = f.Get(hname)
  if not htmp:  return htmp
  ROOT.gDirectory.cd('PyROOT:/')
  res = htmp.Clone()
  f.Close()
  return res

def passPUJetID(flag, level="Tight"): #Medium, #Loose,  kTight  = 0,   kMedium = 1,   kLoose  = 2
  if type(level)==type(0):
    return ( flag & (1 << level) ) != 0
  if level=="Tight":
    l=0
  if level=="Medium":
    l=1
  if level=="Loose":
    l=2
  return ( flag & (1 << l) ) != 0

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    return c.GetLeaf(leaf).GetValue(n)
  else:
    l = c.GetLeaf(var)
    if l:return l.GetValue(n)
    return float('nan')

#def getValue(chain, varname):
#  alias = chain.GetAlias(varname)
#  if alias!='':
#    return chain.GetLeaf( alias ).GetValue()
#  else:
#    return chain.GetLeaf( varname ).GetValue()
#

def deltaPhi(phi1, phi2):
  dphi = phi2-phi1
  if  dphi > pi:
    dphi -= 2.0*pi
  if dphi <= -pi:
    dphi += 2.0*pi
  return abs(dphi)

def minAbsDeltaPhi(phi, phis):
  if len(phis) > 0:
    return min([abs(deltaPhi(phi, x)) for x in phis])
  else: return float('inf')

def minAbsPiMinusDeltaPhi(phi, phis):
  if len(phis)>0:
    return min([abs(abs(deltaPhi(phi, x)) - pi) for x in phis])
  else: return float('inf')

def invMassOfLightObjects(p31, p32):
  [px1, py1, pz1] = p31
  [px2, py2, pz2] = p32
  px = px1+px2
  py = py1+py2
  pz = pz1+pz2
  p1 = sqrt(px1*px1+py1*py1+pz1*pz1)
  p2 = sqrt(px2*px2+py2*py2+pz2*pz2)
  p = sqrt(px*px+py*py+pz*pz)
  return   sqrt((p1 + p2)*(p1 + p2) - p*p)

def deltaR(l1, l2):
  return sqrt(deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2)

def getJets(c):
  njets = int(c.GetLeaf('njetCount').GetValue())
  jets =[]
  for i in range(njets):
    jets.append({'pt':getVarValue(c, 'jetPt', i), 'eta':getVarValue(c, 'jetEta', i), 'phi':getVarValue(c, 'jetPhi', i)})
  return jets

def minDeltaRLeptonJets(c):
  jets = getJets(c)
  return min([deltaR(j, {'phi':getVarValue(c, 'softIsolatedMuPhi'), 'eta':getVarValue(c, 'softIsolatedMuEta')}) for j in jets])

#def getSoftIsolatedMu(c):
#  return {'pt':c.GetLeaf('softIsolatedMuPt').GetValue(), 'eta':c.GetLeaf('softIsolatedMuEta').GetValue(), 'phi':c.GetLeaf('softIsolatedMuPhi').GetValue()}

def calcHTRatio(jets, metPhi):
  htRatio = -1
  den=0.
  num=0.
  for j in jets:
    den+=j["pt"]
    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
      num+=j["pt"]
  if len(jets)>0:
    htRatio = num/den
  return htRatio

def calcHTRatio(jets, metPhi):
  htRatio = -1
  den=0.
  num=0.
  for j in jets:
    den+=j["pt"]
    if abs(deltaPhi(metPhi, j["phi"])) <= pi/2:
      num+=j["pt"]
  if len(jets)>0:
    htRatio = num/den
  return htRatio

def findClosestJet(jets, obj):
##  jets = getJets(c)
  res=[]
  for j in jets:
    res.append([sqrt((j['phi'] - obj['phi'])**2 + (j['eta'] - obj['eta'])**2), j])
  res.sort()
  if len(res)>0:
    return {'deltaR':res[0][0], 'jet':res[0][1]}

def closestMuJetDeltaR(c):
  return findClosestJet(c, getSoftIsolatedMu(c))['deltaR']

def invMass(p1 , p2):

  pxp1 = p1['pt']*cos(p1['phi']) 
  pyp1 = p1['pt']*sin(p1['phi']) 
  pzp1 = p1['pt']*sinh(p1['eta'])
  Ep1 = sqrt(pxp1**2 + pyp1**2 + pzp1**2)

  pxp2 = p2['pt']*cos(p2['phi'])
  pyp2 = p2['pt']*sin(p2['phi'])
  pzp2 = p2['pt']*sinh(p2['eta'])
  Ep2 = sqrt(pxp2**2 + pyp2**2 + pzp2**2)

  return sqrt( (Ep1 + Ep2)**2 - (pxp1 + pxp2)**2 - (pyp1 + pyp2)**2 - (pzp1 + pzp2)**2)

def htRatio(c):
  jets = getJets(c)
  metPhi = c.GetLeaf('type1phiMetphi').GetValue()
#  print calcHTRatio(jets, metPhi)
  return calcHTRatio(jets, metPhi)

def KolmogorovDistance(s0, s1): #Kolmogorov distance from two list of values (unbinned, discrete)
  from fractions import Fraction, gcd

  s0.sort()
  s1.sort()

  tot = [[x,0] for x in s0] + [[x,1] for x in s1]
  tot.sort()
  F={}
  lenS={}
  lenS[0] = len(s0)
  lenS[1] = len(s1)
  F[0] = 0
  F[1] = 0
  l = len(tot)
#  print tot
  maxDist = Fraction(0,1)
  for i, t in enumerate(tot):
#    print "Now",F
    F[t[1]]+=1#lenS[t[1]]
#    print "...",F
    if i+1<l and tot[i+1][0]==t[0]:
      continue
#    print "Calc dist..."
    dist= abs(Fraction(F[0],lenS[0])-Fraction(F[1],lenS[1]))
    if dist>maxDist:
      maxDist=dist
#    print dist, maxDist
  return maxDist

def KolmogorovProbability(s0, s1):
  ksDist = float(KolmogorovDistance(s0, s1))
  return ROOT.TMath.KolmogorovProb(ksDist*sqrt(len(s0)*len(s1)/float(len(s0)+len(s1))))

def getISRweight(c, mode="Central"):
  ptISR = c.GetLeaf('ptISR').GetValue()
  if mode.lower()=='central':
    if ptISR<120:return 1.
    if ptISR<150:return .95
    if ptISR<250:return .90
    return 0.80
  if mode.lower()=='down':
    if ptISR<120:return 1.
    if ptISR<150:return .90
    if ptISR<250:return .80
    return 0.60
  if mode.lower()=='up':
    return 1.0

def getISRweightString(mode="Central", var="ptISR"):
    if mode.lower()=="down"   : return "(1.*("+var+"<120) + "+".90*( "+var+">120&&"+var+"<150) + "+".80*( "+var+">150&&"+var+"<250) + "+".60*( "+var+">250))"
    if mode.lower()=="up": return "(1)"
    return "(1.*("+var+"<120) + "+".95*( "+var+">120&&"+var+"<150) + "+".90*( "+var+">150&&"+var+"<250) + "+".80*( "+var+">250))"

def goodMuID(c, imu ):
  if isPF and (isGlobal or isTracker) and pt>5. and abs(eta)<2.1 and abs(dz)<0.5:
    return {'pt':pt, 'phi':getVarValue(c, 'muonsPhi', imu), 'eta':eta, 'IsGlobal':isGlobal, 'IsTracker':isTracker, 'IsPF':isPF, 'relIso':getVarValue(c, 'muonsPFRelIso', imu), 'Dz':dz}


def getHardestMuon(c):
  for imu in reversed(range(int(getVarValue(c, 'nmuCount')))):
    relIso = getVarValue(c, 'muRelIso', imu)
    pt = getVarValue(c, 'muPt', imu)
    if (pt<20. and pt*relIso<10) or (pt>20. and relIso<0.2):
      return {'pt':getVarValue(c, 'muPt', imu), 'eta':getVarValue(c, 'muEta', imu), 'phi':getVarValue(c, 'muPhi', imu), 'pdg':getVarValue(c, 'muPdg', imu)}
def calcMT(lepton, met):
  if lepton and met:
    return sqrt(2.*met['pt']*lepton['pt']*(1-cos(lepton['phi'] - met['phi'])))
  else:
    return float('nan')