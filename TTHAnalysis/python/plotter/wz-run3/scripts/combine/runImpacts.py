import argparse
#import functions as f  

def add_parsing_options():
  parser = argparse.ArgumentParser()
  parser.add_argument('--outpath', '-o', dest = "outpath", default = "fits",
                     help = "Folder where to store the combined card")
  parser.add_argument('--workspace', dest = "WS")
  parser.add_argument('--POIs', action = "append",dest = "POIs") 
  parser.add_argument('--signalPOI', dest = 'signalPOI')
  parser.add_argument('--cluster','-c', dest = "cluster") 
  parser.add_argument('--ncores','-j', dest = "ncores")
  parser.add_argument('--queue','-q', dest = "queue")
  return parser.parse_args()


if __name__ == "__main__":
  options = add_parsing_options()
  outpath = options.outpath
  WS = options.WS
  POIs = options.POIs
  signalPOI = options.signalPOI
  cluster = options.cluster
  queue = options.queue
  ncores = options.ncores
  blind = True    
      
  doBlind = "" if not blind else "-t -1 --setParameters %s"%(",".join(["%s=1"%poi for poi in POIs]))
  submitCluster = "--job-mode slurm --sub-opts='-p %s'"%queue if cluster == "slurm" else ""

  # Do the initial fit
  print("\n---> Command to perform the initial fit\n")
  initialFit_cmd = "cd %s; combineTool.py -M Impacts -m 125 -d %s --doInitialFit %s --redefineSignalPOI %s --X-rtd MINIMIZER_MaxCalls=99999999999 --maxFailedSteps 500 --X-rtd MINIMIZER_analytic --setRobustFitTolerance 0.05 --cminPreScan --cminDefaultMinimizerStrategy 0; cd - "%(outpath, WS, doBlind, signalPOI)
  print(initialFit_cmd)
  # Do the sequential fits
  print("\n---> Command to perform the sequential fits. PLEASE CHECK THE ENVIRONMENT IN WHICH THIS COMMAND WILL RUN (local or cluster)\n")
  doFits_cmd = initialFit_cmd.replace("doInitialFit", "doFits --parallel %s "%(ncores))
  if submitCluster != "": doFits_cmd += " %s"%submitCluster
  print(doFits_cmd)

  print("\n---> Produce the impacts\n")
  # Run the impacts
  impacts_cmd =  "cd %s; combineTool.py -M Impacts -m 125 -o impacts.json --redefineSignalPOI %s %s -d %s; cd -"%(outpath, signalPOI, doBlind, WS)
  print(impacts_cmd)
  print("\n---> Plot the impacts\n")

  # plot the impacts
  plotImpacts_cmd = "cd %s; plotImpacts.py -i impacts.json -o impacts;cd -"%(outpath)
  print(plotImpacts_cmd)
