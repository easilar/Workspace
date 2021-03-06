from Workspace.DegenerateStopAnalysis.tools.degTools import fixForLatex


def fix_region_name(name):
    return name.replace("_","/").replace("pos","Q+").replace("neg","Q-")

def dict_operator ( yldsByBin , keys = [] , func =  lambda *x: sum(x) ):
    """
    use like this dict_operator( yields_sr, keys = ['DataBlind', 'Total'] , func = lambda a,b: a/b)
    """ 
    args = [ yldsByBin[x] for x in keys]
    return func(*args) 



if __name__ == '__main__':

    lepCol = "LepAll"
    lep    = "lep"

    make_lumi_tag = lambda l: "%0.0fpbm1"%(l)

    sys_label = "AdjustedSys"
    cut_name = cfg.cutInstList[0].fullName

    tags = ["", "wpt", ]#"2wpt" ] 

    yieldPkls=  {}
    yields   =  {}
    yieldDict = {}
    yieldTotals={}
    yieldW={}
    for tag in tags:
        runTag = 'PreApp_Mt95_Inccharge_{lepCol}_{lep}_pu{tag}_SF'.format(lepCol=lepCol,lep=lep, tag= "_%s"%tag if tag else "")
        saveDir              =  cfg.saveDirBase+'/%s/%s'%(runTag,cfg.htString)
        results_dir          =  cfg.cardDirBase + "/13TeV/{ht}/{run}/".format( ht = cfg.htString , run = runTag )
        #lumiTag              =  make_lumi_tag( cfg.lumi_info['DataUnblind_lumi'] )
        lumiTag              =  make_lumi_tag( cfg.lumi_info['DataBlind_lumi'] )
        yieldPkls[tag]     =  results_dir + sys_label  + "/" + cfg.baseCutSaveDir  + "/Yields_%s_%s_%s.pkl"%( lumiTag , runTag, cut_name)    
        yields[tag]        =  pickle.load(file( yieldPkls[tag]  ))
        yieldDict[tag]     =  yields[tag].getNiceYieldDict()
        yieldTotals[tag]   =  yieldDict[tag]['Total']
        yieldW[tag]        =  yieldDict[tag]['WJets']

    res_wpt  =    dict_manipulator( [ yieldTotals['wpt'] , yieldTotals['']  ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)
    #res_2wpt =    dict_manipulator( [ yieldTotals['2wpt'] , yieldTotals[''] ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)

    res_W_wpt  =    dict_manipulator( [ yieldW['wpt']  , yieldW['']  ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)
    #res_W_2wpt =    dict_manipulator( [ yieldW['2wpt'] , yieldW[''] ] , lambda a,b: ( abs(1.-(a/b).val) ) * 100)

    tags         = tags
    res_dir      = os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag) )
    yldinsts_dir = "%s/YieldInsts/"%(res_dir)
    ylds_dir     = "%s/YieldDicts/"%(res_dir)
    global_yield_dict = res_dir + "/YieldDictWithVars.pkl"
    makeDir(ylds_dir)
    makeDir(yldinsts_dir)
    for tag in tags:
        pickle.dump(  yields[tag] , open( "%s/YieldInst_%s.pkl"%(yldinsts_dir, tag) ,'w' ) )
        pickle.dump(  yieldDict[tag] , open( "%s/YieldDict_%s.pkl"%(ylds_dir, tag) ,'w' ) )
    
    for tag in tags:
        if os.path.isfile(global_yield_dict):
            global_pkl = pickle.load( file(global_yield_dict) )
        else:
            global_pkl = {}
        global_pkl[tag] = yieldDict[tag]
        pickle.dump(  global_pkl , open( "%s/YieldDictWithVars.pkl"%(res_dir ) ,'w' ) )
    
    ##FIX ME
    #regions = yld.cutNames

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
             '\hline',
             'CR1a',
             'CR1b',
             'CR1c',
             'CR2',
             'CRTT2',
                ]

    region_names = regions
    
    first_row = True
    table_list = [] 
    for region_name in region_names:
            if region_name == "\hline":
                table_list.append([region_name])
                continue
            region   = region_name
    
    
            toPrint = [   
                          ["Region"              ,  fix_region_name( region_name )         ], 
                          ['no Wpt Reweight'     ,  yieldTotals[''][region_name]         ],
                          ['Wpt Reweight'        ,  yieldTotals['wpt'][region_name]    ],
                          #['2*Wpt Reweight'      ,  yieldTotals['2wpt'][region_name]      ],
                          ['WOnly Syst. Wpt (\%)'      ,  round (res_W_wpt[region_name] ,2)            ],
                          ['Syst. Wpt (\%)'              ,  round (res_wpt[region_name] ,2)            ],
                          #['Syst. 2*Wpt (\%)'              ,  round (res_2wpt[region_name] ,2)            ],
                          #['WOnly no Wpt Reweight'     ,  yieldW[''][region_name]         ],
                          #['WOnly Wpt Reweight'        ,  yieldW['wpt'][region_name]    ],
                          #['WOnly 2*Wpt Reweight'      ,  yieldW['2wpt'][region_name]      ],
                          #['WOnly Syst. 2*Wpt (\%)'    ,  round (res_W_2wpt[region_name] ,2)            ],
    
                       ]#dataCR( dataMCsf * yldDict[tt][region]).round(2)  ]
    
    
            align = "{:<20}"*len(toPrint)
    
            if first_row:
                print align.format(*[x[0] for x in toPrint])
                first_row = False
                table_list.append( [x[0] for x in toPrint]  ) 
    
            print align.format(*[x[1] for x in toPrint])
            table_list.append( [x[1] for x in toPrint])
    
    
    bkg_systs_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/results/2016/%s_%s_%s/BkgSysts/"%(cfg.cmgTag, cfg.ppTag, cfg.runTag)
    makeDir(os.path.expandvars(bkg_systs_dir))
    pickle.dump(res_W_wpt , open( os.path.expandvars( bkg_systs_dir+"/Wpt_wonly.pkl")  ,"w"))
    pickle.dump(res_wpt , open( os.path.expandvars( bkg_systs_dir+"/Wpt_fullbkg.pkl")  ,"w"))
    table = makeSimpleLatexTable( table_list, "WPt.tex", cfg.saveDirBase+"/BkgSysts/", align_char = "c"        ,  align_func= lambda char, table: "c|cc|c|c" )
    table = makeSimpleLatexTable( table_list, "Wpt.tex", os.path.expandvars( bkg_systs_dir ), align_char = "c" ,  align_func= lambda char, table: "c|cc|c|c" )
    
    print table
