# Jannicke Pearkes
# Test code for looking at the samples 
# Plot, debug, loop, extract modes 

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

    def sort_topos(topos):
      topo_list = [None]*(topos.size())
      #for topo in xrange(topos.size()):
      #  topo_list[topo]=topos.at(topo)
      topo_list = [topos.at(topo) for topo in xrange(topos.size())]
      topo_list.sort(key=lambda topo: topo.pt(), reverse=True)
      return topo_list

    gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");  
    # Set up the input files:
    #tt 400 example
    #file_name = "/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.07896478._000001.pool.root.1"
    #output_file_name = "zprime400_tt"
    # tt 5000
    file_name = "/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.07618499._000005.pool.root.1"
    output_file_name = "zprime5000_tt"
    # dijet 
    #file_name = "/data/wfedorko/mc15_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618436_00/DAOD_EXOT7.07618436._000001.pool.root.1"
    #output_file_name = "dijet"

    treeName = "CollectionTree" # default when making transient tree anyway
    f = ROOT.TFile.Open(file_name)
    t = ROOT.xAOD.MakeTransientTree(f, treeName)    
    # Setup the output file
    f_out = ROOT.TFile(output_file_name+".root", "recreate")   

    eta_range = (-3, 3)
    phi_range = (-math.pi, math.pi)
    eta_block_size = 0.1
    phi_block_size = 0.1
    n_bins_eta = int((eta_range[1]-eta_range[0])/eta_block_size)
    n_bins_phi = int((phi_range[1]-phi_range[0])/phi_block_size)  

    # Set up histograms 
    # File wide histograms
    h_num_jets = ROOT.TH1F('num_jets','num_jets',30,0.0,30.0)
    h_num_jets.GetXaxis().SetTitle("Number of jets for each event") 

    # Jet histograms
    h_jet_pt = ROOT.TH1F('jet_pt','jet_pt',300,0.0,5.0e3)
    h_jet_pt.GetXaxis().SetTitle("P_t of all jets in all events [GeV]") 

    h_jet_eta = ROOT.TH1F('jet_eta','jet_eta',n_bins_eta,eta_range[0],eta_range[1])
    h_jet_eta.GetXaxis().SetTitle("Eta of all jets in all events") 

    h_jet_phi = ROOT.TH1F('jet_phi','jet_phi',n_bins_phi,phi_range[0],phi_range[1])
    h_jet_phi.GetXaxis().SetTitle("Phi of all jets in all events [rad]") 
    
    h_jet_frac_pt = ROOT.TH1F('jet_frac_pt','jet_frac_pt',100,0,1)
    h_jet_frac_pt.GetXaxis().SetTitle("Fractional pt of jets")

    h_num_topos = ROOT.TH1F('num_topos','num_topos',100,0.0,100)
    h_num_topos.GetXaxis().SetTitle("Number of topocluster per jet ") 

    h_jet_frac_i = [ROOT.TH1F('jet_frac'+str(i),'jet_frac'+str(i),100,0,1) for i in xrange(6)]
    h_jet_pt_i = [ROOT.TH1F('jet_pt'+str(i),'jet_pt'+str(i),100,0.0,5e3) for i in xrange(6)]
    h_jet_phi_i = [ROOT.TH1F('jet_phi'+str(i),'jet_phi'+str(i),n_bins_phi,phi_range[0],phi_range[1]) for i in xrange(6)]
    h_jet_eta_i = [ROOT.TH1F('jet_eta'+str(i),'jet_eta'+str(i),n_bins_eta,eta_range[0],eta_range[1]) for i in xrange(6)]

    # Topo histograms
    h_topo_pt = ROOT.TH1F('topo_pt','topo_pt',100,-10.0,300000.0)
    h_topo_pt.GetXaxis().SetTitle("p_t of topoclusters [MeV]")  

    h_topo_eta = ROOT.TH1F('topo_eta','topo_eta',n_bins_eta,eta_range[0],eta_range[1])
    h_topo_eta.GetXaxis().SetTitle("eta of topoclusters")  

    h_topo_phi = ROOT.TH1F('topo_phi','topo_phi',n_bins_phi,phi_range[0],phi_range[1])
    h_topo_phi.GetXaxis().SetTitle("phi of topoclusters [rad]")  

    h_topo_frac_pt = ROOT.TH1F('topo_frac_pt','topo_frac_pt',100,0,1)
    h_topo_frac_pt.GetXaxis().SetTitle("fractional pt of topoclusters") 

    num_topos_to_plot = 21
    h_topo_frac_i = [ROOT.TH1F('topo_frac'+str(i),'topo_frac'+str(i),100,0,1) for i in xrange(num_topos_to_plot)]
    h_topo_pt_i = [ROOT.TH1F('topo_pt'+str(i),'topo_pt'+str(i),100,0.0,5e3) for i in xrange(num_topos_to_plot)]
    h_topo_phi_i = [ROOT.TH1F('topo_phi'+str(i),'topo_phi'+str(i),n_bins_phi,phi_range[0],phi_range[1]) for i in xrange(num_topos_to_plot)]
    h_topo_eta_i = [ROOT.TH1F('topo_eta'+str(i),'topo_eta'+str(i),n_bins_eta,eta_range[0],eta_range[1]) for i in xrange(num_topos_to_plot)]

    max_jet_num = 30 
    h_invalid_jets = ROOT.TH1F('invalid_jets','invalid_jets',max_jet_num,0,max_jet_num)
    h_invalid_jets.GetXaxis().SetTitle("Jet number")     
    h_invalid_jets.GetYaxis().SetTitle("Number of invalid jets")

    h_all_jets = ROOT.TH1F('all_jets','all_jets',max_jet_num,0,max_jet_num)
    h_all_jets.GetXaxis().SetTitle("Jet number")     
    h_all_jets.GetYaxis().SetTitle("Number of jets")

    h_frac_invalid_jets = ROOT.TH1F('frac_invalid_jets','frac_invalid_jets',max_jet_num,0,max_jet_num)
    h_frac_invalid_jets.GetXaxis().SetTitle("Jet number")   

    eta_range_2 = (-1, 1)
    phi_range_2 = (-1, 1)
    eta_block_size_2 = 0.01
    phi_block_size_2 = 0.01
    n_bins_eta_2 = int((eta_range_2[1]-eta_range_2[0])/eta_block_size_2)
    n_bins_phi_2 = int((phi_range_2[1]-phi_range_2[0])/phi_block_size_2)  

    h_calo_towers = ROOT.TH2F('calo_towers','calo_towers',
      n_bins_phi_2, phi_range_2[0], phi_range_2[1],
      n_bins_eta_2, eta_range_2[0], eta_range_2[1])
    h_calo_towers.GetXaxis().SetTitle(" Phi  [rad] ")
    h_calo_towers.GetYaxis().SetTitle(" Eta   ")

    print( "Number of input events: %s" % t.GetEntries())
    # Loop over all events
    for entry in xrange(t.GetEntries()): 
      t.GetEntry(entry)
      h_num_jets.Fill(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()) 
      #print( "Processing run #%i, event #%i ###########################" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber() ) )
      #print( "Number of jets: %i" %  t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size() )
      total_jet_pt = 0
      for i in xrange(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
        total_jet_pt += t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).pt() # Jet
     
      # Loop over all jets in an event
      for i in xrange(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
        if(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).pt()>=150e3 and abs(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).eta())< 2.7):
          jet = t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i) # Jet
          if (i<=5):
              h_jet_frac_i[i].Fill(jet.pt()/total_jet_pt) 
              h_jet_pt_i[i].Fill(jet.pt()/GeV)
              h_jet_eta_i[i].Fill(jet.eta())  
              h_jet_phi_i[i].Fill(jet.phi())
          h_jet_pt.Fill(jet.pt()/GeV)
          h_jet_frac_pt.Fill(jet.pt()/total_jet_pt)
          h_jet_phi.Fill(jet.phi())
          h_jet_eta.Fill(jet.eta())
          #print("Jet "+str(i)+"-------------------------------------")
          #print("Jet Pt = %g, Jet Eta = %g, Jet Phi = %g" % (jet.pt(),jet.eta(),jet.phi()))          
          #topos = jet.getConstituents()
          topos = jet.getConstituents()
          #weights = jet.getConstituentWeights()
          #print(weights)
          #topos = sorted(topos, key=lambda x: x.pt, reverse=True)
          l = dir(topos)
          pprint(l)
          #topos = topos.split()
          #topos.sort(key=lambda x: x.pt(), reverse=True)
          #pt_jet_total = 0
          # Loop over all jet constituents
          #print("Size of topos: "+str(topos.size())+", Valid? "+str(topos.isValid())) #roughly half of these are invalid
          h_num_topos.Fill(topos.size())
          if(topos.isValid()):
              #print(topos)
              #print(topos.size())
              topos = sort_topos(topos)
              #print(topos)
              jet_pt_from_topos = 0
              for index in xrange(len(topos)):
                    topo = topos[index]#
                    jet_pt_from_topos += topo.pt()
              #print("length of topos:"+str(len(topos)))
              for index in xrange(len(topos)):
              #for index in xrange(topos.size()):
                    topo = topos[index]# #topos[index] topos.at(index)#
                    #print( "Constit: pt = %g, eta = %g, phi = %g" % (topo.pt(), topo.eta(), topo.phi()))
                    #l = dir(topo)
                    #pprint(l)
                    raw_cluster = topo.rawConstituent()
                    #print( "Raw Cluster: pt = %g, eta = %g, phi = %g" % (raw_cluster.pt(), raw_cluster.eta(), raw_cluster.phi()))    
                    l = dir(raw_cluster)
                    pprint(l)
                    h_calo_towers.Fill(topo.eta()-jet.eta(), topo.phi()-jet.phi(),topo.pt())# for i in xrange(5)] # before transformations
                    h_topo_pt.Fill(topo.pt()) 
                    h_topo_phi.Fill(topo.phi()) 
                    h_topo_eta.Fill(topo.eta()) 
                    h_topo_frac_pt.Fill(topo.pt()/jet.pt())
                    if (index <num_topos_to_plot):
                        h_topo_frac_i[index].Fill(topo.pt()/jet_pt_from_topos) 
                        h_topo_pt_i[index].Fill(topo.pt()/GeV)
                        h_topo_eta_i[index].Fill(topo.eta())  
                        h_topo_phi_i[index].Fill(topo.phi())
              #print("Jet_pt from Jet   = %g" % jet.pt())
              #print("Jet_pt from Topos = %g" % jet_pt_from_topos)
          else:
            h_invalid_jets.Fill(i)
          h_all_jets.Fill(i)     
          #pt_jet_total += topo.pt()
          #print("Jet total pt: "+str(pt_jet_total))

    h_frac_invalid_jets.Divide(h_invalid_jets,h_all_jets,1.0,1.0)
    f_out.Write()
    f_out.Close()
    f.Close()  
    ROOT.xAOD.ClearTransientTrees() 

if __name__ == '__main__':
    traverse_daods()
