from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

class addExtraLepVarsForLepUncs(Module):
    def __init__(self, label = "corrAll",  muonvars = "mu", 
                 elecdatavars = "elscale", elecmcvars = "elsigma", isMC = True):
        self.label     = label
        self.muonvars  = muonvars
        self.elecdatavars = elecdatavars
        self.elecmcvars   = elecmcvars
        self.isMC      = isMC
        self.branches  = [("LepGood_pt_" + self.label,             "F", "", "nLepGood"),]
        if self.isMC:
            self.branches.append(("LepGood" + self.muonvars + "Up_pt_" + self.muonvars + "Up",              "F", "", "nLepGoodmuUp"))
            self.branches.append(("LepGood" + self.muonvars + "Down_pt_" + self.muonvars + "Down",          "F", "", "nLepGoodmuDown"))
            self.branches.append(("LepGood" + self.elecmcvars + "Up_pt_"   + self.elecmcvars + "Up",        "F", "", "nLepGoodelsigmaUp"))
            self.branches.append(("LepGood" + self.elecmcvars + "Down_pt_" + self.elecmcvars + "Down",      "F", "", "nLepGoodelsigmaDown"))
        else:
            self.branches.append(("LepGood" + self.elecdatavars + "Up_pt_"   + self.elecdatavars + "Up",    "F", "", "nLepGoodelscaleUp"))
            self.branches.append(("LepGood" + self.elecdatavars + "Down_pt_" + self.elecdatavars + "Down",  "F", "", "nLepGoodelscaleDown"))
        return


    # Old interface (CMG)
    def listBranches(self):
        return self.branches[:]


    def __call__(self, event):
        return self.run(event, CMGCollection)


    # New interface (nanoAOD-tools)
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)


    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True


    # Common processing
    def run(self, event, Collection):
        leps  = [l for l in Collection(event, "LepGood")]

        newvals    = []
        newvalsupmu = []
        newvalsdnmu = []
        newvalsupel = []
        newvalsdnel = []
        for lep in leps:
            if abs(lep.pdgId) == 11:
                newvals.append(  lep.pt)
            else:
                newvals.append(  lep.corrected_pt)

        allret = {"LepGood_pt_" + self.label : newvals}

        if self.isMC:
            leps  = [l for l in Collection(event, "LepGoodmuUp")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsupmu.append(lep.pt)
                else:
                    newvalsupmu.append(lep.correctedUp_pt)
            leps  = [l for l in Collection(event, "LepGoodmuDown")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsdnmu.append(lep.pt)
                else:
                    newvalsdnmu.append(lep.correctedDown_pt)

            allret["LepGoodmuUp_pt_muUp"]     = newvalsupmu
            allret["LepGoodmuDown_pt_muDown"] = newvalsdnmu
            
            leps  = [l for l in Collection(event, "LepGoodelsigmaUp")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsupel.append(lep.sigmaUp_pt)
                else:
                    newvalsupel.append(lep.pt)
            leps  = [l for l in Collection(event, "LepGoodelsigmaDown")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsdnel.append(lep.sigmaDown_pt)
                else:
                    newvalsdnel.append(lep.pt)

            allret["LepGood" + self.elecmcvars + "Up_pt_"   + self.elecmcvars + "Up"]   = newvalsupel
            allret["LepGood" + self.elecmcvars + "Down_pt_" + self.elecmcvars + "Down"] = newvalsdnel
        else:
            leps  = [l for l in Collection(event, "LepGoodelscaleUp")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsupel.append(lep.scaleUp_pt)
                else:
                    newvalsupel.append(lep.pt)
            leps  = [l for l in Collection(event, "LepGoodelscaleDown")]
            for lep in leps:
                if abs(lep.pdgId) == 11:
                    newvalsdnel.append(lep.scaleDown_pt)
                else:
                    newvalsdnel.append(lep.pt)

            allret["LepGood" + self.elecdatavars + "Up_pt_"   + self.elecdatavars + "Up"]   = newvalsupel
            allret["LepGood" + self.elecdatavars + "Down_pt_" + self.elecdatavars + "Down"] = newvalsdnel

        return allret
