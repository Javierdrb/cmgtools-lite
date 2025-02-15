import os, sys, enum
import ROOT as r

class ch(enum.IntEnum):
    NoChan = 0
    ElMu   = 1
    Muon   = 2
    Elec   = 3
    ElMuFromTaus = 4
    MuonFromTaus = 5
    ElecFromTaus = 6
    ElMuMixedFromTaus = 7
    MuonMixedFromTaus = 8
    ElecMixedFromTaus = 9


class tags(enum.IntEnum):
    NoTag      = 0
    mc         = 1
    singlemuon = 2
    singleelec = 3
    doublemuon = 4
    doubleeg   = 5
    muoneg     = 6

# =========================================================================================================================
# ============================================================================================ TRIGGER
# =========================================================================================================================
def _fires(ev, path):
    if "/hasfiredtriggers_cc.so" not in r.gSystem.GetLibraries():
        r.gROOT.ProcessLine(".L %s/src/CMGTools/Production/src/hasfiredtriggers.cc+" % os.environ['CMSSW_BASE'])
    if not hasattr(ev, path): return False

    if ev.run == 1:  # is MC
        return getattr(ev, path)
    else :
        return getattr(r, 'fires_%s_%d'%(path, ev.year))( ev.run, getattr(ev, path) )

'''
#stop
triggerGroups = dict(
    Trigger_1e = {
        2016 : lambda ev : _fires(ev, 'HLT_Ele27_WPTight_Gsf'),
        2017 : lambda ev : _fires(ev, 'HLT_Ele35_WPTight_Gsf'),
        2018 : lambda ev : _fires(ev, 'HLT_Ele32_WPTight_Gsf'),
    },
    Trigger_1m = {
        2016 : lambda ev : (   _fires(ev, 'HLT_IsoMu24')
                            or _fires(ev, 'HLT_IsoTkMu24')),
        2017 : lambda ev : (   _fires(ev, 'HLT_IsoMu27')
                            or _fires(ev,'HLT_IsoMu24_eta2p1')), #change
        2018 : lambda ev :     _fires(ev, 'HLT_IsoMu24'),
    },
    Trigger_2e = {
        2016 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 : lambda ev : (_fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL') or _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')),#change
        2018 : lambda ev : (_fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL') or _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')), #change
    },
    Trigger_2m = {
        2016 : lambda ev : ((   _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL')
                             or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else
                            
                            (  _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ')
                            or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'))),
        2017 : lambda ev : ( _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ')
                            if (ev.datatag == tags.mc or ev.run <= 299368) else

                            (  _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8')
                            or _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'))), #change
        2018 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    },
    Trigger_em = {
        2016 : lambda ev : ((  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else

                            (  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"))),
        2017 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')), #change
        2018 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')), #change
    },
)
'''
triggerGroups = dict(
    Trigger_1e = {
        2016 : lambda ev : _fires(ev, 'HLT_Ele27_WPTight_Gsf'),
        2017 : lambda ev : _fires(ev, 'HLT_Ele35_WPTight_Gsf'),
        2018 : lambda ev : _fires(ev, 'HLT_Ele32_WPTight_Gsf'),
    },
    Trigger_1m = {
        2016 : lambda ev : (   _fires(ev, 'HLT_IsoMu24')
                            or _fires(ev, 'HLT_IsoTkMu24')),
        2017 : lambda ev :     _fires(ev, 'HLT_IsoMu27'),
        2018 : lambda ev :     _fires(ev, 'HLT_IsoMu24'),
    },
    Trigger_2e = {
        2016 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
        2018 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
    },
    Trigger_2m = {
        2016 : lambda ev : ((   _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL')
                             or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else

                            (  _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ')
                            or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'))),
        2017 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'),
        2018 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    },
    Trigger_em = {
        2016 : lambda ev : ((  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else

                            (  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"))),
        2017 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
        2018 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
    },
)

from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
Trigger_1e = lambda : EvtTagger('Trigger_1e',  [ lambda ev : triggerGroups['Trigger_1e'][ev.year](ev) ])
Trigger_1m = lambda : EvtTagger('Trigger_1m',  [ lambda ev : triggerGroups['Trigger_1m'][ev.year](ev) ])
Trigger_2e = lambda : EvtTagger('Trigger_2e',  [ lambda ev : triggerGroups['Trigger_2e'][ev.year](ev) ])
Trigger_2m = lambda : EvtTagger('Trigger_2m',  [ lambda ev : triggerGroups['Trigger_2m'][ev.year](ev) ])
Trigger_em = lambda : EvtTagger('Trigger_em',  [ lambda ev : triggerGroups['Trigger_em'][ev.year](ev) ])

remove_overlap_booleans = [ lambda ev : (
                            (  (ev.channel == ch.ElMu and (ev.Trigger_em or ev.Trigger_1m or ev.Trigger_1e))
                            or (ev.channel == ch.Muon and (ev.Trigger_1m or ev.Trigger_2m))
                            or (ev.channel == ch.Elec and (ev.Trigger_1e or ev.Trigger_2e)) )
                            if ev.datatag == tags.mc else

                            (  (ev.channel == ch.ElMu and (not ev.Trigger_em) and ev.Trigger_1m)
                            or (ev.channel == ch.Muon and (not ev.Trigger_2m) and ev.Trigger_1m))
                            if ev.datatag == tags.singlemuon else

                            ((  ev.channel == ch.ElMu and (not ev.Trigger_em) and (not ev.Trigger_1m) and ev.Trigger_1e)
                            or (ev.channel == ch.Elec and (not ev.Trigger_2e) and ev.Trigger_1e))
                            if ev.datatag == tags.singleelec else

                            (   ev.channel == ch.Muon and ev.Trigger_2m)
                            if ev.datatag == tags.doublemuon else

                            (  ev.channel == ch.Elec and ev.Trigger_2e)
                            if ev.datatag == tags.doubleeg else

                            (  ev.channel == ch.ElMu and ev.Trigger_em)
                            if ev.datatag == tags.muoneg else

                            (False)
                        )]

remove_overlap = lambda : EvtTagger('pass_trigger', remove_overlap_booleans)

triggerSeq = [Trigger_1e, Trigger_1m, Trigger_2e, Trigger_2m, Trigger_em, remove_overlap]

# =========================================================================================================================
# ============================================================================================ OTHER GENERAL MODULES
# =========================================================================================================================



# =========================================================================================================================
# ============================================================================================ ANALYSIS MODULES & SETTINGS
# =========================================================================================================================

# %%%%%%%%%%%%%%%%%%%%%%%%%% tW full Run 2 inclusive & differential
#### LEPTON TREATMENTS ###
IDDict = {}
IDDict["muons"] = {
    #"pt"       : 20,
    "pt"       : 18, # Lo del stop
    "eta"      : 2.4,
    "isorelpf" : 0.15,
}

IDDict["elecs"] = {
    #"pt"   : 20,
    "pt"   : 18, # Lo del stop
    "eta0" : 1.4442,
    "eta1" : 1.566,
    "eta2" : 2.4,
    "dxy_b" : 0.05,
    "dz_b"  : 0.10,
    "dxy_e" : 0.10,
    "dz_e"  : 0.20,
    "etasc_be" : 1.479,
}

IDDict["jets"] = {
    "pt"      : 30,
    "pt2"     : 20,
    "ptmin"   : 15,
    "ptfwdnoise" : 60,
    "eta"     : 2.4,
    "etafwd"  : 5.0,
    "etafwdnoise0" : 2.7,
    "etafwdnoise1" : 3.0,
    "jetid_2016" : 0,  # > X
    #"jetid_2016" : 1,  # > X Lo del stop
    "jetid_2017" : 1,  # > X
    "jetid_2018" : 1,  # > X
}

#muonID = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      #and l.tightId == 1 )
muonID = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.corrected_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )
#muonID_validacion = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      #and l.tightId == 1 ) #### VALIDACION CRAMONAL

elecID = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       #and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (l.eta <= IDDict["elecs"]["etasc_be"])   #### COMOL STOP
                       #else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
                       #and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.deltaEtaSC - l.eta) <= IDDict["elecs"]["etasc_be"]) ### COMO IGUAL ES
                       #else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )


muonID_lepenUp = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedUp_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

# TODO: esto de aqui ponerlo bien
elecID_lepenUp = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )

muonID_lepenDn = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedDown_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

# TODO: esto de aqui ponerlo bien
elecID_lepenDn = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )



dresslepID         = lambda l : ( (abs(l.eta) < IDDict["muons"]["eta"] and l.pt > IDDict["muons"]["pt"]) if (abs(l.pdgId) == 13) else
                                  (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"])
                                   and l.pt > IDDict["elecs"]["pt"]) if (abs(l.pdgId) == 11) else False )
dressjetID         = lambda j : ( abs(j.eta) < 2.4 and j.pt > IDDict["jets"]["pt"] )
dressloosejetID    = lambda j : ( abs(j.eta) < 2.4 and j.pt > IDDict["jets"]["pt2"] and j.pt < IDDict["jets"]["pt"] )
dressfwdjetID      = lambda j : ( abs(j.eta) >= 2.4 and abs(j.eta) < 5.0 and
                                  ( ((abs(j.eta) < 2.7 or abs(j.eta) >= 3.0) and j.pt > IDDict["jets"]["pt"]) or
                                    ((abs(j.eta) >= 2.7 or abs(j.eta) < 3.0) and j.pt > IDDict["jets"]["ptfwdnoise"]) ) )
dressfwdloosejetID = lambda j : ( abs(j.eta) >= 2.4 and abs(j.eta) < 5.0 and (abs(j.eta) < 2.7 or abs(j.eta) >= 3.0) and j.pt > IDDict["jets"]["pt2"] )



from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = lambda : collectionMerger(input = ["Electron", "Muon"],
                                     output = "LepGood",
                                     selector = dict(Muon = muonID, Electron = elecID))
#lepMerge_validacion = lambda : collectionMerger(input = ["Electron", "Muon"],
                                     #output = "LepGood",
                                     #selector = dict(Muon = muonID_validacion, Electron = elecID))

lepMerge_muenUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuUp",
                                            selector = dict(Muon = muonID_lepenUp, Electron = elecID))
lepMerge_muenDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuDown",
                                            selector = dict(Muon = muonID_lepenDn, Electron = elecID))

lepMerge_elenUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodelUp",
                                            selector = dict(Muon = muonID, Electron = elecID_lepenUp))
lepMerge_elenDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodelDown",
                                            selector = dict(Muon = muonID, Electron = elecID_lepenDn))
# Lepton & trigger SF
from CMGTools.TTHAnalysis.tools.nanoAOD.lepScaleFactors_ttbarRun2 import lepScaleFactors_ttbarRun2
leptrigSFs = lambda : lepScaleFactors_ttbarRun2()


#### JET TREATMENTS ###
from CMGTools.TTHAnalysis.tools.nanoAOD.btag_weighter               import btag_weighter
from CMGTools.TTHAnalysis.tools.nanoAOD.jetmetGrouper               import groups as jecGroups

## b-tagging
btagEffpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/TopRun2/btagging/"
btagSFpath  = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/"

btagWeights_2016 = lambda : btag_weighter(btagSFpath + "DeepJet_2016LegacySF_V1.csv",  btagEffpath + "BtagMCSF.root", 'deepjet', year = 2016)
btagWeights_2017 = lambda : btag_weighter(btagSFpath + "DeepFlavour_94XSF_V3_B_F.csv", btagEffpath + "BtagMCSF.root", 'deepjet', year = 2017)
btagWeights_2018 = lambda : btag_weighter(btagSFpath + "DeepJet_102XSF_V1.csv",        btagEffpath + "BtagMCSF.root", 'deepjet', year = 2018)


# Cleaning
#from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaningTopRun2     import CombinedObjectTaggerForCleaningTopRun2
#from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleanerTopRun2 import fastCombinedObjectRecleanerTopRun2
#from CMGTools.TTHAnalysis.tools.nanoAOD.cleaningTopRun2 import cleaningTopRun2
from CMGTools.TTHAnalysis.tools.nanoAOD.pythonCleaningttbarRun2 import pythonCleaningttbarRun2

#cleaning_mc = lambda : cleaningTopRun2(label = "Recl",
                                       #jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                       #jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"], isMC = True,
                                       #jecvars   = ['jesTotal', 'jer'],
                                       #lepenvars = ["mu"],
                                       ##variations = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups]
#)

#cleaning_data = lambda : cleaningTopRun2(label = "Recl",
                                         #jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                         #jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"], isMC = False,
                                         #jecvars   = [],
                                         #lepenvars = [],
#)


cleaning_mc = lambda : pythonCleaningttbarRun2(label = "Recl",
                                             jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                             jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                             jecvars   = ['jesTotal', 'jer'],
                                             lepenvars = ["mu"],
                                             isMC = True,
                                             #debug = True,
                                             #variations = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups]
)

#cleaning_mc_validacion = lambda : pythonCleaningTopRun2(label = "Recl",
                                             #jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                             #jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                             #jecvars   = [],
                                             #lepenvars = [],
                                             #isMC = False,
#)

cleaning_data = lambda : pythonCleaningttbarRun2(label = "Recl",
                                               jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                               jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                               jecvars   = [], lepenvars = [], isMC = False,
)


#### EVENT VARIABLES ###
from CMGTools.TTHAnalysis.tools.eventVars_ttbarRun2 import EventVars_ttbarRun2
eventVars_mc = lambda : EventVars_ttbarRun2('', 'Recl',
                                        #jecvars = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups])
                                         jecvars = ['jesTotal', 'jer'],
                                         lepvars = ['mu'])
#eventVars_mc_validacion = lambda : EventVars_tWRun2('', 'Recl',
                                         #jecvars = [],
                                         #lepvars = [], isMC = False)
eventVars_data = lambda : EventVars_ttbarRun2('', 'Recl', isMC = False,
                                           #jecvars = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups])
                                           jecvars = [],
                                           lepvars = [])


#### Add year
from CMGTools.TTHAnalysis.tools.addYear import addYear
addYear_2016 = lambda : addYear(2016)
addYear_2017 = lambda : addYear(2017)
addYear_2018 = lambda : addYear(2018)  #### NOTE: this also adds the PrefireWeight as a branch for this year

#### Add data tag
from CMGTools.TTHAnalysis.tools.addDataTag import addDataTag
addMuonEG     = lambda : addDataTag(tags.muoneg)
addDoubleMuon = lambda : addDataTag(tags.doublemuon)
addDoubleEG   = lambda : addDataTag(tags.doubleeg)
addSingleMuon = lambda : addDataTag(tags.singlemuon)
addSingleElec = lambda : addDataTag(tags.singleelec)
addMC         = lambda : addDataTag(tags.mc)
addMC_ttbar   = lambda : addDataTag(tags.mc, isTop = True)

from CMGTools.TTHAnalysis.tools.addJetPtCorr_ttbar import addJetPtCorr

addJetPtCorrAll = lambda : addJetPtCorr()

addYearTag_2016_mc         = [addYear_2016, addMC        ]#, addJetPtCorrAll]
addYearTag_2016_mc_ttbar   = [addYear_2016, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2016_singlemuon = [addYear_2016, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2016_singleelec = [addYear_2016, addSingleElec]#, addJetPtCorrAll]
addYearTag_2016_doublemuon = [addYear_2016, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2016_doubleeg   = [addYear_2016, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2016_muoneg     = [addYear_2016, addMuonEG    ]#, addJetPtCorrAll]

addYearTag_2017_mc         = [addYear_2017, addMC        ]#, addJetPtCorrAll]
addYearTag_2017_mc_ttbar   = [addYear_2017, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2017_singlemuon = [addYear_2017, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2017_singleelec = [addYear_2017, addSingleElec]#, addJetPtCorrAll]
addYearTag_2017_doublemuon = [addYear_2017, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2017_doubleeg   = [addYear_2017, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2017_muoneg     = [addYear_2017, addMuonEG    ]#, addJetPtCorrAll]

addYearTag_2018_mc         = [addYear_2018, addMC        ]#, addJetPtCorrAll]
addYearTag_2018_mc_ttbar   = [addYear_2018, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2018_singlemuon = [addYear_2018, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2018_singleelec = [addYear_2018, addSingleElec]#, addJetPtCorrAll]
addYearTag_2018_doublemuon = [addYear_2018, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2018_doubleeg   = [addYear_2018, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2018_muoneg     = [addYear_2018, addMuonEG    ]#, addJetPtCorrAll]


#### Add Rochester corrections
from CMGTools.TTHAnalysis.tools.addRochester import addRochester
#from CMGTools.TTHAnalysis.tools.addRochesterValid import addRochesterValid
addRoch_mc = lambda : addRochester()
#addRoch_mc_validacion = lambda : addRochesterValid()
addRoch_data = lambda : addRochester(isMC = False)

from CMGTools.TTHAnalysis.tools.nanoAOD.selectParticleAndPartonInfo_ttbar import selectParticleAndPartonInfo
theDressAndPartInfo = lambda : selectParticleAndPartonInfo(dresslepSel_         = dresslepID,
                                                           dressjetSel_         = dressjetID,
                                                           dressloosejetSel_    = dressloosejetID,
                                                           dressfwdjetSel_      = dressfwdjetID,
                                                           dressfwdloosejetSel_ = dressfwdloosejetID)

#lepMerge_roch_mc   = [lepMerge, lepMerge_muenUp, lepMerge_muenDn, lepMerge_elenUp, lepMerge_elenDn, addRoch_mc, theDressAndPartInfo] ### FIXME: este es el "bueno"
lepMerge_roch_mc   = [lepMerge, lepMerge_muenUp, lepMerge_muenDn, addRoch_mc, theDressAndPartInfo]
#lepMerge_roch_mc_validacion   = [lepMerge_validacion, addRoch_mc_validacion, theDressAndPartInfo]
lepMerge_roch_data = [lepMerge, addRoch_data]


#### BDT
from CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2 import MVA_tWRun2
MVAProc_mc   = lambda : MVA_tWRun2()
MVAProc_data = lambda : MVA_tWRun2(isData = True)

mvas_mc   = [MVAProc_mc]
mvas_data = [MVAProc_data]

'''
from CMGTools.TTHAnalysis.tools.nanoAOD.createTrainingMiniTree_tWRun2 import createTrainingMiniTree_tWRun2

createMVAMiniTree = lambda : createTrainingMiniTree_tWRun2()
'''

from CMGTools.TTHAnalysis.tools.particleAndPartonVars_ttbarRun2 import particleAndPartonVars_tWRun2
theDressAndPartVars = lambda : particleAndPartonVars_tWRun2()

varstrigger_mc   = [eventVars_mc, theDressAndPartVars] + triggerSeq
#varstrigger_mc_validacion = [eventVars_mc_validacion, theDressAndPartVars] + triggerSeq
varstrigger_data = [eventVars_data] + triggerSeq


from CMGTools.TTHAnalysis.tools.nanoAOD.TopPtWeight import TopPtWeight
addTopPtWeight = lambda : TopPtWeight()

from CMGTools.TTHAnalysis.tools.addSeparationIndex import addSeparationIndex

applicationProportion = 0.6

addSeparationIndex_nomva   = lambda : addSeparationIndex(isThisSampleForMVA = False, applicationProp = applicationProportion)
addSeparationIndex_mva     = lambda : addSeparationIndex(isThisSampleForMVA = True, applicationProp = applicationProportion)
addSeparationIndex_mva_ent = lambda : addSeparationIndex(isThisSampleForMVA = True, isEntire = True, applicationProp = applicationProportion)

sfSeq_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_nomva]
sfSeq_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_nomva]
sfSeq_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_nomva]

sfSeq_mvatrain_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_mva]
sfSeq_mvatrain_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_mva]
sfSeq_mvatrain_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_mva]

sfSeq_mvatrain_ent_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_mva_ent]
sfSeq_mvatrain_ent_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_mva_ent]
sfSeq_mvatrain_ent_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_mva_ent]


#### TEMPORAL
#addYearTag_2016_mc_validacion         = [addYear_2016, addMC        ]
#addYearTag_2016_singlemuon_validacion = [addYear_2016, addSingleMuon]
#addYearTag_2016_singleelec_validacion = [addYear_2016, addSingleElec]
#addYearTag_2016_doublemuon_validacion = [addYear_2016, addDoubleMuon]
#addYearTag_2016_doubleeg_validacion   = [addYear_2016, addDoubleEG  ]
#addYearTag_2016_muoneg_validacion     = [addYear_2016, addMuonEG    ]






# %%%%%%%%%%%%%%%%%%%%%%%%%% WWbb
# TODO

# %%%%%%%%%%%%%%%%%%%%%%%%%% tW+/tW-
# TODO
