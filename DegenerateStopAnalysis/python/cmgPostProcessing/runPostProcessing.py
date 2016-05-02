''' Run in multiprocessing the CMG post-processing script for the samples defined here.

https://docs.python.org/2/library/multiprocessing.html
'''

# imports python standard modules or functions

import argparse
import logging
import tempfile
import subprocess
import pprint
import copy
import multiprocessing

# imports user modules or functions

import Workspace.DegenerateStopAnalysis.cmgPostProcessing.cmgPostProcessing_parser as cmgPostProcessing_parser
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

#

pprint_cust = pprint.PrettyPrinter(indent=3, depth=5 , width=140)


sampleSets = {
                'signals':{
                            'samples':[ 
                                        "T2tt_300_270_FastSim",      
                                        "T2DegStop_300_270",         
                                        "T2DegStop_300_290_FastSim", 
                                        "T2DegStop_300_240_FastSim", 
                                        "T2DegStop_300_270_FastSim", 
                                        ],
                             
                            },


                'wjets':{
                            'samples':[
                                         "WJetsToLNu",             
                                         "WJetsToLNu_HT100to200",  
                                         "WJetsToLNu_HT200to400",  
                                         "WJetsToLNu_HT400to600",  
                                         "WJetsToLNu_HT600toInf",  
                                         "WJetsToLNu_HT600to800",  
                                         "WJetsToLNu_HT800to1200", 
                                         "WJetsToLNu_HT1200to2500",
                                         "WJetsToLNu_HT2500toInf", 
                                        ],
                             
                            },
                'ttjets':{
                            'samples':[
                                        "TTJets_LO",                                   
                                        ["TTJets_LO",               "--skim='lheHTlow'"      ],
                                        ["TTJets_LO_HT600to800",    "--skim='lheHThigh'"     ],
                                        "TTJets_LO_HT800to1200",
                                        "TTJets_LO_HT1200to2500",
                                        "TTJets_LO_HT2500toInf",
                                        ],
                             
                            },
                'dyjets':{
                            'samples':[
                                         "DYJetsToLL_M5to50_LO",
                                         "DYJetsToNuNu_M50",
                                         "DYJetsToLL_M5to50_HT100to200",
                                         "DYJetsToLL_M5to50_HT200to400",
                                         "DYJetsToLL_M5to50_HT400to600",
                                         "DYJetsToLL_M5to50_HT600toInf",
                                        ],
                            },
                'zjets':{
                            'samples':[ 

                                        "ZJetsToNuNu_HT100to200",
                                        "ZJetsToNuNu_HT200to400",
                                        "ZJetsToNuNu_HT400to600",
                                        "ZJetsToNuNu_HT600toInf",

                                        ],
                             
                            },
                'qcd':{
                            'samples':[

                                        "QCD_HT200to300", 
                                        "QCD_HT300to500",  
                                        "QCD_HT500to700",  
                                        "QCD_HT700to1000", 
                                        "QCD_HT1000to1500",
                                        "QCD_HT1500to2000",
                                        "QCD_HT2000toInf", 
 
                                        ],
                             
                            },
                'data':{
                            'samples':[

                                        "MET_Run2015D_05Oct",           
                                        "MET_Run2015D_v4",              
                                        #"SingleElectron_Run2015D_05Oct",
                                        #"SingleElectron_Run2015D_v4",   
                                        #"SingleMuon_Run2015D_05Oct",    
                                        #"SingleMuon_Run2015D_v4",       
                                        ],
                             
                            },


            }
    

StopSamples={
 '100': 'SMS_T2_4bd_mStop_100_mLSP_20to90',
 '125': 'SMS_T2_4bd_mStop_125_mLSP_45to115',
 '150': 'SMS_T2_4bd_mStop_150_mLSP_70to140',
 '175': 'SMS_T2_4bd_mStop_175_mLSP_95to165',
 '200': 'SMS_T2_4bd_mStop_200_mLSP_120to190',
 '225': 'SMS_T2_4bd_mStop_225_mLSP_145to225',
 '250': 'SMS_T2_4bd_mStop_250_mLSP_170to240',
 '275': 'SMS_T2_4bd_mStop_275_mLSP_195to265',
 '300': 'SMS_T2_4bd_mStop_300_mLSP_220to290',
 '325': 'SMS_T2_4bd_mStop_325_mLSP_245to315',
 '350': 'SMS_T2_4bd_mStop_350_mLSP_270to340',
 '375': 'SMS_T2_4bd_mStop_375_mLSP_295to365',
 '400': 'SMS_T2_4bd_mStop_400_mLSP_320to390',
 '500': 'SMS_T2_4bd_mStop_500to550_mLSP_420t540',
 '525': 'SMS_T2_4bd_mStop_500to550_mLSP_420t540',
 '525': 'SMS_T2_4bd_mStop_500to550_mLSP_420t540',
 '550': 'SMS_T2_4bd_mStop_550to600_mLSP_470t590',
 '600': 'SMS_T2_4bd_mStop_550to600_mLSP_470t590'}


signalSets=\
{  'mStop100': {  'samples': [  ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "20"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "30"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "40"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "50"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "60"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "70"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "80"],
                                ['SMS_T2_4bd_mStop_100_mLSP_20to90', '--processSignalScan', "100", "90"]]},

   'mStop125': {  'samples': [  ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "45"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "55"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "65"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "75"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "85"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "95"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "105"],
                                ['SMS_T2_4bd_mStop_125_mLSP_45to115', '--processSignalScan', "125", "115"]]},

   'mStop150': {  'samples': [  ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "70"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "80"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "90"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "100"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "110"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "120"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "130"],
                                ['SMS_T2_4bd_mStop_150_mLSP_70to140', '--processSignalScan', "150", "140"]]},

   'mStop175': {  'samples': [  ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "95"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "105"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "115"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "125"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "135"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "145"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "155"],
                                ['SMS_T2_4bd_mStop_175_mLSP_95to165', '--processSignalScan', "175", "165"]]},

   'mStop200': {  'samples': [  ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "120"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "130"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "140"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "150"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "160"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "170"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "180"],
                                ['SMS_T2_4bd_mStop_200_mLSP_120to190', '--processSignalScan', "200", "190"]]},

   'mStop225': {  'samples': [  ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "145"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "155"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "165"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "175"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "185"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "195"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "205"],
                                ['SMS_T2_4bd_mStop_225_mLSP_145to225', '--processSignalScan', "225", "215"]]},

   'mStop250': {  'samples': [  ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "170"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "180"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "190"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "200"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "210"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "220"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "230"],
                                ['SMS_T2_4bd_mStop_250_mLSP_170to240', '--processSignalScan', "250", "240"]]},

   'mStop275': {  'samples': [  ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "195"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "205"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "215"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "225"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "235"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "245"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "255"],
                                ['SMS_T2_4bd_mStop_275_mLSP_195to265', '--processSignalScan', "275", "265"]]},

   'mStop300': {  'samples': [  ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "220"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "230"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "240"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "250"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "260"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "270"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "280"],
                                ['SMS_T2_4bd_mStop_300_mLSP_220to290', '--processSignalScan', "300", "290"]]},

   'mStop325': {  'samples': [  ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "245"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "255"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "265"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "275"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "285"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "295"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "305"],
                                ['SMS_T2_4bd_mStop_325_mLSP_245to315', '--processSignalScan', "325", "315"]]},

   'mStop350': {  'samples': [  ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "270"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "280"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "290"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "300"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "310"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "320"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "330"],
                                ['SMS_T2_4bd_mStop_350_mLSP_270to340', '--processSignalScan', "350", "340"]]},

   'mStop375': {  'samples': [  ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "295"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "305"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "315"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "325"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "335"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "345"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "355"],
                                ['SMS_T2_4bd_mStop_375_mLSP_295to365', '--processSignalScan', "375", "365"]]},

   'mStop400': {  'samples': [  ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "320"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "330"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "340"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "350"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "360"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "370"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "380"],
                                ['SMS_T2_4bd_mStop_400_mLSP_320to390', '--processSignalScan', "400", "390"]]},

   'mStop425': {  'samples': [  ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "345"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "355"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "365"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "375"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "385"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "395"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "405"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "425", "415"]]},

   'mStop450': {  'samples': [  ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "370"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "380"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "390"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "400"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "410"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "420"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "430"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "450", "440"]]},

   'mStop475': {  'samples': [  ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "495"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "405"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "415"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "425"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "435"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "445"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "455"],
                                ['SMS_T2_4bd_mStop_425to475_mLSP_345to465', '--processSignalScan', "475", "465"]]},

   'mStop500': {  'samples': [  ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "420"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "430"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "440"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "450"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "460"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "470"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "480"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "500", "490"]]},

   'mStop525': {  'samples': [  ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "445"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "455"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "465"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "475"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "485"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "495"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "505"],
                                ['SMS_T2_4bd_mStop_500to550_mLSP_420to540', '--processSignalScan', "525", "515"]]},

   'mStop550': {  'samples': [  ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "470"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "480"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "490"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "500"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "510"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "520"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "530"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "550", "540"]]},

   'mStop575': {  'samples': [  ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "495"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "505"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "515"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "525"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "535"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "545"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "555"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "575", "565"]]},

   'mStop600': {  'samples': [  ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "520"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "530"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "540"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "550"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "560"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "570"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "580"],
                                ['SMS_T2_4bd_mStop_550to600_mLSP_470to590', '--processSignalScan', "600", "590"]]}}




sampleSets.update(signalSets)



def get_parser():
    ''' Argument parser for running the post processing module.
    
    Include all the options from cmgPostProcessing_parser, which are also used in 
    cmgPostProcessing_v1 script.
    
    '''
        
    argParser = argparse.ArgumentParser(
        description="Argument parser for runPostProcessing",
        parents=[cmgPostProcessing_parser.get_parser()]
        )
        
    # define all arguments which are added on top of cmgPostProcessing_parser arguments
    # collect them in argsRun group
    
    argsRun = argParser.add_argument_group('argsRun')
    
    argsRun.add_argument('--sampleSet',
        action='store',
        type=str,
        choices=sampleSets.keys(),
        default='ttjets',
        help="Set of samples to run the post processing on"
        )
        
    argsRun.add_argument('--numberOfProcesses',
        action='store',
        type=int,
        default='5',
        help="Number of processes to run in parallel"
        )

    argsRun.add_argument('--run',
        action='store_true',
        help="Run Post processing!"
        )
    
    # 
    return argParser, argsRun


def make_default_command(args, argsRun):
    ''' Create the default command for post-processing script.
        
    The default command is created from the arguments of the cmgPostProcessing_v1.py
    given on the command line and the default values of the cmgPostProcessing_v1.py arguments (for 
    arguments not given on the command line). 
    
    The arguments specific to runPostProcessing script only, given in argsRun group, are not considered.
    '''

    logger = logging.getLogger('runPostProcessing.make_default_command')

    command_default = [
        'python',
        'cmgPostProcessing_v1.py',
        ]

    argsRunList = []
    for a in argsRun._group_actions:
        argsRunList.extend(a.option_strings)
        
    logger.debug("\n List of arguments from the argsRun group: \n %s \n", pprint_cust.pformat(argsRunList))
        
    for arg in vars(args):
        argWm = '--' + arg
        if argWm not in argsRunList:
            argValue = getattr(args, arg)
            if isinstance(argValue, bool):
                if argValue:
                    argWmStr = argWm
                else:
                    continue
            else:
                argWmStr = argWm + "='{}'".format(argValue)
                
            command_default.append(argWmStr)
           
    logger.debug("\n command_default: \n %s \n", pprint_cust.pformat(command_default))

    #
    return command_default


def make_command(sampleSet, command_default=[]):
    ''' Create the final command for post-processing script.
    
    The command is created from the default command, replacing the "--processSample=..." argument 
    with the sample specific argument. Optional arguments included in the "samples" definition  
    replace also the arguments from the default command. 
    '''
    logger = logging.getLogger('runPostProcessing.make_command')
    
    commands = []
    for samp in sampleSets[sampleSet]['samples']:
        
        command = copy.deepcopy(command_default)
        extraOptions = []
        if type(samp) == type(""):
            sampName = samp
        elif type(samp) == type([]):
            sampName = samp[0]
            extraOptions = samp[1:]
        else:
            raise Exception("\n type not recognized for %s" % samp)
        
        logger.debug(
            "\n Extra options from sample definition for sample %s: \n, %s \n",
            sampName, pprint_cust.pformat(extraOptions)
            )
        
        # replace the existing arguments in the command with the arguments from the file
        for idx, arg in enumerate(command):
            logger.trace ('\n argument: %s\n', arg)
            if 'processSample' in arg:
                command[idx] = "--processSample='{}'".format(sampName)
                continue
            
            optWithArg = ''
            for idxOpt, opt in enumerate(extraOptions):
                if (opt.split('=')[0]) == (arg.split('=')[0]):
                    optWithArg = opt
                
                    # check if next item is an option or an argument to an option, based on the first character ('-')
                    for idxOptNext in range(idxOpt + 1, len(extraOptions)):
                        if extraOptions[idxOptNext].startswith('-'):
                            break
                        else:
                            optWithArg += ' ' + extraOptions[idxOptNext]
                            logger.trace ('\n option with arguments: %s \n', optWithArg) 
                                           
                    command[idx] = optWithArg
                    
            if "None" in command[idx]:
                del command[idx]
                
                    
        pprint_cust.pprint(" ".join(command))
        
        logger.info(
            "\n Command to be processed: \n, %s \n",
            pprint_cust.pformat(" ".join(command))
            )
        
        commands.append(command)
    
    #
    return commands


def run_commands(commands):
    for command in commands:
        subprocess.call(command)



if __name__ == '__main__':

    # argument parser
    
    parser, argsRun = get_parser() 
    args= parser.parse_args()
    
    # logging
    
    logLevel = args.logLevel
    
    # use a unique name for the log file, write file in the dataset directory
    prefixLogFile = 'runPostProcessing' + args.sampleSet + \
         '_' + logLevel + '_'
    logFile = tempfile.NamedTemporaryFile(suffix='.log', prefix=prefixLogFile, delete=False) 

    get_logger_rtuple = helpers.get_logger('runPostProcessing', logLevel, logFile.name)
    logger = get_logger_rtuple.logger

    #
    
    print "{:-^80}".format(" Running Post Processing! ")
    print '\n Log file: ', logFile.name
    print "{:-^80}".format(" %s "%args.numberOfProcesses )
    print "\nSamples:"
    pprint_cust.pprint(sampleSets[args.sampleSet])
    print 
    
    logger.info(
        "\n runPostProcessing script arguments" + \
        "\n some arguments will be overwritten from sample definition: \n\n %s \n", 
        pprint.pformat(vars(args))
        )
    logger.info("\n Samples: \n %s \n", pprint_cust.pformat(sampleSets[args.sampleSet]))

    command_default = make_default_command(args, argsRun)
    commands = make_command(args.sampleSet, command_default)
    

    if args.run:
        pool = multiprocessing.Pool(processes=args.numberOfProcesses)
        results = pool.map(subprocess.call, commands)
        pool.close()
        pool.join()

        print "{:-^80}".format(" FIN ")
    else:
        print "\n Run the script adding the option --run to actually run over the chosen sample.\n "
