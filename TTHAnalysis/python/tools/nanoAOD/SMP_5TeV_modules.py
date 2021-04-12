import os
import ROOT 
conf = dict(
        muPt = 5, 
        elePt = 7, 
        miniRelIso = 0.4, 
        sip3d = 8, 
        dxy =  0.05, 
        dz = 0.1
)

WZ_skim_cut = ("nMuon + nElectron >= 2 &&" + 
               "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
               "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d})").format(**conf)


muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] 

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(1,  ## this is the prescale factor (OS events are prescaled otherwise)
                muonSel = muonSelection, electronSel = electronSelection,
                minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                minLeptons = 2, requireSameSignPair = False,
                jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0, 
                minJets = 0, minMET = 0)

from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = lambda : collectionMerger(input = ["Electron","Muon"], 
                                     output = "LepGood", 
                                     selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = lambda : ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.TTHAnalysis.tools.nanoAOD.yearTagger import yearTag
from CMGTools.TTHAnalysis.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepJetBTagDeepFlavC
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_2017G, puAutoWeight_2017G
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import prefCorr_2017G
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes2017G

WZ5TeV_sequence_step1 = [lepSkim, lepMerge, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepMasses, puWeight_2017G, prefCorr_2017G]

##add weights



#==== 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0
lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, requirePair = True)

lepFRVars = lambda : ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
                                               pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                               maxLeptons = 1, requirePair = True)

from CMGTools.TTHAnalysis.tools.nanoAOD.nBJetCounter import nBJetCounter
nBJetDeepCSV25NoRecl = lambda : nBJetCounter("DeepCSV25", "btagDeepB", centralJetSel)
nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

WZ5TeV_sequence_step1_FR = [lepMerge, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepMasses,lepFR, nBJetDeepCSV25NoRecl, nBJetDeepFlav25NoRecl]
#WZ5TeV_sequence_step1_FR = [m for m in WZ5TeV_sequence_step1 if (m != lepSkim)] + [ lepFR, nBJetDeepCSV25NoRecl, nBJetDeepFlav25NoRecl ]
WZ5TeV_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
                      "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
                      "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d})").format(**conf)


#==== items below are normally run as friends ====
def conept_5TeV(lep): 
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if ((abs(lep.pdgId)==13 and lep.mvaTTH>0.55 and lep.miniPFRelIso_all < 0.325) or (abs(lep.pgdId)==11 and lep.mvaTTH>0.125 and lep.miniPFRelIso_all < 0.085)) and lep.jetBTagDeepCSV<0.1522:  
        return lep.pt
    else: 
        return 0.90 * lep.pt * (1 + lep.jetRelIso)

def clean_and_FO_selection_5TeV(lep):
    if (lep.pt < 8): return False
    if (abs(lep.eta) > (2.4 if abs(lep.pdgId)==13 else 2.5)): return False 
    if (abs(lep.dxy)>0.05 or abs(lep.dz)>0.1): return False   
    if (lep.sip3d > 8): return False
    return (abs(lep.pdgId)!=11 or (lep.convVeto and lep.lostHits==0 and lep.mvaFall17V2Iso_WPL)) and (abs(lep.pdgId)!=13 or lep.mediumPromptId>0)
                                                            
tightLeptonSel = lambda lep,jet : clean_and_FO_selection_5TeV(lep) and lep.mvaTTH > (0.55 if abs(lep.pdgId)==13 else 0.125) and lep.miniPFRelIso_all < (0.325 if abs(lep.pdgId)==13 else 0.085) and lep.jetBTagDeepCSV<0.1522

from CMGTools.TTHAnalysis.tools.nanoAOD.jetmetGrouper import groups as jecGroups
from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner

recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                                           looseLeptonSel = lambda lep : lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8 and (abs(lep.pdgId)!=11 or lep.lostHits<=1) and (abs(lep.pdgId)!=13 or lep.looseId),
                                                           cleaningLeptonSel = clean_and_FO_selection_5TeV,
                                                           FOLeptonSel = clean_and_FO_selection_5TeV,
                                                           tightLeptonSel = tightLeptonSel,
                                                           FOTauSel = lambda tau : False,
                                                           tightTauSel = lambda tau : False,
                                                           selectJet = lambda jet: jet.jetId > 0 and abs(jet.eta)<2.4, # pt and eta cuts are (hard)coded in the step2 
#                                                          coneptdef = lambda lep: conept_5TeV(lep),
)

recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                          cleanTausWithLooseLeptons=False,
                                                          cleanJetsWithFOTaus=False,
                                                          doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                          jetPts=[25,40],
                                                          jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                          btagL_thr=99, # they are set at runtime 
                                                          btagM_thr=99,
                                                          jetBTag='btagDeepB',
                                                          isMC = True,
                                                          variations=['jesTotal'] + ["jer"]                                                       
)

recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                            cleanTausWithLooseLeptons=False,
                                                            cleanJetsWithFOTaus=False,
                                                            doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                            jetPts=[25,40],
                                                            jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                            btagL_thr=-99., # they are set at runtime  
                                                            btagM_thr=-99., # they are set at runtime  
                                                            jetBTag='btagDeepB',
                                                            isMC = False,
                                                            variations = []
)


recleaner_step1_tight = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                                           looseLeptonSel = lambda lep : lep.pt > 10 and lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8 and (abs(lep.pdgId)!=11 or lep.lostHits<=1) and (abs(lep.pdgId)!=13 or lep.looseId), ## we need a 10GeV to be consistent with Xuan's analysis
                                                           cleaningLeptonSel = tightLeptonSel,
                                                           FOLeptonSel = tightLeptonSel,
                                                           tightLeptonSel = tightLeptonSel,
                                                           FOTauSel = lambda tau : False,
                                                           tightTauSel = lambda tau : False,
                                                           selectJet = lambda jet: jet.jetId > 0 and abs(jet.eta)<2.4  # pt and eta cuts are (hard)coded in the step2 
                                                                 
)

recleaner_step2_tight_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                                cleanTausWithLooseLeptons=False,
                                                                cleanJetsWithFOTaus=False,
                                                                doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                                jetPts=[25,40],
                                                                jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                                btagL_thr=99, # they are set at runtime 
                                                                btagM_thr=99,
                                                                jetBTag='btagDeepB',
                                                                isMC = True,
                                                                variations=['jesTotal'] + ["jer"]                                                       
)

recleaner_step2_tight_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                                  cleanTausWithLooseLeptons=False,
                                                                  cleanJetsWithFOTaus=False,
                                                                  doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                                  jetPts=[25,40],
                                                                  jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                                  btagL_thr=-99., # they are set at runtime  
                                                                  btagM_thr=-99., # they are set at runtime
                                                                  jetBTag='btagDeepB',  
                                                                  isMC = False,
                                                                  variations = []
                                                              )



from CMGTools.TTHAnalysis.tools.eventVars_5TeV import EventVars_5TeV
eventVars = lambda : EventVars_5TeV('','Recl')


from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger
isMatchRightCharge = lambda : ObjTagger('isMatchRightCharge','LepGood', [lambda l,g : (l.genPartFlav==1 or l.genPartFlav == 15) and (g.pdgId*l.pdgId > 0) ], linkColl='GenPart',linkVar='genPartIdx')
mcMatchId     = lambda : ObjTagger('mcMatchId','LepGood', [lambda l : (l.genPartFlav==1 or l.genPartFlav == 15) ])
mcPromptGamma = lambda : ObjTagger('mcPromptGamma','LepGood', [lambda l : (l.genPartFlav==22)])
mcMatch_seq   = [ isMatchRightCharge, mcMatchId ,mcPromptGamma]


from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2016All,jetmetUncertainties2017All,jetmetUncertainties2018All,jetmetUncertainties20175TeV,jetmetUncertainties20175TeVData
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import * 

from CMGTools.TTHAnalysis.tools.nanoAOD.jetmetGrouper import jetMetCorrelate2016, jetMetCorrelate2017, jetMetCorrelate2018
from CMGTools.TTHAnalysis.tools.nanoAOD.jetMetCorrelator import jetMetCorrelations2016, jetMetCorrelations2017, jetMetCorrelations2018

jme2016_allvariations = [jetmetUncertainties2016All,jetMetCorrelate2016] 
jme2017_allvariations = [jetmetUncertainties2017All,jetMetCorrelate2017]
jme2018_allvariations = [jetmetUncertainties2018All,jetMetCorrelate2018]

jme2016 = [jetmetUncertainties2016All,jetMetCorrelations2016] 
jme2017 = [jetmetUncertainties2017All,jetMetCorrelations2017]
jme2018 = [jetmetUncertainties2018All,jetMetCorrelations2018]

jme2017_5TeV = createJMECorrector(True, "2017", "G", "Total", False, "AK4PFchs", False)
jme2017_5TeV_Data = createJMECorrector(False, "2017", "G", "Total", False, "AK4PFchs", False)

def _fires(ev, path):
    if "/hasfiredtriggers_cc.so" not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/Production/src/hasfiredtriggers.cc+" % os.environ['CMSSW_BASE'])
    if not hasattr(ev,path): return False 

    if ev.run == 1:  # is MC
        return getattr( ev,path ) 
    else : #if hasattr(ev,"year"): 
        return getattr(ROOT, 'fires_%s_%d'%(path,ev.year))( ev.run, getattr(ev,path))
##    else:
##        return getattr(ROOT, 'fires_%s'%(path))( ev.run, getattr(ev,path))


triggerGroups=dict(
    Trigger_5TeV_FR={
        2017 : lambda ev : _fires(ev,'HLT_HIEle15_CaloIdL_TrackIdL_IsoVL_PFJet30') or _fires(ev,'HLT_HIL3Mu7') or _fires(ev,'HLT_HIL3Mu5_AK4PFJet30') or _fires(ev,'HLT_HIAK4PFJet30')
    },
    Trigger_5TeV_1e={
        2017 : lambda ev : _fires(ev,'HLT_HIEle20_WPLoose_Gsf') or _fires(ev,'HLT_HIEle17_WPLoose_Gsf')
    },
    Trigger_5TeV_1m={
        2017 : lambda ev : _fires(ev,'HLT_HIL3Mu20') or _fires(ev,'HLT_HIMu17') or _fires(ev,'HLT_HIL3Mu12') 
    },
    Trigger_5TeV_2e={
        2017 : lambda ev : _fires(ev,'HLT_HIEle20_Ele12_CaloIdL_TrackIdL_IsoVL_DZ') or _fires(ev,'HLT_HIEle15_Ele8_CaloIdL_TrackIdL_IsoVL')
    },
    Trigger_5TeV_2m={
        2017 : lambda ev : _fires(ev,'HLT_HIL3DoubleMu10') 
    },
    Trigger_1e={
        2016 : lambda ev : _fires(ev,'HLT_Ele27_WPTight_Gsf') or _fires(ev,'HLT_Ele25_eta2p1_WPTight_Gsf') or _fires(ev,'HLT_Ele27_eta2p1_WPLoose_Gsf'),
        2017 : lambda ev : _fires(ev,'HLT_Ele32_WPTight_Gsf') or _fires(ev,'HLT_Ele35_WPTight_Gsf'),
        2018 : lambda ev : _fires(ev,'HLT_Ele32_WPTight_Gsf'),
    },
    Trigger_1m={
        2016 : lambda ev : _fires(ev,'HLT_IsoMu24') or _fires(ev,'HLT_IsoTkMu24') or _fires(ev,'HLT_IsoMu22_eta2p1') or _fires(ev,'HLT_IsoTkMu22_eta2p1') or _fires(ev,'HLT_IsoMu22') or _fires(ev,'HLT_IsoTkMu22'),
        2017 : lambda ev : _fires(ev,'HLT_IsoMu24') or _fires(ev,'HLT_IsoMu27'),
        2018 : lambda ev : _fires(ev,'HLT_IsoMu24'),
    },
    Trigger_2e={
        2016 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
        2018 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
    },
    Trigger_2m={
        2016 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL') or _fires(ev,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL') or  _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ') or _fires(ev,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'),
        2017 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8') or _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
        2018 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    },
    Trigger_em={
        2016 :  lambda ev : _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL') or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ') \
        or _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL') or _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 :  lambda ev : _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')\
        or _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'),
        2018 :  lambda ev : _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')\
        or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'),
    },
    Trigger_3e={
        2016 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'),
        2018 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'), # prescaled in the two years according to https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018
    },
    Trigger_3m={
        2016 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
        2017 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
        2018 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
    },
    Trigger_mee={
        2016 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
        2018 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
    },
    Trigger_mme={
        2016 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'),
        2018 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'),
    },
    Trigger_2lss={
        2016 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
        2017 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
        2018 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
    },
    Trigger_3l={
        2016 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
        2017 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
        2018 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
    },
    Trigger_MET={
        2016 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
        2017 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
        2018 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
    }
)


triggerGroups_dict=dict(
    Trigger_5TeV_FR={
        2017 : ['HLT_HIEle15_CaloIdL_TrackIdL_IsoVL_PFJet30','HLT_HIL3Mu5_AK4PFJet30','HLT_HIL3Mu7','HLT_HIAK4PFJet30']
    },
    Trigger_5TeV_1e={
        2017 : ['HLT_HIEle20_WPLoose_Gsf','HLT_HIEle17_WPLoose_Gsf']
    },
    Trigger_5TeV_1m={
        2017 : ['HLT_HIL3Mu20','HLT_HIMu17','HLT_HIL3Mu12'] 
    },
    Trigger_5TeV_2e={
        2017 : ['HLT_HIEle20_Ele12_CaloIdL_TrackIdL_IsoVL_DZ','HLT_HIEle15_Ele8_CaloIdL_TrackIdL_IsoVL']
    },
    Trigger_5TeV_2m={
        2017 : ['HLT_HIL3DoubleMu10'] 
    },
    Trigger_1e={
        2016 :  ['HLT_Ele27_WPTight_Gsf' , 'HLT_Ele25_eta2p1_WPTight_Gsf' , 'HLT_Ele27_eta2p1_WPLoose_Gsf'],
        2017 :  ['HLT_Ele32_WPTight_Gsf' , 'HLT_Ele35_WPTight_Gsf'],
        2018 :  ['HLT_Ele32_WPTight_Gsf'],
    },
    Trigger_1m={
        2016 :  ['HLT_IsoMu24' , 'HLT_IsoTkMu24' , 'HLT_IsoMu22_eta2p1' , 'HLT_IsoTkMu22_eta2p1' , 'HLT_IsoMu22' , 'HLT_IsoTkMu22'],
        2017 :  ['HLT_IsoMu24' , 'HLT_IsoMu27'],
        2018 :  ['HLT_IsoMu24'],
    },
    Trigger_2e={
        2016 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
        2017 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        2018 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
    },
    Trigger_2m={
        2016 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL' ,  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'],
        2017 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8' , 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
        2018 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
    },
    Trigger_em={
        2016 :   ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'],
        2017 :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        2018 :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
    },
    Trigger_3e={
        2016 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        2017 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        2018 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'], # prescaled in the two years according to https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018
    },
    Trigger_3m={
        2016 :  ['HLT_TripleMu_12_10_5'],
        2017 :  ['HLT_TripleMu_12_10_5'],
        2018 :  ['HLT_TripleMu_12_10_5'],
    },
    Trigger_mee={
        2016 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        2017 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        2018 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
    },
    Trigger_mme={
        2016 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL'   ],
        2017 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
        2018 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
    },
)


from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
Trigger_5TeV_FR = lambda : EvtTagger('Trigger_5TeV_FR',[ lambda ev : triggerGroups['Trigger_5TeV_FR'][2017](ev) ])
Trigger_5TeV_1e = lambda : EvtTagger('Trigger_5TeV_1e',[ lambda ev : triggerGroups['Trigger_5TeV_1e'][2017](ev) ])
Trigger_5TeV_1m = lambda : EvtTagger('Trigger_5TeV_1m',[ lambda ev : triggerGroups['Trigger_5TeV_1m'][2017](ev) ])
Trigger_5TeV_2e = lambda : EvtTagger('Trigger_5TeV_2e',[ lambda ev : triggerGroups['Trigger_5TeV_2e'][2017](ev) ])
Trigger_5TeV_2m = lambda : EvtTagger('Trigger_5TeV_2m',[ lambda ev : triggerGroups['Trigger_5TeV_2m'][2017](ev) ])

Trigger_1e   = lambda : EvtTagger('Trigger_1e',[ lambda ev : triggerGroups['Trigger_1e'][ev.year](ev) ])
Trigger_1m   = lambda : EvtTagger('Trigger_1m',[ lambda ev : triggerGroups['Trigger_1m'][ev.year](ev) ])
Trigger_2e   = lambda : EvtTagger('Trigger_2e',[ lambda ev : triggerGroups['Trigger_2e'][ev.year](ev) ])
Trigger_2m   = lambda : EvtTagger('Trigger_2m',[ lambda ev : triggerGroups['Trigger_2m'][ev.year](ev) ])
Trigger_em   = lambda : EvtTagger('Trigger_em',[ lambda ev : triggerGroups['Trigger_em'][ev.year](ev) ])
Trigger_3e   = lambda : EvtTagger('Trigger_3e',[ lambda ev : triggerGroups['Trigger_3e'][ev.year](ev) ])
Trigger_3m   = lambda : EvtTagger('Trigger_3m',[ lambda ev : triggerGroups['Trigger_3m'][ev.year](ev) ])
Trigger_mee  = lambda : EvtTagger('Trigger_mee',[ lambda ev : triggerGroups['Trigger_mee'][ev.year](ev) ])
Trigger_mme  = lambda : EvtTagger('Trigger_mme',[ lambda ev : triggerGroups['Trigger_mme'][ev.year](ev) ])
Trigger_2lss = lambda : EvtTagger('Trigger_2lss',[ lambda ev : triggerGroups['Trigger_2lss'][ev.year](ev) ])
Trigger_3l   = lambda : EvtTagger('Trigger_3l',[ lambda ev : triggerGroups['Trigger_3l'][ev.year](ev) ])
Trigger_MET  = lambda : EvtTagger('Trigger_MET',[ lambda ev : triggerGroups['Trigger_MET'][ev.year](ev) ])

triggerSequence = [Trigger_5TeV_FR,Trigger_5TeV_1e,Trigger_5TeV_1m,Trigger_5TeV_2e,Trigger_5TeV_2m] #,Trigger_em,Trigger_3e,Trigger_3m,Trigger_mee,Trigger_mme,Trigger_2lss,Trigger_3l ,Trigger_MET]


from CMGTools.TTHAnalysis.tools.BDT_eventReco_cpp import BDT_eventReco

BDThttTT_Hj = lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjtagger_legacy_xgboost_v1.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HTT_HadTopTagger_2017_nomasscut_nvar17_resolved.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                     algostring = 'k_httTT_Hj',
                                     csv_looseWP = 0.5426, 
                                     csv_mediumWP = 0.8484,
                                     selection = [
                                         lambda leps,jets,event : len(leps)>=2,
                                         lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                                     ]
)

BDThttTT_allvariations = lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjtagger_legacy_xgboost_v1.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HTT_HadTopTagger_2017_nomasscut_nvar17_resolved.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                                algostring = 'k_httTT_Hj',
                                                csv_looseWP = 0.5426, 
                                                csv_mediumWP = 0.8484,
                                                selection = [
                                                    lambda leps,jets,event : len(leps)>=2,
                                                    lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                                                ],
                                                variations = [ 'jes%s'%v for v in jecGroups] + ['jer'] ,
)



from CMGTools.TTHAnalysis.tools.finalMVA_DNN import finalMVA_DNN
finalMVA = lambda : finalMVA_DNN()
finalMVA_allVars = lambda : finalMVA_DNN( variations = [ 'jes%s'%v for v in jecGroups] + ['jer'])

from CMGTools.TTHAnalysis.tools.finalMVA_DNN_3l import finalMVA_DNN_3l
finalMVA3L = lambda : finalMVA_DNN_3l()
finalMVA3L_allVars = lambda : finalMVA_DNN_3l(variations = [ 'jes%s'%v for v in jecGroups] + ['jer'])

from CMGTools.TTHAnalysis.tools.nanoAOD.finalMVA_4l import FinalMVA_4L
finalMVA_4l = lambda : FinalMVA_4L()


from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer


btagSF2016_dj = lambda : btagSFProducer("Legacy2016",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)
btagSF2017_dj = lambda : btagSFProducer("2017",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)
btagSF2018_dj = lambda : btagSFProducer("2018",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)

from CMGTools.TTHAnalysis.tools.nanoAOD.BtagSFs import BtagSFs
bTagSFs = lambda : BtagSFs("JetSel_Recl",
                           corrs={  "AbsoluteScale": 1., "AbsoluteStat":0., "FlavorQCD":1.,"Fragmentation":1.,"PileUpDataMC":0.5,"PileUpPtBB":0.5,"PileUpPtEC1":0.5,"PileUpPtEC2":0.5,"PileUpPtHF":0.5,"PileUpPtRef":0.5,"RelativeFSR":0.5,"RelativeJEREC1":0., "RelativeJEREC2":0., "RelativeJERHF":0.5,"RelativePtBB":0.5,"RelativePtEC1":0.,"RelativePtEC2":0.,"RelativePtHF":0.5, "RelativeBal":0.5, "RelativeStatEC":0., "RelativeStatFSR":0., "RelativeStatHF":0.,"SinglePionECAL":1., "SinglePionHCAL": 1., "TimePtEta":0., "AbsoluteMPFBias": 1.} # relative sample not there 
                       )

bTagSFs_allvars = lambda : BtagSFs("JetSel_Recl",
                                   corrs=jecGroups,
                       )

from CMGTools.TTHAnalysis.tools.nanoAOD.lepScaleFactors_WZ5TeV import lepScaleFactors_WZ5TeV
leptonSFs = lambda : lepScaleFactors_WZ5TeV()

scaleFactorSequence_2016 = [btagSF2016_dj,bTagSFs] 
scaleFactorSequence_2017 = [btagSF2017_dj,bTagSFs] 
scaleFactorSequence_2018 = [btagSF2018_dj,bTagSFs]

scaleFactorSequence_allVars_2016 = [btagSF2016_dj,bTagSFs_allvars] 
scaleFactorSequence_allVars_2017 = [btagSF2017_dj,bTagSFs_allvars] 
scaleFactorSequence_allVars_2018 = [btagSF2018_dj,bTagSFs_allvars]


from CMGTools.TTHAnalysis.tools.nanoAOD.higgsDecayFinder import higgsDecayFinder
higgsDecay = lambda : higgsDecayFinder()

from CMGTools.TTHAnalysis.tools.nanoAOD.VHsplitter import VHsplitter
vhsplitter = lambda : VHsplitter()

# from CMGTools.TTHAnalysis.tools.synchTools import SynchTuples
# synchTuples = lambda : SynchTuples()


# instructions to friend trees  code 

# 0_jmeUnc_v1
# mc only (per year) 
# jetmetUncertainties2016 
# jetmetUncertainties2017
# jetmetUncertainties2018

# 3_recleaner_v0 (recleaner, also containing mc matching and trigger bits) 
# recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence (MC)
# recleaner_step1,recleaner_step2_data,triggerSequence (data)

# 4_leptonSFs_v0 (lepton, trigger and btag scale factors, to run after recleaning) 
# mc only (per year)
# scaleFactorSequence_2016
# scaleFactorSequence_2017
# scaleFactorSequence_2018

# 5_evtVars_v0
from CMGTools.TTHAnalysis.tools.nanoAOD.ttH_gen_reco import ttH_gen_reco
