from hepdata_lib import RootFileReader, Submission, Variable, Uncertainty, Table
import numpy as np
import os, sys

sys.path.append('./tw-run2')
from plot_postfit import dictBinsCenterRegions, dictRegionsYaxisLabels, dictRegionsXaxisLabels

### To do list
#   - Differential plots


#Create the submission obj
submission = Submission()


#### Configurations  Inclusive-------
pathOfCards = "/nfs/fanae/user/asoto/Proyectos/tW-Victor/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/temp_cards/2022-04-21_withMETUncertainty/run2/"
fitDiagnosticsName = "fitDiagnosticsrun2_1j1t2j1t2j2t.root"

processes = {"tw": "tW (signal)", "ttbar": "ttbar", "vvttv": "VV+ttbarV", "dy": "DY", "nonworz": "Non-W/Z", "total_background": "Total background", "data": "Data"}
channels = {"ch1": "a", "ch2": "b", "ch3": "c"}
channelsJets = {"ch1": "1j1b", "ch2": "2j1b", "ch3": "2j2b"}
unitsDict = {"ch1": "", "ch2": "", "ch3": "GeV"}
preOrPost = {"shapes_prefit": "prefit", "shapes_fit_s": "postfit"}
figure = {"ch1": "tmvaBDT_1j1b_20binspost.pdf", "ch2": "tmvaBDT_2j1b_12binspost.pdf", "ch3": "jet2_pt_rebinpost.pdf"}
positionCh = {"ch1": "top left", "ch2": "top right", "ch3": "bottom"}
numberBins = {"ch1": 20, "ch2": 12, "ch3": 16}
dictBinsExtremesRegions = {
    "ch1"      : [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20)],
    "ch2"      : [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12)],
    "ch3"      : [(30, 35), (40, 45), (50, 55), (60, 65), (70, 75), (80, 85), (90, 95), (100, 105), (110, 115), (120, 125), (130, 135), (140, 145), (150, 155), (160, 165), (170, 175), (180, 185)],
    #"ch1"      : [1,2],
    #"ch2"      : [1,2],
    #"ch3"      : [70,150],
}
dictRegionsXaxisLabels = {
    "ch1"      : "BDT discriminant",
    "ch2"      : "BDT discriminant",
    "ch3"      : "Subleading jet $p_{T}$",
}

#### -------

#### Configurations  Differential-------
pathOfDiffCards = "/nfs/fanae/user/vrbouza/Proyectos/tw_run2/desarrollo/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/temp_2022_06_13_diffentera/differential/run2/"
histosFile = "/particlefidbinOutput.root"
variablesOrdered = ["Lep1_Pt", "Lep1Lep2Jet1MET_Pz","Jet1_Pt", "Lep1Lep2Jet1_M", "Lep1Lep2_DPhi", "Lep1Lep2Jet1MET_Mt"]
variablesOrdered2 = ["Lep1_Pt", "Jet1_Pt", "Lep1Lep2_DPhi", "Lep1Lep2Jet1MET_Pz", "Lep1Lep2Jet1MET_Mt", "Lep1Lep2Jet1_M"]
variables = {"Lep1_Pt": "$Leading$ $lepton$ $p_{T}$", "Lep1Lep2Jet1MET_Pz": "$p_{Z}(e^{\pm}, \mu^{\pm}, j)$","Jet1_Pt": "$Jet$ $p_{T}$", "Lep1Lep2Jet1_M": "$m(e^{\pm}, \mu^{\pm}, j)$", "Lep1Lep2_DPhi": "$\Delta\phi(e^{\pm}, \mu^{\pm})/\pi$", "Lep1Lep2Jet1MET_Mt": "$m_{T}(e^{\pm}, \mu^{\pm}, j, p_{T}^{miss})$"}
processesDiff = {"tru": "tW PH DR + P8", "tru_DS": "tW PH DS + P8", "tru_herwig": "tW PH DR + H7", "tru_aMC_dr": "tW aMC DR + P8", "tru_aMC_dr2": "tW aMC DR2 + P8", "tru_aMC_ds": "tW aMC DS + P8", "tru_aMC_ds_runn": "tW aMC DS dyn. + P8"} #Here the data has the same name as the variable
figureDiff = {"Jet1_Pt": "Jet1_Pt_particlefidbin.pdf", "Lep1Lep2Jet1MET_Mt": "Lep1Lep2Jet1MET_Mt_particlefidbin.pdf", "Lep1Lep2Jet1MET_Pz": "Lep1Lep2Jet1MET_Pz_particlefidbin.pdf", "Lep1Lep2Jet1_M": "Lep1Lep2Jet1_M_particlefidbin.pdf", "Lep1Lep2_DPhi": "Lep1Lep2_DPhi_particlefidbin.pdf", "Lep1_Pt": "Lep1_Pt_particlefidbin.pdf"}
unitsDiff = {"Jet1_Pt": "GeV", "Lep1Lep2Jet1MET_Mt": "GeV", "Lep1Lep2Jet1MET_Pz": "GeV", "Lep1Lep2Jet1_M": "GeV", "Lep1Lep2_DPhi": "", "Lep1_Pt": "GeV"}
names = {"Jet1_Pt": "c", "Lep1Lep2Jet1MET_Mt": "f", "Lep1Lep2Jet1MET_Pz": "b", "Lep1Lep2Jet1_M": "d", "Lep1Lep2_DPhi": "e", "Lep1_Pt": "a"}
positionDiff = {"Lep1_Pt": "top left", "Lep1Lep2Jet1MET_Pz": "top right","Jet1_Pt": "middle left", "Lep1Lep2Jet1_M": "middle right", "Lep1Lep2_DPhi": "bottom left", "Lep1Lep2Jet1MET_Mt": "bottom right"}

#### -------

pathOfPaperFig = "/nfs/fanae/user/asoto/Proyectos/tW-Victor/Documentacion/TOP-21-010/figures/"

def createIndependentVar(xBins, name, is_binned, units):
    indep = Variable(name, is_independent=True, is_binned=is_binned, units=units)
    
    if type(xBins) == type([1,2]):
        indep.values = xBins
    
    else:
        if is_binned:
            edges = "_edges"
        else:
            edges = ""
        indep.values = xBins["x"+edges]
    
    return indep
    
def createDependentVar(process, name, is_binned, units, nBins,uncType, symm, uncHisto=False, alsoStat = None, depLabel = "y"):
    dep = Variable(name, is_independent=False, is_binned=is_binned, units=units)
    if nBins == -1:
        nBins = len(process[depLabel])
    
    dep.values = process[depLabel][0:nBins]
    
    # Add uncertainty
    if uncType == None:
        return dep
    
    if alsoStat != None:
        uncStat = Uncertainty("Statistical uncertainty", is_symmetric = symm)
        uncStat.values = alsoStat
        dep.add_uncertainty(uncStat)    

    if uncHisto:
        unc = Uncertainty(uncType, is_symmetric = symm)
        unc.values = uncHisto
        dep.add_uncertainty(unc)
    else:
        unc = Uncertainty(uncType, is_symmetric = symm)
        unc.values = process["d"+depLabel][0:nBins]
        dep.add_uncertainty(unc)
    
    return dep


if __name__=="__main__":
    
    # Inclusive cross section results ----
    reader = RootFileReader(pathOfCards + fitDiagnosticsName)
    for folder in ["shapes_fit_s"]: #["shapes_prefit", "shapes_fit_s"]:
        for ch in channels:
            ## Table
            table = Table("Figure 6" + channels[ch])
            #table.description = preOrPost[folder].capitalize() + " distribution of the " + dictRegionsXaxisLabels[ch] + " in the " + channelsJets[ch] + "  region. The uncertainty band includes the postfit uncertainties. The bottom of each panel shows the ratios of data to the predictions after the fit (points)."
            table.description = "The distribution of the " + dictRegionsXaxisLabels[ch] + " for events in the " + channelsJets[ch] + "  region. The data (points) and the MC predictions (coloured histograms) after the fit are shown. The vertical bars on the points represent the statistical uncertainty in the data, and the hatched band the total uncertainty in the MC prediction. The lower panels display the ratio of the data to the sum of the MC (points) predictions after the fit, with the bands giving the corresponding uncertainties."
            table.location = "Data from Figure 6 (" + positionCh[ch] + "), located on page 14."
            #table.keywords["observables"] = ["N"]
            table.add_image(pathOfPaperFig + figure[ch])
            
            nameX, nameY, units = dictRegionsXaxisLabels[ch], dictRegionsYaxisLabels[ch] + " ", unitsDict[ch]
            table.add_variable(createIndependentVar(dictBinsExtremesRegions[ch], nameX, True, units))
    
            for process in processes:
                if process == "data":
                    dataGraph = reader.read_graph(folder + "/" + ch + "/" + process)
                    table.add_variable(createDependentVar(dataGraph, nameY + processes[process], False, "", numberBins[ch],"Statistical uncertainty", False))
                else:
                    histogram = reader.read_hist_1d(folder + "/" + ch + "/" + process)
                    table.add_variable(createDependentVar(histogram, nameY + processes[process], False, "", numberBins[ch], "Total uncertainty", True))
            ## Add table and create the yaml files
            submission.add_table(table)
    
    # ----
    table = Table("Cross section")
    table.location = "Data from page 13."
    table.description = "Observed and theoretical cross sections. In the observed, the first uncertainty is statistical, the second is the systematic, and the third the luminosity. In the theoretical, the first uncertainty is due to scale variations, the second due to the choice of PDF. The theoretical cross section has been computed at approximate next-to-next-to-leading order (aNNLO) assuming a top quark mass of 172.5 GeV."
    sigmaTheo = Variable("$\sigma_{tW}^{SM}$ ($\sqrt{s}=13$ TeV)", is_independent=False, is_binned=False, units="pb")
    sigmaTheoUncScale = Uncertainty("scale", is_symmetric = True)
    sigmaTheoUncPDF = Uncertainty("PDF", is_symmetric = True)
    sigmaTheo.values = [71.7]
    sigmaTheoUncScale.values = [1.8]
    sigmaTheoUncPDF.values = [3.4]
    sigmaTheo.add_uncertainty(sigmaTheoUncScale)
    sigmaTheo.add_uncertainty(sigmaTheoUncPDF)
    
    sigmaExp = Variable("$\sigma_{tW}^{Obs.}$ ($\sqrt{s}=13$ TeV)", is_independent=False, is_binned=False, units="pb")
    sigmaExpUncStat = Uncertainty("stat", is_symmetric = True)
    sigmaExpUncSys = Uncertainty("syst", is_symmetric = False)
    sigmaExpUncLum = Uncertainty("lumi", is_symmetric = True)
    sigmaExp.values = [79.2]
    sigmaExpUncStat.values = [0.9]
    sigmaExpUncSys.values = [(-8.0,7.7)]
    sigmaExpUncLum.values = [1.2]
    sigmaExp.add_uncertainty(sigmaExpUncStat)
    sigmaExp.add_uncertainty(sigmaExpUncSys)
    sigmaExp.add_uncertainty(sigmaExpUncLum)
    
    table.add_variable(sigmaExp)
    table.add_variable(sigmaTheo)
    submission.add_table(table)
    
    # Yields
    table = Table("Table 3")
    table.description = "The number of observed and MC predicted events after the fit in the 1j1b, 2j1b, and 2j2b regions. The statistical uncertainties in the data and the total uncertainties in the predictions are given."
    table.location = "Data from Table 3, located on page 14."
    col1 = Variable("Process", is_independent=True, is_binned=False, units="")
    processesList = ["tW", "ttbar", "Drell-Yan", "VV+ttbarV", "Non-W/Z", "Total", "Data"]
    col1.values = processesList
    table.add_variable(col1)
    
    processesList_Yields = {"1j1b": [31600,131200,3990,2800,1140,170800,170900], 
                            "2j1b": [16600,160300,1630,3300,3700,185400,185400],
                            "2j2b": [5500,141100,260,1700,470,149100,148900],
                            #"Postfit/prefit" : [1.11,0.91,1.09,1.18,1.68,0.94,""],
                            }
    
    processesList_unc = {"1j1b": [600,500,190,300,150,300,400], 
                            "2j1b": [500,600,100,500,700,400,400],
                            "2j2b": [200,400,20,400,120,300,400],
                           # "Postfit/prefit" : ["","","","","","",""],
                            }
  
    channelslist = ["1j1b", "2j1b", "2j2b"]#, "Postfit/prefit"]
    for ch in channelslist:
        ## Table
        nameX, nameY, units = "", "Events", ""
        cols = Variable(ch, is_independent=False, is_binned=False, units="")
        cols.values = processesList_Yields[ch]
        uncTot = Uncertainty("Total uncertainty", is_symmetric = True)
        uncTot.values = processesList_unc[ch]
        cols.add_uncertainty(uncTot)   
        table.add_variable(cols)  
        
        
    ## Add table and create the yaml files
    submission.add_table(table)
    
    
    # Differential cross section ----
    for folder in variablesOrdered:
        processesDiff[folder] = "Data"
        reader = RootFileReader(pathOfDiffCards + folder + histosFile)
        ## Table
        table = Table("Figure 8" + names[folder])
        table.description = "Normalised fiducial differential tW production cross section as a function of the " + variables[folder] + ". The vertical bars on the points give the statistical uncertainty in the data, the horizontal bars show the bin width. Predictions from POWHEG (PH) + PYTHIA 8 (P8) DR and DS, POWHEG + HERWIG 7 (H7) DR, MADGRAPH5_aMC@NLO (aMC) + PYTHIA 8 DR, DR2, DS and DS with a dynamic factor are also shown. The grey band represents the statistical uncertainty and the orange band the total uncertainty. In the lower panels, the ratio of the predictions to the data is shown."
        table.location = "Data from Figure 8 (" + positionDiff[folder] + "), located on page 17."
        #table.keywords["observables"] = ["N"]
        table.add_image(pathOfPaperFig + figureDiff[folder])
        
        nameX, nameY, unitsX, unitsY = variables[folder], "$(1/\sigma_{fid.})d\sigma/d$" + variables[folder], unitsDiff[folder], "1/GeV"
        
    
        for process in processesDiff:
            if processesDiff[process] == "Data":
                dataGraph = reader.read_hist_1d(folder)
                table.add_variable(createIndependentVar(dataGraph, nameX, True, unitsX))
                histSysUp = reader.read_hist_1d(folder + "_totalUp")
                histSysDown = reader.read_hist_1d(folder + "_totalDown")
                histSysUpVal = histSysUp["dy"]
                histSysDownVal = histSysDown["dy"]
                histStatUp = reader.read_hist_1d(folder + "_statUp")
                histStatDown = reader.read_hist_1d(folder + "_statDown")
                histStatUpVal = histStatUp["dy"]
                histStatDownVal = histStatDown["dy"]
                for nbin in range(0,len(histSysUpVal)):
                    histSysUpVal[nbin] = abs(histSysUpVal[nbin])
                    histSysDownVal[nbin] = -abs(histSysDownVal[nbin])
                    histStatUpVal[nbin] = abs(histStatUpVal[nbin])
                    histStatDownVal[nbin] = -abs(histStatDownVal[nbin])

                histoSys = list(zip(histSysUpVal,histSysDownVal))
                histoStat = list(zip(histStatUpVal,histStatDownVal))
                table.add_variable(createDependentVar(dataGraph, nameY + " " + processesDiff[process], False, unitsY, -1,"Total uncertainty", False, histoSys, histoStat))
                
            else:
                histogram = reader.read_hist_1d(process)
                table.add_variable(createDependentVar(histogram, nameY + " " + processesDiff[process], False, unitsY, -1, None, True))
        
        del processesDiff[folder]
        ## Add table and create the yaml files
        submission.add_table(table)  
    

    
    # Create the chi2 tables for the differential measurements
    processesDiff = {"tru": "PH DR + P8", "tru_DS": "PH DS + P8", "tru_herwig": "PH DR + H7", "tru_aMC_dr": "aMC DR + P8", "tru_aMC_dr2": "aMC DR2 + P8", "tru_aMC_ds": "aMC DS + P8", "tru_aMC_ds_runn": "aMC DS dyn. + P8"}
    
    ## Table
    table = Table("Tables 4 and 5")
    table.description = "The p-values from the goodness-of-fit tests comparing the six differential cross section measurements with the predictions from POWHEG (PH) + PYTHIA 8 (P8) DR and DS,  POWHEG + HERWIG 7 (H7) DR, MADGRAPH5 aMC@NLO (aMC) + PYTHIA 8 DR, DR2, DS, and DS with a dynamic factor. The complete covariance matrix from the results and the statistical uncertainties of the predictions are taken into account."
    table.location = "Data from Tables 4 and 5 located on page 15."

    col1 = Variable("Variable", is_independent=True, is_binned=False, units="")
    variablesTable = []
    for folder in variablesOrdered2:

        #table.keywords["observables"] = ["N"]
        
        nameX, nameY, unitsX, unitsY = "", "$\chi^2$", "", ""
        variablesTable.append(variables[folder])   
    
    col1.values = variablesTable
    table.add_variable(col1)       
    
    cols_vals = {"tru": [0.02,0.14,0.26,0.70,0.54,0.03], 
            "tru_DS": [0.01,0.27,0.29,0.77,0.60,0.02], 
            "tru_herwig": [0.03,0.01,0.32,0.82,0.59,0.28], 
            "tru_aMC_dr": [0.05,0.15,0.33,0.76,0.49,0.09], 
            "tru_aMC_dr2": [0.04,0.11,0.40,0.86,0.51,0.12], 
            "tru_aMC_ds": [0.03,0.14,0.37,0.84,0.48,0.10], 
            "tru_aMC_ds_runn": [0.07,0.12,0.32,0.82,0.52,0.14]}
    for process in processesDiff:
        cols = Variable(processesDiff[process], is_independent=False, is_binned=False, units="")
        cols.values = cols_vals[process]
        table.add_variable(cols)                    
                
        
        #del processesDiff[folder]
        ## Add table and create the yaml files
      
    submission.add_table(table) 
    # ----

    ## Suplementary material
    
    pathOfSuplementary = "/nfs/fanae/user/vrbouza/Proyectos/tw_run2/desarrollo/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/temp_2022_06_13_diffentera/differential/run2/"
    listOfObs = ["Lep1_Pt", "Lep1Lep2Jet1MET_Pz", "Jet1_Pt", "Lep1Lep2Jet1_M", "Lep1Lep2_DPhi", "Lep1Lep2Jet1MET_Mt"]
    templateName = "R{Var}_"
    responseMatrices = "UnfoldingInfo.root"
    covMatrices = "CovMat_particlefidbin_v2.root"
    
    for var in listOfObs:
        reader = RootFileReader(pathOfSuplementary + var + "/" + responseMatrices)
        ## Table
        table = Table("Supplemental material: " + var + " response matrix")
        table.description = "Response matrix between detector and particle level for the " +  variables[var] + "."
        table.location = "Supplemental material."
        
        table.add_image(pathOfSuplementary +  var + "/responseplots/" + "Rnonumb_{Var}_.pdf".format(Var = var))
        
        nameX, nameY, unitsX, unitsY = variables[var] + "[particle level]", variables[var] + "[detector level]", unitsDiff[var], unitsDiff[var]
        
        histogram = reader.read_hist_2d(templateName.format(Var=var))
        table.add_variable(createIndependentVar(histogram["x_edges"], nameX, True, unitsX))
        table.add_variable(createIndependentVar(histogram["y_edges"], nameY, True, unitsY))
        table.add_variable(createDependentVar(histogram, "Response", False, "", -1, "Statistical uncertainty", True,depLabel="z"))
        submission.add_table(table)


    for var in listOfObs:
        reader = RootFileReader(pathOfSuplementary + var + "/" + covMatrices)
        ## Table
        table = Table("Supplemental material: " + var + " covariance matrix")
        table.description = "Covariance matrix including all uncertainties of the differential result for the " +  variables[var] + "."
        table.location = "Supplemental material."
        
        table.add_image(pathOfSuplementary +  var + "/CovMatplots/" + "Cov_{Var}_fidbin.pdf".format(Var = var))
        
        nameX, nameY, unitsX, unitsY = variables[var], variables[var]+ " ", unitsDiff[var], unitsDiff[var]
        
        histogram = reader.read_hist_2d("CovMat_fidbin")
        table.add_variable(createIndependentVar(histogram["x_edges"], nameX, True, unitsX))
        table.add_variable(createIndependentVar(histogram["y_edges"], nameY, True, unitsY))
        table.add_variable(createDependentVar(histogram, "Covariance", False, "", -1, None, True,depLabel="z"))
        submission.add_table(table)


    
    submission.create_files("./tw-run2/HEP-Data/example_output")
    os.system("mv submission.tar.gz ./tw-run2/HEP-Data/example_output")

