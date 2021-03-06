from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex , dict_operator, any_in, whichIn 
import os,sys
import pickle
import numpy as np
from copy import deepcopy

def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

#def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
#    """
#    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
#    """ 
#    args = [ yldsByBin[x] for x in keys]
#    return func(*args) 



def getPkl( pkl_path, def_dict={}):
    pkl_path = os.path.expandvars(pkl_path)
    print 'get pkl %s'%pkl_path
    if os.path.isfile( pkl_path):
        try:
            ret = pickle.load( open(pkl_path,'r') )
            
        except:
            print "Something wrong with the pickle file:\n %s \n Got this Error: \n %s"%(pkl_path, sys.exc_info()[0] )
            raise
    else:
        ret = deepcopy( def_dict )
        print "def", ret.keys()
    return ret


make_lumi_tag = lambda l: "%0.0fpbm1"%(l)
absSysFunc    = lambda a,b : (abs(1.- (b/a).val)   * 100) if a.val else 0
SignedSysFunc = lambda a,b : ((-1.+ (b/a).val)   * 100) if a.val else 0
#sysFunc    = lambda a,b : abs((b/a).val)  
#sysPercFunc= lambda a,b : abs(1.-(b/a).val)   
mean   = lambda l :   sum(l)/float(len(l)) if len(l) else None

w   = "WJets"
tt  = "TTJets"
qcd = "QCD"
z   = "ZJetsInv"

def meanSys(*a):
    """assume first value is the central value"""
    central = a[0]
    variations = a[1:]
    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    for var in variations:
        systs.append( absSysFunc(central, var) ) 
    #print systs, mean(systs)
    return mean(systs)



qpairs = [
           ( 'Q2centralup' , 'Q2centraldown'  )  ,
           ( 'Q2upcentral' , 'Q2downcentral'  )  ,
           ( 'Q2updown'    , 'Q2downup'  )          ,
         ]
qvariations = ['Q2_centralcentral', 'Q2_centralup', 'Q2_centraldown', 'Q2_upcentral', 'Q2_downcentral', 'Q2_updown', 'Q2_downup']

def q2EvSys(*a):
    """assume first value is the central value"""
    central = a[0]
    variations = a[1:]
    assert len(a)==7

    qsysts = []
    for nq in range(len(qvariations)):
        qvars = variations[nq:nq+2]
        print list(qvars)
        print [central]
        print list(qvars) + [central]
        qsysts.append( meanSys(*[central]+list(qvars) ) )

    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    for var in variations:
        systs.append( absSysFunc(central, var) ) 
    #print systs, mean(systs)
    return mean(systs)
    
def meanSysSigned(*a): ### keep track of the signs somehow for systematics in cards
    """assume first value is the central value
    """
    central = a[0]
    variations = a[1:]
    if not variations:
        raise Exception("No Variations Given! %s"%a)
    systs = []
    sign = 1
    #signed_systs = []
    for var in variations:
        syst_val = sign*SignedSysFunc(central, var) 
        #syst_val = SignedSysFunc(central, var) 
        systs.append( syst_val) 
        #signed_systs.append( sign* syst_val ) 
        sign *= -1
    print systs
    #print signed_systs
    #print systs, mean(systs)
    syst_sign = (sum(systs) < 0)*(-1) + (sum(systs) >= 0)*(1)
    syst_mean = mean([abs(x) for x in systs])
    return syst_sign * syst_mean 
    

import itertools
def addInQuad(l):
    s = 0
    for v in l:
        s += v**2
    return math.sqrt(s) 
def addInQuad100PerctCorr(l):
    s = 0
    for v in l:
        s += v**2
    chi = 0
    for e1,e2 in itertools.combinations(l,2):
        #print e1,e2
        chi += e1*e2
    chi = 2*chi
    #print 'math.sqrt(%s+%s)'%(s,chi)
    return math.sqrt(s+chi) 




regions =  [\
                     'SRL1a',
                     'SRH1a',
                     'SRV1a',
                     '\hline',
                     'SR1a',
                     '\hline',
                     'SRL1b',
                     'SRH1b',
                     'SRV1b',
                     '\hline',
                     'SR1b',
                     '\hline',
                     'SRL1c',
                     'SRH1c',
                     'SRV1c',
                     '\hline',
                     'SR1c',
                     '\hline',
                     'SRL2',
                     'SRH2',
                     'SRV2',
                     '\hline',
                     'SR2',
                     '\hline',
                     #'\hline',
                     '\hline',
                     'CR1a',
                     'CR1b',
                     'CR1c',
                     'CR2',
                     'CRTT2',
                        ]
bins = [x for x in regions if 'hline' not in x]
main_sr =[
            'SR1a',
            'SR1b',
            'SR1c',
            'SR2',
         ]
main_cr =[
            'CR1a',
            'CR1b',
            'CR1c',
            'CR2',
         ]



#sf_bins_map={\
#                     'SRL1a'         : "CR1a",
#                     'SRH1a'         : "CR1a",
#                     'SRV1a'         : "CR1a",
#                     'SR1a'          : "CR1a",
#                     'SRL1b'         : "CR1b",
#                     'SRH1b'         : "CR1b",
#                     'SRV1b'         : "CR1b",
#                     'SR1b'          : "CR1b",
#                     'SRL1c'         : "CR1c",
#                     'SRH1c'         : "CR1c",
#                     'SRV1c'         : "CR1c",
#                     'SR1c'          : "CR1c",
#                     'SRL2'          : "CR2",
#                     'SRH2'          : "CR2",
#                     'SRV2'          : "CR2",
#                     'SR2'           : "CR2",
#                     'CR1a'          : "",
#                     'CR1b'          : "",
#                     'CR1c'          : "",
#                     'CR2'           : "",
#                     'CRTT2'         : "",
#                        }
#
otherBkg = ['DYJetsM50', 'ST', 'Diboson']


card_bins =[ x for x in bins if x not in main_sr]
pt_srs = [x for x in bins if 'SR' in x and x not in main_sr]

WPtShape_bins  = { '1a': 10 , '1b': 20, '1c':30, '2':20}
ttPtShape_bins = 20#{ '1a': 20 , '1b': 20, '1c':20, '2':20}


w_uncert_sr1a = WPtShape_bins['1a']
w_uncert_sr1b = WPtShape_bins['1b']
w_uncert_sr1c = WPtShape_bins['1c']
w_uncert_sr2  = WPtShape_bins['2']
tt_uncert     = ttPtShape_bins #self.CR_SFs[variation]['CRTT2'][tt]
zinv_uncert   = 50
small_bkg_uncert= 50
ptShapeUncerts={
    w:{\
        'SRL1a':  w_uncert_sr1a     ,
        'SRH1a':  w_uncert_sr1a     ,
        'SRV1a':  w_uncert_sr1a     ,
        'SR1a' :  w_uncert_sr1a     ,
        'SRL1b':  w_uncert_sr1b     ,
        'SRH1b':  w_uncert_sr1b     ,
        'SRV1b':  w_uncert_sr1b     ,
        'SR1b' :  w_uncert_sr1b     , 
        'SRL1c':  w_uncert_sr1c     ,
        'SRH1c':  w_uncert_sr1c     ,
        'SRV1c':  w_uncert_sr1c     ,
        'SR1c' :  w_uncert_sr1c     ,
        'SRL2' :  w_uncert_sr2      ,
        'SRH2' :  w_uncert_sr2      ,
        'SRV2' :  w_uncert_sr2      ,
        'SR2'  :  w_uncert_sr2      ,
      },
    tt:{\
        'SRL1a':  tt_uncert     ,
        'SRH1a':  tt_uncert     ,
        'SRV1a':  tt_uncert     ,
        'SR1a' :  tt_uncert     ,
        'SRL1b':  tt_uncert     ,
        'SRH1b':  tt_uncert     ,
        'SRV1b':  tt_uncert     ,
        'SR1b' :  tt_uncert     , 
        'SRL1c':  tt_uncert     ,
        'SRH1c':  tt_uncert     ,
        'SRV1c':  tt_uncert     ,
        'SR1c' :  tt_uncert     ,
        'SRL2' :  tt_uncert     ,
        'SRH2' :  tt_uncert     ,
        'SRV2' :  tt_uncert     ,
        'SR2'  :  tt_uncert     ,
        }
    }
other_bkg_sys={}
other_bkg_sys.update({
    z:{\
        'SRL1a':  zinv_uncert     ,
        'SRH1a':  zinv_uncert     ,
        'SRV1a':  zinv_uncert     ,
        'SR1a' :  zinv_uncert     ,
        'SRL1b':  zinv_uncert     ,
        'SRH1b':  zinv_uncert     ,
        'SRV1b':  zinv_uncert     ,
        'SR1b' :  zinv_uncert     , 
        'SRL1c':  zinv_uncert     ,
        'SRH1c':  zinv_uncert     ,
        'SRV1c':  zinv_uncert     ,
        'SR1c' :  zinv_uncert     ,
        'SRL2' :  zinv_uncert     ,
        'SRH2' :  zinv_uncert     ,
        'SRV2' :  zinv_uncert     ,
        'SR2'  :  zinv_uncert     ,
      },
    "small_bkg_uncert":{\
        'SRL1a':  small_bkg_uncert     ,
        'SRH1a':  small_bkg_uncert     ,
        'SRV1a':  small_bkg_uncert     ,
        'SR1a' :  small_bkg_uncert     ,
        'SRL1b':  small_bkg_uncert     ,
        'SRH1b':  small_bkg_uncert     ,
        'SRV1b':  small_bkg_uncert     ,
        'SR1b' :  small_bkg_uncert     , 
        'SRL1c':  small_bkg_uncert     ,
        'SRH1c':  small_bkg_uncert     ,
        'SRV1c':  small_bkg_uncert     ,
        'SR1c' :  small_bkg_uncert     ,
        'SRL2' :  small_bkg_uncert     ,
        'SRH2' :  small_bkg_uncert     ,
        'SRV2' :  small_bkg_uncert     ,
        'SR2'  :  small_bkg_uncert     ,
      },

 #'CR1a':
 #'CR1b':
 #'CR1c':
 #'CR2' :
    })


qcd_pred_pkl = "/afs/hephy.at/user/m/mzarucki/public/results/QCD/QCDyields_final_stat.pkl"  
qcd_pred     = pickle.load( open(qcd_pred_pkl) ) 
qcd_sys_pkl  = "/afs/hephy.at/user/m/mzarucki/public/results/QCD/QCDyields_final_sys.pkl"  
qcd_sys      = pickle.load( open(qcd_sys_pkl) ) 

zinv_el_sf_pkl = "/afs/hephy.at/user/m/mzarucki/public/results/Zinv/ZinvSFs_electrons_stat.pkl"
zinv_mu_sf_pkl = "/afs/hephy.at/user/m/mzarucki/public/results/Zinv/ZinvSFs_muons_stat.pkl"
zinv_el_sf     = pickle.load(open(zinv_el_sf_pkl,'r'))
zinv_mu_sf     = pickle.load(open(zinv_mu_sf_pkl,'r'))


wpol_sys_pkl  = "/afs/hephy.at/user/m/mzarucki/public/results/Wpol/WpolSysUnc.pkl"  
wpol_sys      = pickle.load( open(wpol_sys_pkl) ) 

other_bkg_sys.update({w:wpol_sys})


#
# Turning Other Background Systematics to Percents for consistancy
#
#other_bkg_sys = {}
for samp,syst in {'QCD':qcd_sys}.iteritems():
    other_bkg_sys[samp] = {}
    for b in syst:
        val,err = (syst[b].val, syst[b].sigma)
        perc_err = err/val * 100 if val else 0
        other_bkg_sys[samp][b]= perc_err



lepCol = "LepAll"
lep    = "lep"
puRunTagParams =    {   
                    'up'    :   { 'pu':'pu_up' },
                    'down'  :   { 'pu':'pu_down' },
                    }
SigAndBkgTagParams       =   {
                      ##"central":\
                      ##      {
                      ##          ''  :   { },
                      ##      },
                      "PU":\
                            {
                                'up'    :   { 'pu':'pu_up' },
                                'down'  :   { 'pu':'pu_down' },
                            },
                      "BTag_l":\
                            {
                                'up'    :   { 'btag':'SF_L_UP'  },
                                'down'  :   { 'btag':'SF_L_DOWN'  },
                            },
                      "BTag_b":\
                            {
                                'up'    :   { 'btag':'SF_B_UP'  },
                                'down'  :   { 'btag':'SF_B_DOWN'  },
                            },
                      "jec":\
                            {
                                'up'    :   { 'jec':'jec_up' },
                                'down'  :   { 'jec':'jec_down' },
                            },
                      "jer":\
                            {
                                'up'    :   { 'jer':'jer_up' },
                                'down'  :   { 'jer':'jer_down' },
                            },
                      "lepEff":\
                            {  
                               'up':    { 'other': 5. }
                            },



                    }

#bkgTagParams =   deepcopy( SigAndBkgTagParams )
bkgTagParams  = {}
bkgTagParams.update( {
                      #"WPol":\
                      #      {
                      #         'up':    { 'other': {w : other_bkg_sys[w] }  } 
                      #      },
                      "WPt":\
                            {
                                '1x'  :   { 'wpt':'_wpt'  },
                            },
                      #"ttpt":\
                      #      {
                      #          '1x'  :   { 'ttpt':'_ttpt'  },
                      #      },
                      #"ttPtShape":\
                      #      {  
                      #         'up':    { 'other': {tt: ptShapeUncerts[tt] }  } 
                      #      },
                      #"WPtShape":\
                      #      {  
                      #         'up':    { 'other': {w : ptShapeUncerts[w] }  } 
                      #      },
                      #"QCDEst":
                      #      {
                      #         'up':    { 'other': {qcd : other_bkg_sys[qcd] }  } 
                      #      },
                      #"ZInvEst":
                      #      {
                      #         'up':    { 'other': {z : other_bkg_sys[z] }  } 
                      #      },
                    })
bkgTagParams.update({
                      #"%sXSec"%x: { 
                      #          'up':      { 'other': {x   : other_bkg_sys['small_bkg_uncert'] }}
                      #      } for x in otherBkg
                    })




#sigTagParams = { key,val for key,val in tagParams.iteritems() if key in ['PU','BTag_b', 'BTag_l', "jec", "jer", 'lepEff'] }
#sigTagParams = deepcopy( SigAndBkgTagParams )
sigTagParams = deepcopy( {} )
sigTagParams.update({

                      #"Lumi":\
                      #      {  
                      #         'up':    { 'other': 6.2 }
                      #      },
                      #"FastFullEff":\
                      #      {  
                      #         'up':    { 'other': 5.  }
                      #      },
                      "BTag_FS":
                            {
                                'up'    :   { 'btag':'SF_FS_UP'  },
                                'down'  :   { 'btag':'SF_FS_DOWN'  },
                            },

                      "met":\
                            {
                                'GenMET' :   { 'met':'met_gen' },
                                'MET'    :   { 'met':'met_met' },       # same as central. in order to average the systematics
                            },
                      "Q2":\
                            {  
                                 #'upup'           :   {'lhe':'_Q2upup'            }   ,
                                 'centralcentral' :   {'lhe':'_Q2centralcentral'  }   ,
                                 #'downdown'       :   {'lhe':'_Q2downdown'        }   ,
                                 'downup'         :   {'lhe':'_Q2downup'          }   ,
                                 'updown'         :   {'lhe':'_Q2updown'          }   ,
                                 'downcentral'    :   {'lhe':'_Q2downcentral'     }   ,
                                 'centralup'      :   {'lhe':'_Q2centralup'       }   ,
                                 'centraldown'    :   {'lhe':'_Q2centraldown'     }   ,
                                 'upcentral'      :   {'lhe':'_Q2upcentral'       }   ,
                            },
                      "ISR":\
                            {
                                'noisr' :   { 'isr':'_noisr' },
                                'rewgt' :   { 'isr':'' },       ## same as central in order to average the systematics
                            },
                      }
                    ) 


#tagParams = { key:val for key,val in tagParams.iteritems() if key in ["ZInvEst"] }#, "SmallBkg", "PU"] or "XSec" in key}


centralParamsBkg   =   { 
                    'lepCol':lepCol,
                    'lep'   :lep,
                    'pu'    :'pu',
                    'btag'  :'SF',
                    'jec'   :'',
                    'jer'   :'',
                    'wpt'   :'',
                    'ttpt'  :'',
                    'met'   :'',
                    'lhe'   :'',
                    'isr'   :'',
                    }
centralParamsSig   =   { 
                    'lepCol':lepCol,
                    'lep'   :lep,
                    'pu'    :'pu',
                    'btag'  :'SF',
                    'jec'   :'',
                    'jer'   :'',
                    'wpt'   :'',
                    'ttpt'  :'',
                    'met'   :'',
                    'lhe'   :'',
                    #'isr'   :'_isr',
                    'isr'   : '',
                    }

class Systematics():
    def __init__(self, cfg, variationTagParams = puRunTagParams, centralParams = {}, name = "Syst", syst_type = "bkg"):
        self.name = name
        self.syst_name = name
        temp_dict = {}

        isBkgSys = False
        isSigSys = False
        if syst_type == "bkg":
            isBkgSys = True
        if syst_type == "sig":
            isSigSys = True
        if syst_type == "both":
            isSigSys = True
            isBkgSys = True

        original_variations = variationTagParams.keys()
        if any( [ 'central' in x for x in original_variations]):
            makeCentral = False
            variations  = []
        else:
            makeCentral = True
            variations = ['%s_central'%self.name]
        for key, val in variationTagParams.iteritems():
            for def_key, def_val in centralParams.iteritems():
                val.setdefault(def_key, def_val)
            temp_dict["%s_%s"%(self.name, key)] = val
        variations.extend( temp_dict.keys() )
        if makeCentral:
            temp_dict['%s_central'%self.name] = {}
            for def_key, def_val in centralParams.iteritems():
                temp_dict['%s_central'%self.name].setdefault(def_key, def_val)
        data          = 'DataBlind'
        data_lumi_tag = '%s_lumi'%data
        #for var, params in variationTagParams.iteritems():
        #    if params.get("jec"):
        #        isJEC = True
        #    if params.get("jer"):
        #        isJER = True
        self.variationTagParams = variationTagParams
        variationTagParams      = temp_dict
        #print variationTagParams
        sys_label       = "AdjustedSys"
        cut_name        = cfg.cutInstList[0].fullName
        self.yieldPkls  = {}
        self.yields     = {}
        self.yieldDict  = {}
        self.yieldTotals= {}
        variation_dict  = {}
        #variations = variationTagParams.keys()
        self.variations = variations
        tags            = variations
        self.runTags    = {} 
        print ""
        for variation, params in variationTagParams.iteritems():
            runTag_prefix = cfg.runTag.split("_")[0]
            print "Printing variation, params in variationTagParams: ", params
            runTag = ('%s_Mt95_Inccharge_{lepCol}_{lep}_{pu}{isr}{lhe}{wpt}{ttpt}_{btag}'%runTag_prefix).format(**params)
            self.runTags[variation] = runTag
            results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
            #lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
            lumiTag              =  make_lumi_tag( cfg.lumi_info[data_lumi_tag] )
            self.yieldPkls[variation]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
            if params.get('WPol'):
                print variation, params,
                assert False, 'what to do now'
    
            if params.get('jec') or params.get('jer'):
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'/presel/', u'/presel_%s/'%variation)
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'.pkl', u'_%s.pkl'%variation)
            if params.get('met'):
                vt   = variation.replace("met_","").replace("central","GenMET")
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'/presel/', u'/presel_%s/'%vt)
                self.yieldPkls[variation] = self.yieldPkls[variation].replace(u'.pkl', u'_%s.pkl'%vt)
                print params.get("met")
                print vt, variation
            #print self.yieldPkls
            self.yields[variation]        =  pickle.load(file( self.yieldPkls[variation]  ))
            self.yieldDict[variation]     =  self.yields[variation].getNiceYieldDict()
            #self.yieldTotals[variation]   =  self.yieldDict[variation]['Total']
            for samp  in self.yieldDict[variation].keys():
                if "FOM" in samp:
                    self.yieldDict[variation].pop(samp)
        samples = [x for x in self.yieldDict[tags[0]].keys() if "FOM" not in x]

        self.samples    =  samples
        self.bkgTotList =  [x for x in samples if "Data" not in x and "SMS" not in x and "T2tt" not in x and "FOM" not in x]
        self.bkgList    =  [x for x in self.bkgTotList if "Total" not in x ]
        self.bkgTotList =  self.bkgList + ['Total']
        self.sigList    =  sorted( [x for x in samples if ("SMS" in x or "T2tt" in x) and "FOM" not in x] )

        ##
        ## creating yieldDict with flat systs (Lumi, pt shape uncerts, etc)
        ##
        other_uncerts = {} 
        for variation_ in self.variationTagParams.keys():
            variation = self.name + "_" + variation_
            if 'other' in self.variationTagParams[variation_]:
                other_uncerts[variation]={}
                otherUnc = self.variationTagParams[variation_]['other']  # in percent
                #print "......................", variation_, variation, otherUnc
                if type(otherUnc) in [float, int]:
                    flatUnc = otherUnc
                

                for samp in self.bkgList + self.sigList:
                    other_uncerts[variation][samp]={}
                    for b, val in self.yieldDict[variation][samp].iteritems():
                        #self.yieldDict[variation][samp] = flatUnc/100. * self.yieldDict[variation][samp] 
                        if type(otherUnc) in [float, int]:
                            unc_val = otherUnc
                        else:
                            try:
                                unc_val = otherUnc[samp][b]
                            except KeyError:
                                #print "did not find the following keys %s,%s"%(samp,b) , otherUnc
                                unc_val = 0.
                        other_uncerts[variation][samp][b]  = unc_val
                        #self.yieldDict[variation][samp][b] = (1+ unc_val/100.) * val
                        #print '-+-+-+ ', samp, variation, unc_val, val, self.yieldDict[variation][samp][b]

                
        if "ZJetsInv" in samples and isBkgSys:
            mu_yield_inst = self.yieldPkls[variations[0]].replace("lep","mu")
            el_yield_inst = self.yieldPkls[variations[0]].replace("lep","el")
            yieldDictMu   = pickle.load(open(mu_yield_inst,'r')).getNiceYieldDict()
            yieldDictEl   = pickle.load(open(el_yield_inst,'r')).getNiceYieldDict()
            print 'zinv yield insts:'
            print mu_yield_inst
            print el_yield_inst

        
                    


        #    print variation , params
        #    print params.get('jec')
        #assert False
        #self.res =    dict_manipulator( [ yields['pu_down'].getNiceYieldDict()['Total'] , yields['pu_up'].getNiceYieldDict()['Total'] , yields['pu'].getNiceYieldDict()['Total'] ] , lambda a,b,c: ( abs(1.-(a/c).val) + abs(1.-(b/c).val) )/2. * 100)

        #self.tot_sys      =  dict_manipulator( [self.yieldDict[x]["Total"] for x in variations  ] , lambda *vals : meanSys(*vals)  )   

        self.res_dir      = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )
        self.cr_sfs_path  = "%s/CR_SFs.pkl"%self.res_dir
        yldinsts_dir      = "%s/YieldInsts/"%(self.res_dir)
        ylds_dir          = "%s/YieldDicts/"%(self.res_dir)
        global_yield_pkl  = "%s/YieldDictWithVars.pkl"%(self.res_dir)
        global_sf_pkls    = "%s/BkgSFs.pkl"%(self.res_dir)
        global_bkgpred_pkl= "%s/BkgPredWithVars.pkl"%(self.res_dir)
        makeDir(ylds_dir)
        makeDir(yldinsts_dir)

        other_predictions = {
                          "QCD"         : {'pkl_path': qcd_pred_pkl },
                          # z           : {'el'      : zinv_el_sf },
                          # "ZJetsInv"  : {'pkl_path':""},
                       }
        for samp in other_predictions:
            other_predictions[samp]['dict'] = pickle.load( open(other_predictions[samp]['pkl_path']))


        #
        #   Dealing with Met for FastSim Signal
        #

        if True and isSigSys and  any(["genmet" in x.lower() for x in variations]):
            print "MET SYST! .... Averaging MET and GEN MET acceptances"
            yieldDictCentral = self.yieldDict[variations[0]]
            #yieldDictCentral = deepcopy( self.all_yield_dict['PU_central'] )
            for samp in self.sigList:
                for b, yl in yieldDictCentral[samp].iteritems():
                    ave_yl = (self.yieldDict[variations[1]][samp][b] + self.yieldDict[variations[2]][samp][b]) / 2.
                    #print samp, b,  yl,  self.yieldDict[variations[1]][samp][b] , self.yieldDict[variations[2]][samp][b], ave_yl
                    yieldDictCentral[samp][b] = ave_yl




        #
        # Loading SF
        #
        self.bkg_est_dir = {}
        self.CR_SFs      = {}
        self.SFs         = {}
        self.bkg_ests    = {}
        for variation, runTag in self.runTags.iteritems():

            self.bkg_ests[variation]={}
            #self.bkg_est_dir[variation] = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
            self.bkg_est_dir[variation] = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, runTag)
            self.bkg_est_dir[variation] = os.path.expandvars( self.bkg_est_dir[variation] )

            if not os.path.isfile(self.bkg_est_dir[variation] + "/CR_SFs.pkl" ) :
                self.bkg_est_dir[variation] = os.path.expandvars( "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/BkgEst/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )

            #print self.bkg_est_dir
            if isBkgSys:
                self.CR_SFs[variation]      = pickle.load(file(self.bkg_est_dir[variation]+"/CR_SFs.pkl"))
            else:
                self.CR_SFs[variation]      = pickle.load(file(self.bkg_est_dir[variations[0]]+"/CR_SFs.pkl"))
    
            #sf_bin_keys = [ '1a' , '1b' , '1c', '2']
            #SFs = {}
    
            w_sf_sr1a = self.CR_SFs[variation]['CR1a'][w]
            w_sf_sr1b = self.CR_SFs[variation]['CR1b'][w]
            w_sf_sr1c = self.CR_SFs[variation]['CR1c'][w]
            w_sf_sr2  = self.CR_SFs[variation]['CR2'][w]
            tt_sf     = self.CR_SFs[variation]['CRTT2'][tt]
    
            SFs={ 
             'SRL1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
             'SRH1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
             'SRV1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
             'SR1a' :{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
             'SRL1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
             'SRH1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
             'SRV1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
             'SR1b' :{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
             'SRL1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf }, 
             'SRH1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf }, 
             'SRV1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
             'SR1c' :{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf },
             'SRL2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
             'SRH2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
             'SRV2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },
             'SR2'  :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf },

             'CR1a':{qcd:1.0 , z:1.0 , w: w_sf_sr1a , tt: tt_sf }, 
             'CR1b':{qcd:1.0 , z:1.0 , w: w_sf_sr1b , tt: tt_sf }, 
             'CR1c':{qcd:1.0 , z:1.0 , w: w_sf_sr1c , tt: tt_sf }, 
             'CR2' :{qcd:1.0 , z:1.0 , w: w_sf_sr2  , tt: tt_sf }, 
            }
    
            self.SFs[variation] = SFs


            #print "OTHER UNCERTS", other_uncerts
            ##
            ##  New YieldDict taking into account the SFs
            ##

            #for samp, binylds in self.yieldDict[variation].iteritems():
            for samp  in self.bkgList+self.sigList:
                #print self.yieldDict[variation].keys()
                binylds = self.yieldDict[variation][samp]
                self.bkg_ests[variation][samp]={}
                for b, y in binylds.iteritems():
                    ##
                    ## get sf:
                    ##
                    if b in SFs and samp in SFs[b]:
                        sf = SFs[b][samp]
                    else:
                        sf = u_float(1)
                    #print samp, b, sf
                    self.bkg_ests[variation][samp][b]=sf*y
                    ##
                    ##  For backgrounds predicated seperately
                    ##
                    if samp in other_predictions.keys():
                        # print variation 
                        #print other_predictions[samp]['dict'].keys()
                        #for b in self.bkg_ests[variation][samp].keys():
                        if b in other_predictions[samp]['dict']:
                            self.bkg_ests[variation][samp][b] = other_predictions[samp]['dict'][b]
                            #print "OTHER PREDS:" , samp, b, self.bkg_ests[variation][samp][b], other_predictions[samp]['dict'][b]
                        else:
                            print "NOT IN OTHER PRED" , samp, b, other_predictions[samp]['dict'].keys() 
                    elif samp=="ZJetsInv" and isBkgSys:
                        mu_val =  yieldDictMu[samp][b]
                        el_val =  yieldDictEl[samp][b]
                        mu_sf  =  zinv_mu_sf.get(b,1)
                        el_sf  =  zinv_mu_sf.get(b,1)
                        zinv_pred =  mu_val * mu_sf + el_val*el_sf
        
                        zinv_mc_uncert = self.yieldDict[variation][samp][b]/self.yieldDict[variations[0]][samp][b] if self.yieldDict[variations[0]][samp][b].val else u_float(1.0 )
                        #print syst_name, variation, samp, b, self.yieldDict[variations[0]][samp][b], self.yieldDict[variation][samp][b], zinv_mc_uncert
                        self.bkg_ests[variation][samp][b]   = zinv_pred * (zinv_mc_uncert)

                    ##
                    ##  Applying uncertainties for variations (only for flat uncertainties)
                    ##
                    if "central" not in variation:
                        if other_uncerts.has_key(variation):
                            
                            #pp.pprint(other_uncerts.keys())
                            #assert False
                            self.yieldDict[variation][samp][b] *= (1+ other_uncerts[variation][samp][b]/100.)
                            self.bkg_ests[variation][samp][b] *= (1+ other_uncerts[variation][samp][b]/100.)
                    #else:
                    #    if samp==qcd:
                    #        uncert  = self.yieldDict[variation][samp][b]/self.yieldDict[variations[0]][samp][b] if self.yieldDict[variations[0]][samp][b].val else u_float(1.0 )
                    #        print "QCD MC VARIATION:", samp, variation, b ,uncert
                    #        print variations[0] , self.yieldDict[variation][samp][b] , variation ,":", self.yieldDict[variation][samp][b]
                    #        self.bkg_ests[variation][samp][b] *= (u_float(1)+ uncert/100.)

            #print "------------------------------------------------------"
            #print variation,
            #print "Before",
            #print self.bkg_ests[variation]["Total"]
            self.bkg_ests[variation]["Total"] = dict_manipulator( [ self.bkg_ests[variation][bkg] for bkg in self.bkgList],  lambda *a: sum(a) )
            self.yieldDict[variation]["Total"] = dict_manipulator( [ self.yieldDict[variation][bkg] for bkg in self.bkgList],  lambda *a: sum(a) )
            #print self.bkg_ests[variation]["Total"]
            #print "------------------------------------------------------"

        #for samp, regions in self.yieldDict[tag].iteritems():
        #    for b,val in regions.iteritems():
        #        pass


        #
        # Storing YieldDicts for all variations
        # 
        for tag in tags:
            pickle.dump(  self.yields[tag] , open( "%s/YieldInst_%s.pkl"%(yldinsts_dir, tag) ,'w' ) )
            pickle.dump(  self.yieldDict[tag] , open( "%s/MCTruthDict_%s.pkl"%(ylds_dir, tag) ,'w' ) )
        global_yield_dict   = getPkl( global_yield_pkl ) 
        global_bkgpred_dict = getPkl( global_bkgpred_pkl ) 
        global_sf_dict      = getPkl( global_sf_pkls  )
        for tag in tags:
            global_yield_dict[tag]   = self.yieldDict[tag]
            global_bkgpred_dict[tag] = self.bkg_ests[tag]
            global_sf_dict[tag]      = self.SFs[tag]

        pickle.dump(  global_yield_dict , open( global_yield_pkl ,'w' ) )
        pickle.dump(  global_bkgpred_dict , open( global_bkgpred_pkl ,'w' ) )
        pickle.dump(  global_sf_dict , open( global_sf_pkls ,'w' ) )
        self.all_yield_dict = global_yield_dict
        self.all_sfs        = global_sf_dict
        self.all_bkgpred    = global_bkgpred_dict

        all_syst_cards_pkl       =  "%s/SystDictForCards.pkl"%(self.res_dir)
        all_syst_dict_pkl        =  "%s/SystDict.pkl"%(self.res_dir)


        self.card_systs_pkl      = "%s/SystDictForCards.pkl"%(self.res_dir)
        sample_card_systs = {}
        sample_systs = {}

        #sample_card_truth_systs = {}
        sample_mctruth_systs = {}

        

        for samp in self.bkgTotList + self.sigList :
            # use N_pred or N_mctruth for calculating systs: 
            # mc_truth:
            #sample_mctruth_systs[samp]     =  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : meanSys(*vals)  )   
            #sample_card_systs[samp]=  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : 1+ meanSys(*vals)/100.  )   
            # N_pred


            #if isSigSys and self.name == 'Q2':
            #    print variations
            #    sample_systs[samp]     =  dict_manipulator( [self.bkg_ests[x][samp] for x in qvariations  ] , lambda *vals : q2EvSys(*vals)  )   
            #    #sample_card_systs[samp]=  dict_manipulator( [self.bkg_ests[x][samp] for x in variations  ] , lambda *vals : ( 1+ envSysSigned(*vals)/100. ) if envSysSigned(*vals) else 1.0  )   
                #assert False
            if samp=="QCD":
                sample_systs[samp]     =  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : meanSys(*vals)  )   
                sample_card_systs[samp]=  dict_manipulator( [self.yieldDict[x][samp] for x in variations  ] , lambda *vals : 1+ meanSysSigned(*vals)/100.  if meanSysSigned  else 1.0)   
            else: 
                sample_systs[samp]     =  dict_manipulator( [self.bkg_ests[x][samp] for x in variations  ] , lambda *vals : meanSys(*vals)  )   
                sample_card_systs[samp]=  dict_manipulator( [self.bkg_ests[x][samp] for x in variations  ] , lambda *vals : ( 1+ meanSysSigned(*vals)/100. ) if meanSysSigned(*vals) else 1.0  )   



        self.tot_sys = sample_systs['Total']
        bins_card_systs           =  Yields.getByBins(self.yields[tag], sample_card_systs)
        self.card_bins = bins_card_systs
    
        all_syst_cards_dict = getPkl( all_syst_cards_pkl )
        all_syst_dict       = getPkl( all_syst_dict_pkl  )
        
        #print all_syst_dict_pkl
        #print all_syst_dict.keys()
        if "WPt_central" in all_syst_dict: assert False,all_syst_dict.keys()

        all_syst_cards_dict[self.name] = {'bins':bins_card_systs , 'type':'lnN'}
        all_syst_dict[self.name]       = sample_systs
        #for x in all_syst_cards_dict:
        #    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #    print x
        #    print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        pickle.dump( all_syst_cards_dict ,  open( all_syst_cards_pkl ,'w' ) ) 
        pickle.dump( all_syst_dict       ,  open( all_syst_dict_pkl , 'w' ) )  

        self.all_syst_cards = all_syst_cards_dict
        self.all_syst_dict  = all_syst_dict

        if "WPt_central" in all_syst_dict: assert False,all_syst_dict.keys()



        #
        #   Getting the Syst range for signals
        #
        self.sample_systs   = sample_systs
        if isSigSys:
            syst_range = {}
            syst_range_sample = {}
            for b in bins_card_systs.keys():
                #sig_systs = np.array( [ (sample_systs[sig][b],sig) if sample_systs[sig][b] else ( np.nan,sig)  for sig in self.sigList ] ) 
                #max_syst  = np.nanmax(sig_systs) 
                #min_syst  = np.nanmin(sig_systs) 
                #sig_systs = np.array( [ (sample_systs[sig][b],sig)   for sig in self.sigList   if sample_systs[sig][b]]) 
                #max_syst  = np.ndarray.tolist( max(sig_systs, key = lambda x: float(x[0]) ) )
                #min_syst  = np.ndarray.tolist( min(sig_systs, key = lambda x: float(x[0]) ) )
                sig_systs = [ (sample_systs[sig][b],sig)   for sig in self.sigList   if sample_systs[sig][b]] 
                max_syst  = max(sig_systs, key = lambda x: x[0] ) 
                min_syst  = min(sig_systs, key = lambda x: x[0] ) 
                #print sig_systs
                #print min_syst 
                #print max_syst
                syst_range_sample[b]= (min_syst, max_syst)
                if not "%.2f"%min_syst[0] == "%.2f"%max_syst[0]:
                    syst_range[b] = "%.2f-%.2f"%(float(min_syst[0]),float(max_syst[0]))
                else:
                    syst_range[b] = "%.2f"%max_syst[0]
            self.syst_range = syst_range
            self.syst_range_sample = syst_range_sample



        ##
        ##  Making Tables
        ##

        # bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgSysts/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
        # bkg_systs_dir = os.path.expandvars(bkg_systs_dir)
        base_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s/%s/%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
        base_systs_dir = os.path.expandvars(base_systs_dir)

        if isBkgSys:
            sig_bkg_infos = { \
                                "BkgSysts":  { 'sampleList':self.bkgTotList  , 'total':True}  ,
                            }
        elif isSigSys:
            benchMarkPoints    = ['T2tt-300-220', 'T2tt-300-270','T2tt-400-370']
            sig_bkg_infos = { \
                                "SigSysts": { 'sampleList':benchMarkPoints   , 'total':False} ,
                            }


        #sig_bkg_infos = { \
        #                    "BkgSysts":  { 'sampleList':self.bkgTotList  , 'total':True}  ,
        #                    "SigSysts": { 'sampleList':self.sigList   , 'total':False} , 
        #                }

        self.rets = [] 
        for sampleType, info in sig_bkg_infos.iteritems():
            
            systs_dir = base_systs_dir + "/" + sampleType
            sampleSet   = info['sampleList']
            doTotal   = info['total']

            first_row  = True
            table_list = [] 
            makeDir(os.path.expandvars(systs_dir))
            for region_name in regions:
                    if region_name == "\hline":
                        table_list.append([region_name])
                        continue
                    region   = region_name
                    toPrint = [   
                                  ["Region"     ,  fix_region_name( region_name )], 
                              ]
                    for var in variations:
                        if isBkgSys:
                            toPrint.append( [ var ,  self.bkg_ests[var]['Total'][region_name].round(2) ])
                        if isSigSys:
                            toPrint.append( [ var ,  self.bkg_ests[var]['T2tt-300-270'][region_name].round(2) ])

                    if isBkgSys:                        
                        toPrint.append(  ['Syst. ' , round (self.tot_sys[region_name] ,2)      ] )
                    if isSigSys:
                        toPrint.append( ['Syst Range. ' ,  self.syst_range[region_name] ])
                    align = "{:<20}"*len(toPrint)
                    if first_row:
                        print align.format(*[x[0] for x in toPrint])
                        first_row = False
                        table_list.append( [x[0] for x in toPrint]  ) 
            
                    print align.format(*[x[1] for x in toPrint])
                    table_list.append( [x[1] for x in toPrint])
            #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))
            makeDir(cfg.saveDir+"/%s/"%sampleType) #NOTE: Added
            table = makeSimpleLatexTable( table_list, "%s.tex"%self.name, cfg.saveDir+"/%s/"%sampleType, align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-2)).rstrip("|")+"|c" )
            #print table

            #
            #   Syst and Yields per Sample
            #

            first_row = True
            table_list = []
            #nptable = np.array([])
            for region in regions:
                    if region == "\hline":
                        table_list.append([region])
                        continue
                    toPrint = [   
                                  ["Region"     ,  fix_region_name( region )], 
                              ]
                    for samp in sampleSet:
                        #toPrint.append( [ samp , self.yieldDict[variations[1]][samp][region]  ] )
                        for var in variations:
                            #toPrint.append( [ var , self.yieldDict[var][samp][region].round(3)] )
                            toPrint.append( [ var , self.bkg_ests[var][samp][region].round(3)] )
                        toPrint.append(  ['%s Syst. '%samp , round (sample_systs[samp][region] ,3)      ] )

                        #toPrint.append( [ samp ,   round( sample_systs[samp][region] ,2 ) ] )
                    toPrint.append(  ['Syst. ' , round (self.tot_sys[region] ,2)      ] )
                    align = "{:<20}"*len(toPrint)
                    if first_row:
                        print align.format(*[x[0] for x in toPrint])
                        first_row = False
                        table_list.append( [x[0] for x in toPrint]  ) 
            
                    print align.format(*[x[1] for x in toPrint])
                    table_list.append( [x[1] for x in toPrint])
            makeDir(os.path.expandvars(systs_dir))
            #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))

            nptable = np.concatenate( [ [x] for x in table_list if 'hline' not in x[0]]  )
            nptable_T = nptable.T
            nptable_T[0][0] = ""
            #table = makeSimpleLatexTable( table_list, "%s_YieldAndSystPerSample.tex"%self.name, cfg.saveDir+"/%s/"%sampleType, align_char = "c" ,  align_func= lambda char, table: "c|"+ ((char*(len(variations)+1) +"|") *(len(table[1])-1)).rstrip("|") )
            table = makeSimpleLatexTable( nptable_T, "%s_YieldAndSystPerSample.tex"%self.name, cfg.saveDir+"/%s/"%sampleType, align_char = "c"  )
            #print table
            self.rets.append(nptable_T)
            #
            #   Systematics per sample
            #

            first_row = True
            table_list = []
            for region in regions:
                    if region == "\hline":
                        table_list.append([region])
                        continue
                    toPrint = [   
                                  ["Region"     ,  fix_region_name( region )], 
                              ]
                    for samp in sampleSet:
                        #toPrint.append( [ samp , self.yieldDict[variations[1]][samp][region]  ] )
                        toPrint.append( [ samp ,   round( sample_systs[samp][region] ,2 ) ] )
                    toPrint.append(  ['Syst. ' , round (self.tot_sys[region] ,2)      ] )
                    align = "{:<20}"*len(toPrint)
                    if first_row:
                        print align.format(*[x[0] for x in toPrint])
                        first_row = False
                        table_list.append( [x[0] for x in toPrint]  ) 
                    print align.format(*[x[1] for x in toPrint])
                    table_list.append( [x[1] for x in toPrint])
            makeDir(os.path.expandvars(systs_dir))
            #pickle.dump(res , open( os.path.expandvars( bkg_systs_dir+"/%s.pkl"%self.name)  ,"w"))
            table = makeSimpleLatexTable( table_list, "%s_SystPerSample.tex"%self.name, cfg.saveDir+"/%s/"%sampleType, align_char = "c" ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )
            #print table


            
            #
            #   Combined Systs Per Sample
            #


            #
            #   All Systs 
            #

        



        if False:
    
            region_names = regions
            
            first_row = True
            table_list = [] 
            for region_name in region_names:
                    if region_name == "\hline":
                        table_list.append([region_name])
                        continue
                    region   = region_name
                    toPrint = [   
                                  ["Region"     ,  fix_region_name( region_name )], 
                                  ['PU Down'    ,  yieldTotals['pu_down'][region_name]    ],
                                  ['PU Central' ,  yieldTotals['pu'][region_name]         ],
                                  ['PU Up'      , yieldTotals['pu_up'][region_name]      ],
                                  ['Syst. ' , round (res[region_name] ,2)      ],
            
                              ]#dataCR( dataMCsf * yldDict[tt][region]).round(2)  ]
                    align = "{:<20}"*len(toPrint)
                    if first_row:
                        print align.format(*[x[0] for x in toPrint])
                        first_row = False
                        table_list.append( [x[0] for x in toPrint]  ) 
                    print align.format(*[x[1] for x in toPrint])
                    table_list.append( [x[1] for x in toPrint])



if __name__ == "__main__":
    #jecSyst = Systematics(cfg, jecRunTagParams, centralParams, name="jec")
    #self = jecSyst
    BkgSysts = {}
    #for syst_name, systTagParams in tagParams.iteritems():
    SigSysts = {}
    CommonSysts = {}

    if True:
        pass
        for syst_name, systTagParams in bkgTagParams.iteritems(): #NOTE: WAS COMMENTED OUT
           BkgSysts[syst_name] = Systematics(cfg, systTagParams, centralParamsBkg, name=syst_name, syst_type = "bkg") #NOTE: WAS COMMENTED OUT 
        #for syst_name, systTagParams in SigAndBkgTagParams.iteritems():
        #   CommonSysts[syst_name] = Systematics(cfg, systTagParams, centralParamsBkg, name=syst_name, syst_type = "both") 
    #for syst_name, systTagParams in sigTagParams.iteritems():
    #    if syst_name =="met":
    #        centralParamsSig_ = deepcopy( centralParamsSig )
    #        centralParamsSig_['pu'] = 'nopu'
    #    else:
    #        centralParamsSig_ = deepcopy( centralParamsSig )
    #    SigSysts[syst_name] = Systematics(cfg, systTagParams, centralParamsSig_, name=syst_name, syst_type = "sig") 
    #self = SigSysts[syst_name]



    fixSystNameDict={
                    'ttPtShape': "CR/SR transf. fact. W",
                    'WPtShape' : "CR/SR transf. fact. tt",
                    'ttpt'     : "tt $p_{T}$",
                    'WPt'      : "W $p_{T}$",
                    'jec'      : "JEC",
                    'jer'      : "JER", 
                'DYJetsM50XSec': 'Drell-Yan xsec',
                'STXSec'       : 'Single top xsec',
                'DibosonXSec'  : 'Diboson xsec',
                'ZInvEst'      : '$Z_{Inv}$ estimation',
                'QCDEst'       : 'QCD estimation',
                'lepEff'       : "Lepton efficiency" ,
                'PU'           : "Pile-up",
                }
    def fixSystName(name):
        return fixSystNameDict.get(name,name)





    

    if SigSysts or CommonSysts:
    
        first_row = True
        table_list = []
        nptable = np.array([])
        main_sr_table = []

        syst_list = CommonSysts.keys() + SigSysts.keys()
        allSigSysts={}
        allSigSysts.update(CommonSysts)
        allSigSysts.update(SigSysts)
        

        bmSig = 'T2tt-300-270'
        #{b:v for b,v in x.syst_range.iteritems() if b in ['SR1a', 'SR1b', 'SR1c', 'SR2'] }
        

        table_list2=[]

        for region in ['SR1a', 'SR1b', 'SR1c', 'SR2']:
            toPrint = [
                          ["Region"                     ,     region     ],
                       ]
            toPrint2=toPrint[:]
            for syst_name in sorted(syst_list):
                toPrint2.append( [  fixSystName(syst_name) , allSigSysts[syst_name].syst_range[region]  ] )
                toPrint.append( [  fixSystName(syst_name) , round( allSigSysts[syst_name].sample_systs[bmSig][region],1 )  ] )
    
            align = "{:<20}"*len(toPrint)
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                table_list.append( [x[0] for x in toPrint]  )
                table_list2.append( [x[0] for x in toPrint]  )
            print align.format(*[x[1] for x in toPrint])
            table_list.append( [x[1] for x in toPrint])
            table_list2.append( [x[1] for x in toPrint2])

        nptable = np.concatenate( [ [x] for x in table_list if 'hline' not in x[0]]  )
        nptable2 = np.concatenate( [ [x] for x in table_list2 if 'hline' not in x[0]]  )
        #main_sr_nptable = np.concatenate( [ [x] for x in main_sr_table if 'hline' not in x[0]]  )

        table  = makeSimpleLatexTable( nptable.T, "SigSystExample_%s.tex"%bmSig, cfg.saveDir+"/SigSysts/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|")  )
        table2 = makeSimpleLatexTable( nptable2.T, "SigSystSummaryRange.tex", cfg.saveDir+"/SigSysts/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|")  )
        #table = makeSimpleLatexTable( table_list, "SigSummary_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-2)).rstrip("|") + "|c" )
        #main_sr_nptable_T = main_sr_nptable.T
        #main_sr_nptable_T[0][0]='Syst'
        #SRtable = makeSimpleLatexTable( main_sr_nptable_T, "SystsSummaryMainSRs_%s.tex"%lumitag, saveDirBase+"/Results/", align_char = "c"        ,  align_func= lambda char, table: "c|"+ (char *(len(table[1])-1)).rstrip("|") )


