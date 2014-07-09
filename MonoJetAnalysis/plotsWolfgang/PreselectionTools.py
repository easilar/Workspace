import math
from EventHelper import EventHelper
from KinematicUtilities import *
from LeptonUtilities import *

isrJetPtMin = 110
njet60Max = 2
type1phiMetMin = 200.
htMin = 300.
isrJetBTBVeto = True
softIsolatedPtMin = ( 7., 5. )
softIsolatedPtMax = ( 20., 20. )
hardIsolatedPtMin = ( 30., 30. )
softIsolatedEtaMax = ( 999., 999. )
regionIndices = { "SR1a" : 0, "SR1b" : 1, "SR1c" : 2, "SR2" : 3,
                  "CR1a" : 4, "CR1b" : 5, "CR1c" : 6, "CR2" : 7 }

def passesHadronicSelection(eh,recalculatedMet=None):
    isrJetPt = eh.get("isrJetPt")
    if math.isnan(isrJetPt) or isrJetPt<isrJetPtMin:
        return False

    met = eh.get("type1phiMet") if recalculatedMet==None else recalculatedMet
    if math.isnan(isrJetPt) or met<type1phiMetMin:
        return False

    if eh.get("njet60")>njet60Max:
        return False

#
# match with HT-binned W+jets sample
#
    if eh.get("ht")<htMin:
        return False

    assert not math.isnan(eh.get("isrJetBTBVetoPassed"))
    if isrJetBTBVeto and eh.get("isrJetBTBVetoPassed")==0:
        return False

    return True

def selectedLepton(eh,leptonPdg,mode="all"):

    leptonSel = mode.lower()

    leptons = ( ( 11, "el" ) , ( 13, "mu" ) )
    leptonIndex = None
    for i,l in enumerate(leptons):
        if abs(leptonPdg)==l[0]:
            leptonIndex = i
            leptonPrefix = l[1]
            break
    assert leptonIndex!=None

    if eh.get("nHardTaus")>0:
        return None

    if abs(leptonPdg)==11:
        if eh.get("nHardMuonsMediumWP")>0:
            return None
        ileptons = isolatedElectrons(eh,ptmin=softIsolatedPtMin[leptonIndex], \
                                         etamax=softIsolatedEtaMax[leptonIndex])
    else:
        if eh.get("nHardElectrons")>0:
            return None
#        mediumMuIndex = int(eh.get("mediumMuIndex"))
#        if mediumMuIndex<0:
#            return None
        ileptons = isolatedMuons(eh,ptmin=softIsolatedPtMin[leptonIndex], \
                                     etamax=softIsolatedEtaMax[leptonIndex])

    if len(ileptons)==0:
        leptonPts = eh.get(leptonPrefix+"Pt")
        mediumMuIndex = int(eh.get("mediumMuIndex"))
        if ( mediumMuIndex>-1 and ( leptonPts[mediumMuIndex]<20 or int(eh.get("nHardMuonsMediumWP"))==1 ) ):
            print "***** inconsistency A ",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
                eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP")
        return None

        
    ilepton = ileptons[0]


    leptonEtas = eh.get(leptonPrefix+"Eta")
    if abs(leptonEtas[ilepton])>softIsolatedEtaMax[leptonIndex]:
        return None

    leptonPts = eh.get(leptonPrefix+"Pt")
    leptonPt = leptonPts[ilepton]
    # require minimum Pt
    if leptonPt<softIsolatedPtMin[leptonIndex]:
        mediumMuIndex = int(eh.get("mediumMuIndex"))
        if ( mediumMuIndex>-1 and ( leptonPts[mediumMuIndex]<20 or int(eh.get("nHardMuonsMediumWP"))==1 ) ):
            print "***** inconsistency B ",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
                eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP")
        return None

#    mediumsoft = [ ]
#    mediumhard = [ ]
#    for i in range(len(ileptons)):
#        if leptonPts[i]<20:
#            mediumsoft.append(i)
#        if leptonPts[i]>20:
#            mediumhard.append(i)
#    if ( len(mediumsoft+mediumhard)==0 and eh.get("mediumMuIndex")>-1 ) or \
#            ( len(mediumsoft+mediumhard)>0 and eh.get("mediumMuIndex")<0 ):
#        print "***** inconsistency mediumMuIndex (soft)",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
#            eh.get("lumi"),eh.get("event"),mediumsoft,eh.get("mediumMuIndex")
#    if len(mediumhard)==0!=int(eh.get("nHardMuonsMediumWP")):
#        print "***** inconsistency mediumMuIndex (hard)",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
#            eh.get("lumi"),eh.get("event"),mediumhard,eh.get("nHardMuonsMediumWP")

    # veto other leptons above 20GeV
    for i in range(len(ileptons)):
        j = ileptons[i]
        if j!=ilepton and leptonPts[j]>softIsolatedPtMax[leptonIndex]:
            mediumMuIndex = int(eh.get("mediumMuIndex"))
            if ( mediumMuIndex>-1 and ( leptonPts[mediumMuIndex]<20 or int(eh.get("nHardMuonsMediumWP"))==1 ) ):
                print "***** inconsistency C ",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
                    eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP"),i,j,ilepton,ileptons,leptonPts,leptonEtas,eh.get("muRelIso")
            if int(eh.get("run"))==193336 and int(eh.get("lumi"))==925 and eh.get("event")==661128520:
                print "Returning False"
            return None
    
    if int(eh.get("run"))==193336 and int(eh.get("lumi"))==925 and eh.get("event")==661128520:
        mediumMuIndex = int(eh.get("mediumMuIndex"))
        print "***** inconsistency AAA ",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
            eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP"),ileptons,eh.get("muPt"),eh.get("muEta"),eh.get("muRelIso")


    if leptonSel=="soft":
        if leptonPt>softIsolatedPtMax[leptonIndex]:
            return None
    elif leptonSel=="hard":
        if leptonPt<hardIsolatedPtMin[leptonIndex]:
            return None
#    else:
#        mediumMuIndex = int(eh.get("mediumMuIndex"))
#        if not ( mediumMuIndex>-1 and ( leptonPts[mediumMuIndex]<20 or int(eh.get("nHardMuonsMediumWP"))==1 ) ):
#            print "***** inconsistency",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
#                eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP")
            
    mediumMuIndex = int(eh.get("mediumMuIndex"))
    if ( mediumMuIndex<0 or ( leptonPts[mediumMuIndex]>20 and int(eh.get("nHardMuonsMediumWP"))>1 ) ):
        print "***** inconsistency D ",eh.tree.GetCurrentFile().GetName(),eh.get("run"), \
            eh.get("lumi"),eh.get("event"),ilepton,mediumMuIndex,eh.get("nHardMuonsMediumWP"),ilepton,ileptons,leptonPts,leptonEtas,eh.get("muRelIso")

    return ( ilepton, leptonPrefix )

def bjetMultiplicity(eh):
    njet = int(eh.get("njetCount")+0.5)
    jetPts = eh.get("jetPt")
    jetEtas = eh.get("jetEta")
    jetBtags = eh.get("jetBtag")
    nbsoft = 0
    nbhard = 0
    for i in range(njet):
        if jetPts[i]>30 and abs(jetEtas[i])<2.4 and jetBtags[i]>0.679:
            if jetPts[i]<60:
                nbsoft += 1
            else:
                nbhard += 1
    return (nbsoft,nbhard)
    
def signalOrControlRegion(eh,ilep,prefix):
    # btags
    nbsoft, nbhard = bjetMultiplicity(eh)
    nball = nbsoft + nbhard

    met = eh.get("type1phiMet")
    if met<300.:
        return None

    # R1
    if nball==0 and eh.get("ht")>400:
        softLepPt = eh.get(prefix+"Pt")[ilep]
        softLepPhi = eh.get(prefix+"Phi")[ilep]
        metphi = eh.get("type1phiMetphi")
        mt = math.sqrt(2*met*softLepPt*(1-math.cos(metphi-softLepPhi)))
        if mt<60:
            return "R1a"
        elif mt>88:
            return "R1c"
        else:
            return "R1b"

    # CR2
    if nbsoft>0 and nbhard==0:
        if eh.get("isrJetPt")>325:
            return "R2"
        
    return None

def signalRegion(eh,ilep,prefix):
    region = signalOrControlRegion(eh,ilep,prefix)
    if region==None:
        return region

    softLepPt = eh.get(prefix+"Pt")[ilep]
    if softLepPt>5. and softLepPt<20.:
        return "S"+region

    return None

def controlRegion(eh,ilep,prefix):
    region = signalOrControlRegion(eh,ilep,prefix)
    if region==None:
        return region

    softLepPt = eh.get(prefix+"Pt")[ilep]
    if softLepPt>30.:
        return "S"+region

    return None