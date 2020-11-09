# -*- coding: UTF-8 -*-.
#!/usr/bin/env python
import os, sys, enum, argparse
from multiprocessing import Pool
import warnings as wr
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

#### Settings
friendspath = "/pool/phedexrw/userstorage/vrbouza/proyectos/tw_run2/productions"
#prodname    = "2020-05-29" # veya
#prodname    = "2020-06-01_bkp" # veya
#prodname    = "2020-06-17" # nova


#prodname    = "2020-07-03" # con sistematicos, en 2016 col tuning veyo
#prodname    = "2020-07-29" # prueba para Sheyla
#prodname    = "2020-09-16" # prueba tras profundos cambios
prodname    = "2020-09-20" # tras la prueba, todo aparentemente en orden; BUENA
#prodname    = "2020-09-23" # validacion cramonal



datasamples  = ["SingleMuon", "SingleElec", "DoubleMuon", "DoubleEG", "MuonEG", "LowEGJet", "HighEGJet", "EGamma"]
mcpath       = "/pool/ciencias/nanoAODv6/29jan2020_MC"
mcpathdiv    = "/pool/phedex/userstorage/vrbouza/proyectos/tw_run2/misc/divisiones/"
#mcpath       = "/pool/phedex/userstorage/clara/NanoAOD/Top_Nanov6_09_sep/2016_MC" # validacion cramonal
datapath     = "/pool/ciencias/nanoAODv6/13jan2020"
logpath      = friendspath + "/" + prodname + "/{y}/{step_prefix}/logs"
utilspath    = "/nfs/fanae/user/vrbouza/Proyectos/tw_run2/desarrollo/susyMaintenanceScripts/friendsWithBenefits"
commandscaff = "python prepareEventVariablesFriendTree.py -t NanoAOD {inpath} {outpath} -I CMGTools.TTHAnalysis.tools.nanoAOD.TopRun2_modules {module} {friends} {dataset} -N {chunksize} {cluster} {ex}"
clusterscaff = "--log {logdir} --name {jobname} -q {queue} --env oviedo"
#friendfolders = ["0_yeartag", "1_lepmerge_roch", "2_cleaning", "3_varstrigger", "4_scalefactors", "5_mvas"]


friendfolders = {0 : "0_yeartag",
                 1 : "1_lepmerge_roch",
                 2 : "2_cleaning",
                 3 : "3_varstrigger",
                 4 : "4_scalefactors",
                 5 : "5_mvas",
                 #5 : "5_mvas_new",
                 "mvatrain" : "x_mvatrain"
                }


chunksizes    = {0          : 5000000,
                 1          : 200000,
                 2          : 5000000,
                 #2          : 500000, #PARA DY DE 2017
                 3          : 500000,
                 4          : 500000,
                 5          : 250000,
                 "mvatrain" : 500000,
                 }

minchunkbytes = 1000

class errs(enum.IntEnum):
    NoErr   = 0
    exist   = 1
    size    = 2
    entries = 3
    corrupt = 4


minitnamedict = {
    "ttbar"     : ["TTTo2L2Nu_division2"],
    "tw"        : ["tW", "tW_division2"],
    "tbarw"     : ["tbarW", "tbarW_division2"],
    "dy_10to50" : ["DYJetsToLL_M_10to50", "DYJetsToLL_M_10to50_MLM"],
    "dy_50"     : ["DYJetsToLL_M_50"],
    }


sampledict  = {}
sampledict[2016] = {}; sampledict[2017] = {}; sampledict[2018] = {}
sampledict[2016] = {
    #### Nominales

    ### ttbar
    # CP5
    #"TTTo2L2Nu"        : ['Tree_TTTo2L2Nu_TuneCP5_PSweights_0','Tree_TTTo2L2Nu_TuneCP5_PSweights_1','Tree_TTTo2L2Nu_TuneCP5_PSweights_2','Tree_TTTo2L2Nu_TuneCP5_PSweights_3','Tree_TTTo2L2Nu_TuneCP5_PSweights_4','Tree_TTTo2L2Nu_TuneCP5_PSweights_5','Tree_TTTo2L2Nu_TuneCP5_PSweights_6','Tree_TTTo2L2Nu_TuneCP5_PSweights_7','Tree_TTTo2L2Nu_TuneCP5_PSweights_8','Tree_TTTo2L2Nu_TuneCP5_PSweights_9','Tree_TTTo2L2Nu_TuneCP5_PSweights_10','Tree_TTTo2L2Nu_TuneCP5_PSweights_11','Tree_TTTo2L2Nu_TuneCP5_PSweights_12'],

    "TTTo2L2Nu_division1" : ['Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_0','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_1','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_2','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_3','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_4','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_5','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_6','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_7','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_8','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_9','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_10','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_11','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_12'],

    "TTTo2L2Nu_division2" : ['Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_0','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_1','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_2','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_3','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_4','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_5','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_6','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_7','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_8','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_9','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_10','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_11','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_12'],

    "TTToSemiLeptonic" : "Tree_TTToSemiLeptonic_TuneCP5_PSweights_",

    # CUETP8M1
    #"TT_CUETP8M2T4"    : ["Tree_TT_TuneCUETP8M2T4_nobackup_*", "Tree_TT_TuneCUETP8M2T4_PSweights*", "Tree_TT_TuneCUETP8M2T4_0", "Tree_TT_TuneCUETP8M2T4_1", "Tree_TT_TuneCUETP8M2T4_2", "Tree_TT_TuneCUETP8M2T4_3"],
    #"TT_CUETP8M2T4"    : ["Tree_TT_TuneCUETP8M2T4_PSweights*", "Tree_TT_TuneCUETP8M2T4_0", "Tree_TT_TuneCUETP8M2T4_1", "Tree_TT_TuneCUETP8M2T4_2", "Tree_TT_TuneCUETP8M2T4_3"], # Nobackup ta mal

    ### tW
    # CP5
    #"tW"    : "Tree_tW_5f_inclusiveDecays_TuneCP5_PSweights_",
    #"tbarW" : "Tree_tbarW_5f_inclusiveDecays_TuneCP5_PSweights_",

    "tW_division1"    : "Tree_tWdiv1_5f_inclusiveDecays_TuneCP5_PSweights_",
    "tbarW_division1" : "Tree_tbarWdiv1_5f_inclusiveDecays_TuneCP5_PSweights_",

    "tW_division2"    : "Tree_tWdiv2_5f_inclusiveDecays_TuneCP5_PSweights_",
    "tbarW_division2" : "Tree_tbarWdiv2_5f_inclusiveDecays_TuneCP5_PSweights_",

    # CUETP8M1
    #"tW_noFullHad_CUETP8M2T4"    : "Tree_tW_5f_noFullHad_",
    #"tbarW_noFullHad_CUETP8M2T4" : "Tree_tbarW_5f_noFullHad_",

    ### WJets
    "WJetsToLNu_MLM": "Tree_WJetsToLNu_TuneCUETP8M1_MLM",

    ### DY
    "DYJetsToLL_M_10to50" : "Tree_DYJetsToLL_M_10to50_TuneCUETP8M1_amcatnloFXFX",
    "DYJetsToLL_M_50"     : "Tree_DYJetsToLL_M_50_TuneCUETP8M1_amcatnloFXFX",

    ### WW
    "WWTo2L2Nu" : "Tree_WWTo2L2Nu",
    "WWToLNuQQ" : "Tree_WWToLNuQQ",

    ### WZ
    "WZTo2L2Q"             : "Tree_WZTo2L2Q_amcatnloFXFX_madspin",
    "WZTo3LNu"             : "Tree_WZTo3LNu_TuneCUETP8M1",
    "WZTo1L1Nu2Q_aMCatNLO" : "Tree_WZTo1L1Nu2Q_amcatnloFXFX_madspin",
    "WZTo1L1Nu2Q"          : "Tree_WZToLNu2Q_0",

    ### ZZ
    "ZZTo2L2Nu"         : "Tree_ZZTo2L2Nu",
    "ZZTo2L2Q_aMCatNLO" : "Tree_ZZTo2L2Q_amcatnloFXFX_madspin",
    "ZZTo2L2Q"          : "Tree_ZZTo2L2Q_0",
    "ZZTo4L"            : "Tree_ZZTo4L",

    ### ttW
    "TTWJetsToLNu" : "Tree_TTWJetsToLNu_TuneCUETP8M1_amcatnloFXFX_madspin",
    "TTWJetsToQQ"  : "Tree_TTWJetsToQQ_TuneCUETP8M1_amcatnloFXFX_madspin",

    ### ttZ
    "TTZToLL_M_1to10_MLM" : "Tree_TTZToLL_M_1to10_TuneCUETP8M1_MLM",
    "TTZToLLNuNu_M_10"    : "Tree_TTZToLLNuNu_M_10_TuneCUETP8M1_amcatnlo",
    "TTZToQQ"             : "Tree_TTZToQQ_TuneCUETP8M1_amcatnlo",


    ##### Incertidumbres
    #### tW

    # CUETP8M1
    #"tW_noFullHad_DS_CUETP8M2T4"    : "Tree_tW_5f_DS_noFullHad_TuneCUETP8M",
    #"tbarW_noFullHad_DS_CUETP8M2T4" : "Tree_tbarW_5f_DS_noFullHad",

    # CP5


    #### ttbar
    ## hdamp CUETP8M1
    #"TT_hdampUp_CUETP8M2T4"     : "Tree_TT_hdampUP_TuneCUETP8M2T4",
    #"TT_hdampDown_CUETP8M2T4"   : "Tree_TT_hdampDOWN_TuneCUETP8M2T4",

    ## CR CUETP8M1
    #"TT_GluonMoveCRTune_CUETP8M2T4"      : "Tree_TT_TuneCUETP8M2T4_GluonMoveCRTune_ext1",
    #"TT_QCDbasedCRTune_erdON_CUETP8M2T4" : "Tree_TT_TuneCUETP8M2T4_QCDbasedCRTune_erdON",
    #"TT_erdON_CUETP8M2T4"                : "Tree_TT_TuneCUETP8M2T4_erdON",

    ## UE CUETP8M1
    #"TT_UEUp_CUETP8M2T4"   : "Tree_TT_TuneCUETP8M2T4up",
    #"TT_UEDown_CUETP8M2T4" : "Tree_TT_TuneCUETP8M2T4down",

    ## mtop CUETP8M1
    #"TT_mtop1735_CUETP8M2T4" : "Tree_TT_TuneCUETP8M2T4_mtop1735",
    #"TT_mtop1715_CUETP8M2T4" : "Tree_TT_TuneCUETP8M2T4_mtop1715",

    # hdamp CP5
    "TTTo2L2Nu_hdampUp"     : "Tree_TTTo2L2Nu_hdampUP_TuneCP5_PSweights_",
    "TTTo2L2Nu_hdampDown"   : "Tree_TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_",

    # CR CP5
    "TTTo2L2Nu_GluonMoveCRTune"      : "Tree_TTTo2L2Nu_TuneCP5CR2_GluonMove_PSweights_",
    "TTTo2L2Nu_QCDbasedCRTune_erdON" : "Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_",
    "TTTo2L2Nu_erdON"                : "Tree_TTTo2L2Nu_TuneCP5_PSweights_erdON_",

    # UE CP5
    "TTTo2L2Nu_UEUp"   : ['Tree_TTTo2L2Nu_TuneCP5up_PSweights_1','Tree_TTTo2L2Nu_TuneCP5up_PSweights_2','Tree_TTTo2L2Nu_TuneCP5up_PSweights_3','Tree_TTTo2L2Nu_TuneCP5up_PSweights_4','Tree_TTTo2L2Nu_TuneCP5up_PSweights_5','Tree_TTTo2L2Nu_TuneCP5up_PSweights_6','Tree_TTTo2L2Nu_TuneCP5up_PSweights_7','Tree_TTTo2L2Nu_TuneCP5up_PSweights_8','Tree_TTTo2L2Nu_TuneCP5up_PSweights_9','Tree_TTTo2L2Nu_TuneCP5up_PSweights_10','Tree_TTTo2L2Nu_TuneCP5up_PSweights_11','Tree_TTTo2L2Nu_TuneCP5up_PSweights_12','Tree_TTTo2L2Nu_TuneCP5up_PSweights_13','Tree_TTTo2L2Nu_TuneCP5up_PSweights_14','Tree_TTTo2L2Nu_TuneCP5up_PSweights_15','Tree_TTTo2L2Nu_TuneCP5up_PSweights_16','Tree_TTTo2L2Nu_TuneCP5up_PSweights_17', "Tree_TTTo2L2Nu_TuneCP5up_PSweights_ext1_*"], ### WARNING: EL 0 ESTÁ CORRUPTO
    "TTTo2L2Nu_UEDown" : "Tree_TTTo2L2Nu_TuneCP5down_PSweights_",



    #### Datos
    "SingleMuon"     : "Tree_SingleMuon_Run2016",
    "SingleElectron" : "Tree_SingleElectron_Run2016",
    "DoubleMuon"     : "Tree_DoubleMuon_Run2016",
    "DoubleEG"       : "Tree_DoubleEG_Run2016",
    "MuonEG"         : "Tree_MuonEG_Run2016",


    #### Validacion cramonal
    #"validttz"       : "TTZToLLNuNu_m1to10",
}



sampledict[2017] = {
    #### Nominales
    ### ttbar
    #"TTTo2L2Nu"        : ["Tree_TTTo2L2Nu_TuneCP5_PSweights_*", "Tree_TTTo2L2Nu_TuneCP5_*"],
    #"TTTo2L2Nu"        :['Tree_TTTo2L2Nu_TuneCP5_PSweights_0','Tree_TTTo2L2Nu_TuneCP5_PSweights_1','Tree_TTTo2L2Nu_TuneCP5_PSweights_2','Tree_TTTo2L2Nu_TuneCP5_PSweights_3','Tree_TTTo2L2Nu_TuneCP5_PSweights_4','Tree_TTTo2L2Nu_TuneCP5_PSweights_5','Tree_TTTo2L2Nu_TuneCP5_PSweights_6','Tree_TTTo2L2Nu_TuneCP5_PSweights_7','Tree_TTTo2L2Nu_TuneCP5_PSweights_8','Tree_TTTo2L2Nu_TuneCP5_PSweights_9','Tree_TTTo2L2Nu_TuneCP5_PSweights_10','Tree_TTTo2L2Nu_TuneCP5_PSweights_11','Tree_TTTo2L2Nu_TuneCP5_PSweights_12','Tree_TTTo2L2Nu_TuneCP5_PSweights_13','Tree_TTTo2L2Nu_TuneCP5_PSweights_14','Tree_TTTo2L2Nu_TuneCP5_PSweights_15','Tree_TTTo2L2Nu_TuneCP5_PSweights_16','Tree_TTTo2L2Nu_TuneCP5_PSweights_17','Tree_TTTo2L2Nu_TuneCP5_PSweights_18','Tree_TTTo2L2Nu_TuneCP5_PSweights_19','Tree_TTTo2L2Nu_TuneCP5_PSweights_20', "Tree_TTTo2L2Nu_TuneCP5_0", "Tree_TTTo2L2Nu_TuneCP5_1", "Tree_TTTo2L2Nu_TuneCP5_2"], ### THIS INCLUDES THE SAMPLE W/O PSWEIGHTS, NOW NOT USING IT

    #"TTTo2L2Nu"        :['Tree_TTTo2L2Nu_TuneCP5_PSweights_0','Tree_TTTo2L2Nu_TuneCP5_PSweights_1','Tree_TTTo2L2Nu_TuneCP5_PSweights_2','Tree_TTTo2L2Nu_TuneCP5_PSweights_3','Tree_TTTo2L2Nu_TuneCP5_PSweights_4','Tree_TTTo2L2Nu_TuneCP5_PSweights_5','Tree_TTTo2L2Nu_TuneCP5_PSweights_6','Tree_TTTo2L2Nu_TuneCP5_PSweights_7','Tree_TTTo2L2Nu_TuneCP5_PSweights_8','Tree_TTTo2L2Nu_TuneCP5_PSweights_9','Tree_TTTo2L2Nu_TuneCP5_PSweights_10','Tree_TTTo2L2Nu_TuneCP5_PSweights_11','Tree_TTTo2L2Nu_TuneCP5_PSweights_12','Tree_TTTo2L2Nu_TuneCP5_PSweights_13','Tree_TTTo2L2Nu_TuneCP5_PSweights_14','Tree_TTTo2L2Nu_TuneCP5_PSweights_15','Tree_TTTo2L2Nu_TuneCP5_PSweights_16','Tree_TTTo2L2Nu_TuneCP5_PSweights_17','Tree_TTTo2L2Nu_TuneCP5_PSweights_18','Tree_TTTo2L2Nu_TuneCP5_PSweights_19','Tree_TTTo2L2Nu_TuneCP5_PSweights_20'],

    "TTTo2L2Nu_division1" :['Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_0','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_1','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_2','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_3','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_4','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_5','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_6','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_7','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_8','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_9','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_10','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_11','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_12','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_13','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_14','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_15','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_16','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_17','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_18','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_19','Tree_TTTo2L2Nudiv1_TuneCP5_PSweights_20'],

    "TTTo2L2Nu_division2" :['Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_0','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_1','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_2','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_3','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_4','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_5','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_6','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_7','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_8','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_9','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_10','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_11','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_12','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_13','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_14','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_15','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_16','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_17','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_18','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_19','Tree_TTTo2L2Nudiv2_TuneCP5_PSweights_20'],

    "TTToSemiLeptonic" : "Tree_TTToSemiLeptonic_TuneCP5_",

    ### tW
    # inclusiva
    "tW"              : "Tree_tW_5f_inclusiveDecays_TuneCP5_PSweights_pythia8new_",
    #"tW"              : ["Tree_tW_5f_inclusiveDecays_TuneCP5_0", "Tree_tW_5f_inclusiveDecays_TuneCP5_1", "Tree_tW_5f_inclusiveDecays_TuneCP5_2", "Tree_tW_5f_inclusiveDecays_TuneCP5_3", "Tree_tW_5f_inclusiveDecays_TuneCP5_4", "Tree_tW_5f_inclusiveDecays_TuneCP5_5", "Tree_tW_5f_inclusiveDecays_TuneCP5_6"], ### WARNING: CORRUPTOS LOS pythia8new
    "tbarW"           : ["Tree_tbarW_5f_inclusiveDecays_TuneCP5_1", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_2", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_3", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_4", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_5", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_6", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_7", "Tree_tbarW_5f_inclusiveDecays_TuneCP5_PSweights_pythia_*"],   ### WARNING: EL 0 ESTÁ CORRUPTO

    # nofullyhad
    "tW_noFullHad"    : "Tree_tW_5f_noFullHad_TuneCP5_",
    "tbarW_noFullHad" : "Tree_tbarW_5f_noFullHad_TuneCP5_",

    ### WJets
    "WJetsToLNu_MLM" : "Tree_WJetsToLNu_TuneCP5_MLM",

    ### DY
    "DYJetsToLL_M_10to50_MLM" : "Tree_DYJetsToLL_M_10to50_TuneCP5_MLM",
    "DYJetsToLL_M_50"         : "Tree_DYJetsToLL_M_50_TuneCP5_amcatnloFXFX",

    ### WW
    "WWTo2L2Nu" : "Tree_WWTo2L2Nu_NNPDF31_TuneCP5",

    ### WZ
    "WZTo2L2Q" : "Tree_WZTo2L2Q_amcatnloFXFX_madspin",
    "WZTo3LNu_aMCatNLO" : "Tree_WZTo3LNu_TuneCP5_amcatnloFXFX",
    "WZTo3LNu" : "Tree_WZTo3LNu_0",

    ### ZZ
    "ZZTo2L2Nu" : "Tree_ZZTo2L2Nu",
    "ZZTo2L2Q"  : "Tree_ZZTo2L2Q_amcatnloFXFX_madspin",
    "ZZTo4L"    : "Tree_ZZTo4L",

    ### ttW
    "TTWJetsToLNu" : "Tree_TTWJetsToLNu_TuneCP5_",
    "TTWJetsToQQ"  : "Tree_TTWJetsToQQ_TuneCP5_amcatnloFXFX_madspin",

    ### ttZ
    "TTZToLL_M_1to10"  : "Tree_TTZToLL_M_1to10_TuneCP5_amcatnlo",
    "TTZToLLNuNu_M_10" : "Tree_TTZToLLNuNu_M_10_TuneCP5_amcatnlo",
    "TTZToQQ"          : "Tree_TTZToQQ_TuneCP5_amcatnlo",


    #### Incertidumbres

    ### tW
    # DS inclusiva
    "tW_DS"             : "Tree_tW_5f_DS_inclusiveDecays_TuneCP5_PSweights_",
    #"tbarW_DS"          : "",                               # NUN TA

    # UE inclusiva
    "tW_TuneCP5Up"      : "Tree_tW_5f_inclusiveDecays_TuneCP5up_PSweights_",
    "tbarW_TuneCP5Up"   : "Tree_tbarW_5f_inclusiveDecays_TuneCP5up_PSweights_pyth_",
    #"tW_TuneCP5Down"    : "",                            # NUN TA
    #"tbarW_TuneCP5Down" : "",                            # NUN TA

    # UE nofullyhad
    #"tW_noFullHad_TuneCP5Up"      : "", # NUN TA
    #"tbarW_noFullHad_TuneCP5Up"   : "", # NUN TA
    "tW_noFullHad_TuneCP5Down"    : "Tree_tW_5f_noFullHad_TuneCP5down_PSweights_",
    "tbarW_noFullHad_TuneCP5Down" : "Tree_tbarW_5f_noFullHad_TuneCP5down_PSweights_pow_",

    # mtop inclusiva
    #"tW_mtop173p5"      : "",                                   # NUN TA
    "tbarW_mtop173p5"   : "Tree_tbarW_5f_inclusiveDecays_mtop1735_TuneCP5_PSweights_powh_",
    "tW_mtop171p5"      : "Tree_tW_5f_inclusiveDecays_mtop1715_TuneCP5_PSweights_p_",
    "tbarW_mtop171p5"   : "Tree_tbarW_5f_inclusiveDecays_mtop1715_TuneCP5_PSweights_powh_",

    #### ttbar
    # hdamp
    "TTTo2L2Nu_hdampUp"     : "Tree_TTTo2L2Nu_hdampUP_TuneCP5_PSweights",
    "TTTo2L2Nu_hdampDown"   : "Tree_TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights",

    # UE
    "TTTo2L2Nu_TuneCP5Up"   : "Tree_TTTo2L2Nu_TuneCP5up_PSweights",
    "TTTo2L2Nu_TuneCP5Down" : "Tree_TTTo2L2Nu_TuneCP5down_PSweights",

    # mtop
    "TTTo2L2Nu_mtop173p5"   : "Tree_TTTo2L2Nu_mtop173p5_TuneCP5_PSweights",
    "TTTo2L2Nu_mtop171p5"   : "Tree_TTTo2L2Nu_mtop171p5_TuneCP5_PSweights",

    # CR
    "TTTo2L2Nu_GluonMoveCRTune"      : "Tree_TTTo2L2Nu_TuneCP5CR2_GluonMove_PSweights_",
    "TTTo2L2Nu_QCDbasedCRTune_erdON" : ["Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_1", "Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_2", "Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_3", "Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_PSweights_ext1_*"], ### WARNING: EL 0 ESTÁ CORRUPTO
    "TTTo2L2Nu_erdON"                : "Tree_TTTo2L2Nu_TuneCP5_erdON_",


    #### Datos
    "SingleMuon"     : "Tree_SingleMuon_Run2017",
    "SingleElectron" : "Tree_SingleElectron_Run2017",
    "DoubleMuon"     : "Tree_DoubleMuon_Run2017",
    "DoubleEG"       : "Tree_DoubleEG_Run2017",
    "MuonEG"         : "Tree_MuonEG_Run2017",
}



sampledict[2018] = {
    #### Nominales
    # ttbar
    #"TTTo2L2Nu"        : "Tree_TTTo2L2Nu_TuneCP5_",
    #"TTTo2L2Nu" : ['Tree_TTTo2L2Nu_TuneCP5_0','Tree_TTTo2L2Nu_TuneCP5_1','Tree_TTTo2L2Nu_TuneCP5_2','Tree_TTTo2L2Nu_TuneCP5_3','Tree_TTTo2L2Nu_TuneCP5_4','Tree_TTTo2L2Nu_TuneCP5_5','Tree_TTTo2L2Nu_TuneCP5_6','Tree_TTTo2L2Nu_TuneCP5_7','Tree_TTTo2L2Nu_TuneCP5_8','Tree_TTTo2L2Nu_TuneCP5_9','Tree_TTTo2L2Nu_TuneCP5_10','Tree_TTTo2L2Nu_TuneCP5_11','Tree_TTTo2L2Nu_TuneCP5_12','Tree_TTTo2L2Nu_TuneCP5_13','Tree_TTTo2L2Nu_TuneCP5_14','Tree_TTTo2L2Nu_TuneCP5_15','Tree_TTTo2L2Nu_TuneCP5_16','Tree_TTTo2L2Nu_TuneCP5_17','Tree_TTTo2L2Nu_TuneCP5_18','Tree_TTTo2L2Nu_TuneCP5_19','Tree_TTTo2L2Nu_TuneCP5_20','Tree_TTTo2L2Nu_TuneCP5_21','Tree_TTTo2L2Nu_TuneCP5_22','Tree_TTTo2L2Nu_TuneCP5_23','Tree_TTTo2L2Nu_TuneCP5_24','Tree_TTTo2L2Nu_TuneCP5_25','Tree_TTTo2L2Nu_TuneCP5_26','Tree_TTTo2L2Nu_TuneCP5_27','Tree_TTTo2L2Nu_TuneCP5_28','Tree_TTTo2L2Nu_TuneCP5_29','Tree_TTTo2L2Nu_TuneCP5_30','Tree_TTTo2L2Nu_TuneCP5_31','Tree_TTTo2L2Nu_TuneCP5_32','Tree_TTTo2L2Nu_TuneCP5_33','Tree_TTTo2L2Nu_TuneCP5_34','Tree_TTTo2L2Nu_TuneCP5_35','Tree_TTTo2L2Nu_TuneCP5_36','Tree_TTTo2L2Nu_TuneCP5_37','Tree_TTTo2L2Nu_TuneCP5_38','Tree_TTTo2L2Nu_TuneCP5_39','Tree_TTTo2L2Nu_TuneCP5_40','Tree_TTTo2L2Nu_TuneCP5_41','Tree_TTTo2L2Nu_TuneCP5_42','Tree_TTTo2L2Nu_TuneCP5_43','Tree_TTTo2L2Nu_TuneCP5_44'],

    "TTTo2L2Nu_division1" : ['Tree_TTTo2L2Nudiv1_TuneCP5_0','Tree_TTTo2L2Nudiv1_TuneCP5_1','Tree_TTTo2L2Nudiv1_TuneCP5_2','Tree_TTTo2L2Nudiv1_TuneCP5_3','Tree_TTTo2L2Nudiv1_TuneCP5_4','Tree_TTTo2L2Nudiv1_TuneCP5_5','Tree_TTTo2L2Nudiv1_TuneCP5_6','Tree_TTTo2L2Nudiv1_TuneCP5_7','Tree_TTTo2L2Nudiv1_TuneCP5_8','Tree_TTTo2L2Nudiv1_TuneCP5_9','Tree_TTTo2L2Nudiv1_TuneCP5_10','Tree_TTTo2L2Nudiv1_TuneCP5_11','Tree_TTTo2L2Nudiv1_TuneCP5_12','Tree_TTTo2L2Nudiv1_TuneCP5_13','Tree_TTTo2L2Nudiv1_TuneCP5_14','Tree_TTTo2L2Nudiv1_TuneCP5_15','Tree_TTTo2L2Nudiv1_TuneCP5_16','Tree_TTTo2L2Nudiv1_TuneCP5_17','Tree_TTTo2L2Nudiv1_TuneCP5_18','Tree_TTTo2L2Nudiv1_TuneCP5_19','Tree_TTTo2L2Nudiv1_TuneCP5_20','Tree_TTTo2L2Nudiv1_TuneCP5_21','Tree_TTTo2L2Nudiv1_TuneCP5_22','Tree_TTTo2L2Nudiv1_TuneCP5_23','Tree_TTTo2L2Nudiv1_TuneCP5_24','Tree_TTTo2L2Nudiv1_TuneCP5_25','Tree_TTTo2L2Nudiv1_TuneCP5_26','Tree_TTTo2L2Nudiv1_TuneCP5_27','Tree_TTTo2L2Nudiv1_TuneCP5_28','Tree_TTTo2L2Nudiv1_TuneCP5_29','Tree_TTTo2L2Nudiv1_TuneCP5_30','Tree_TTTo2L2Nudiv1_TuneCP5_31','Tree_TTTo2L2Nudiv1_TuneCP5_32','Tree_TTTo2L2Nudiv1_TuneCP5_33','Tree_TTTo2L2Nudiv1_TuneCP5_34','Tree_TTTo2L2Nudiv1_TuneCP5_35','Tree_TTTo2L2Nudiv1_TuneCP5_36','Tree_TTTo2L2Nudiv1_TuneCP5_37','Tree_TTTo2L2Nudiv1_TuneCP5_38','Tree_TTTo2L2Nudiv1_TuneCP5_39','Tree_TTTo2L2Nudiv1_TuneCP5_40','Tree_TTTo2L2Nudiv1_TuneCP5_41','Tree_TTTo2L2Nudiv1_TuneCP5_42','Tree_TTTo2L2Nudiv1_TuneCP5_43','Tree_TTTo2L2Nudiv1_TuneCP5_44'],

    "TTTo2L2Nu_division2" : ['Tree_TTTo2L2Nudiv2_TuneCP5_0','Tree_TTTo2L2Nudiv2_TuneCP5_1','Tree_TTTo2L2Nudiv2_TuneCP5_2','Tree_TTTo2L2Nudiv2_TuneCP5_3','Tree_TTTo2L2Nudiv2_TuneCP5_4','Tree_TTTo2L2Nudiv2_TuneCP5_5','Tree_TTTo2L2Nudiv2_TuneCP5_6','Tree_TTTo2L2Nudiv2_TuneCP5_7','Tree_TTTo2L2Nudiv2_TuneCP5_8','Tree_TTTo2L2Nudiv2_TuneCP5_9','Tree_TTTo2L2Nudiv2_TuneCP5_10','Tree_TTTo2L2Nudiv2_TuneCP5_11','Tree_TTTo2L2Nudiv2_TuneCP5_12','Tree_TTTo2L2Nudiv2_TuneCP5_13','Tree_TTTo2L2Nudiv2_TuneCP5_14','Tree_TTTo2L2Nudiv2_TuneCP5_15','Tree_TTTo2L2Nudiv2_TuneCP5_16','Tree_TTTo2L2Nudiv2_TuneCP5_17','Tree_TTTo2L2Nudiv2_TuneCP5_18','Tree_TTTo2L2Nudiv2_TuneCP5_19','Tree_TTTo2L2Nudiv2_TuneCP5_20','Tree_TTTo2L2Nudiv2_TuneCP5_21','Tree_TTTo2L2Nudiv2_TuneCP5_22','Tree_TTTo2L2Nudiv2_TuneCP5_23','Tree_TTTo2L2Nudiv2_TuneCP5_24','Tree_TTTo2L2Nudiv2_TuneCP5_25','Tree_TTTo2L2Nudiv2_TuneCP5_26','Tree_TTTo2L2Nudiv2_TuneCP5_27','Tree_TTTo2L2Nudiv2_TuneCP5_28','Tree_TTTo2L2Nudiv2_TuneCP5_29','Tree_TTTo2L2Nudiv2_TuneCP5_30','Tree_TTTo2L2Nudiv2_TuneCP5_31','Tree_TTTo2L2Nudiv2_TuneCP5_32','Tree_TTTo2L2Nudiv2_TuneCP5_33','Tree_TTTo2L2Nudiv2_TuneCP5_34','Tree_TTTo2L2Nudiv2_TuneCP5_35','Tree_TTTo2L2Nudiv2_TuneCP5_36','Tree_TTTo2L2Nudiv2_TuneCP5_37','Tree_TTTo2L2Nudiv2_TuneCP5_38','Tree_TTTo2L2Nudiv2_TuneCP5_39','Tree_TTTo2L2Nudiv2_TuneCP5_40','Tree_TTTo2L2Nudiv2_TuneCP5_41','Tree_TTTo2L2Nudiv2_TuneCP5_42','Tree_TTTo2L2Nudiv2_TuneCP5_43','Tree_TTTo2L2Nudiv2_TuneCP5_44'],

    "TTToSemiLeptonic" : "Tree_TTToSemiLeptonic_TuneCP5_",

    ### tW
    # inclusiva
    "tW"              : "Tree_tW_5f_inclusiveDecays_TuneCP5_ext1_",
    "tbarW"           : "Tree_tbarW_5f_inclusiveDecays_TuneCP5_ext1_",

    # nofullyhad
    "tW_noFullHad"    : ["Tree_tW_5f_noFullHad_TuneCP5_ext1_0"],
    "tbarW_noFullHad" : ["Tree_tbarW_5f_noFullHad_TuneCP5_ext_0"],


    ### WWbb
    "WWbb" : "Tree_b_bbar_4l_TuneCP5_ext1",
    #"WWbb_noskim_4files" : ["8D0A2ECF-09D2-6841-BE66-0BCECFE4942A_Skim",
                            #"C14C273E-2210-DA4E-AE8A-1D283123146B_Skim",
                            #"EE18ACF2-2CB7-214F-93B9-B70E7861F9E7_Skim",
                            #"FF50A220-4B88-A349-B802-28FD77C317EA_Skim"],

    # W Jets
    "WJetsToLNu_MLM" : "Tree_WJetsToLNu_TuneCP5_MLM",

    # DY
    "DYJetsToLL_M_10to50_MLM" : "Tree_DYJetsToLL_M_10to50_TuneCP5_MLM",
    "DYJetsToLL_M_50"         : "Tree_DYJetsToLL_M_50_TuneCP5_amcatnloFXFX",

    # WW
    "WWTo2L2Nu"            : "Tree_WWTo2L2Nu_NNPDF31_TuneCP5",
    "WWTo1L1Nu2Q_aMCatNLO" : "Tree_WWTo1L1Nu2Q_amcatnloFXFX_madspin",
    "WWTo1L1Nu2Q"          : "Tree_WWToLNuQQ_NNPDF31_TuneCP5",
    "WWTo4Q"               : "Tree_WWTo4Q_NNPDF31_TuneCP5",

    # WZ
    "WZTo1L3Nu"         : "Tree_WZTo1L3Nu_amcatnloFXFX_madspin",
    "WZTo2L2Q"          : "Tree_WZTo2L2Q_amcatnloFXFX_madspin",
    "WZTo3LNu_aMCatNLO" : "Tree_WZTo3LNu_TuneCP5_amcatnloFXFX",
    "WZTo3LNu"          : "Tree_WZTo3LNu_TuneCP5_ext1_0",

    # ZZ
    "ZZTo2L2Nu"      : "Tree_ZZTo2L2Nu_TuneCP5",
    "ZZTo2L2Q"       : "Tree_ZZTo2L2Q_amcatnloFXFX_madspin",
    "ZZTo2Q2Nu"      : "Tree_ZZTo2Q2Nu_TuneCP5_amcatnloFXFX_madspin",
    "ZZTo4L"         : "Tree_ZZTo4L",
    #"ZZGJetsTo4L2Nu" : "Tree_ZZGJetsTo4L2Nu_4f_TuneCP5_amcatnloFXFX",

    # WWW
    #"WWW_dilepton"   : "Tree_WWW_4F_DiLeptonFilter_TuneCP5_amcatnlo",

    # WWZ
    #"WWZ"            : "Tree_WWZ_TuneCP5_amcatnlo",
    #"WWZJetsTo4L2Nu" : "Tree_WWZJetsTo4L2Nu_4f_TuneCP5_amcatnloFXFX",

    # WZZ
    #"WZZ"            : "Tree_WZZ_TuneCP5_amcatnlo",
    #"WZZJetsTo4L2Nu" : "Tree_WZZJetsTo4L2Nu_4f_TuneCP5_amcatnloFXFX",

    # ZZZ
    #"ZZZJetsTo4L2Nu" : "Tree_ZZZJetsTo4L2Nu_4f_TuneCP5_amcatnloFXFX",

    # ttW
    "TTWJetsToLNu" : "Tree_TTWJetsToLNu_TuneCP5_amcatnloFXFX_madspin",
    "TTWJetsToQQ"  : "Tree_TTWJetsToQQ_TuneCP5_amcatnloFXFX_madspin",

    # ttZ
    "TTZToLL_M_1to10"  : "Tree_TTZToLL_M_1to10_TuneCP5_amcatnlo",
    "TTZToLLNuNu_M_10" : "Tree_TTZToLLNuNu_M_10_TuneCP5_amcatnlo",
    "TTZToQQ"          : "Tree_TTZToQQ_TuneCP5_amcatnlo",


    #### Incertidumbres

    #### tW
    #"tW_DS"             : "", # NUN TA
    #"tbarW_DS"          : "", # NUN TA

    "tW_TuneCP5Up"      : "Tree_tW_5f_inclusiveDecays_TuneCP5up_PSweights_",
    "tbarW_TuneCP5Up"   : "Tree_tbarW_5f_inclusiveDecays_TuneCP5up_",
    "tW_TuneCP5Down"    : "Tree_tW_5f_inclusiveDecays_TuneCP5down_PSweights_pythia_",
    "tbarW_TuneCP5Down" : "Tree_tbarW_5f_inclusiveDecays_TuneCP5down_",

    "tW_noFullHad_TuneCP5Up"      : "Tree_tW_5f_noFullHad_TuneCP5up_",
    "tbarW_noFullHad_TuneCP5Up"   : "Tree_tbarW_5f_noFullHad_TuneCP5up_",
    "tW_noFullHad_TuneCP5Down"    : "Tree_tW_5f_noFullHad_TuneCP5down_",
    "tbarW_noFullHad_TuneCP5Down" : "Tree_tbarW_5f_noFullHad_TuneCP5down_pythia_",


    #### ttbar
    "TTTo2L2Nu_hdampUp"     : "Tree_TTTo2L2Nu_hdampUP_TuneCP5",
    "TTTo2L2Nu_hdampDown"   : "Tree_TTTo2L2Nu_hdampDOWN_TuneCP5",

    "TTTo2L2Nu_TuneCP5Up"   : "Tree_TTTo2L2Nu_TuneCP5up",
    "TTTo2L2Nu_TuneCP5Down" : "Tree_TTTo2L2Nu_TuneCP5down",

    "TTTo2L2Nu_mtop173p5"   : "Tree_TTTo2L2Nu_mtop173p5_TuneCP5",
    "TTTo2L2Nu_mtop171p5"   : "Tree_TTTo2L2Nu_mtop171p5_TuneCP5",

    "TTTo2L2Nu_GluonMoveCRTune"      : "Tree_TTTo2L2Nu_TuneCP5CR2_GluonMove_",
    "TTTo2L2Nu_QCDbasedCRTune_erdON" : "Tree_TTTo2L2Nu_TuneCP5CR1_QCDbased_",
    "TTTo2L2Nu_erdON"                : ["Tree_TTTo2L2Nu_TuneCP5_erdON_1", "Tree_TTTo2L2Nu_TuneCP5_erdON_2", "Tree_TTTo2L2Nu_TuneCP5_erdON_3", "Tree_TTTo2L2Nu_TuneCP5_erdON_ext1_*"], ### WARNING: EL 0 ESTÁ CORRUPTO


    #### Datos
    "SingleMuon" : "Tree_SingleMuon_Run2018",
    "EGamma"     : "Tree_EGamma_Run2018",
    "DoubleMuon" : "Tree_DoubleMuon_Run2018",
    "MuonEG"     : "Tree_MuonEG_Run2018",
}

trainsampledict = {}; trainsampledict[2016] = {}; trainsampledict[2017] = {}; trainsampledict[2018] = {}
trainsampledict[2016] = {
    ### ttbar
    #"TTTo2L2Nu" : ['Tree_TTTo2L2Nu_TuneCP5_PSweights_0', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_1', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_2', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_3', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_4', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_5', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_6', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_7', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_8', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_9', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_10', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_11', 'Tree_TTTo2L2Nu_TuneCP5_PSweights_12'],
    #"TTTo2L2Nu" : sampledict[2016]["TTTo2L2Nu"],

    ### tW

    #"tW"    : "Tree_tW_5f_inclusiveDecays_TuneCP5_PSweights_",
    #"tW"    : sampledict[2016]["tW"],
    #"tbarW" : "Tree_tbarW_5f_inclusiveDecays_TuneCP5_PSweights_",
    #"tbarW" : sampledict[2016]["tbarW"],

    "TTTo2L2Nu_division2" : sampledict[2016]["TTTo2L2Nu_division2"],

    "tW_division2"        : sampledict[2016]["tW_division2"],
    "tbarW_division2"     : sampledict[2016]["tbarW_division2"],

    "DYJetsToLL_M_10to50" : sampledict[2016]["DYJetsToLL_M_10to50"],
    "DYJetsToLL_M_50"     : sampledict[2016]["DYJetsToLL_M_50"],
}


trainsampledict[2017] = {
    #"TTTo2L2Nu"           : ['Tree_TTTo2L2Nu_TuneCP5_PSweights_0','Tree_TTTo2L2Nu_TuneCP5_PSweights_1','Tree_TTTo2L2Nu_TuneCP5_PSweights_2','Tree_TTTo2L2Nu_TuneCP5_PSweights_3','Tree_TTTo2L2Nu_TuneCP5_PSweights_4','Tree_TTTo2L2Nu_TuneCP5_PSweights_5','Tree_TTTo2L2Nu_TuneCP5_PSweights_6','Tree_TTTo2L2Nu_TuneCP5_PSweights_7','Tree_TTTo2L2Nu_TuneCP5_PSweights_8','Tree_TTTo2L2Nu_TuneCP5_PSweights_9','Tree_TTTo2L2Nu_TuneCP5_PSweights_10','Tree_TTTo2L2Nu_TuneCP5_PSweights_11','Tree_TTTo2L2Nu_TuneCP5_PSweights_12','Tree_TTTo2L2Nu_TuneCP5_PSweights_13','Tree_TTTo2L2Nu_TuneCP5_PSweights_14','Tree_TTTo2L2Nu_TuneCP5_PSweights_15','Tree_TTTo2L2Nu_TuneCP5_PSweights_16','Tree_TTTo2L2Nu_TuneCP5_PSweights_17','Tree_TTTo2L2Nu_TuneCP5_PSweights_18','Tree_TTTo2L2Nu_TuneCP5_PSweights_19','Tree_TTTo2L2Nu_TuneCP5_PSweights_20', "Tree_TTTo2L2Nu_TuneCP5_0", "Tree_TTTo2L2Nu_TuneCP5_1", "Tree_TTTo2L2Nu_TuneCP5_2"],
    #"TTTo2L2Nu"       : sampledict[2017]["TTTo2L2Nu"],
    "TTTo2L2Nu_division2" : sampledict[2017]["TTTo2L2Nu_division2"],

    "tW"    : sampledict[2017]["tW"],
    "tbarW" : sampledict[2017]["tbarW"],

    #"tW_noFullHad"        : "Tree_tW_5f_noFullHad_TuneCP5_",
    #"tW_noFullHad"    : sampledict[2017]["tW_noFullHad"],
    #"tbarW_noFullHad"     : "Tree_tbarW_5f_noFullHad_TuneCP5_",
    #"tbarW_noFullHad" : sampledict[2017]["tbarW_noFullHad"],

    "DYJetsToLL_M_10to50_MLM" : sampledict[2017]["DYJetsToLL_M_10to50_MLM"],
    "DYJetsToLL_M_50"         : sampledict[2017]["DYJetsToLL_M_50"],
}


trainsampledict[2018] = {
    # ttbar
    #"TTTo2L2Nu" : ['Tree_TTTo2L2Nu_TuneCP5_0', 'Tree_TTTo2L2Nu_TuneCP5_1', 'Tree_TTTo2L2Nu_TuneCP5_2', 'Tree_TTTo2L2Nu_TuneCP5_3', 'Tree_TTTo2L2Nu_TuneCP5_4', 'Tree_TTTo2L2Nu_TuneCP5_5', 'Tree_TTTo2L2Nu_TuneCP5_6', 'Tree_TTTo2L2Nu_TuneCP5_7', 'Tree_TTTo2L2Nu_TuneCP5_8', 'Tree_TTTo2L2Nu_TuneCP5_9', 'Tree_TTTo2L2Nu_TuneCP5_10', 'Tree_TTTo2L2Nu_TuneCP5_11', 'Tree_TTTo2L2Nu_TuneCP5_12', 'Tree_TTTo2L2Nu_TuneCP5_13', 'Tree_TTTo2L2Nu_TuneCP5_14', 'Tree_TTTo2L2Nu_TuneCP5_15', 'Tree_TTTo2L2Nu_TuneCP5_16', 'Tree_TTTo2L2Nu_TuneCP5_17', 'Tree_TTTo2L2Nu_TuneCP5_18', 'Tree_TTTo2L2Nu_TuneCP5_19', 'Tree_TTTo2L2Nu_TuneCP5_20', 'Tree_TTTo2L2Nu_TuneCP5_21', 'Tree_TTTo2L2Nu_TuneCP5_22', 'Tree_TTTo2L2Nu_TuneCP5_23', 'Tree_TTTo2L2Nu_TuneCP5_24', 'Tree_TTTo2L2Nu_TuneCP5_25', 'Tree_TTTo2L2Nu_TuneCP5_26', 'Tree_TTTo2L2Nu_TuneCP5_27', 'Tree_TTTo2L2Nu_TuneCP5_28', 'Tree_TTTo2L2Nu_TuneCP5_29', 'Tree_TTTo2L2Nu_TuneCP5_30', 'Tree_TTTo2L2Nu_TuneCP5_31', 'Tree_TTTo2L2Nu_TuneCP5_32', 'Tree_TTTo2L2Nu_TuneCP5_33', 'Tree_TTTo2L2Nu_TuneCP5_34', 'Tree_TTTo2L2Nu_TuneCP5_35', 'Tree_TTTo2L2Nu_TuneCP5_36', 'Tree_TTTo2L2Nu_TuneCP5_37', 'Tree_TTTo2L2Nu_TuneCP5_38', 'Tree_TTTo2L2Nu_TuneCP5_39', 'Tree_TTTo2L2Nu_TuneCP5_40', 'Tree_TTTo2L2Nu_TuneCP5_41', 'Tree_TTTo2L2Nu_TuneCP5_42', 'Tree_TTTo2L2Nu_TuneCP5_43', 'Tree_TTTo2L2Nu_TuneCP5_44'],
    #"TTTo2L2Nu"       : sampledict[2018]["TTTo2L2Nu"],

    # tW
    #"tW"              : "Tree_tW_5f_inclusiveDecays_TuneCP5_ext1_",
    #"tbarW"           : "Tree_tbarW_5f_inclusiveDecays_TuneCP5_ext1_",

    #"tW_noFullHad"    : ["Tree_tW_5f_noFullHad_TuneCP5_ext1_0"],
    #"tW_noFullHad"    : sampledict[2018]["tW_noFullHad"],
    #"tbarW_noFullHad" : ["Tree_tbarW_5f_noFullHad_TuneCP5_ext_0"],
    #"tbarW_noFullHad" : sampledict[2018]["tbarW_noFullHad"],

    "TTTo2L2Nu_division2"       : sampledict[2018]["TTTo2L2Nu_division2"],

    "tW"    : sampledict[2018]["tW"],
    "tbarW" : sampledict[2018]["tbarW"],

    "DYJetsToLL_M_10to50_MLM" : sampledict[2018]["DYJetsToLL_M_10to50_MLM"],
    "DYJetsToLL_M_50"         : sampledict[2018]["DYJetsToLL_M_50"],
}


#### xsecs (del stop): TEMPORAL
#DYJetsToLL_M_10to50_aMCatNLO : 22635.09
#DYJetsToLL_M_50_a       : 6025.2

#tbarW_noFullHad         : 19.4674104


#TTTo2L2Nu               : 88.28769753
#TTToSemiLeptonic        : 365.3994209
#TT                      : 831.76

#b_bbar_4l               : 8.402

#TTGJets                 : 3.697

#TTWJetsToLNu            : 0.2043
#TTWJetsToQQ             : 0.4062

#TTZToLL_M_1to10         : 0.0493
#TTZToLLNuNu_M_10_a      : 0.2529
#TTZToQQ                 : 0.5297

#WJetsToLNu_MLM          : 61526.7

#WW                      : 115
#WWTo2L2Nu               : 12.178

#WZ                      : 47.13
#WZTo2L2Q                : 5.595
#WZTo3LNu                : 4.42965

#ZZ                      : 16.523
#ZZTo2L2Nu               : 0.564
#ZZTo2L2Q                : 3.28
#ZZTo2Q2Nu               : 4.04
#ZZTo4L                  : 1.256

#WWW                     : 0.2086
#WWZ                     : 0.1651
#WWG                     : 0.2147
#WZZ                     : 0.05565
#WZG                     : 0.0412
#ZZZ                     : 0.01398



def getFriendsFolder(dataset, basepath, step_friends):
    doihavefibrefriends = False
    rwfolder = basepath + "/" + friendfolders[step_friends]
    rofolder = basepath.replace("phedexrw", "phedex").replace("cienciasrw", "ciencias") + "/" + friendfolders[step_friends]
    if os.path.isdir(rofolder):
        myfibrefriends = [f for f in os.listdir(rofolder) if (".root" in f and dataset in f and "chunk" not in f and "Friend" in f)]
        if len(myfibrefriends) > 0: doihavefibrefriends = True

    if doihavefibrefriends:
        wr.warn("\n====== WARNING! Friends detected in RO folder for this production. Using them for dataset {d} and step (of the friends) {s}".format(d = dataset, s = step_friends))
        return rofolder
    else:
        return rwfolder
    return rwfolder


def SendDatasetJobs(task):
    dataset, year, step, inputpath_, isData, queue, extra, regexp, pretend, nthreads = task
    outpath_ = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step]
    dataset_ = ("--dm " if regexp else "-d ") + dataset
    jobname_ = "happyTF_{y}_{d}_{s}".format(y = year, d = dataset, s = step)
    logdir_  = logpath.format(step_prefix = friendfolders[step], y = year)

    friendsbasepath = friendspath + "/" + prodname + "/" + str(year) + "/"
    friendpref = "-F Friends "
    friendsuff = "/{cname}_Friend.root"

    comm = ""; module_ = ""; friends_ = ""

    if   step == 0:
        module_ = "addYearTag_{y}_{ty}".format(y  = year,
                                               ty = ("mc"         if not isData else
                                                     "singlemuon" if "singlemuon" in dataset.lower() else
                                                     "singleelec"
                                                     if ("singleelec" in dataset.lower() or "egamma" in dataset.lower()) else
                                                     "doublemuon" if "doublemuon" in dataset.lower() else
                                                     "doubleeg"   if "doubleeg"   in dataset.lower() else
                                                     "muoneg")
                                                    )
        #module_ = "addYearTag_{y}_{ty}_validacion".format(y  = year,
                                               #ty = ("mc"         if not isData else
                                                     #"singlemuon" if "singlemuon" in dataset.lower() else
                                                     #"singleelec"
                                                     #if ("singleelec" in dataset.lower() or "egamma" in dataset.lower()) else
                                                     #"doublemuon" if "doublemuon" in dataset.lower() else
                                                     #"doubleeg"   if "doubleeg"   in dataset.lower() else
                                                     #"muoneg")
                                                    #)
        friends_ = ""

    elif step == 1:
        module_  = "lepMerge_roch_" + ("mc" if not isData else "data")
        #module_  = "lepMerge_roch_" + ("mc" if not isData else "data") + "_validacion"
        friends_ += friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff

    elif step == 2:
        #module_  = "cleaning_{ty}_{y}".format(y = year, ty = "data" if isData else "mc")
        module_  = "cleaning_{ty}".format(ty = "data" if isData else "mc")
        #module_  = "cleaning_{ty}_validacion".format(ty = "data" if isData else "mc")
        friends_ +=       friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 1) + friendsuff

    elif step == 3:
        module_  = "varstrigger_" + ("mc" if not isData else "data")
        #module_  = "varstrigger_" + ("mc" if not isData else "data") + "_validacion"
        friends_ +=       friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 1) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 2) + friendsuff

    elif step == 4 and not isData:
        print dataset
        if any([dataset.replace("*", "") in iD if type(iD) == str else any([dataset.replace("*", "") in jD for jD in iD]) for key,iD in trainsampledict[year].iteritems()] +
               [iD.replace("*", "") in dataset  if type(iD) == str else any([jD.replace("*", "") in dataset in jD for jD in iD]) for key,iD in trainsampledict[year].iteritems()]):
            if "noFullHad" in dataset: module_  = "sfSeq_mvatrain_ent_{y}".format(y = year)
            else:                      module_  = "sfSeq_mvatrain_{y}".format(y = year)
        else:
            module_  = "sfSeq_{y}".format(y = year)
        friends_ +=       friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 1) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 2) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 3) + friendsuff

    elif step == 5:
        module_  = "mvas_" + ("mc" if not isData else "data")
        friends_ +=       friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 1) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 2) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 3) + friendsuff

    elif step == "mvatrain":
        module_  = "createMVAMiniTree"
        friends_ +=       friendpref + getFriendsFolder(dataset, friendsbasepath, 0) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 1) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 2) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 3) + friendsuff
        friends_ += " " + friendpref + getFriendsFolder(dataset, friendsbasepath, 4) + friendsuff

    if module_ != "":
        comm = commandscaff.format(inpath  = inputpath_,
                                   outpath = outpath_,
                                   module  = module_,
                                   friends = friends_,
                                   dataset = dataset_,
                                   chunksize = chunksizes[step],
                                   cluster = (clusterscaff.format(jobname = jobname_, logdir = logdir_, queue = queue)
                                              if (queue != "") else
                                              #("--split-factor=-1 -j " + str(nthreads))
                                              ("-j " + str(nthreads))
                                              if nthreads != 1 else
                                              ""),
                                   ex      = extra
        )

        print "\nCommand: ", comm
        if not pretend: os.system(comm)

    return


def GeneralSubmitter(task):
    dataset, year, step, queue, extra, pretend, nthreads = task
    for dataset_ in dataset.split(","):
        isData     = any(ext in dataset_ for ext in datasamples)
        isDivision = ("division" in dataset_)
        inputpath_ = ((datapath if isData else mcpath) + "/" + str(year) + "/") if not isDivision else (mcpathdiv + ("ttbar" if "TTTo2L2Nu" in dataset_ else "tw_incl") + "/" + str(year) + "/")
        #inputpath_ = (datapath if isData else mcpath) + "/" #### validacion cramonal
        print inputpath_

        if not os.path.isdir(logpath.format(step_prefix = friendfolders[step], y = year)):
            os.system("mkdir -p " + logpath.format(step_prefix = friendfolders[step], y = year))

        if isinstance(sampledict[year][dataset_], list):
            #### 1) There are multiple elements in the sample dict, that may or not have regular expressions.
            #    We will have to check each element to find whether it has or not an asterisk at the end (this
            #    is the only allowed regular expression). If it has not an asterisk, we will assume that it
            #    should not have a regular expression.
            for el in sampledict[year][dataset_]:
                SendDatasetJobs( (el, year, step, inputpath_, isData, queue, extra, (el[-1] == "*"), pretend, nthreads ) )

        else:
            #### 2) There is only one element in the sample dict.. We assume it to have a regular expression.
            SendDatasetJobs( (sampledict[year][dataset_], year, step, inputpath_, isData, queue, extra, True, pretend, nthreads) )
    return


def getActualDatasets(listoffiles):
    listofdatasets = []
    for el in listoffiles:
        tmpstr = "_".join(el.split("_")[:-1])
        if tmpstr not in listofdatasets: listofdatasets.append( tmpstr )

    return listofdatasets


def getNchunks(fileparts, year, step, folder):
    isData = any(ext in (fileparts[0] if isinstance(fileparts, list) else fileparts) for ext in datasamples)
    #folder = (datapath if isData else mcpath) + "/" + str(year) + "/"

    totalEntries = 0
    if isinstance(fileparts, list):
        for f in fileparts:
            tmpf = r.TFile(folder + f, "READ")
            totalEntries += tmpf.Get("Events").GetEntries()
            tmpf.Close()
    else:
        tmpf = r.TFile(folder + fileparts, "READ")
        totalEntries += tmpf.Get("Events").GetEntries()
        tmpf.Close()

    nch = float(totalEntries)/chunksizes[step]
    nch = int(nch) + 1 * (nch != 0)
    return nch, totalEntries


def CheckChunksByDataset(task):
    dataset, year, step = task
    isData     = any(ext in dataset for ext in datasamples)
    isDivision = ("division" in dataset)
    inputpath_ = ((datapath if isData else mcpath) + "/" + str(year) + "/") if not isDivision else (mcpathdiv + ("ttbar" if "TTTo2L2Nu" in dataset else "tw_incl") + "/" + str(year) + "/")
    basefolder = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step]


    if isinstance(sampledict[year][dataset], list):
        filelist = [f for f in os.listdir(inputpath_) if any(ext.replace("*", "") in f for ext in sampledict[year][dataset])]
    else:
        filelist = [f for f in os.listdir(inputpath_) if (sampledict[year][dataset] in f)]


    pendingdict = {}

    for dat in filelist:
        pendingdict[dat] = {}
        nchks = 0; totEnt = 0
        try:
            nchks, totEnt = getNchunks(dat, year, step, inputpath_)
        except:
            raise RuntimeError("FATAL: could not access {d} to obtain the number of chunks from dataset group {dg}.".format(d = dat, dg = dataset))
        print "    - Checking dataset", dat, "(expected chunks: {nch})".format(nch = nchks)

        for ch in range(nchks):
            chkpath = basefolder + "/" + dat.replace(".root", "") + ("_Friend.chunk{chk}.root".format(chk = ch)
                                                                     if nchks > 1 else
                                                                     "_Friend.root")
            #print "opening", chkpath

            if not os.path.isfile(chkpath):                                 #### 1st: existance
                print "# Chunk {chk} has not been found.".format(chk = ch)
                pendingdict[dat][ch] = errs.exist
            elif os.path.getsize(chkpath) <= minchunkbytes:                 #### 2nd: size
                print "# Chunk {chk} has less size than the minimum.".format(chk = ch)
                pendingdict[dat][ch] = errs.size
            else:
                fch = r.TFile.Open(chkpath, "READ")
                if not fch:                                                 #### 3rd: ROOT access (corruption)
                    print "# Chunk {chk} cannot be accessed: it is corrupted.".format(chk = ch)
                    pendingdict[dat][ch] = errs.corrupt
                else:
                    tmpentries = 0
                    try:
                        tmpentries = fch.Get("Friends").GetEntries()
                    except:
                        print "# Chunk {chk} can be opened, but the TTree cannot be accessed: it is corrupted.".format(chk = ch)
                        pendingdict[dat][ch] = errs.corrupt
                    else:
                        #print tmpentries
                        fch.Close()
                        if ch == (nchks - 1):                                   #### 4th: number of entries
                            expEnt = totEnt - chunksizes[step] * (nchks - 1)
                            if int(tmpentries) != int(expEnt):
                                print "# Chunk {chk} does not have the expected entries ({ent}), it has {realent}.".format(chk = ch, ent = expEnt, realent = tmpentries)
                                pendingdict[dat][ch] = errs.entries
                        elif tmpentries != chunksizes[step]:
                            print "# Chunk {chk} does not have the expected entries ({ent}), it has {realent}.".format(chk = ch, ent = chunksizes[step], realent = tmpentries)
                            pendingdict[dat][ch] = errs.entries

                del fch

    return pendingdict, dataset


def CheckMergedDataset(task):
    dataset, year, step = task
    isData     = any(ext in dataset for ext in datasamples)

    isDivision = ("division" in dataset)
    inputpath_ = ((datapath if isData else mcpath) + "/" + str(year) + "/") if not isDivision else (mcpathdiv + ("ttbar" if "TTTo2L2Nu" in dataset else "tw_incl") + "/" + str(year) + "/")
    basefolder = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step]


    if isinstance(sampledict[year][dataset], list):
        filelist = [f for f in os.listdir(inputpath_) if any(ext.replace("*", "") in f for ext in sampledict[year][dataset])]
    else:
        filelist = [f for f in os.listdir(inputpath_) if (sampledict[year][dataset] in f)]


    pendingdict = {}

    for dat in filelist:
        pendingdict[dat] = errs.NoErr
        nchks = 0; totEnt = 0
        try:
            nchks, totEnt = getNchunks(dat, year, step, inputpath_)
        except:
            raise RuntimeError("FATAL: could not access {d} to obtain the number of entries.".format(d = dat))
        print "    - Checking dataset", dat, "(expected entries: {ent})".format(ent = totEnt)

        friendname = dat.replace(".root", "") + "_Friend.root"
        filepath   = basefolder + "/" + friendname
        #print "opening", filepath

        if not os.path.isfile(filepath):                  #### 1st: existance
            print "# Merged friendtree {chk} has not been found.".format(chk = friendname)
            pendingdict[dat] = errs.exist
        elif os.path.getsize(filepath) <= minchunkbytes:  #### 2nd: size
            print "# Merged friendtree {chk} has less size than the minimum.".format(chk = friendname)
            pendingdict[dat] = errs.size
        else:
            fch = r.TFile.Open(filepath, "READ")
            if not fch:                                   #### 3rd: ROOT access (corruption)
                print "# Merged friendtree {chk} cannot be accessed: it is corrupted.".format(chk = friendname)
                pendingdict[dat] = errs.corrupt
            else:
                tmpentries = fch.Get("Friends").GetEntries()
                #print tmpentries
                fch.Close()
                if int(tmpentries) != int(totEnt):        #### 4th: number of entries
                    print "# Merged friendtree {chk} does not have the expected entries ({ent}), it has {realent}.".format(chk = friendname, ent = totEnt, realent = tmpentries)
                    pendingdict[dat] = errs.entries

            del fch

    return pendingdict, dataset


#### NOTE: for completeness, here lies the old MergeThoseChunks function.
#def MergeThoseChunks(year, step, queue, extra):
    #basefolder = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step]
    #chunklist  = [f for f in os.listdir(basefolder) if (".root" in f and "chunk" in f)]
    #if len(chunklist) == 0:
        #print "> No chunks found in the search folder! ({f})".format(f = basefolder)
    #else:
        #wpath = os.getcwd()
        #os.chdir(utilspath)
        #os.system("bash chunkDealer.sh " + basefolder + " merge")
        #os.chdir(wpath)
    #return



def MergeThoseChunks(year, step, queue, extra, noconf = False):
    basefolder = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step]
    chunklist  = [f for f in os.listdir(basefolder) if (".root" in f and "chunk" in f)]
    if len(chunklist) == 0:
        print "> No chunks found in the search folder! ({f})".format(f = basefolder)
    else:
        allRfileslist  = [f for f in os.listdir(basefolder) if (".root" in f and f not in [el + ".root" for el in minitnamedict.keys()])]
        print "> Chunks found in {b}. Please, take into account that no check upon the chunks will be done here.".format(b = basefolder)
        dictofmerges = {}
        for chk in allRfileslist:
            tmplex = chk.split("Friend")[0]
            tmpsuf = chk.split("Friend")[1]
            if tmplex in dictofmerges:
                dictofmerges[tmplex].append(tmpsuf)
            else:
                dictofmerges[tmplex] = [tmpsuf]

        nsuscept = len(list(dictofmerges.keys()))
        nmerged  = len( [f for f in list(dictofmerges.keys()) if ".root" in dictofmerges[f]] )

        print "\n> {n1} datasets found susceptible to be merged, of which {n2} have already merged files and will be ignored.".format(n1 = nsuscept, n2 = nmerged )


        if nsuscept != nmerged:
            print "    - The ones without merged files are the following."
            for dat in dictofmerges:
                if ".root" not in dictofmerges[dat]:
                    print "# Dataset: {d}".format(d = dat)

            cont = False
            if noconf:
                cont = True
            elif confirm("\n> Do you want to merge the chunks of those datasets?"):
                cont = True

            if cont:
                print "\n> Beginning merge."
                for dat in dictofmerges:
                    if ".root" not in dictofmerges[dat]:
                        print "\n    - Merging the {nch} chunks of dataset {d}.".format(nch = len(dictofmerges[dat]), d = dat)
                        comm = "hadd -f3 " + basefolder + "/" + dat + "Friend.root "


                        #### NOTE: this step of ordering is EXTREMELY IMPORTANT. PLEASE DO NOT MERGE FTREES W/O FIRST ORDERING THE CHUNKS!!!! In addition, please note THAT HERE NO ATTENTION IS PAYED TO WHETHER ALL THE INTERMEDIATE CHUNKS EXIST OR IF SOME EXTRA CHUNK SHOULD BE INCLUDED. You should CHECK the chunks BEFORE merging.

                        tmpnchks = 1 + max( [ int(el.replace(".chunk", "").replace(".root", "")) for el in dictofmerges[dat] ] )

                        for ichk in range(tmpnchks): comm += " " + basefolder + "/" + dat + "Friend.chunk{i}.root".format(i = ichk)
                        print "Command: " + comm
                        #sys.exit()
                        os.system(comm)

    ### EXTRA MERGE FOR MVA TRAINING MINITREES
    if step == "mvatrain":
        if confirm("\n> Do you want to merge the minitrees for MVA trainings?"):
            print "\n> Final merge for training purposes."
            for finalfile in minitnamedict:
                listofsamplegs = []
                for dat in trainsampledict[year]:
                    if dat in minitnamedict[finalfile]: listofsamplegs.append(dat)

                listoffiles = []
                mergedlist  = [f for f in os.listdir(basefolder) if ("Friend.root" in f and "chunk" not in f)]
                for el in listofsamplegs:
                    if isinstance(trainsampledict[year][el], list):
                        for cand in trainsampledict[year][el]:
                            if cand[-1] == "*": listoffiles.extend( [f for f in mergedlist if cand.replace("*", "") in f] )
                            else:               listoffiles.append( cand + "_Friend.root")
                    else:
                        listoffiles.extend( [f for f in mergedlist if (trainsampledict[year][el] in f)] )


                print "    - Merging into " + basefolder + "/" + finalfile + ".root these files:"
                for el in listoffiles: print "# " + el

                print "\n"
                comm = "hadd -f3 " + basefolder + "/" + finalfile + ".root"

                for ifile in listoffiles: comm += " " + basefolder + "/" + ifile
                print "Command: " + comm
                #sys.exit()
                os.system(comm)
    return


def CheckLotsOfMergedDatasets(dataset, year, step, queue, extra, ncores):
    fullpendingdict = {}
    totalcount = 0
    if dataset.lower() != "all":
        tmpdict, dat = CheckMergedDataset( (dataset, year, step) )
        tmpcount = sum([1 for td in tmpdict if tmpdict[td] != 0])
        totalcount += tmpcount
        if tmpcount != 0: fullpendingdict[dat] = tmpdict
    else:
        tasks = []
        for dat in sampledict[year]:
            isData = any(ext in dat for ext in datasamples)
            if not isData or (isData and step != 4):
                tasks.append( (dat, year, step) )
        if ncores > 1:
            pool = Pool(ncores)
            listofdicts = pool.map(CheckMergedDataset, tasks)
            pool.close()
            pool.join()
            del pool
            for tmptupl in listofdicts:
                tmpcount = sum([1 for td in tmptupl[0] if tmptupl[0][td] != 0])
                totalcount += tmpcount
                if tmpcount != 0: fullpendingdict[tmptupl[1]] = tmptupl[0]
        else:
            for task in tasks:
                tmpdict, dat = CheckChunksByDataset(task)
                tmpcount = sum([1 for td in tmpdict if tmpdict[td] != 0])
                totalcount += tmpcount
                if tmpcount != 0: fullpendingdict[dat] = tmpdict


    #print fullpendingdict
    print "\n> Finished checks."
    if len(list(fullpendingdict.keys())) != 0:
        print "    - {nch} merged datasets should be remerged. These are:".format(nch = totalcount)
        for d in fullpendingdict:
            for part in fullpendingdict[d]:
                print "# Dataset: {dat}".format(dat = part)

        if confirm("> Do you want to remerge these datasets? The current merged files will be deleted and afterwards, they will be reproduced (please note that all non-merged chunks in the folder will be merged!)"):
            for d in fullpendingdict:
                for part in fullpendingdict[d]:
                    tmpfile = friendspath + "/" + prodname + "/" + str(year) + "/" + friendfolders[step] + "/" + part.replace(".root", "") + "_Friend.root"
                    print "   - Erasing file {f}".format(f = tmpfile)
                    os.system("rm " + tmpfile)
            MergeThoseChunks(year, step, queue, extra, noconf = True)
        else:
            return


def CheckLotsOfChunks(dataset, year, step, queue, extra, ncores, mva, nthreads):
    fullpendingdict = {}
    totalcount = 0
    if dataset.lower() != "all":
        tmpdict, dat = CheckChunksByDataset( (dataset, year, step) )
        tmpcount = sum([len(list(tmpdict[td].keys())) for td in tmpdict])
        totalcount += tmpcount
        if tmpcount != 0: fullpendingdict[dat] = tmpdict
    else:
        tasks = []
        thedict = trainsampledict[year] if mva else sampledict[year]
        for dat in thedict:
            isData = any(ext in dat for ext in datasamples)
            if not isData or (isData and step != 4):
                tasks.append( (dat, year, step) )
        if ncores > 1:
            pool = Pool(ncores)
            listofdicts = pool.map(CheckChunksByDataset, tasks)
            pool.close()
            pool.join()
            del pool
            for tmptupl in listofdicts:
                tmpcount = sum([len(list(tmptupl[0][td].keys())) for td in tmptupl[0]])
                totalcount += tmpcount
                if tmpcount != 0: fullpendingdict[tmptupl[1]] = tmptupl[0]
        else:
            for task in tasks:
                tmpdict, dat = CheckChunksByDataset(task)
                tmpcount = sum([len(list(tmpdict[td].keys())) for td in tmpdict])
                totalcount += tmpcount
                if tmpcount != 0: fullpendingdict[dat] = tmpdict

    #print fullpendingdict
    print "\n> Finished checks."
    if len(list(fullpendingdict.keys())) != 0:
        print "    - {nch} chunks should be reprocessed. These are:".format(nch = totalcount)
        for d in fullpendingdict:
            for part in fullpendingdict[d]:
                for ch in fullpendingdict[d][part]:
                    print "# Dataset: {dat} - chunk: {c}".format(dat = part, c = ch)

        if confirm("\n> Do you want to send these jobs?"):
            if not os.path.isdir(logpath.format(step_prefix = friendfolders[step], y = year)):
                os.system("mkdir -p " + logpath.format(step_prefix = friendfolders[step], y = year))

            tasks = []
            for d in fullpendingdict:
                for part in fullpendingdict[d]:
                    for ch in fullpendingdict[d][part]:
                        isData     = any(ext in part for ext in datasamples)
                        isDivision = ("division" in d)
                        inputpath_ = ((datapath if isData else mcpath) + "/" + str(year) + "/") if not isDivision else (mcpathdiv + ("ttbar" if "TTTo2L2Nu" in d else "tw_incl") + "/" + str(year) + "/")
                        tasks.append( (part.replace(".root", ""), year, step, inputpath_, isData, queue, "-c {chk} ".format(chk = ch) + extra, False, False, nthreads) )
                        #sys.exit()

            if ncores > 1:
                pool = Pool(ncores)
                pool.map(SendDatasetJobs, tasks)
                pool.close()
                pool.join()
                del pool
            else:
                for task in tasks:
                    SendDatasetJobs(task)
            return
        else:
            return


def confirm(message = "Do you wish to continue?"):
    """
    Ask user to enter y(es) or n(o) (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n", "yes", "no"]:
        answer = raw_input(message + " [Y/N]\n").lower()
    return answer[0] == "y"



if __name__=="__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--year',    '-y', metavar = 'year',     dest = "year",    required = False, default = 2016, type = int)
    parser.add_argument('--dataset', '-d', metavar = 'dataset',  dest = "dataset", required = False, default = "TTTo2L2Nu")
    parser.add_argument('--step',    '-s', metavar = 'step',     dest = "step",    required = False, default = "0")
    parser.add_argument('--extraArgs','-e', metavar = 'extra',   dest = "extra",   required = False, default = "")
    parser.add_argument('--queue',   '-q', metavar = 'queue',    dest = "queue",   required = False, default = "")
    parser.add_argument('--threads', '-j', metavar = 'nthreads', dest = "nthreads",required = False, default = 1, type = int)
    parser.add_argument('--ncores',  '-n', metavar = 'ncores',   dest = "ncores",  required = False, default = 1, type = int)
    parser.add_argument('--check',   '-c', action = "store_true",dest = "check",   required = False, default = False)
    parser.add_argument('--merge',   '-m', action = "store_true",dest = "merge",   required = False, default = False)
    parser.add_argument('--pretend', '-p', action = "store_true",dest = "pretend", required = False, default = False)
    parser.add_argument('--eraseChunks',   action = "store_true",dest = "eraseCh", required = False, default = False)


    args     = parser.parse_args()
    year     = args.year
    dataset  = args.dataset
    check    = args.check
    step     = args.step if not args.step.isdigit() else int(args.step)
    queue    = args.queue
    extra    = args.extra
    ncores   = args.ncores
    nthreads = args.nthreads
    merge    = args.merge
    pretend  = args.pretend
    mva      = (step == "mvatrain")
    erasech  = args.eraseCh

    if erasech:
        print "\n====== ATTENTION!!!!!! ======"
        print "This will erase ALL CHUNKS in production " + prodname + "'s folder for year " + str(year) + " that are present in these subfolders (if they exist):"
        erasecomm = "rm -f {path}"
        for step,name in friendfolders.iteritems():
            print "- " + name
        if confirm("\n> Do you REALLY want to continue?"):
            basefolder = friendspath + "/" + prodname + "/" + str(year) + "/"
            for step,name in friendfolders.iteritems():
                if os.path.isdir(basefolder + name):
                    if any(["chunk" in el for el in os.listdir(basefolder + name)]):
                        print "# Erasing chunks in subfolder " + name + " of step " + str(step)
                        #print erasecomm.format(path = basefolder + name + "/*chunk*.root")
                        os.system(erasecomm.format(path = basefolder + name + "/*chunk*.root"))
                        #sys.exit()


    elif check and not merge:
        print "\n> Beginning checks of all chunks for the production of year {y}, of the friend trees of step {s} for {d} dataset(s).".format(y = year, s = step, d = dataset)
        CheckLotsOfChunks(dataset, year, step, queue, extra, ncores, mva, nthreads)
    elif merge and not check:
        MergeThoseChunks(year, step, queue, extra)
    elif merge and check:
        CheckLotsOfMergedDatasets(dataset, year, step, queue, extra, ncores)
    else:
        if dataset.lower() != "all":
            GeneralSubmitter( (dataset, year, step, queue, extra, pretend, nthreads) )
        else:
            tasks   = []
            thedict = trainsampledict[year] if mva else sampledict[year]
            for dat in thedict: tasks.append( (dat, year, step, queue, extra, pretend, nthreads) )
            print "> A total of {n} commands (that might send one, or more jobs) are going to be executed for year {y}, step {s} in the queue {q} and parallelised with {j} cores.".format(n = len(tasks), y = year, s = step, q = queue, j = ncores)

            if confirm("\n> Do you want to send these jobs?"):
                print "> Beginning submission."
                if ncores > 1:
                    pool = Pool(ncores)
                    pool.map(GeneralSubmitter, tasks)
                    pool.close()
                    pool.join()
                    del pool
                else:
                    for tsk in tasks: GeneralSubmitter(tsk)
