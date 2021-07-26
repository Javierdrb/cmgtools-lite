import os, sys, argparse
from multiprocessing import Pool
from copy import deepcopy
import warnings as wr
import ROOT as r

#sys.path.append('{cmsswpath}/src/CMGTools/TTHAnalysis/python/plotter/tw-run2/differential/'.format(cmsswpath = os.environ['CMSSW_BASE']))
#import varList as vl

r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

#groups    = ["ttbar", "tw"]
#variables = ["x"]
#variables = ["LeadingJetPt", "Fiducial"]

#variations = ["Btag", "ElecEff", "JES", "Mistag", "MuonEff", "PU", "TopPt", "Trig", "JER", "UE", "hDamp", "isr", "pdf", "tWME", "ttbarME", "fsr", "ColourQCDbasedCRTuneerdON", "ColourGluonMoveCRTuneerdON", "ColourPowhegerdON", "ColourGluonMoveCRTune", "ttbar", "Non-WorZ", "VVttbarV", "DY", "mtop"]
#variations = ["isr_tw", "fsr_tw", "isr_ttbar", "fsr_ttbar"]

#colour_syst    = ["ColourQCDbasedCRTuneerdON", "ColourGluonMoveCRTuneerdON", "ColourPowhegerdON", "ColourGluonMoveCRTune"]
#colour_syst    = []

vetolist       = ["UnfoldingInfo", "detector.root", "detectorparticleResponse.root", "nonfiducial", "particle.root", "particleOutput.root", "particlefidOutput.root", "particlefidbinOutput.root", "particlebinOutput.root". "higgsCombine", "combcard"]
#vetolist       = ["UnfoldingInfo", "detector", "nonfiducial", "particle.root"]
foldervetolist = ["responseplots", "particleplots", "detectorplots", "impacts_"]


def getOutSuffix(s):
    if "cuts" in s or "plots" in s:
        return ""

    ret = "_" + s.replace(".root", "")

    if   "forExtr" in ret:
        ret = "_detector"
    elif "particleOutput" in ret:
        ret = "_particle"

    return ret


def getFiles(path):
    theinfo = next(os.walk(path))
    #print(theinfo)
    retlist = []
    if len(theinfo[1]) != 0:
        for iF in theinfo[2]:
            if ".root" in iF and not any([el in iF for el in vetolist]):
                retlist.append( (iF, path) )
        for iD in theinfo[1]:
            if not any([el in iD for el in foldervetolist]):
                retlist.extend(getFiles(path + "/" + iD))
    else:
        for iF in theinfo[2]:
            if ".root" in iF and not any([el in iF for el in vetolist]):
                retlist.append( (iF, path) )
    return retlist


def plotVariationsFromOneProcess(tsk):
    thevar, theproc, subdict, outpath = tsk
    for iU in subdict:
        if iU == "": continue

        c = r.TCanvas("c", "", 600, 600)

        c.Divide(1, 2)
        c.GetPad(1).SetPad(*tuple([float(i) for i in "0.00, 0.25, 1.00, 1.00".split(',')]))
        c.GetPad(2).SetPad(*tuple([float(i) for i in "0.00, 0.00, 1.00, 0.25".split(',')]))
        c.GetPad(1).SetTopMargin(0.08)
        c.GetPad(1).SetRightMargin(0.03)
        c.GetPad(1).SetLeftMargin(0.16)
        c.GetPad(1).SetBottomMargin(0.025)

        c.GetPad(2).SetBottomMargin(0.3)
        c.GetPad(2).SetBottomMargin(0.35)
        c.GetPad(2).SetBottomMargin(0.375)
        c.GetPad(2).SetRightMargin(0.03)
        c.GetPad(2).SetLeftMargin(0.16)

        c.cd(1)
#        print thevar, theproc, iU
        nominal = subdict[""]
        varup   = subdict[iU]["Up"]
        vardn   = subdict[iU]["Down"]

        leg = r.TLegend( .52, .9 - 0.18, .735, .9)
        leg.SetTextFont(42)
        leg.SetTextSize(0.0435)
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetFillStyle(0); # transparent legend!

        nominal.SetLineColor(r.kBlack)
        nominal.SetFillStyle(0)
        nominal.SetStats(0)
        nominal.SetTitle("")
        nominal.GetXaxis().SetTitle("BDT disc." if any([el in outpath for el in ["1j1t", "2j1t"]]) else "Subleading jet p_{T}")
        nominal.SetMaximum(-1111); varup.SetMaximum(-1111); vardn.SetMaximum(-1111);
        nominal.GetYaxis().SetRangeUser(0, max([nominal.GetMaximum(), varup.GetMaximum(), vardn.GetMaximum()]) * 1.1)
        nominal.GetXaxis().SetLabelOffset(999)
        nominal.GetXaxis().SetLabelSize(0)
        nominal.GetXaxis().SetTitle(' ')
        leg.AddEntry(nominal, "Nominal", "f")

        varup.SetLineColor(r.kBlue)
        varup.SetLineWidth(2)
        varup.SetFillStyle(0)
        leg.AddEntry(varup, "Up", "f")

        vardn.SetLineColor(r.kRed)
        vardn.SetLineWidth(2)
        vardn.SetFillStyle(0)
        leg.AddEntry(vardn, "Down", "f")

        nominal.Draw("P,E")
        varup.Draw("histsame")
        vardn.Draw("histsame")
        leg.Draw("same")

        c.cd(2)
        ratioUp   = deepcopy(nominal.Clone("ratioUp"))
        ratioDown = deepcopy(vardn.Clone("ratioDown"))
        constant  = deepcopy(nominal.Clone("constant"))

        for iB in range(1, ratioUp.GetNbinsX() + 1):
            try:
                ratioUp.SetBinContent(iB, varup.GetBinContent(iB) / nominal.GetBinContent(iB))
            except ZeroDivisionError:
                ratioUp.SetBinContent(iB, 1)
            try:
                ratioDown.SetBinContent(iB, ratioDown.GetBinContent(iB) / nominal.GetBinContent(iB))
            except ZeroDivisionError:
                ratioDown.SetBinContent(iB, 1)

            constant.SetBinContent(iB, 1)

        ratioUp.SetStats(0)
        ratioUp.SetTitle(" ")
        ratioUp.SetLineColor(r.kBlue)
        ratioUp.SetLineWidth(2)
        ratioUp.SetFillStyle(0)
        ratioUp.GetXaxis().SetTitle(nominal.GetXaxis().GetTitle())
        ratioUp.GetXaxis().SetTitleFont(43)
        ratioUp.GetXaxis().SetTitleSize(22)
        ratioUp.GetXaxis().SetTitleOffset(4)
        ratioUp.GetXaxis().SetLabelFont(43)
        ratioUp.GetXaxis().SetLabelSize(22)
        ratioUp.GetXaxis().SetLabelOffset(0.007)
        ratioUp.GetXaxis().SetNdivisions(510, True)
        #ratioUp.GetXaxis().SetNdivisions(505, False)
        ratioUp.GetXaxis().SetRangeUser(nominal.GetXaxis().GetBinLowEdge(1), nominal.GetXaxis().GetBinUpEdge(nominal.GetNbinsX()))

        #ratioUp.GetYaxis().SetRangeUser(0.8, 1.2)
        ratioUp.GetYaxis().SetRangeUser(0.95, 1.05)
        ratioUp.GetYaxis().SetTitle('Vars./Nom.')
        ratioUp.GetYaxis().SetTitleFont(43)
        ratioUp.GetYaxis().SetTitleSize(16)
        ratioUp.GetYaxis().SetTitleOffset(2.2)
        ratioUp.GetYaxis().CenterTitle(True)
        ratioUp.GetYaxis().SetLabelFont(43)
        ratioUp.GetYaxis().SetLabelSize(16)
        ratioUp.GetYaxis().SetLabelOffset(0.007)
        ratioUp.GetYaxis().SetNdivisions(505, True)

        constant.SetLineWidth(1)

        ratioUp.Draw("histsame")
        ratioDown.Draw("histsame")
        constant.Draw("histsame")

        c.SaveAs(outpath + "/uncVar_" + thevar + "_" + theproc + "_" + iU + ".png")
        c.SaveAs(outpath + "/uncVar_" + thevar + "_" + theproc + "_" + iU + ".pdf")
        c.Close(); del c; del leg
    return



def plotVariations(tup, outname, ncores = -1):
    histodict = {}
    rF = r.TFile(tup[1] + "/" + tup[0], "READ")

    outfolder = tup[1] + "/" + outname + getOutSuffix(tup[0])
    if not os.path.isdir(outfolder):
        os.system("mkdir -p " + outfolder)

    print("\n> Reading file " + tup[1] + "/" + tup[0] + " ...")
    nplots = 0
    #thisisnotacard = False
    varprefix = "x"
    vetostring = "ptcmtptoverhttotdetadphibtagdrpzptsum2j1b1j1brebin"
    thisisandiffrfile = "Output" in tup[0] or "detectorsignal_bs" in tup[0]

    for key in rF.GetListOfKeys():
        tmpnam     = key.GetName()
        if any([el in tmpnam for el in ["hincsyst", "hincmax", "canvas", "stack", "CovMat", "nom0", "nom1", "tot_weight","tmvaBDT_2j1b_12bins","tmvaBDT_2j1b_rebin","tmvaBDT_2j1b_smallb","tmvaBDT_1j1b_20bins","tmvaBDT_1j1b_rebin","tmvaBDT_1j1b_smallb"]]): continue
        if not thisisandiffrfile:
            if "data" in tmpnam: continue

        #print tmpnam

        #### OLD
        #if not "x_" in tmpnam and not thisisnotacard:
            #print "    - This is not a card!"
            #thisisnotacard = True
            #tmpprefix = tup[1].split("/")[-1] if tup[1][-1] != "/" else tup[1].split("/")[-2]
            ##tmpprefix = tmpnam.split("_")[0]
            ##print tmpprefix

        if thisisandiffrfile:
            varprefix = "signal"

        elif (varprefix + "_") != tmpnam[:len((varprefix + "_"))] or (tmpnam.replace(varprefix, "").split("_")[0].lower() in vetostring):
            varprefix = (tmpnam.split("_")[0]
                         if ( len(tmpnam.split("_")) < 2 )
                         else tmpnam.split("_")[0]
                         if ( (tmpnam.split("_")[1]).lower() not in vetostring )
                         else "_".join(tmpnam.split("_")[0:2]) )

        #varprefix = "tmvaBDT_2j1b_12bins"
        #varprefix = "jet2_pt_rebin"

        #cleanednam = "signal" * (thisisnotacard) + tmpnam.replace(tmpprefix, "")
        cleanednam = tmpnam.replace(varprefix + "_", "")
        if cleanednam[-1] == "_":
            cleanednam = cleanednam[:-1]
        #print cleanednam, varprefix, tmpnam

        if varprefix not in histodict:
            histodict[varprefix] = {}

        if all([el not in tmpnam for el in ["Up", "Down"]]): # It is the nominal value of a process
            if cleanednam not in histodict[varprefix]:
                histodict[varprefix][cleanednam] = {}
            #if "dy" in cleanednam:
                #print tmpnam, cleanednam
            histodict[varprefix][cleanednam][""] = deepcopy(rF.Get(tmpnam).Clone(cleanednam + "_" + varprefix))
        else:
            tmpproc = cleanednam.split("_")[0]

            tmpunc  = ("_".join( cleanednam.split("_")[1:] )).replace("Up", "").replace("Down", "")
            tmpvar  = "Up" if "Up" in cleanednam else "Down" if "Down" in cleanednam else "OTHER"

            #print(varprefix, tmpnam, tmpproc, tmpunc, tmpvar)

            if tmpproc not in histodict[varprefix]:
                histodict[varprefix][tmpproc] = {}
            if tmpunc not in histodict[varprefix][tmpproc]:
                histodict[varprefix][tmpproc][tmpunc] = {}
                nplots += 1

            histodict[varprefix][tmpproc][tmpunc][tmpvar] = deepcopy(rF.Get(tmpnam).Clone(tmpproc + "_" + tmpunc))

    rF.Close()
    #print(histodict["nloosejets"])
    #sys.exit()

    print("    - Plotting " + str(nplots) + " histograms...")
    tasks = []
    for iV in histodict:
        for iP in histodict[iV]:
            #print iP
            tasks.append( (iV, iP, histodict[iV][iP], outfolder) )
    if ncores < 2:
        for tsk in tasks:
            plotVariationsFromOneProcess(tsk)
    else:
        pool = Pool(ncores)
        pool.map(plotVariationsFromOneProcess, tasks)
        pool.close()
        pool.join()
        del pool
    print("    - Done!")
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
    parser = argparse.ArgumentParser(usage = "python plotUncsVariations.py folder", description = "Helper for plotting.", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('infolder')
    parser.add_argument('--varsFolderName',  "-n", metavar = 'outname',  dest = "outname", required = False, default = "uncVariations")
    parser.add_argument("-j", metavar = 'ncores',  dest = "ncores", required = False, default = -1, type = int)



    args     = parser.parse_args()
    infolder = args.infolder
    outname  = args.outname
    ncores   = args.ncores

    filelist = getFiles(infolder)

    #print(filelist)
    #sys.exit()

    for iT in filelist:
        plotVariations(iT, outname, ncores)
