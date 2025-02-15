'''
Modules used for the WZ-Run3 Analysis.
'''
import os
import ROOT 
# ---------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON MERGER+SKIM+LABELTAGGERS  -------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------------------- #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from CMGTools.TTHAnalysis.tools.nanoAOD.skimNRecoLeps import SkimRecoLeps
from CMGTools.TTHAnalysis.tools.nanoAOD.DatasetTagger import datasetTagger

### Lepton definitions 
# Muons 
min_mu_pt = 5
max_mu_eta = 2.4

# Electrons  
min_el_pt = 5
max_el_eta = 2.5

# Common
relIso = 0.4
dxy = 0.05
dz = 0.1
sip3d = 8

### Lambda selectors
isoAndIPCuts  = lambda  l : l.miniPFRelIso_all < relIso  and abs(l.dxy) < dxy and abs(l.dz) < dz and l.sip3d < sip3d 
muonSelection = lambda l : ((abs(l.eta) < max_mu_eta) and (l.pt > min_mu_pt)
                             and isoAndIPCuts(l) and l.looseId)
elecSelection = lambda l : (( abs(l.eta) < max_el_eta) and (l.pt > min_el_pt)
                              and isoAndIPCuts(l) and l.lostHits < 2)


lepMerge = collectionMerger(input = ["Electron", "Muon"], 
                            output = "LepGood",
                            selector = dict(Muon = muonSelection, Electron = elecSelection))

lepSkim = SkimRecoLeps() # Skim configuration: at least 2 leptons
tagger = lambda : datasetTagger()

lepCollector = [lepMerge, lepSkim, tagger]


leptongroups = ["elScaleUp", "muScaleUp", "elScaleDown", "muScaleDown"]

# --------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- JET CORRECTIONS ------------------------------------------------------ # 
# --------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.jetMetGrouper_wzRun3 import jetMetCorrelate2022, groups
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

addJECs_2022_mc    = createJMECorrector(dataYear      = "2022",
                                        jetType       = "AK4PFPuppi",
                                        jesUncert     = "All",
                                        metBranchName = "PuppiMET",
                                        splitJER      = True,
                                        applyHEMfix   = False)
addJECs_2022_data = createJMECorrector(isMC          = False,
                                       dataYear      = "2022",
                                       runPeriod     = "D",
                                       jetType       = "AK4PFPuppi",
                                       jesUncert     = "All",
                                       metBranchName = "PuppiMET",
                                       splitJER      = True,
                                       applyHEMfix   = False)


jecgroups = [ "jes%s%s"%(jecgroup, sign) for jecgroup in groups for sign in ["Up", "Down"] ]
jmeUncertainties_mc   = [addJECs_2022_mc, jetMetCorrelate2022]
jmeUncertainties_data = [addJECs_2022_data, jetMetCorrelate2022]

# --------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON RECLEANER ----------------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------------------------- #

from CMGTools.TTHAnalysis.tools.nanoAOD.leptonJetRecleanerWZSM import LeptonJetRecleanerWZSM

## Loose selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_lepton

## Fakeable selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_lepton

## Tight selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_lepton

from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import conept

recleaner_2022 = lambda : LeptonJetRecleanerWZSM(
  "Mini",
  lambda lep :        _loose_lepton(lep, 0.0494, 0.2770),          #Loose selection 
  lambda lep,jetlist: _fO_lepton(lep, 0.0494, 0.2770, jetlist),    #Clean on FO
  lambda lep,jetlist: _fO_lepton(lep, 0.0494, 0.2770, jetlist),    #FO selection
  lambda lep,jetlist: _tight_lepton(lep, 0.0494, 0.2770, jetlist), #Tight selection
  cleanJet  = lambda lep,jet,dr : dr<0.4,
  selectJet = lambda jet: abs(jet.eta)<4.7 and (jet.jetId & 2), 
  cleanTau  = lambda lep,tau,dr: True, 
  looseTau  = lambda tau: True, # Used in cleaning
  tightTau  = lambda tau: True, # On top of loose
  cleanJetsWithTaus = False,
  cleanTausWithLoose = False,
  systsJEC      = jecgroups,
  systsLepScale = leptongroups,
  doVetoZ = False,
  doVetoLMf = False,
  doVetoLMt = True,
  jetPt = 30,
  bJetPt = 25,
  coneptdef = lambda lep: conept(lep),
  year = 2022,
  bAlgo = "DeepCSV"
)

leptonJetRecleaning = [recleaner_2022]
# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON BUILDER  ------------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.leptonBuilderWZSM import leptonBuilderWZSM
leptonBuilderWZSM_2022 =  lambda : leptonBuilderWZSM(
  "Mini", 
  metbranch="PuppiMET",
  systsJEC      = jecgroups,
  lepScaleSysts = leptongroups 
)
leptonBuilder = [leptonBuilderWZSM_2022]
# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- TRIGGERS -------------------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
# -- Define different trigger strategies in this dictionary
#    to target different topologies.
triggerGroups = dict(
  # Double lepton triggers
  triggers_ee  = { 2022 : lambda ev: ev.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL \
                          or ev.HLT_DoubleEle25_CaloIdL_MW},
  triggers_mm  = { 2022 : lambda ev: ev.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8},
  triggers_em  = { 2022 : lambda ev: ev.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ \
                          or ev.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL},
  # Single lepton triggers
  triggers_se  = { 2022 : lambda ev: ev.HLT_Ele32_WPTight_Gsf},
  triggers_sm  = { 2022 : lambda ev: ev.HLT_IsoMu24},

  # Tri-lepton triggers
  triggers_mmm = { 2022 : lambda ev: ev.HLT_TripleMu_12_10_5 or ev.HLT_TripleMu_10_5_5_DZ},
  triggers_eee = { 2022 : lambda ev: 0 }, # Only one is prescaled in some of the data
  triggers_mme = { 2022: lambda ev : ev.HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ},
  triggers_mee = { 2022: lambda ev : ev.HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ},
  
  # MET triggers
  triggers_met = {2022 : lambda ev: ev.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight or ev.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight},

  # Combinations
  triggers_2lss = { 2022 : lambda ev: ev.Trigger_se or ev.Trigger_sm or ev.Trigger_mm or ev.Trigger_ee or ev.Trigger_em },
  triggers_3l = { 2022 : lambda ev: ev.Trigger_2lss or ev.Trigger_eee or ev.Trigger_mee or ev.Trigger_mme or ev.Trigger_mmm},
  triggers_jme = { 2022: lambda ev: ev.Trigger_jetmet or ev.Trigger_met or ev.Trigger_jetht }
)

# Prompt triggers
Trigger_sm   = lambda : EvtTagger('Trigger_sm',   [lambda ev : triggerGroups['triggers_sm'][2022](ev)])
Trigger_se   = lambda : EvtTagger('Trigger_se',   [lambda ev : triggerGroups['triggers_se'][2022](ev)])
Trigger_mm   = lambda : EvtTagger('Trigger_mm',   [lambda ev : triggerGroups['triggers_mm'][2022](ev)])
Trigger_ee   = lambda : EvtTagger('Trigger_ee',   [lambda ev : triggerGroups['triggers_ee'][2022](ev)])
Trigger_em   = lambda : EvtTagger('Trigger_em',   [lambda ev : triggerGroups['triggers_em'][2022](ev)])
Trigger_eee  = lambda : EvtTagger('Trigger_eee',  [lambda ev : triggerGroups['triggers_eee'][2022](ev)])
Trigger_mee  = lambda : EvtTagger('Trigger_mee',  [lambda ev : triggerGroups['triggers_mee'][2022](ev)])
Trigger_mme  = lambda : EvtTagger('Trigger_mme',  [lambda ev : triggerGroups['triggers_mme'][2022](ev)])
Trigger_mmm  = lambda : EvtTagger('Trigger_mmm',  [lambda ev : triggerGroups['triggers_mmm'][2022](ev)])
Trigger_2lss = lambda : EvtTagger('Trigger_2lss', [lambda ev : triggerGroups['triggers_2lss'][2022](ev)])
Trigger_3l   = lambda : EvtTagger('Trigger_3l',   [lambda ev : triggerGroups['triggers_3l'][2022](ev)])

# JetMET triggers
Trigger_met    = lambda : EvtTagger('Trigger_met',   [lambda ev : triggerGroups['triggers_met'][2022](ev)])

triggerSequence = [Trigger_sm, Trigger_se, Trigger_mm, Trigger_ee, Trigger_em, Trigger_eee, Trigger_mee, Trigger_mme, Trigger_mmm, Trigger_2lss, Trigger_3l, Trigger_met]

# ------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------- SCALE FACTORS ----------------------------------------------------------- # 
# ------------------------------------------------------------------------------------------------------------------------------ #


# Lepton Scale factors
from CMGTools.TTHAnalysis.tools.nanoAOD.lepScaleFactors_wzRun3 import lepScaleFactors_wzrun3
lepscalefactors = lambda: lepScaleFactors_wzrun3( 2018, keepOutput = 2, summary = True ) 

# bTag Scale factors
from CMGTools.TTHAnalysis.tools.nanoAOD.btag_weighterRun3 import btag_weighterRun3
btagpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/WZRun3/btagging"
btagWeights_2022 = lambda : btag_weighterRun3(btagpath + "/" + "wp_deepCSV_106XUL18_v2_mod.csv",
                                            btagpath + "/" + "btagEffs_2022_11_30.root",
                                            'deepcsv',
                                            branchJet = "iJSel_Mini",
                                            labelJet  = "",
                                            jecvars   = [ "jes%s"%(jecgroup) for jecgroup in groups ],
                                            lepenvars = [],
                                            splitCorrelations = True,
                                            year = "2022")

scalefactors = [lepscalefactors]#, btagWeights_2022]

# ---------------------------------------------------------------------------------------------------------------------------- #
### To be implemented
if __name__ == "__main__":
  pass
