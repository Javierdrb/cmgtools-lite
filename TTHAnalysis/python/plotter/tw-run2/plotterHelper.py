# -*- coding: UTF-8 -*-.
#!/usr/bin/env python
import os, sys, enum, argparse
from multiprocessing import Pool
import warnings as wr
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

#### Settings
friendspath  = "/pool/phedexrw/userstorage/vrbouza/proyectos/tw_run2/productions"
datasamples  = ["SingleMuon", "SingleElec", "DoubleMuon", "DoubleEG", "MuonEG", "LowEGJet", "HighEGJet", "EGamma"]

#mcpath       = "/pool/ciencias/nanoAODv6/29jan2020_MC"
#datapath     = "/pool/ciencias/nanoAODv6/13jan2020"
mcpath       = "/pool/phedex/nanoAODv6v7"
mcpathdiv    = "/pool/phedex/userstorage/vrbouza/proyectos/tw_run2/misc/2021_04_nuevasdivisiones"
datapath     = "/pool/phedex/nanoAODv6v7"

logpath      = friendspath + "/{p}/{y}/logs/plots"
#logpath = "/nfs/fanae/user/asoto/Proyectos/tW-Victor/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/python/plotter/plot_logs"

#mcpathdiv    = "/pool/phedex/userstorage/vrbouza/proyectos/tw_run2/misc/divisiones/"
#logpath      = friendspath + "/{p}/{y}/logs/plots"


#friendsscaff = "--Fs {fpath}/{p}/{y}/0_yeartag --Fs {fpath}/{p}/{y}/1_lepmerge_roch --Fs {fpath}/{p}/{y}/2_cleaning --Fs {fpath}/{p}/{y}/3_varstrigger --FMCs {fpath}/{p}/{y}/4_scalefactors --Fs {fpath}/{p}/{y}/5_mvas"

#friendsscaff = "--Fs {P}/0_yeartag --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/5_mvas"
#friendsscaff = "--Fs {P}/0_yeartag --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/5_mvas_new"
#friendsscaff = "--Fs {P}/0_yeartag --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/5_mvas_bkp20200807"
#friendsscaff = "--Fs {P}/0_yeartag --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors_bkp" ### Nueva, dejando la incorporacion del quinto ftree opcional
friendsscaff = "--FDs {P}/0_lumijson --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/6_hemissue" ### Nueva, dejando la incorporacion del quinto ftree opcional

#commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} --maxRatioRange 0.8 1.2 --ratioYNDiv 210 --showRatio --attachRatioPanel --fixRatioRange --legendColumns 3 --legendWidth 0.52 --legendFontSize 0.042 --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{{#bf{{CMS}}}} #scale[0.9]{{#it{{Preliminary}}}}' --showMCError -W 'MuonSF * ElecSF * TrigSF * puWeight * bTagWeight{extraweights}' -L tw-run2/functions_tw.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra}"

# Pre-separar SF
#commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --ratioYNDiv 210 --showRatio --attachRatioPanel --fixRatioRange --legendColumns 3 --legendWidth 0.52 --legendFontSize 0.042 --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{{#bf{{CMS}}}} #scale[0.9]{{#it{{Preliminary}}}}' --showMCError -W 'MuonSF * ElecSF * TrigSF * puWeight * bTagWeight * PrefireWeight' -L tw-run2/functions_tw.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra}"

# Post-separar SF
#commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --ratioYNDiv 210 --showRatio --attachRatioPanel --fixRatioRange --legendColumns 3 --legendWidth 0.52 --legendFontSize 0.042 --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{{#bf{{CMS}}}} #scale[0.9]{{#it{{Preliminary}}}}' --neg --showMCError -W 'MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * PrefireWeight' -L tw-run2/functions_tw.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP"

commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --showRatio --fixRatioRange --legendColumns 1 --legendWidth 0.07 --legendFontSize 0.039 --noCms --topSpamSize 1.1 --lspam '#splitline{{#scale[1.1]{{#bf{{CMS}}}}}}{{#scale[0.9]{{#it{{Preliminary}}}}}}' --neg --showMCError -W 'MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * PrefireWeight' -L tw-run2/functions_tw.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP --noStatTotLegendOnRatio --addspam 'e^{{#pm}}#mu^{{#mp}}{nameregion}' --lspamPosition 0.21 .845 .35 .885 --TotalUncRatioStyle 3244 0 --noStatUncOnRatio --YTitleOffset 2.1 2.1 --CanvasSize 600 450 --TotalUncRatioColor 920 920 --addspamPosition .41 .855 .6 .895 --transparentLegend --PrincipalPadDimensions 0.00 0.25 1.00 1.00 --RatioPadDimensions 0.00 0.00 1.00 0.25 --LeftRightMargins 0.16 0.03 --ratioYLabel 'Data/MC' --labelsSize 22 --labelsFont 43 --BottomMarginRatio 0.42 --XTitleOffsetRatio 4.8 --noXErrData --printBin 'bin' --printBinUnity --noExpoShift" #--ratioYNDiv 210 --NotDrawRatioLine --aefr temp_cards/2021-05-28_AllUnc/run2/TablaAlternativa/fitDiagnosticsTest.root fit_s --aefrl Postfit --peg-process tw r

# For blind plots
#commandscaff = "python mcPlots.py --tree NanoAOD --pdir {outpath} {friends} {samplespaths} -f -l {lumi} {nth} --year {year} {ratio} --showRatio --fixRatioRange --legendColumns 1 --legendWidth 0.07 --legendFontSize 0.032 --noCms --topSpamSize 1.1 --lspam '#splitline{{#scale[1.1]{{#bf{{CMS}}}}}}{{#scale[0.9]{{#it{{Preliminary}}}}}}' --neg --showMCError -W 'MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * PrefireWeight' -L tw-run2/functions_tw.cc {selplot} {mcafile} {cutsfile} {plotsfile} {extra} --AP --noStatTotLegendOnRatio --addspam 'e^{{#pm}}#mu^{{#mp}}{nameregion}' --lspamPosition 0.21 .845 .35 .885 --TotalUncRatioStyle 3244 0 --noStatUncOnRatio --YTitleOffset 2.1 2.1 --TotalUncRatioColor 920 920 --addspamPosition .41 .855 .6 .895 --transparentLegend --LeftRightMargins 0.16 0.03  --labelsSize 22 --labelsFont 43 --BottomMarginRatio 0.42 --XTitleOffsetRatio 4.8 --noXErrData --printBin 'bin' --printBinUnity --noExpoShift" #--ratioYNDiv 210 --NotDrawRatioLine


slurmscaff   = 'sbatch -c {nth} -p {queue} -J {jobname} -e {logpath}/log.%j.%x.err -o {logpath}/log.%j.%x.out --wrap "{command}"'
lumidict     = {2016 : 36.33, 
                2017 : 41.53,
                2018 : 59.74}


def GeneralExecutioner(task):
    prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs = task

    if not os.path.isdir(outpath + "/" + str(year)) and not pretend:
        os.system("mkdir -p " + outpath + "/" + str(year))

    if queue != "":
        if not os.path.isdir(logpath.format(y = year, p = prod)) and not pretend:
            os.system("mkdir -p " + logpath.format(y = year, p = prod))

        for reg in region.split(","):
            jobname_   = "CMGTplotter_{y}_{r}_{s}".format(y = year, r = reg, s = "all" if not len(selplot) else ".".join(selplot))
            submitcomm = slurmscaff.format(nth  = nthreads,
                                        queue   = queue,
                                        jobname = jobname_,
                                        logpath = logpath.format(y = year, p = prod),
                                        command = PlottingCommand(prod, year, nthreads, outpath, selplot, reg, ratiorange, extra, useFibre, doUncs))
            print "Command:", submitcomm
            if not pretend: os.system(submitcomm)
    else:
        for reg in region.split(","):
            execcomm = PlottingCommand(prod, year, nthreads, outpath, selplot, reg, ratiorange, extra, useFibre, doUncs)
            print "Command:", execcomm
            if not pretend: os.system(execcomm)


    return



#### OLD
#def PlottingCommand(prod, year, nthreads, outpath, selplot, region, extra):
    #mcafile_   = "tw-run2/mca-tw-{y}.txt".format(y = year)
    #cutsfile_  = "tw-run2/cuts-tw-{reg}.txt".format(reg = region)
    #plotsfile_ = "tw-run2/plots-tw-{reg}.txt".format(reg = region)

    #samplespaths_ = "-P " + mcpath + "/" + str(year) + " -P " + datapath + "/" + str(year)
    #extraweights_ = "" if year == 2018 else " * PrefireWeight"

    #nth_       = "" if nthreads == 0 else ("--split-factor=-1 -j " + str(nthreads))
    #friends_   = friendsscaff.format(fpath = friendspath,
                                     #p     = prod,
                                     #y     = year)
    #outpath_   = outpath + "/" + str(year) + "/" + region


    #comm = commandscaff.format(outpath      = outpath_,
                               #friends      = friends_,
                               #samplespaths = samplespaths_,
                               #lumi      = lumidict[year],
                               #nth       = nth_,
                               #year      = year,
                               #extraweights = extraweights_,
                               #selplot   = "" if selplot == "" else ("--sP " + selplot),
                               #mcafile   = mcafile_,
                               #cutsfile  = cutsfile_,
                               #plotsfile = plotsfile_,
                               #extra     = extra)

    #return comm


def PlottingCommand(prod, year, nthreads, outpath, selplot, region, ratio, extra, useFibre, doUncs):
    mcafile_    = "tw-run2/mca-tw.txt"
    cutsfile_   = "tw-run2/cuts-tw-{reg}.txt".format(reg = region if ("_" not in region) else region.split("_")[0] if ("differential" not in region) else region)
    plotsfile_  = "tw-run2/plots-tw/plots-tw-{reg}.txt".format(reg = region)

    samplespaths_ = "-P " + friendspath + "/" + prod + ("/" + year) * (year != "run2")
    if useFibre: samplespaths_ = samplespaths_.replace("phedexrw", "phedex").replace("cienciasrw", "ciencias")

    nth_        = "" if nthreads == 0 else ("--split-factor=-1 -j " + str(nthreads))
    friends_    = friendsscaff + (" --Fs {P}/5_mvas" * ("MVA" in region))
    outpath_    = outpath + "/" + year + "/" + (region if "_" not in region else (region.split("_")[0] + "/" + region.split("_")[1]))
    selplot_    = " ".join( [ "--sP {p}".format(p = sp) for sp in selplot ] ) if len(selplot) else ""
    ratio_      = "--maxRatioRange " + ratio
    nameregion_ = ""
    if "_" not in region and "nojets" not in region:
        nameregion_ = "+" + region.replace("t", "b").replace("plus", "+")
    elif "differential" in region and "nojets" not in region:
        nameregion_ = "+" + region.split("_")[0].replace("t", "b").replace("plus", "+") + "+0j_{loose}"
    elif "MVA" in region and "nojets" not in region:
        nameregion_ = "+" + region.split("_")[0].replace("t", "b").replace("plus", "+")

    comm = commandscaff.format(outpath      = outpath_,
                               friends      = friends_,
                               samplespaths = samplespaths_,
                               lumi      = lumidict[int(year)] if year != "run2" else str(lumidict[2016]) + "," + str(lumidict[2017]) + "," + str(lumidict[2018]),
                               nth       = nth_,
                               year      = year if year != "run2" else "2016,2017,2018",
                               selplot   = selplot_,
                               mcafile   = mcafile_,
                               cutsfile  = cutsfile_,
                               plotsfile = plotsfile_,
                               ratio     = ratio_,
                               extra     = ("--unc tw-run2/uncs-tw.txt ") * doUncs + extra,
                               nameregion = nameregion_)

    return comm


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
    parser = argparse.ArgumentParser(usage = "python plotterHelper.py [options]", description = "Helper for plotting.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--production','-P', metavar = "prod",      dest = "prod",    required = True)
    parser.add_argument('--year',      '-y', metavar = 'year',      dest = "year",    required = False, default = "2016")
    parser.add_argument('--queue',     '-q', metavar = 'queue',     dest = "queue",   required = False, default = "")
    parser.add_argument('--extraArgs', '-e', metavar = 'extra',     dest = "extra",   required = False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',  dest = "nthreads",required = False, default = 0, type = int)
    parser.add_argument('--select-plot','--sP',action = "append",   dest = "selplot", required = False, default = [])
    parser.add_argument('--pretend',   '-p', action = "store_true", dest = "pretend", required = False, default = False)
    parser.add_argument('--outpath',   '-o', metavar = 'outpath',   dest = "outpath", required = False, default = "./temp/varplots")
    parser.add_argument('--region',    '-r', metavar = 'region',    dest = "region",  required = False, default = "1j1t")
    parser.add_argument('--maxRatioRange', "-R", metavar = 'ratiorange', dest = "ratiorange", required = False, default = "0.8 1.2")
    parser.add_argument('--createSoftLinks', action = "store_true", dest = "createSL", required = False, default = False)
    parser.add_argument('--useFibre',  "-f", action = "store_true", dest = "useFibre", required = False, default = False)
    parser.add_argument('--uncertainties', "-u", action = "store_true", dest = "doUncs", required = False, default = False)
    parser.add_argument('--blind', action = "store_true", dest = "blindornot", required = False, default = False)



    args     = parser.parse_args()
    prod     = args.prod
    year     = args.year
    queue    = args.queue
    extra    = args.extra
    nthreads = args.nthreads
    selplot  = args.selplot
    pretend  = args.pretend
    outpath  = args.outpath
    region   = args.region
    createSL = args.createSL
    useFibre = args.useFibre
    ratiorange = args.ratiorange
    doUncs = args.doUncs
    if args.blindornot: extra += " --xp data"


    if createSL:
        destdir = friendspath + "/" + prod + "/" + str(year)
        SLcommscaff = "ln -s {realdataset} {symlink}"

        #### First, MC
        print "> Creating MC symbolic links..."
        mcsampleslist = os.listdir(mcpath + "/" + str(year))
        for sam in mcsampleslist:
            if not os.path.islink(destdir + "/" + sam):
                os.system(SLcommscaff.format(realdataset = mcpath + "/" + str(year) + "/" + sam,
                                             symlink = destdir + "/" + sam))
        #sys.exit()

        #### Also, the ones from
        print "> Creating MC divisions symbolic links..."
        mcsampleslist = os.listdir(mcpathdiv + "/ttbar/" + str(year))
        for sam in mcsampleslist:
            if not os.path.islink(destdir + "/" + sam):
                os.system(SLcommscaff.format(realdataset = mcpathdiv + "/ttbar/" + str(year) + "/" + sam,
                                             symlink = destdir + "/" + sam))
        #if int(year) == 2016:
            #mcsampleslist = os.listdir(mcpathdiv + "/tw_incl/" + str(year))
            #for sam in mcsampleslist:
                #if not os.path.islink(destdir + "/" + sam):
                    #os.system(SLcommscaff.format(realdataset = mcpathdiv + "/tw_incl/" + str(year) + "/" + sam,
                                                #symlink = destdir + "/" + sam))

        #### Later, data
        print "> Creating data symbolic links..."
        datasampleslist = os.listdir(datapath + "/" + str(year))
        for sam in datasampleslist:
            isData = any(ext in sam for ext in datasamples)
            if not os.path.islink(destdir + "/" + sam) and isData:
                os.system(SLcommscaff.format(realdataset = datapath + "/" + str(year) + "/" + sam,
                                             symlink = destdir + "/" + sam))

        print "> Finished!"
    elif queue != "":
        print "> Plotting jobs will be sent to the cluster."
        if year == "all":
            print "   - All three years and the combination will be plotted."
            cont = False
            if   pretend:
                cont = True
            elif confirm("Four jobs per requested region will be sent to queue {q} with {j} requested threads to plot in each year and in the combination {pls}. Do you want to continue?".format(q = queue, j = nthreads, pls = "all the plots" if not len(selplot) else " and ".join(selplot))):
                cont = True

            if cont:
                for y in ["2016", "2017", "2018", "run2"]:
                    GeneralExecutioner( (prod, y, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs) )
        else:
            cont = False
            if   pretend:
                cont = True
            elif confirm("One job per requested region will be sent to queue {q} with {j} requested threads to plot in year {y} {pls}. Do you want to continue?".format(q = queue, j = nthreads, y = year, pls = "all the plots" if not len(selplot) else " and ".join(selplot))):
                cont = True

            if cont:
                GeneralExecutioner( (prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs) )
    else:
        print "> Local execution chosen."
        if year == "all":
            print "   - All three years and the combination will be plotted."
            for y in ["2016", "2017", "2018", "run2"]:
                GeneralExecutioner( (prod, y, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs) )
        else:
            GeneralExecutioner( (prod, year, nthreads, outpath, selplot, region, ratiorange, queue, extra, pretend, useFibre, doUncs) )
