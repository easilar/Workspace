import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing ('standard')

#options.register ('infile','infile.root',
#          VarParsing.VarParsing.multiplicity.singleton,
#          VarParsing.VarParsing.varType.string,
#          "InputFile")
options.register ('outfile','outfile.root',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "outputFile")
options.register ('decayfile','Workspace/RA4Analysis/data/test_param_card_T5lnu_1100_200_100_AllDecays.dat',
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.string,
          "decayFile")
options.register ('skipEvents',0,
          VarParsing.VarParsing.multiplicity.singleton,
          VarParsing.VarParsing.varType.int,
          "Events to be skipped")

options.parseArguments()


process = cms.Process("PROD")

process.load("Configuration.StandardSequences.SimulationRandomNumberGeneratorSeeds_cff")
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
	    input = cms.untracked.int32(options.maxEvents)
)

# The following three lines reduce the clutter of repeated printouts
# of the same exception message.
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.destinations = ['cerr']
process.MessageLogger.statistics = []
process.MessageLogger.fwkJobReports = []
process.MessageLogger.cerr.FwkReport.reportEvery = 10000


process.source = cms.Source("LHESource",
#    fileNames = cms.untracked.vstring(options.infile),
    fileNames = cms.untracked.vstring(options.files),
    skipEvents = cms.untracked.uint32(options.skipEvents)

)

#from Configuration.Generator.PythiaUEZ2Settings_cfi import *
from Configuration.Generator.PythiaUED6TSettings_cfi import *

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(10),
    pythiaPylistVerbosity = cms.untracked.int32(20),
    comEnergy = cms.double(8000.0),
    pythiaToLHE = cms.bool(True),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring(
'MSEL=0',
'IMSS(1)=11',
#'IMSS(22)=33',##FIXME
'MSTP(161)=67',
'MSTP(162)=68',
'MSTP(163)=69',
),
        SLHAParameters = cms.vstring(
		'SLHAFILE = '+options.decayfile#Workspace/RA4Analysis/data/test_param_card_T5lnu_1100_200_100_AllDecays.dat'
#    'SLHAFILE = Workspace/RA4Analysis/data/param_card_T5lnu_template.dat'
#		'SLHAFILE = Configuration/Generator/data/CSA07SUSYBSM_LM9p_sftsdkpyt_slha.out'
#    'SLHAFILE = Workspace/RA4Analysis/data/lesya.dat'
        ),
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters','SLHAParameters')
    )
)

#from IOMC.RandomEngine.RandomServiceHelper import  RandomNumberServiceHelper
#randHelper =  RandomNumberServiceHelper(process.RandomNumberGeneratorService)
#randHelper.populate()
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    moduleSeeds = cms.PSet(
        generator = cms.untracked.uint32(123456789),
        g4SimHits = cms.untracked.uint32(123456788),
        VtxSmeared = cms.untracked.uint32(123456789)
    ),
)

process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(10)
)


process.out = cms.OutputModule("PoolOutputModule",
     #verbose = cms.untracked.bool(True),
#     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
#     fileName = cms.untracked.string(options.outfile),
     fileName = cms.untracked.string('histo.root'),
#     outputCommands = cms.untracked.vstring()
     outputCommands = cms.untracked.vstring('keep *') 
)

process.outpath = cms.EndPath(process.out)


process.pp = cms.Path(process.generator*process.genParticles*process.printGenParticles)

process.schedule = cms.Schedule(process.pp, process.outpath)

