import os, sys, enum, argparse
from multiprocessing import Pool
import warnings as wr
import ROOT as r
r.PyConfig.IgnoreCommandLineOptions = True
r.gROOT.SetBatch(True)

friendspath  = "/pool/phedexrw/userstorage/vrbouza/proyectos/tw_run2/productions"
logpath      = friendspath + "/{p}/{y}/logs/cards_inclusive"

lumidict     = {2016 : 36.33, 
                2017 : 41.53,
                2018 : 59.74}
#lumidict     = {2016 : 18.165, 
#                2017 : 20.765,
#                2018 : 29.87}

#friendsscaff = "--FDs {P}/0_lumijson --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/5_mvas --Fs {P}/6_hemissue"
friendsscaff = "--FDs {P}/0_lumijson --Fs {P}/1_lepmerge_roch --Fs {P}/2_cleaning --Fs {P}/3_varstrigger --FMCs {P}/4_scalefactors --Fs {P}/5_mvas"

slurmscaff   = "sbatch -c {nth} -p {queue} -J {jobname} -e {logpath}/log.%j.%x.err -o {logpath}/log.%j.%x.out --wrap '{command}'"

listofforcedshape = "btagging_2016,btagging_2017,btagging_2018,btagging_corr,elecidsf,elecrecosf,fsr,isr_ttbar,isr_tw,jer_2016,jer_2017,jer_2018,jes_Absolute,jes_Absolute_2016,jes_Absolute_2017,jes_Absolute_2018,jes_BBEC1,jes_BBEC1_2016,jes_BBEC1_2017,jes_BBEC1_2018,jes_EC2,jes_EC2_2016,jes_EC2_2017,jes_EC2_2018,jes_FlavorQCD,jes_HF,jes_HF_2016,jes_HF_2017,jes_HF_2018,jes_RelativeBal,jes_RelativeSample_2016,jes_RelativeSample_2017,jes_RelativeSample_2018,lumi_2016,lumi_2017,lumi_2018,lumi_corr,lumi_corr1718,mistagging_2016,mistagging_2017,mistagging_2018,mistagging_corr,mtop,muonen_2016,muonen_2017,muonen_2018,muonidsf_stat_2016,muonidsf_stat_2017,muonidsf_stat_2018,muonidsf_syst,muonisosf_stat_2016,muonisosf_stat_2017,muonisosf_stat_2018,muonisosf_syst,pdfhessian,pileup,prefiring_2016,prefiring_2017,topptrew,triggereff_2016,triggereff_2017,triggereff_2018,ttbar_scales,tw_scales,ds,colour_rec_erdon,colour_rec_cr1,colour_rec_cr2"
#For 2016
#listofforcedshape = "btagging_2016,btagging_corr,elecidsf,elecrecosf,fsr,isr_ttbar,isr_tw,jer_2016,jes_Absolute,jes_Absolute_2016,jes_BBEC1,jes_BBEC1_2016,jes_EC2,jes_EC2_2016,jes_FlavorQCD,jes_HF,jes_HF_2016,jes_RelativeBal,jes_RelativeSample_2016,lumi_2016,lumi_corr,mistagging_2016,mistagging_corr,mtop,muonen_2016,muonidsf_stat_2016,muonidsf_syst,muonisosf_stat_2016,muonisosf_syst,pdfhessian,pileup,prefiring_2016,topptrew,triggereff_2016,ttbar_scales,tw_scales,ds,colour_rec_erdon,colour_rec_cr1,colour_rec_cr2"

# ds: forzada para asegurarnos la asimetria

#commandscaff = '''python makeShapeCardsNew.py --tree NanoAOD {mcafile} {cutsfile} "{variable}" "{bins}" {samplespaths} {friends} --od {outpath} -l {lumi} {nth} -f -L tw-run2/functions_tw.cc --neg --threshold 0.01 -W "MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * PrefireWeight" --year {year} {asimovornot} {uncs} {extra} --AP --storeAll --notMinimumFill --notVarsChanges'''

commandscaff = '''python makeShapeCards_TopRun2.py --tree NanoAOD {mcafile} {cutsfile} "{variable}" "{bins}" {samplespaths} {friends} --od {outpath} -l {lumi} {nth} -f -L tw-run2/functions_tw.cc --neg --threshold 0.01 -W "MuonIDSF * MuonISOSF * ElecIDSF * ElecRECOSF * TrigSF * puWeight * bTagWeight * PrefireWeight" --year {year} {asimovornot} {uncs} {extra} --AP --storeAll'''



def GeneralExecutioner(task):
    prod, year, variable, bines, asimov, nthreads, outpath, region, queue, extra, pretend, useFibre, noUnc = task

    if not os.path.isdir(outpath + "/" + str(year)) and not pretend:
        os.system("mkdir -p " + outpath + "/" + str(year))

    if queue != "":
        if not os.path.isdir(logpath.format(y = year, p = prod)) and not pretend:
            os.system("mkdir -p " + logpath.format(y = year, p = prod))

        jobname_   = "Card_{r}_{y}".format(y = year, r = region)
        submitcomm = slurmscaff.format(nth  = nthreads,
                                    queue   = queue,
                                    jobname = jobname_,
                                    logpath = logpath.format(y = year, p = prod),
                                    command = CardsCommand(prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra))
        print "Command:", submitcomm
        if not pretend: os.system(submitcomm)
    else:
        execcomm = CardsCommand(prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra)
        print "Command:", execcomm
        if not pretend: os.system(execcomm)


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


def CardsCommand(prod, year, var, bines, isAsimov, nthreads, outpath, region, noUnc, useFibre, extra):
    mcafile_   = "tw-run2/mca-tw.txt"
    cutsfile_  = "tw-run2/cuts-tw-{reg}.txt".format( reg = region)

    samplespaths_ = "-P " + friendspath + "/" + prod + ("/" + year) * (year != "run2")
    if useFibre: samplespaths_ = samplespaths_.replace("phedexrw", "phedex").replace("cienciasrw", "ciencias")

#    nth_       = "" if nthreads == 0 else ("--split-factor=-1 -j " + str(nthreads))
    nth_       = "" if nthreads == 0 else ("--split-factor=0 -j " + str(nthreads))
    friends_   = friendsscaff
    outpath_   = outpath + "/" + year + "/" + region

    extra_ = extra + " --forceShape {l}".format(l = listofforcedshape)

    comm = commandscaff.format(outpath      = outpath_,
                               friends      = friends_,
                               samplespaths = samplespaths_,
                               lumi      = lumidict[int(year)] if year != "run2" else str(lumidict[2016]) + "," + str(lumidict[2017]) + "," + str(lumidict[2018]),
                               variable  = var,
                               bins      = bines,
                               nth       = nth_,
                               year      = year if year != "run2" else "2016,2017,2018",
                               asimovornot = "--asimov s+b" if isAsimov else "",
                               mcafile   = mcafile_,
                               cutsfile  = cutsfile_,
                               uncs      = "--unc tw-run2/uncs-tw_{r}mva.txt --amc".format(r = region) if not noUnc else "--amc",
                               #uncs      = "--unc tw-run2/uncs-tw_{r}mvaTodoSmoothMenosABSB-BEC1.txt --amc".format(r = region) if not noUnc else "--amc",
                               #uncs      = "--unc tw-run2/uncs-tw.txt --amc" if not noUnc else "--amc",
                               #uncs      = "--unc tw-run2/uncs-tw_nadasuavizado.txt --amc" if not noUnc else "--amc",
                               extra     = extra_)

    return comm


def ExecuteOrSubmitTask(tsk):
    prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra, pretend, queue = tsk

    if not os.path.isdir(outpath + "/" + year + "/" + region):
        os.system("mkdir -p " + outpath + "/" + year + "/" + region)

    if queue == "":
        thecomm = CardsCommand(prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra)
        print "Command: " + thecomm

        if not pretend:
            os.system(thecomm)

    else:
        if not os.path.isdir(logpath.format(p = prod, y = yr)):
            os.system("mkdir -p " + logpath.format(p = prod, y = yr))

        thecomm = slurmscaff.format(nth     = nthreads,
                                    queue   = queue,
                                    jobname = "CMGTcards_" + year + "_" + (variable.replace("(", "").replace(")", "") if not "min" in variable else "Jet2_Pt") + "_" + region,
                                    logpath = logpath.format(p = prod, y = yr),
                                    command = CardsCommand(prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra))

        print "Command: " + thecomm

        if not pretend:
            os.system(thecomm)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--production','-P', metavar = "prod",       dest = "prod",     required = True)
    parser.add_argument('--year',      '-y', metavar = 'year',       dest = "year",     required = False, default = "2016")
    parser.add_argument('--queue',     '-q', metavar = 'queue',      dest = "queue",    required = False, default = "")
    parser.add_argument('--extraArgs', '-e', metavar = 'extra',      dest = "extra",    required = False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',   dest = "nthreads", required = False, default = 0, type = int)
    parser.add_argument('--pretend',   '-p', action  = "store_true", dest = "pretend",  required = False, default = False)
    parser.add_argument('--outpath',   '-o', metavar = 'outpath',    dest = "outpath",  required = False, default = "./temp/cards")
    parser.add_argument('--region',    '-r', metavar = 'region',     dest = "region",   required = False, default = "1j1t")
    parser.add_argument('--nounc',     '-nu',action  = "store_true", dest = "nounc",    required = False, default = False)
    parser.add_argument('--variable',  '-v', metavar = 'variable',   dest = "variable", required = False, default = "getBDtW(tmvaBDT_1j1b)")
    parser.add_argument('--bines',     '-b', metavar = 'bines',      dest = "bines",    required = False, default = "[0.5,1.5,2.5,3.5,4.5,5.5, 6.5, 7.5, 8.5, 9.5, 10.5]")
    parser.add_argument('--asimov',    '-a', action  = "store_true", dest = "asimov",   required = False, default = False)
    parser.add_argument('--useFibre',  '-f', action  = "store_true", dest = "useFibre", required = False, default = False)


    args     = parser.parse_args()
    prod     = args.prod
    year     = args.year
    queue    = args.queue
    extra    = args.extra
    nthreads = args.nthreads
    pretend  = args.pretend
    outpath  = args.outpath
    region   = args.region
    noUnc    = args.nounc
    variable = args.variable
    bines    = args.bines
    asimov   = args.asimov
    useFibre = args.useFibre

    #print CardsCommand(prod, year, variable, bines, asimov, nthreads, outpath, region, noUnc, useFibre, extra)

    theregs  = ["1j1t", "2j1t", "2j2t"]
    thevars  = ["getBDtW20bins{year}(tmvaBDT_1j1b)", "getBDtWOther12bins{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
    #thevars  = ["getBDtW20binsDYtrain{year}(tmvaBDT_1j1b)", "getBDtWOther12binsDYtrain{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
    thebins  = ["[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5]",
                "[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]",
                "[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.]"]              
#    thebins  = ["[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]",
#                "[0.5,1.5,2.5,3.5,4.5,5.5,6.5]",
#                "[30.,50.,70.,90.,110.,130.,150.,170.,190.]"]
    theyears = ["2016", "2017", "2018", "run2"]
    tasks    = []
    
    ########----Binning test-----#######
#    theregs  = ["1j1t", "2j1t", "2j2t"]
#    thevars  = ["theBDT1j1t50Bins{year}(tmvaBDT_1j1b)", "theBDT2j1t50Bins{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
#    #thevars  = ["getBDtW20binsDYtrain{year}(tmvaBDT_1j1b)", "getBDtWOther12binsDYtrain{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
#    thebins  = ["[ 0.5,  1.5,  2.5,  3.5,  4.5,  5.5,  6.5,  7.5,  8.5,  9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5, 33.5, 34.5, 35.5, 36.5, 37.5, 38.5, 39.5, 40.5, 41.5, 42.5, 43.5, 44.5, 45.5, 46.5, 47.5, 48.5, 49.5, 50.5]",
#                "[ 0.5,  1.5,  2.5,  3.5,  4.5,  5.5,  6.5,  7.5,  8.5,  9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5, 33.5, 34.5, 35.5, 36.5, 37.5, 38.5, 39.5, 40.5, 41.5, 42.5, 43.5, 44.5, 45.5, 46.5, 47.5, 48.5, 49.5, 50.5]",
#                "[ 30.        ,  32.91666667,  35.83333333,  38.75      ,41.66666667,  44.58333333,  47.5       ,  50.41666667,53.33333333,  56.25      ,  59.16666667,  62.08333333,65.        ,  67.91666667,  70.83333333,  73.75      ,76.66666667,  79.58333333,  82.5       ,  85.41666667,88.33333333,  91.25      ,  94.16666667,  97.08333333, 100.      ,110.,120.,130.,140.,150.,160.,170.,180.,190.]"]
#    theyears = ["2016", "2017", "2018", "run2"]
#    tasks    = []
    ########----Binning test-----#######
#    theregs  = ["1j1t", "2j1t", "2j2t"]
#    thevars  = ["theBDTJetsFwd1j1t{year}(tmvaBDT_1j1b)", "theBDTJetsFwd2j1t{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
#    #thevars  = ["getBDtW20binsDYtrain{year}(tmvaBDT_1j1b)", "getBDtWOther12binsDYtrain{year}(tmvaBDT_2j1b)", "min(max(Jet2_Pt, 30.), 189.)"]
#    thebins  = ["[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5]",
#                "[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5]",
#                "[30.,40.,50.,60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.]"]
#    theyears = ["2016", "2017", "2018", "run2"]
#    tasks    = []
    ########----Binning test-----#######
    if variable.lower() != "all":
        if "," in variable:
            thevars = variable.split(",")
        else:
            thevars = [ variable ]

    if region.lower() != "all":
        if "," in region:
            theregs = region.split(",")
        else:
            theregs = [ region ]

    if year.lower() != "all":
        if "," in year:
            theyears = year.split(",")
        else:
            theyears = [ year ]

    for yr in theyears:
        for i in range(len(theregs)):
            if "{year}" in thevars[i] and yr != "run2":
                tasks.append( (prod, yr, thevars[i].format(year = yr), thebins[i], asimov, nthreads, outpath, theregs[i], noUnc, useFibre, extra, pretend, queue) )
            elif "{year}" in thevars[i] and yr == "run2":
                tasks.append( (prod, yr, thevars[i].format(year = ""), thebins[i], asimov, nthreads, outpath, theregs[i], noUnc, useFibre, extra, pretend, queue) )
            else:
                tasks.append( (prod, yr, thevars[i], thebins[i], asimov, nthreads, outpath, theregs[i], noUnc, useFibre, extra, pretend, queue) )

    #print tasks
    calculate = True
    for task in tasks:
        print "\nProcessing " + str(task) + "\n"

        if calculate:
            ExecuteOrSubmitTask(task)
