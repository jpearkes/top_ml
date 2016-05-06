# Jannicke Pearkes
# Test script for looking at different attributes of DAODs 

#Set up ROOT and RootCore:
import ROOT
from pprint import pprint
import math
import numpy as np
import itertools as IT
from ROOT import gROOT

def traverse_daods():
  # Constants
  GeV = 1000.
  max_size = 0
  max_index = 0
  count = 0
  eta_range = (-1, 1)
  phi_range = (-1, 1)
  eta_block_size = 0.1
  phi_block_size = 0.1
  n_bins_eta = int((eta_range[1]-eta_range[0])/eta_block_size)
  n_bins_phi = int((phi_range[1]-phi_range[0])/phi_block_size)

  gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");

  # Set up the input files:
  #tt 400 example
  #fileName = "/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.07896478._000001.pool.root.1"
  # tt 5000
  fileName = "/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.07618499._000005.pool.root.1"
  # dijet 
  #fileName = "/data/wfedorko/mc15_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618436_00/DAOD_EXOT7.07618436._000005.pool.root.1"
  treeName = "CollectionTree" # default when making transient tree anyway

  f = ROOT.TFile.Open(fileName)
  t = ROOT.xAOD.MakeTransientTree(f, treeName)

  # Setup the ROOT output file
  f_out = ROOT.TFile("output"+".root", "recreate")

  # #print( "Number of input events: %s" % t.GetEntries() )

  for entry in xrange(1):#t.GetEntries()): 
    x=[]
    t.GetEntry(entry)
    print( "Processing run #%i, event #%i" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber() ) )
    print( "Number of jets: %i" %  t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size() )
    for i in xrange(1):#t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
      j = t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i)
      print("Jet"+str(i))
      print("Jet Pt = %g, Jet Eta = %g, Jet Phi = %g" % (j.pt(),j.eta(),j.phi()))
      constituents = j.getConstituents()
      for index in xrange(constituents.size()):
        constit = constituents[index]
        print( "pt = %g, eta = %g, phi = %g" % (constit.pt(), constit.eta(), constit.phi()))
        x.append([constit.eta()-j.eta(), constit.phi()-j.phi(),constit.pt()])
      x = j.getAssociatedObject() 
      print(x)
      #pprint(dir(j))  
      
      #print(x)
      #x = np.array(x)
      
      f_out.Write()
      f_out.Close()
      f.Close()  
  ROOT.xAOD.ClearTransientTrees() 
    # for c in j.getConstituents():
    #   print(c.pt() , c.eta())
    #   # access the raw underlying cluster :
    #   rawCluster = c.rawConstituent()
  # BE CAREFULL if you use a EMTopo Jet rather than LCTopo jet
  # in this case c.pt() != rawCluster.pt() : always use the
  # kinematics from c, not from  rawCluster
  #----------
  # for entry in xrange(1):#t.GetEntries()): 
  #   t.GetEntry(entry)    
  #   for i in xrange(1): #t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
  #     x = []
  #     el = t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i)
  #     jet_eta = el.eta()
  #     jet_phi = el.phi()
  #     print("Jet")
  #     print( "pt = %g, eta = %g, phi = %g, m = %g, e = %g" % (el.pt(), el.eta(), el.phi(), el.m(),el.e()))
  #     print("Corressponding topoclusters")
  #     for j in xrange(t.CaloCalTopoClusters.size()):
  #       topo = t.CaloCalTopoClusters.at(j)
  #       topo_phi = topo.phi() 
  #       topo_eta = topo.eta()
  #       delta_phi = abs(topo_phi-jet_phi)
  #       delta_eta = abs(topo_eta-jet_eta)
  #       delta_r = math.sqrt(delta_phi**2+delta_eta**2)
  #       if(delta_r<=1):
  #         print( "pt = %g, eta = %g, phi = %g" % (topo.pt(), topo.eta(), topo.phi()))
  #         x.append([topo_eta-jet_eta, topo_phi-jet_phi,topo.pt()])
  #     print x
  #     h_calo_towers = ROOT.TH2F('calo_towers','calo_towers',
  #                                  n_bins_phi, phi_range[0], phi_range[1],
  #                                  n_bins_eta, eta_range[0], eta_range[1])
  #     h_calo_towers.GetXaxis().SetTitle(" Phi  [rad] ")
  #     h_calo_towers.GetYaxis().SetTitle(" Eta   ")
  #     [h_calo_towers.Fill(x[i][1],x[i][2],x[i][0]) for i in xrange(30)] # before transformations
  #     f_out.Write()
  #     f_out.Close()
  #     f.Close() # see if this does anything... 
  # # add to (xby3) numpy array 
      
  '''

  # Something to find the topoclusters that each jet is made of 
  #print("constituent links"+str(el.constituentLinks)
  #print(el.constituentLinks().size())
  #for j in xrange(el.constituentLinks().size()):
  #ele = el.constituentLinks.at(i)
  #print(ele)


  #tree = file.Get('tree')
   
  listOfBranches = t.GetListOfBranches()
  numBranches = listOfBranches.GetEntries()

  for br in range (0,numBranches):
  keyname = (listOfBranches.At(br)).GetName()
  thetype = (listOfBranches.At(br)).GetClassName()
  print ("{0:>30} : {1}".format(keyname, thetype))

  t.GetEntry(0) # get first event
  reg = ROOT.SG.AuxTypeRegistry.instance()

  # getBranch


  object = t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(0)
  auxids = list(object.getAuxIDs())
  l = dir(object)
  pprint(l)
  print (object.numConstituents())
  c = object.getConstituents()
  print(c)
  l = dir(c)
  pprint(l)


  for id in auxids:
  name = reg.getName(id)  
  if name == "LCTopo":
  print name

  '''

if __name__ == '__main__':
    traverse_daods()