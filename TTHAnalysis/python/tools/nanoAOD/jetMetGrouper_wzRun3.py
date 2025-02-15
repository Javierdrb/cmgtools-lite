import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# group jec components 
# taken from https://docs.google.com/spreadsheets/d/1Feuj1n0MdotcPq19Mht7SUIgvkXkA4hiB0BxEuBShLw/edit?ouid=111820255692530107608&usp=sheets_home&ths=true

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class jetmetGrouper(Module):
    def __init__(self, groups, jetbranch, metbranch, dumpMore=[], fullyCorr = False):
        self.groups     = groups    
        self.jetbranch = jetbranch
        self.metbranch = metbranch
        self.dumpMore  = dumpMore

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for group in self.groups:
            for sign in ['Up','Down']:
                self.wrappedOutputTree.branch("%s_pt_jes%s%s"%(self.jetbranch,group,sign) , "F", lenVar="n%s"%self.jetbranch)
                self.wrappedOutputTree.branch("%s_pt_jes%s%s"%(self.metbranch,group,sign) , "F")
                self.wrappedOutputTree.branch("%s_phi_jes%s%s"%(self.metbranch,group,sign) , "F")
        for br in self.dumpMore:
            self.wrappedOutputTree.branch(**br)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):

        """Nominal variables"""
        jets = Collection(event, '%s'%self.jetbranch)
        met = Object(event, self.metbranch)
        metPt  = getattr(met, "pt")
        metPhi = getattr(met, "phi")
        metPx  = metPt*math.cos(metPhi)
        metPy  = metPt*math.sin(metPhi)


        for group in self.groups:
            for sign in ['Up','Down']:
                jetVar    = []
                metPxVar  = metPx
                metPyVar  = metPy
                for j in jets: 
                    thePt  = getattr(j, "pt_nom", "pt")
                    thePhi = getattr(j, "phi") 
                    jetVar.append(0)
                    for comp in self.groups[group]:
                        jetVar[-1] = (jetVar[-1]**2 + (getattr(j,"pt_jes"+ comp + sign)-thePt)**2)**0.5
                    
                    metPxVar    = metPxVar - (1 if sign == 'Up' else -1) * jetVar[-1] * math.cos(thePhi)
                    metPyVar    = metPyVar - (1 if sign == 'Up' else -1) * jetVar[-1] * math.sin(thePhi)
                    jetVar[-1]  = thePt + (1 if sign == 'Up' else -1) * jetVar[-1]
                self.wrappedOutputTree.fillBranch("%s_pt_jes%s%s"%(self.jetbranch,group,sign),  jetVar       )
                self.wrappedOutputTree.fillBranch("%s_pt_jes%s%s"%(self.metbranch,group,sign),  (metPxVar**2 + metPyVar**2)**0.5)
                
                self.wrappedOutputTree.fillBranch("%s_phi_jes%s%s"%(self.metbranch,group,sign), math.atan2(metPyVar,  metPxVar))
        for br in self.dumpMore:
            self.wrappedOutputTree.fillBranch(br['name'], getattr(event, br['name']))

        return True

moreVars = [
    {'name' : 'Jet_pt_nom'           ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_pt_jerUp'         ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_pt_jerDown'       ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    #{'name' : 'Jet_pt_jesHEMIssueUp',       'rootBranchType' : 'F','lenVar': 'nJet'},
    #{'name' : 'Jet_pt_jesHEMIssueDown',     'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_pt_jesTotalUp',          'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_pt_jesTotalDown',        'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_mass_nom'         ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_mass_jerUp'       ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_mass_jerDown'     ,      'rootBranchType' : 'F','lenVar': 'nJet'},
    #{'name' : 'Jet_mass_jesHEMIssueUp',     'rootBranchType' : 'F','lenVar': 'nJet'},
    #{'name' : 'Jet_mass_jesHEMIssueDown',   'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_mass_jesTotalUp',        'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'Jet_mass_jesTotalDown',      'rootBranchType' : 'F','lenVar': 'nJet'},
    {'name' : 'PuppiMET_T1_pt'               ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_jerUp'         ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_jerDown'       ,   'rootBranchType' : 'F'},
    #{'name' : 'PuppiMET_T1_pt_jesHEMIssueUp',    'rootBranchType' : 'F'},
    #{'name' : 'PuppiMET_T1_pt_jesHEMIssueDown',  'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_jesTotalUp',       'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_jesTotalDown',     'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_unclustEnUp'   ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_pt_unclustEnDown' ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi'              ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_jerUp'        ,   'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_jerDown'      ,   'rootBranchType' : 'F'},
    #{'name' : 'PuppiMET_T1_phi_jesHEMIssueUp'  , 'rootBranchType' : 'F'},
    #{'name' : 'PuppiMET_T1_phi_jesHEMIssueDown', 'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_jesTotalUp',      'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_jesTotalDown',    'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_unclustEnUp',     'rootBranchType' : 'F'},
    {'name' : 'PuppiMET_T1_phi_unclustEnDown',   'rootBranchType' : 'F'},
]

for jer in list(range(6)):
    for var in ['Up','Down']:
        moreVars.extend( [
            {'name' : 'Jet_pt_jer%s%s'%(jer,var) ,   'rootBranchType' : 'F','lenVar': 'nJet'},
            {'name' : 'Jet_mass_jer%s%s'%(jer,var) , 'rootBranchType' : 'F','lenVar': 'nJet'},
            {'name' : 'PuppiMET_T1_pt_jer%s%s'%(jer,var) ,'rootBranchType' : 'F'},
            {'name' : 'PuppiMET_T1_phi_jer%s%s'%(jer,var),'rootBranchType' : 'F'},
        ])


#moreVars = [
#    {'name' : 'Jet_pt_nom'            ,'rootBranchType' : 'F','lenVar': 'nJet'},
#    {'name' : 'PuppiMET_T1_pt_jerUp'          ,'rootBranchType' : 'F'},
#    {'name' : 'PuppiMET_T1_pt'                ,'rootBranchType' : 'F'},
#    {'name' : 'PuppiMET_T1_pt_unclustEnUp'    ,'rootBranchType' : 'F'},
#    {'name' : 'PuppiMET_T1_pt_unclustEnDown'  ,'rootBranchType' : 'F'},
#    {'name' : 'PuppiMET_T1_phi_unclustEnUp'   ,'rootBranchType' : 'F'},
#    {'name' : 'PuppiMET_T1_phi_unclustEnDown' ,'rootBranchType' : 'F'},
#]

#groups = {'Total': [
#    'PileUpPtHF', 
#    'RelativeJERHF', 
#    'RelativePtHF', 
#    'RelativeJEREC1', 
#    'RelativePtEC1', 
#    'RelativeStatEC',
#    'FlavorQCD',
#    'RelativeSample',
#    'PileUpPtEC2',
#    'RelativeStatHF',
#    'RelativeBal',
#    'AbsoluteStat', 
#    'RelativeStatFSR', 
#    'TimePtEta',
#    'PileUpPtBB', 
#    'PileUpPtEC1', 
#    'RelativePtBB',
#    'RelativeJEREC2', 
#    'RelativePtEC2', 
#    'AbsoluteMPFBias', 
#    'AbsoluteScale', 
#    'Fragmentation', 
#    'PileUpDataMC',
#    'PileUpPtRef', 
#    'RelativeFSR', 
#    'SinglePionECAL', 
#    'SinglePionHCAL'
#],
#}
groups = {'HF'                 : ['PileUpPtHF', 'RelativeJERHF', 'RelativePtHF'],
          'BBEC1_year'         : ['RelativeJEREC1', 'RelativePtEC1', 'RelativeStatEC'],
          'FlavorQCD'          : ['FlavorQCD'],
          'RelativeSample_year': ['RelativeSample'],
          'EC2'                : ['PileUpPtEC2'],
          'HF_year'            : ['RelativeStatHF'],
          'RelativeBal'        : ['RelativeBal'],
          'Absolute_year'      : ['AbsoluteStat', 'RelativeStatFSR', 'TimePtEta'],
          'BBEC1'              : ['PileUpPtBB', 'PileUpPtEC1', 'RelativePtBB'],
          'EC2_year'           : ['RelativeJEREC2', 'RelativePtEC2'],
          'Absolute'           : ['AbsoluteMPFBias', 'AbsoluteScale', 'Fragmentation', 'PileUpDataMC',
                                  'PileUpPtRef', 'RelativeFSR', 'SinglePionECAL', 'SinglePionHCAL'],
}

jetMetCorrelate2022 = lambda  : jetmetGrouper( groups, "Jet", "PuppiMET_T1", dumpMore=moreVars, fullyCorr = True)
