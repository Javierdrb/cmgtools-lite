# -*- coding: UTF-8 -*-.
#!/usr/bin/env python
import os, sys, enum, argparse
from multiprocessing import Pool
import warnings as wr
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

#### Settings
friendspath  = "/pool/phedexrw/userstorage/vrbouza/proyectos/twttbar_run2/productions"
datasamples  = ["SingleMuon", "SingleElec", "DoubleMuon", "DoubleEG", "MuonEG", "LowEGJet", "HighEGJet", "EGamma"]

#mcpath       = "/beegfs/data/nanoAODv9/"
mcpath       = "/pool/phedex/nanoAODv9/"
datapath     = mcpath

logpath      = friendspath + "/{p}/{y}/logs/plots"

#friendsscaff = "--FMCs {P}/0_jecs --Fs {P}/1_lepsuncsAndParticle --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors"
friendsscaff = "--FMCs {P}/0_jecs --Fs {P}/1_lepsuncsAndParticle --Fs {P}/2_cleaning --Fs {P}/3_varstrigger_compgen --FMCs {P}/4_scalefactors"

#commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --showRatio --fixRatioRange --legendColumns 1 --legendWidth 0.07 --legendFontSize 0.039 --noCms --topSpamSize 1.1 --lspam '#splitline{{#scale[1.1]{{#bf{{CMS}}}}}}{{#scale[0.9]{{#it{{Preliminary}}}}}}' --neg --showMCError -W 'MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * L1PreFiringWeight_Nom' -L twttbar-run2UL/functions_twttbar.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP --noStatTotLegendOnRatio --addspam '{nameregion}' --lspamPosition 0.21 .845 .35 .885 --TotalUncRatioStyle 3244 0 --noStatUncOnRatio --YTitleOffset 2.1 2.1 --CanvasSize 600 450 --TotalUncRatioColor 920 920 --addspamPosition .41 .855 .6 .895 --transparentLegend --PrincipalPadDimensions 0.00 0.25 1.00 1.00 --RatioPadDimensions 0.00 0.00 1.00 0.25 --LeftRightMargins 0.16 0.03 --ratioYLabel 'Data/MC' --labelsSize 22 --labelsFont 43 --BottomMarginRatio 0.42 --XTitleOffsetRatio 4.8 --noXErrData --printBin 'bin' --printBinUnity --noExpoShift --no-elist" #--ratioYNDiv 210 --NotDrawRatioLine

#### GENERACION
commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --showRatio --fixRatioRange --legendColumns 1 --legendWidth 0.07 --legendFontSize 0.039 --noCms --topSpamSize 1.1 --lspam '#splitline{{#scale[1.1]{{#bf{{CMS}}}}}}{{#scale[0.9]{{#it{{Preliminary}}}}}}' --neg --showMCError -L twttbar-run2UL/functions_twttbar.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP --noStatTotLegendOnRatio --addspam '{nameregion}' --lspamPosition 0.21 .845 .35 .885 --TotalUncRatioStyle 3244 0 --noStatUncOnRatio --YTitleOffset 2.1 2.1 --CanvasSize 600 450 --TotalUncRatioColor 920 920 --addspamPosition .41 .855 .6 .895 --transparentLegend --PrincipalPadDimensions 0.00 0.25 1.00 1.00 --RatioPadDimensions 0.00 0.00 1.00 0.25 --LeftRightMargins 0.16 0.03 --ratioYLabel 'Data/MC' --labelsSize 22 --labelsFont 43 --BottomMarginRatio 0.42 --XTitleOffsetRatio 4.8 --noXErrData --printBin 'bin' --printBinUnity --noExpoShift --no-elist" #--ratioYNDiv 210 --NotDrawRatioLine

# For blind plots
commandblindscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --showRatio --fixRatioRange --legendColumns 1 --legendWidth 0.07 --legendFontSize 0.032 --noCms --topSpamSize 1.1 --lspam '#splitline{{#scale[1.1]{{#bf{{CMS}}}}}}{{#scale[0.9]{{#it{{Preliminary}}}}}}' --neg --showMCError -W 'MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * L1PreFiringWeight_Nom' -L twttbar-run2UL/functions_twttbar.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP --noStatTotLegendOnRatio --addspam '{nameregion}' --lspamPosition 0.21 .845 .35 .885 --TotalUncRatioStyle 3244 0 --noStatUncOnRatio --YTitleOffset 2.1 2.1 --TotalUncRatioColor 920 920 --addspamPosition .41 .855 .6 .895 --transparentLegend --LeftRightMargins 0.16 0.03  --labelsSize 22 --labelsFont 43 --BottomMarginRatio 0.42 --XTitleOffsetRatio 4.8 --noXErrData --printBin 'bin' --printBinUnity --noExpoShift --no-elist" #--ratioYNDiv 210 --NotDrawRatioLine


slurmscaff   = 'sbatch {extraS} -c {nth} -p {queue} -J {jobname} -e {logpath}/log.%j.%x.err -o {logpath}/log.%j.%x.out --wrap "{command}"'
lumidict     = {"2016apv": 19.52,
                "2016"   : 16.81,
                "2017"   : 41.48,
                "2018"   : 59.83}


def GeneralExecutioner(task):
    prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs, doBlind, extraslurm, doComp = task

    if not os.path.isdir(outpath + "/" + str(year)) and not pretend:
        os.system("mkdir -p " + outpath + "/" + str(year))

    if queue != "":
        if not os.path.isdir(logpath.format(y = year, p = prod)) and not pretend:
            os.system("mkdir -p " + logpath.format(y = year, p = prod))

        for reg in region.split(","):
            jobname_   = "CMGTplotter_{y}_{r}_{s}".format(y = year, r = reg, s = "all" if not len(selplot) else ".".join(selplot))
            submitcomm = slurmscaff.format(extraS = extraslurm,
                                          nth     = nthreads,
                                          queue   = queue,
                                          jobname = jobname_,
                                          logpath = logpath.format(y = year, p = prod),
                                          command = PlottingCommand(prod, year, nthreads, outpath, selplot, reg, ratiorange, extra, useFibre, doUncs, doBlind, doComp))
            print("Command:", submitcomm)
            if not pretend: os.system(submitcomm)
    else:
        for reg in region.split(","):
            execcomm = PlottingCommand(prod, year, nthreads, outpath, selplot, reg, ratiorange, extra, useFibre, doUncs, doBlind, doComp)
            print("Command:", execcomm)
            if not pretend: os.system(execcomm)
    return


def PlottingCommand(prod, year, nthreads, outpath, selplot, region, ratio, extra, useFibre, doUncs, doBlind, doComp):
    mcafile_    = "twttbar-run2UL/mca-twttbar/mca-twttbar.txt" if not doComp else "twttbar-run2UL/mca-twttbar/mca-twttbar-compbb4l.txt"
    cutsfile_   = "twttbar-run2UL/cuts-twttbar/cuts-twttbar-{reg}.txt".format(reg = region if ("_" not in region) else region.split("_")[0] if ("differential" not in region and "cut" not in region) else region)
    plotsfile_  = "twttbar-run2UL/plots-twttbar/plots-twttbar-{reg}.txt".format(reg = region.replace("SF", ""))

    samplespaths_ = "-P " + friendspath + "/" + prod + ("/" + year) * (year != "run2")
    if useFibre: samplespaths_ = samplespaths_.replace("phedexrw", "phedex").replace("cienciasrw", "ciencias")

    nth_        = "" if nthreads == 0 else ("--split-factor=-1 -j " + str(nthreads))
    friends_    = friendsscaff + (" --Fs {P}/5_mvas" * ("MVA" in region))
    outpath_    = outpath + "/" + year + "/" + (region if "_" not in region else (region.split("_")[0] + "/" + region.split("_")[1]))
    selplot_    = " ".join( [ "--sP {p}".format(p = sp) for sp in selplot ] ) if len(selplot) else ""
    ratio_      = "--maxRatioRange " + ratio
    nameregion_ = "e^{#pm}#mu^{#mp}" if not "SF" in region else "e^{#pm}e^{#mp}+#mu^{#pm}#mu^{#mp}"
    if "_" not in region and "nojets" not in region:
        nameregion_ += "+" + region.replace("t", "b").replace("plus", "+")
    elif "differential" in region and "nojets" not in region:
        nameregion_ += "+" + region.split("_")[0].replace("t", "b").replace("plus", "+") + "+0j_{loose}"
    elif "MVA" in region and "nojets" not in region:
        nameregion_ += "+" + region.split("_")[0].replace("t", "b").replace("plus", "+")
    # extra_  = extra + (" --compareWithSignalThis bb4l --compareWithSignalThis bb4l_norm  --compareWithSignalThis bb4l_fix  --compareWithSignalThis bb4l_fix_norm") * doComp + (" --unc twttbar-run2UL/uncs-twttbar/uncs-twttbar.txt ") * doUncs
    #extra_  = extra + (" --compareWithSignalThis bb4l --compareWithSignalThis bb4l_fix ") * doComp + (" --unc twttbar-run2UL/uncs-twttbar/uncs-twttbar.txt ") * doUncs
    #extra_  = extra + (" --compareWithSignalThis bb4l_fix --compareWithSignalThis bb4l_fix_norm ") * doComp + (" --unc twttbar-run2UL/uncs-twttbar/uncs-twttbar.txt ") * doUncs
    extra_  = extra + (" --compareWithSignalThis bb4l_fix_norm ") * doComp + (" --unc twttbar-run2UL/uncs-twttbar/uncs-twttbar.txt ") * doUncs
    thecomm = commandscaff if not doBlind else commandblindscaff
    
    comm = thecomm.format(outpath      = outpath_,
                          friends      = friends_,
                          samplespaths = samplespaths_,
                          lumi         = lumidict[year] if year != "run2" else str(lumidict["2016apv"]) + "," + str(lumidict["2016"]) + "," + str(lumidict["2017"]) + "," + str(lumidict["2018"]),
                          nth          = nth_,
                          year         = year if year != "run2" else "2016apv,2016,2017,2018",
                          selplot      = selplot_,
                          mcafile      = mcafile_,
                          cutsfile     = cutsfile_,
                          plotsfile    = plotsfile_,
                          ratio        = ratio_,
                          extra        = extra_,
                          nameregion   = nameregion_)
    return comm


def confirm(message = "Do you wish to continue?"):
    """
    Ask user to enter y(es) or n(o) (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n", "yes", "no"]:
        answer = input(message + " [Y/N]\n").lower()
    return answer[0] == "y"



if __name__=="__main__":
    parser = argparse.ArgumentParser(usage = "python plotterHelper.py [options]", description = "Helper for plotting.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--production','-P', metavar = "prod",      dest = "prod",    required = True)
    parser.add_argument('--year',      '-y', metavar = 'year',      dest = "year",    required = False, default = "2016")
    parser.add_argument('--queue',     '-q', metavar = 'queue',     dest = "queue",   required = False, default = "")
    parser.add_argument('--extraArgs', '-e', metavar = 'extra',     dest = "extra",   required = False, default = "")
    parser.add_argument('--extraSlurmArgs','-eS',metavar='extraslurm',dest="extraslurm",required=False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',  dest = "nthreads",required = False, default = 0, type = int)
    parser.add_argument('--select-plot','--sP',action = "append",   dest = "selplot", required = False, default = [])
    parser.add_argument('--pretend',   '-p', action = "store_true", dest = "pretend", required = False, default = False)
    parser.add_argument('--outpath',   '-o', metavar = 'outpath',   dest = "outpath", required = False, default = "./temp/varplots")
    parser.add_argument('--region',    '-r', metavar = 'region',    dest = "region",  required = False, default = "1j1t")
    parser.add_argument('--maxRatioRange', "-R", metavar = 'ratiorange', dest = "ratiorange", required = False, default = "0.8 1.2")
    parser.add_argument('--createSoftLinks', action = "store_true", dest = "createSL", required = False, default = False)
    parser.add_argument('--useFibre',  "-f", action = "store_true", dest = "useFibre", required = False, default = False)
    parser.add_argument('--uncertainties', "-u", action = "store_true", dest = "doUncs", required = False, default = False)
    parser.add_argument('--comparison', "-c", action = "store_true", dest = "doComp", required = False, default = False)
    parser.add_argument('--blind', action = "store_true", dest = "blindornot", required = False, default = False)



    args     = parser.parse_args()
    prod     = args.prod
    year     = args.year
    queue    = args.queue
    extra    = args.extra
    extraslurm=args.extraslurm
    nthreads = args.nthreads
    selplot  = args.selplot
    pretend  = args.pretend
    outpath  = args.outpath
    region   = args.region
    createSL = args.createSL
    useFibre = args.useFibre
    ratiorange = args.ratiorange
    doUncs = args.doUncs
    doComp = args.doComp

    if args.blindornot: extra += " --xp data"
    doBlind = args.blindornot


    if createSL:
        destdir = friendspath + "/" + prod + "/" + str(year)
        SLcommscaff = "ln -s {realdataset} {symlink}"

        #### First, MC
        print("> Creating MC symbolic links...")
        mcsampleslist = os.listdir(mcpath + "/" + str(year))
        for sam in mcsampleslist:
            if not os.path.islink(destdir + "/" + sam):
                os.system(SLcommscaff.format(realdataset = mcpath + "/" + str(year) + "/" + sam,
                                             symlink = destdir + "/" + sam))
        #sys.exit()

        #### Later, data
        print("> Creating data symbolic links...")
        datasampleslist = os.listdir(datapath + "/" + str(year))
        for sam in datasampleslist:
            isData = any(ext in sam for ext in datasamples)
            if not os.path.islink(destdir + "/" + sam) and isData:
                os.system(SLcommscaff.format(realdataset = datapath + "/" + str(year) + "/" + sam,
                                             symlink = destdir + "/" + sam))

        print("> Finished!")
    elif queue != "":
        print("> Plotting jobs will be sent to the cluster.")
        if year == "all":
            print("   - All four 'years' and the combination will be plotted.")
            cont = False
            if   pretend:
                cont = True
            elif confirm("Four jobs per requested region will be sent to queue {q} with {j} requested threads to plot in each year and in the combination {pls}. Do you want to continue?".format(q = queue, j = nthreads, pls = "all the plots" if not len(selplot) else " and ".join(selplot))):
                cont = True

            if cont:
                for y in ["2016apv", "2016", "2017", "2018", "run2"]:
                    GeneralExecutioner( (prod, y, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs, doBlind, extraslurm, doComp) )
        else:
            cont = False
            if   pretend:
                cont = True
            elif confirm("One job per requested region will be sent to queue {q} with {j} requested threads to plot in year {y} {pls}. Do you want to continue?".format(q = queue, j = nthreads, y = year, pls = "all the plots" if not len(selplot) else " and ".join(selplot))):
                cont = True

            if cont:
                GeneralExecutioner( (prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs, doBlind, extraslurm, doComp) )
    else:
        print("> Local execution chosen.")
        if year == "all":
            print("   - All four 'years' and the combination will be plotted.")
            for y in ["2016apv", "2016", "2017", "2018", "run2"]:
                GeneralExecutioner( (prod, y, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs, doBlind, extraslurm, doComp) )
        else:
            GeneralExecutioner( (prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs, doBlind, extraslurm, doComp) )
