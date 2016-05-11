# Jannicke Pearkes
# Test code for looking at the samples 
# Plot, debug, loop, extract modes 

import ROOT
from pprint import pprint
import math
import numpy as np
import itertools as IT
from ROOT import gROOT
import re
import sys
import logging as l
import pdg_dictionary
from pdg_dictionary import pdgid_to_name

def traverse_daods(file_name):
    # Constants
    GeV = 1000.
    max_size = 0
    max_index = 0
    count = 0

    def regex_search(file_name, regex):
      search = re.compile(regex) 
      value = search.search(file_name)
      return value

    def parse_file_name(file_name):
      output_file_name = ""

      jzxw = regex_search(file_name,'(JZ\dW)')
      zprimexxx = regex_search(file_name,'(zprime\d+)')
      daod_num = regex_search(file_name,'(\d+).pool.root')
      
      if(jzxw):
         output_file_name = "dijet"+jzxw.group(1)
      elif(zprimexxx):
         output_file_name = zprimexxx.group(1)
      output_file_name = "outputs/"+output_file_name+"_"+daod_num.group(1)+"delta_r.root"

      l.info("Output file:"+output_file_name)
      return output_file_name

    def sort_topos(topos):
      topo_list = [None]*(topos.size())
      topo_list = [topos.at(topo) for topo in xrange(topos.size())]
      topo_list.sort(key=lambda topo: topo.pt(), reverse=True)
      return topo_list

    def calculate_delta_r(eta_1,phi_1,eta_2,phi_2):
      delta_eta = eta_1-eta_2
      delta_phi = phi_1-phi_2
      delta_r = math.sqrt(delta_eta**2+delta_phi**2)
      #l_jet.debug("delta_eta: "+str(delta_eta))
      #l_jet.debug("delta_phi: "+str(delta_phi))
      #l_jet.debug("Delta R: "+str(delta_r))
      return delta_r

    def delta_r_match(eta_1,phi_1,eta_2,phi_2, delta_r_max):
      delta_r = calculate_delta_r(eta_1,phi_1,eta_2,phi_2)
      if(delta_r<delta_r_max):
        return True
      else:
        return False 

    def get_w(truth):
        W = None
        b = None
        l_truth.debug("Number of children: "+str(truth.nChildren()))
        for i in xrange(truth.nChildren()):
            l_truth.debug("----"+str(pdgid_to_name(truth.child(i).pdgId())))
            if(truth.child(i).isTop()):
                get_w(truth.child(i)) # iterate recursively
            if(truth.child(i).pdgId() == 24):
                l_truth.debug("W filled")
                W = truth.child(i)   
            if(truth.child(i).pdgId() == 5):
                l_truth.debug("b filled")
                b = truth.child(i)
        if(W and b):
            return W,b
        return None, None

    def get_w_minus(truth):
        W = None
        b = None
        l_truth.debug("Number of children: "+str(truth.nChildren()))
        for i in xrange(truth.nChildren()):
            l_truth.debug("----"+str(pdgid_to_name(truth.child(i).pdgId())))
            if(truth.child(i).isTop()):
                get_w(truth.child(i)) # iterate recursively
            if(truth.child(i).pdgId() == -24):
                l_truth.debug("W filled")
                W = truth.child(i)   
            if(truth.child(i).pdgId() == -5):
                l_truth.debug("b filled")
                b = truth.child(i)
        if(W and b):
            return W,b
        return None, None

    '''
    # Incorrect
    def calculate_opening_angle(px_1,py_1,pz_1,px_2,py_2,pz_2):
      p_dot = px_1*px_2+py_1*py_2+pz_1*pz_2
      p_mag = math.sqrt((px_1**2+py_1**2+pz_1**2)*(px_2**2+py_2**2+pz_2**2))
      
      l_truth.debug("p_dot: "+str(p_dot))
      l_truth.debug("p_mag: "+str(p_mag))
      l_truth.debug("cos theta :"+str(p_dot/p_mag))
      theta = math.acos(p_dot/p_mag)
      l_truth.debug("Opening angle: "+str(theta))
      return theta
    '''

    def calculate_opening_angle(p_1,p_2):
      # print(np.dot(p_1,p_2))
      # print(np.linalg.norm(p_1))
      # print(np.linalg.norm(p_2))
      theta = math.acos(np.dot(p_1,p_2)/(np.linalg.norm(p_1)*np.linalg.norm(p_2)))
      l_truth.debug("Opening angle: "+str(theta))
      return theta

    def calculate_delta_r_from_particle(W,truth):
        delta_eta = W.eta()-truth.eta()
        delta_phi = W.phi()-truth.phi()
        delta_r = math.sqrt(delta_eta**2+delta_phi**2)
        #l_jet.debug("delta_eta: "+str(delta_eta))
        #l_jet.debug("delta_phi: "+str(delta_phi))
        #l_truth.debug("Delta R: "+str(delta_r))
        #print("Delta R: "+str(delta_r))
        return delta_r

    gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");  
    output_file_name = parse_file_name(file_name)
    treeName = "CollectionTree" # default when making transient tree anyway
    f = ROOT.TFile.Open(file_name)
    t = ROOT.xAOD.MakeTransientTree(f, treeName)    
    f_out = ROOT.TFile(output_file_name, "recreate")   

    # Set up histograms if desired
    fill_histograms = 0
    if(fill_histograms):
      eta_range = (-3, 3) 
      phi_range = (-math.pi, math.pi)
      eta_block_size = 0.1
      phi_block_size = 0.1
      n_bins_eta = int((eta_range[1]-eta_range[0])/eta_block_size)
      n_bins_phi = int((phi_range[1]-phi_range[0])/phi_block_size)  

      h_num_jets = ROOT.TH1F('num_jets','Number of jets per event',30,0.0,30.0)
      h_num_jets.GetXaxis().SetTitle("Number of jets") 

      h_num_valid_jets = ROOT.TH1F('num_valid_jets','Number of valid jets per event',30,0.0,30.0)
      h_num_valid_jets.GetXaxis().SetTitle("Number of jets") 

      # Jet histograms
      h_jet_pt = ROOT.TH1F('jet_pt','Transverse momentum of all jets',100,0.0,5.0e3)
      h_jet_pt.GetXaxis().SetTitle("p_t [GeV]") 

      h_jet_eta = ROOT.TH1F('jet_eta','Eta distribution for all jets',n_bins_eta,eta_range[0],eta_range[1])
      h_jet_eta.GetXaxis().SetTitle("Eta") 

      h_jet_phi = ROOT.TH1F('jet_phi','Phi distribution for all jets',n_bins_phi,phi_range[0],phi_range[1])
      h_jet_phi.GetXaxis().SetTitle("Phi [rad]") 
      
      h_jet_frac_pt = ROOT.TH1F('jet_frac_pt','Fractional pt carried by all jets',100,0,1)
      h_jet_frac_pt.GetXaxis().SetTitle("Fractional pt")

      h_num_topos = ROOT.TH1F('num_topos','Number of topoclusters per jet',100,0.0,100)
      h_num_topos.GetXaxis().SetTitle("Number of topoclusters") 

      num_jets_to_plot = 6
      h_jet_frac_i = [ROOT.TH1F('jet_frac'+str(i),'Fractional pt carried by jet #'+str(i),100,0,1) for i in xrange(num_jets_to_plot)]
      h_jet_pt_i = [ROOT.TH1F('jet_pt'+str(i),'Pt of jet #'+str(i),100,0.0,5e3) for i in xrange(num_jets_to_plot)]
      h_jet_phi_i = [ROOT.TH1F('jet_phi'+str(i),'Phi of jet #'+str(i),n_bins_phi,phi_range[0],phi_range[1]) for i in xrange(num_jets_to_plot)]
      h_jet_eta_i = [ROOT.TH1F('jet_eta'+str(i),'Eta of jet #'+str(i),n_bins_eta,eta_range[0],eta_range[1]) for i in xrange(num_jets_to_plot)]
      for i in xrange(num_jets_to_plot): 
        h_jet_frac_i[i].GetXaxis().SetTitle("Fractional pt") 
        h_jet_pt_i[i].GetXaxis().SetTitle("p_t [MeV]") 
        h_jet_phi_i[i].GetXaxis().SetTitle("Phi [rad]")  
        h_jet_eta_i[i].GetXaxis().SetTitle("Eta") 

      # Topo histograms
      h_topo_pt = ROOT.TH1F('topo_pt','Pt distribution of all jet constituents',100,-10.0,300000.0)
      h_topo_pt.GetXaxis().SetTitle("p_t [MeV]")  

      h_topo_eta = ROOT.TH1F('topo_eta','Eta distribution of all jet constituents',n_bins_eta,eta_range[0],eta_range[1])
      h_topo_eta.GetXaxis().SetTitle("Eta")  

      h_topo_phi = ROOT.TH1F('topo_phi','Phi distribution of all jet constituents',n_bins_phi,phi_range[0],phi_range[1])
      h_topo_phi.GetXaxis().SetTitle("Phi [rad]")  

      h_topo_frac_pt = ROOT.TH1F('topo_frac_pt','Fractional transverse momentum carried by all jet constituents',100,0,1)
      h_topo_frac_pt.GetXaxis().SetTitle("Fractional pt") 

      num_topos_to_plot = 21
      h_topo_frac_i = [ROOT.TH1F('topo_frac'+str(i),'Fractional pt carried by jet constituent #'+str(i),100,0,1) for i in xrange(num_topos_to_plot)]
      h_topo_pt_i = [ROOT.TH1F('topo_pt'+str(i),'Pt of jet constituent #'+str(i),100,0.0,5e3) for i in xrange(num_topos_to_plot)]
      h_topo_phi_i = [ROOT.TH1F('topo_phi'+str(i),'Phi of jet constituent #'+str(i),n_bins_phi,phi_range[0],phi_range[1]) for i in xrange(num_topos_to_plot)]
      h_topo_eta_i = [ROOT.TH1F('topo_eta'+str(i),'Eta of jet constituent #'+str(i),n_bins_eta,eta_range[0],eta_range[1]) for i in xrange(num_topos_to_plot)]
      for i in xrange(num_topos_to_plot): 
        h_topo_frac_i[i].GetXaxis().SetTitle("Fractional pt") 
        h_topo_pt_i[i].GetXaxis().SetTitle("p_t [MeV]") 
        h_topo_phi_i[i].GetXaxis().SetTitle("Phi [rad]")  
        h_topo_eta_i[i].GetXaxis().SetTitle("Eta") 

      '''
      max_jet_num = 30 
      h_invalid_jets = ROOT.TH1F('invalid_jets','Number of invalid jets',max_jet_num,0,max_jet_num)
      h_invalid_jets.GetXaxis().SetTitle("Jet number")     
      h_invalid_jets.GetYaxis().SetTitle("Number of invalid jets")

      h_all_jets = ROOT.TH1F('all_jets','all_jets',max_jet_num,0,max_jet_num)
      h_all_jets.GetXaxis().SetTitle("Jet number")     
      h_all_jets.GetYaxis().SetTitle("Number of jets")

      h_frac_invalid_jets = ROOT.TH1F('frac_invalid_jets','frac_invalid_jets',max_jet_num,0,max_jet_num)
      h_frac_invalid_jets.GetXaxis().SetTitle("Jet number")   
      '''
      eta_range_2 = (-1, 1)
      phi_range_2 = (-1, 1)
      eta_block_size_2 = 0.01
      phi_block_size_2 = 0.01
      n_bins_eta_2 = int((eta_range_2[1]-eta_range_2[0])/eta_block_size_2)
      n_bins_phi_2 = int((phi_range_2[1]-phi_range_2[0])/phi_block_size_2)  

      h_calo_towers = ROOT.TH2F('calo_towers','Calorimeter towers from all jets',
        n_bins_phi_2, phi_range_2[0], phi_range_2[1],
        n_bins_eta_2, eta_range_2[0], eta_range_2[1])
      h_calo_towers.GetXaxis().SetTitle(" Phi  [rad] ")
      h_calo_towers.GetYaxis().SetTitle(" Eta   ")
      h_calo_towers.GetZaxis().SetTitle(" pt [MeV]  ")

    #h_opening_angle = ROOT.TH1F('opening_angle','Opening angle between truth top quarks',40,0,math.pi)
    #h_opening_angle.GetXaxis().SetTitle("Phi [rad]") 

    h_delta_r = ROOT.TH1F('delta_r','Delta R between truth top quarks',30,0,2*math.pi)
    h_delta_r.GetXaxis().SetTitle("Delta R") 

    #h_opening_angle_topos = ROOT.TH1F('opening_angle_topos','Opening angle between constituent 1 and 2 for top jets',40,0,math.pi)
    #h_opening_angle_topos.GetXaxis().SetTitle("Phi [rad]") 
   
    h_delta_r_top_W = ROOT.TH1F('h_delta_r_top_W','Delta R between Top and W',40,0,10)#math.pi)
    h_delta_r_top_W.GetXaxis().SetTitle("$\Delta R$") 

    h_delta_r_top_b = ROOT.TH1F('h_delta_r_top_b','Delta R between Top and b',40,0,10)#math.pi)
    h_delta_r_top_b.GetXaxis().SetTitle("$\Delta$ R") 

    l.info( "Number of input events: %s" % t.GetEntries())
    
    # Loop over all events
    for entry in xrange(4000):#t.GetEntries()): 
      t.GetEntry(entry)
      l.debug( " ################ Run #%i, Event #%i ###########################" % ( t.EventInfo.runNumber(), t.EventInfo.eventNumber() ) )
      l.debug( "Number of jets: %i" %  t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size() )
      if(entry % 1000 == 0 and entry != 0):
        l.info("Processing event: "+str(entry))
      # Loop over truth particles 
      l_truth.debug("Number of truth particles:"+str(t.TruthParticles.size()))
      top = 0
      for i in xrange(t.TruthParticles.size()):   
          truth =  t.TruthParticles.at(i)
          # print("PdgID truth:"+str(truth.pdgId()))
          if(truth.pdgId() == 6):
            truth_top_pt, truth_top_eta, truth_top_phi  = truth.pt(), truth.eta(), truth.phi()
            truth_top_p = np.array([truth.px(), truth.py(), truth.pz()])
            l_truth.debug("Top")
            l_truth.debug("pt = %g, eta = %g, phi = %g" % (truth.pt(), truth.eta(), truth.phi()))
            l_truth.debug("Is top? "+str(truth.isTop()))
            W = None 
            b = None
            if(truth.isTop()):
              W,b = get_w(truth)
              if(W and b):
                delta_r_W_top = calculate_delta_r_from_particle(W,truth)
                h_delta_r_top_W.Fill(delta_r_W_top)
                delta_r_b_top = calculate_delta_r_from_particle(W,b)
                h_delta_r_top_b.Fill(delta_r_b_top)
          
          if(truth.pdgId() == -6):
            truth_anti_top_pt, truth_anti_top_eta, truth_anti_top_phi  = truth.pt(), truth.eta(), truth.phi()
            truth_anti_top_p = np.array([truth.px(), truth.py(), truth.pz()])
            l_truth.debug("Anti-top")
            l_truth.debug("Is anti-top?"+str(truth.isTop()))
            l_truth.debug("pt = %g, eta = %g, phi = %g" % (truth.pt(), truth.eta(), truth.phi()))
            l_truth.debug("Is top? "+str(truth.isTop()))
            W = None 
            b = None
            if(truth.isTop()):
              W,b = get_w_minus(truth)
              if(W and b):
                delta_r_W_top = calculate_delta_r_from_particle(W,truth)
                h_delta_r_top_W.Fill(delta_r_W_top)
                delta_r_b_top = calculate_delta_r_from_particle(W,b)
                h_delta_r_top_b.Fill(delta_r_b_top)
            #for i in xrange(truth.nChildren()):
            #      l_truth.debug(truth.child(i).pdgId())
            top += 1
            
      #theta = calculate_opening_angle(truth_top_px, truth_top_py, truth_top_pz,truth_anti_top_px, truth_anti_top_py, truth_anti_top_pz)
      if(top>=2):
        delta_r = calculate_delta_r(truth_top_eta, truth_top_phi, truth_anti_top_eta, truth_anti_top_phi)
        h_delta_r.Fill(delta_r)

      #for i in xrange(t.AntiKt10TruthJets.size()):
      #    truth_jet = t.AntiKt10TruthJets.at(i)
      #    print("Parton truth label id:"+str(truth_jet.PartonTruthLabelID)) #nope
          #print("ConeTruthLabelID:"+str(truth_jet.ConeTruthLabelID())) #nope
          #print("PdgID:"+str(truth_jet.pdgId()))
      

      if(fill_histograms):
        h_num_jets.Fill(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()) 

      total_jet_pt = 0
      for i in xrange(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
        total_jet_pt += t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).pt() 
     
      # Loop over all jets in an event
      valid_jets = 0
      for i in xrange(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.size()):
        if(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).pt()>=150e3 and abs(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i).eta())< 2.7):
          valid_jets += 1
          jet = t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets.at(i) # Jet
          


          if(fill_histograms):
            if (i<=5):
                h_jet_frac_i[i].Fill(jet.pt()/total_jet_pt) 
                h_jet_pt_i[i].Fill(jet.pt()/GeV)
                h_jet_eta_i[i].Fill(jet.eta())  
                h_jet_phi_i[i].Fill(jet.phi())
            h_jet_pt.Fill(jet.pt()/GeV)
            h_jet_frac_pt.Fill(jet.pt()/total_jet_pt)
            h_jet_phi.Fill(jet.phi())
            h_jet_eta.Fill(jet.eta())
          l_jet.info("Jet "+str(i)+"-------------------------------------")
          l_jet.info("pt = %g, eta = %g, phi = %g" % (jet.pt(),jet.eta(),jet.phi())) 
          matches_top = False
          matches_top = delta_r_match(truth_top_eta, truth_top_phi, jet.eta(),jet.phi(), 0.4)
          if (matches_top):
            l_jet.debug("Jet "+str(i)+" matches top")

          matches_anti_top = False
          matches_anti_top = delta_r_match(truth_anti_top_eta, truth_anti_top_phi, jet.eta(),jet.phi(), 0.4)
          if(matches_anti_top):
            l_jet.debug("Jet "+str(i)+" matches anti-top")

          topos = jet.getConstituents()
          #weights = jet.getConstituentWeights()
          #print(weights)

          #l_jet_sub.debug(pprint.pformat(dir(topos)))

          # Loop over all jet constituents
          l_jet_sub.info("Size of topos: "+str(topos.size())+", Valid? "+str(topos.isValid())) #roughly half of these are invalid
          if(fill_histograms):
            h_num_topos.Fill(topos.size())
          if(topos.isValid()):
              topos = sort_topos(topos)
              # calculate total pt from topoclusters first (needed for fractional pt)
              jet_pt_from_topos = 0
              for index in xrange(len(topos)):
                    topo = topos[index]#
                    jet_pt_from_topos += topo.pt()
              # loop over topoclusters
              for index in xrange(len(topos)):
                    topo = topos[index]# #topos[index] topos.at(index)#
                    l_jet_sub.info( "Constit:     pt = %g, eta = %g, phi = %g" % (topo.pt(), topo.eta(), topo.phi()))
                    #l_jet_sub.debug(pprint.pformat(dir(topo)))
                    #raw_cluster = topo.rawConstituent()
                    #print( "Raw Cluster: pt = %g, eta = %g, phi = %g" % (raw_cluster.pt(), raw_cluster.eta(), raw_cluster.phi()))    
                    #l = dir(raw_cluster)
                    #pprint(l)
                    if(fill_histograms):
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

              l_jet_sub.debug("Jet_pt from Jet   = %g" % jet.pt())
              l_jet_sub.debug("Jet_pt from Topos = %g" % jet_pt_from_topos)
          #else:
            #h_invalid_jets.Fill(i)
          #h_all_jets.Fill(i)     
          #pt_jet_total += topo.pt()
          #print("Jet total pt: "+str(pt_jet_total))
      if(fill_histograms):
        h_num_valid_jets.Fill(valid_jets)

    #h_frac_invalid_jets.Divide(h_invalid_jets,h_all_jets,1.0,1.0)
    
    f_out.Write()
    f_out.Close()
    f.Close()  
    ROOT.xAOD.ClearTransientTrees() 

if __name__ == '__main__':
    # setup loggers 
    l.basicConfig(level=l.INFO, format='%(levelname)s - %(message)s')#%(asctime)s - %(levelname)s - %(message)s')
    l_jet = l.getLogger("jet logger")
    l_jet.setLevel(l.ERROR)
    #l_jet.setLevel(l.DEBUG)
    l_jet_sub = l.getLogger("jet sub logger")
    l_jet_sub.setLevel(l.ERROR)
    #l_jet_sub.setLevel(l.DEBUG)
    l_truth = l.getLogger("truth logger")
    l_truth.setLevel(l.ERROR)
    #l_truth.setLevel(l.DEBUG)

    # read in filename as input
    if len(sys.argv)>=2:
      name,file_name = sys.argv
    else:
      # zprime tt 400
      file_name = "/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.07896478._000001.pool.root.1"
      # zprime tt 2250
      #file_name = "/data/wfedorko/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618509_00/DAOD_EXOT7.07618509._000010.pool.root.1"
      # zprime tt 5000
      #file_name = "/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.07618499._000005.pool.root.1"
      # dijet 
      #file_name = "/data/wfedorko/mc15_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618436_00/DAOD_EXOT7.07618436._000001.pool.root.1"
    l.info("Input file: "+file_name)
    traverse_daods(file_name)
