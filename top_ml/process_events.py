""" Event loop for xAODs """
import math
from utils import *
import logging
import ROOT
from ROOT import gROOT
from pdg_dictionary import pdgid_to_name
import numpy as np
from pprint import pprint
import pdb


def debug_string_particle(truth):       
    string = pdgid_to_name(truth.pdgId())+(": pt = %g, eta = %g, phi = %g" % (truth.pt(), truth.eta(), truth.phi()))
    return 

def debug_string(truth):       
    string = ": pt = %g, eta = %g, phi = %g" % (truth.pt(), truth.eta(), truth.phi())
    return string    

def calculate_delta_r_from_particle(W,truth):
    delta_r = W.p4().DeltaR(truth.p4())
    return delta_r

def sort_topos(topos):
  topo_list = [None]*(topos.size())
  topo_list = [topos.at(topo) for topo in xrange(topos.size())]
  topo_list.sort(key=lambda topo: topo.pt(), reverse=True)
  return topo_list

def get_w(truth):
    """ Recursive function to obtain top daughters """
    W = None
    b = None
    l_truth.debug("Number of children: "+str(truth.nChildren()))
    for i in xrange(truth.nChildren()):
        l_truth.debug("----"+str(pdgid_to_name(truth.child(i).pdgId())))
        if(truth.child(i).isTop()):
            get_w(truth.child(i)) # iterate recursively
        
        if(truth.pdgId() == 6):
            if(truth.child(i).pdgId() == 24):
                l_truth.debug("W filled")
                W = truth.child(i) 
                #get_w_daughters(W)  
            if(truth.child(i).pdgId() == 5):
                l_truth.debug("b filled")
                b = truth.child(i)

        if(truth.pdgId() == -6):
            if(truth.child(i).pdgId() == -24):
                l_truth.debug("W filled")
                W = truth.child(i)   
            if(truth.child(i).pdgId() == -5):
                l_truth.debug("b filled")
                b = truth.child(i)

    if(W and b):
        return W,b
    else:
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
    else:
        return None, None

def get_w_daughters(truth):
  x = []
  l_truth.debug("---- W children"+str(truth.nChildren()))
  for i in xrange(truth.nChildren()):
      l_truth.debug("---- ----"+str(pdgid_to_name(truth.child(i).pdgId())))
      if(truth.child(i).isW()):
          x = get_w_daughters(truth.child(i)) # iterate recursively
      elif (truth.child(i).isQuark()):
          x.append(truth.child(i))
  l_truth.debug("x = "+str(x))
  return x

def check_hadronic_decay(top):
    ''' Checks to make sure W decays hadronically '''
    W,b = get_w(top)

    x = []
    if W: 
       x = get_w_daughters(W)
    if(len(x)> 0):
        return top
    else:
        return None

def truth_particle_loop(truth_particles):
    ''' Extract the relevant truth particles '''

    l_truth.debug("Number of truth particles: "+str(truth_particles.size()))
    
    # z = None
    top = None
    anti_top = None
    
    # Get final state particles 
    for i in xrange(truth_particles.size()):   
        truth = truth_particles.at(i)
        #if(truth.pdgId() == 32): # Z'
        #    z = truth
        #    l_truth.debug(debug_string_particle(z))
        if(truth.pdgId() == 6): # top 
            top = truth
            l_truth.debug(debug_string_particle(top))
            top = check_hadronic_decay(top)  
        if(truth.pdgId() == -6): # anti-top
            anti_top = truth
            l_truth.debug(debug_string_particle(anti_top))
            anti_top = check_hadronic_decay(anti_top)
            
    return top,anti_top

def top_jet_loop(jets, top, anti_top):
    ''' 
    Finds jets that are closest to the two truth tops
    Have not found a way to do this elegantly yet...
    '''

    smallest_delta_r_to_top = 100
    smallest_delta_r_to_anti_top = 100
    delta_r_to_top = 100
    delta_r_to_anti_top = 100
    max_delta_r = 0.75
    max_eta = 2.0

    for i in xrange(jets.size()):
        #
        if(jets.at(i).pt()> 150e3 and abs(jets.at(i).eta())< 2.0): # pt cut is made in the xAOD derivation, we are making 2.0 eta cut 

            jet = jets.at(i) 

            l_jet.info("Jet "+str(i)+"-------------------------------------")
            l_jet.info(debug_string(jet))

            l_jet.debug("Top?"+str(top))
            l_jet.debug("Anti-top?"+str(anti_top))
            # store jets with smallest delta r
            if(top):
                delta_r_to_top = calculate_delta_r_from_particle(top,jet)
                l_jet.debug("Delta r to top: "+str(delta_r_to_top))
            if(anti_top):
                delta_r_to_anti_top = calculate_delta_r_from_particle(anti_top,jet)
                l_jet.debug("Delta r to anti-top: "+str(delta_r_to_anti_top))

            if (delta_r_to_top < smallest_delta_r_to_top):
                smallest_delta_r_to_top = delta_r_to_top
                top_jet = jet
                l_jet.debug("Smallest delta r to top: "+str(smallest_delta_r_to_top))
            if (delta_r_to_anti_top < smallest_delta_r_to_anti_top):
                smallest_delta_r_to_anti_top = delta_r_to_anti_top
                l_jet.debug("Smallest delta r to antitop: "+str(smallest_delta_r_to_anti_top))
                anti_top_jet = jet
            if(i == 0):
                h_first_jet_mass.Fill(jet.m()/GeV) 
            elif i==1:
                h_second_jet_mass.Fill(jet.m()/GeV)
            else:
                h_other_jet_mass.Fill(jet.m()/GeV)

    # set jets to None if do not match
    if (smallest_delta_r_to_top > max_delta_r):
        top_jet = None
    if (smallest_delta_r_to_anti_top > max_delta_r):
        anti_top_jet = None    
    # fill relevant histograms
    if(top_jet):    
        h_delta_r_top_jet.Fill(smallest_delta_r_to_top)
        h_delta_pt_top_jet.Fill((top.pt() - top_jet.pt())/GeV)
        h_jet_pt_cut.Fill(top_jet.pt()/GeV)
        h_jet_eta_cut.Fill(top_jet.eta())
        h_jet_phi_cut.Fill(top_jet.phi())
    if(anti_top_jet):
        h_delta_r_top_jet.Fill(smallest_delta_r_to_anti_top)
        h_delta_pt_top_jet.Fill((anti_top.pt() - anti_top_jet.pt())/GeV)
        h_jet_pt_cut.Fill(anti_top_jet.pt()/GeV)
        h_jet_eta_cut.Fill(anti_top_jet.eta())
        h_jet_phi_cut.Fill(anti_top_jet.phi())
    if(top_jet and anti_top_jet):
        h_inv_mass_jet.Fill((top_jet.p4()+anti_top_jet.p4()).M()/GeV)
    if(top and anti_top):
        h_inv_mass_top.Fill((top.p4()+anti_top.p4()).M()/GeV)
    if(top and top_jet):
        h_delta_pt_delta_r.Fill((top.pt() - top_jet.pt())/GeV, smallest_delta_r_to_top)
    if(anti_top and anti_top_jet):
        h_delta_pt_delta_r.Fill((anti_top.pt() - anti_top_jet.pt())/GeV, smallest_delta_r_to_anti_top)     
    
    return top_jet,anti_top_jet

def jet_loop(jets):
    return

def event_display(top, anti_top, top_jet, anti_top_jet):
    return 

def create_vector(jet):
    print("Subjets")
    print(jet.getAttribute("NTrimSubjets"))
    # print("Dip12")
    # print(jet.getAttribute("Dip12"))
    # print("Tau_2")
    # print(jet.getAttribute("Tau2_wta"))
    # print("Split23")
    # print(jet.getAttribute("Split23"))
    x_jet = np.array([jet.m(),jet.pt()/GeV, jet.eta(), jet.phi()])#[np.array([[jet.pt()/GeV, jet.eta(), jet.phi()]])]

    y_jet = None
    topos = jet.getConstituents()

    # Loop over all jet constituents
    l_jet_sub.info("Size of topos: "+str(topos.size())+", Valid? "+str(topos.isValid())) #roughly half of these are invalid
    if(topos.isValid()):
        #print len(topos)
        energy = 0
        momentum = 0
        topos = sort_topos(topos)
        jet_mass = None
        y_jet = np.zeros((len(topos),3))#[None]*len(topos)#np.zeros((len(topos),3))
        for index in xrange(len(topos)):
            topo = topos[index]# #topos[index] topos.at(index)#
            y_jet[index] = np.array([topo.pt()/GeV,topo.eta(), topo.phi()])
            #energy = energy+topo.e()
            #momentum = momentum+math.sqrt(topo.px()**2+topo.py()**2+topo.pz()**2)
            rawCluster = topo.rawConstituent()
            #print("raw")
            #print(rawCluster.p4())
            if index == 0:
                jet_mass = rawCluster.p4()
            else:
                jet_mass = jet_mass + rawCluster.p4()
            #print("topo")
            #print(topo.p4())
            #h_calo_towers_jet_constit[ry].Fill(topo.eta(), topo.phi(),topo.pt()/GeV)
        #y_jet = [[jet_constit.pt(),jet_conentstit.eta(), jet_constit.phi() for i in top_jet.size()]]
        h_jet_mass.Fill(jet.m()/GeV)

        h_jet_mass_from_raw.Fill(jet_mass.M()/GeV)
        if (jet.pt()>=650e3 and jet.pt()< 1800e3):
            h_jet_mass_after_pt_cut.Fill(jet.m()/GeV)
            if jet.m()> 100e3:
                h_jet_mass_after_pt_and_m_cuts.Fill(jet.m()/GeV)
        h_jet_mass_pt.Fill(jet.pt()/GeV, jet.m()/GeV)
        # if jet_mass<= 0.0:
        #     print ("jet_mass"+str(jet_mass.M()/GeV))
        #     print("num constituents "+str(len(topos)))
        #     print("jet pt "+str(jet.pt()))
    if(y_jet != None):
        #print(x_jet)  
        #print(y_jet) 
        #print(x_jet.shape)
        #print(y_jet.shape)
        z_jet = np.hstack((x_jet,np.ravel(y_jet)))#.append(y_jet) something
        #pprint(z_jet)
        #print(np.ravel(z_jet))
        return np.ravel(z_jet)
    else: 
        return None

def save_jet_constituents(top_jet,anti_top_jet):
    top_vec = None
    if(anti_top_jet and top_jet):
        top_vec = create_vector(top_jet), create_vector(anti_top_jet)
    if(anti_top_jet and not top_jet):
        top_vec = create_vector(anti_top_jet)
    if(top_jet and not anti_top_jet):
        top_vec = create_vector(top_jet)  
    return top_vec

def process_signal_event(truth_particles, jets):
    """ Extract the truth particles and then compare with the jets """
    #pdb.set_trace()
    top = None
    anti_top = None
    top_jet = None
    anti_top_jet = None
    event = None
    top, anti_top = truth_particle_loop(truth_particles)
    top_jet, anti_top_jet = top_jet_loop(jets, top, anti_top) 
    event = save_jet_constituents(top_jet, anti_top_jet)
    return event


def process_background_event(jets):
    vec = []
    new_vec = None
    for i in xrange(jets.size()):
        if(jets.at(i).pt()>=150e3 and abs(jets.at(i).eta())< 2.0): # pt cut is made in the xAOD derivation, we are making 2.0 eta cut 
            jet = jets.at(i)
            h_jet_pt_cut.Fill(jet.pt()/GeV)
            h_jet_eta_cut.Fill(jet.eta())
            h_jet_phi_cut.Fill(jet.phi())
            new_vec = create_vector(jet)
            if(i == 0):
                h_first_jet_mass.Fill(jet.m()/GeV) 
            elif i==1:
                h_second_jet_mass.Fill(jet.m()/GeV)
            else:
                h_other_jet_mass.Fill(jet.m()/GeV)
            if(vec):
                vec.append(new_vec)
            else:
                vec = [new_vec]
    return vec

def init_jet_top_histograms():

    eta_range = (-3, 3) 
    phi_range = (-math.pi, math.pi)
    eta_block_size = 0.1
    phi_block_size = 0.1
    n_bins_eta = int((eta_range[1]-eta_range[0])/eta_block_size)
    n_bins_phi = int((phi_range[1]-phi_range[0])/phi_block_size) 

    global h_delta_r_top_jet
    h_delta_r_top_jet = ROOT.TH1F('h_delta_r_top_jet','Delta R between top quark and matching jet',100,0,math.pi)
    h_delta_r_top_jet.GetXaxis().SetTitle("$\Delta$ R")

    global h_delta_pt_top_jet
    h_delta_pt_top_jet = ROOT.TH1F('h_delta_pt_top_jet','Delta pt between top and matching jet',100,-2500,2500)
    h_delta_pt_top_jet.GetXaxis().SetTitle("p_T [GeV]") 

    global h_inv_mass_jet 
    h_inv_mass_jet = ROOT.TH1F('h_inv_mass_jet','Invariant mass of two top jets passing selection',100,0,5000)
    h_inv_mass_jet.GetXaxis().SetTitle("Mass [GeV]")  

    global h_inv_mass_top 
    h_inv_mass_top= ROOT.TH1F('h_inv_mass_top','Invariant mass of two tops ',100,0,5000)
    h_inv_mass_top.GetXaxis().SetTitle("Mass [GeV]")  

    global h_delta_pt_delta_r 
    h_delta_pt_delta_r  = ROOT.TH2F('h_delta_pt_delta_r','Delta Pt compared with Delta R',
    100,-2500,2500,
    100,0,0.75)
    h_delta_pt_delta_r.GetXaxis().SetTitle(" Delta Pt [GeV] ")
    h_delta_pt_delta_r.GetYaxis().SetTitle(" Delta R   ")
    h_delta_pt_delta_r.GetZaxis().SetTitle(" Events  ")

    global h_jet_pt_cut
    h_jet_pt_cut = ROOT.TH1F('h_jet_pt_cut','Transverse momentum of jets passing selection',100,0,5000)
    h_jet_pt_cut.GetXaxis().SetTitle("p_T [GeV]")

    global h_jet_eta_cut 
    h_jet_eta_cut = ROOT.TH1F('h_jet_eta_cut','Eta distribution of jets passing selection',n_bins_eta,eta_range[0],eta_range[1])
    h_jet_eta_cut.GetXaxis().SetTitle("Eta") 

    global h_jet_phi_cut 
    h_jet_phi_cut = ROOT.TH1F('h_jet_phi_cut','Phi distribution of jets passing selection',n_bins_phi,phi_range[0],phi_range[1])
    h_jet_phi_cut.GetXaxis().SetTitle("Phi [rad]") 

    global h_jet_mass 
    h_jet_mass  = ROOT.TH1F('h_jet_mass','Jet mass of jets passing selection',100,-1e-4,250)
    h_jet_mass.GetXaxis().SetTitle("m [GeV]")    

    global h_jet_mass_from_raw
    h_jet_mass_from_raw  = ROOT.TH1F('h_jet_mass_from_raw','Jet mass of jets passing selection',100,-1e-4,250)
    h_jet_mass_from_raw.GetXaxis().SetTitle("m [GeV]")  

    global h_jet_mass_after_pt_cut
    h_jet_mass_after_pt_cut  = ROOT.TH1F('h_jet_mass_after_pt_cut','Jet mass of jets passing pt cut',100,-1e-4,250)
    h_jet_mass_after_pt_cut.GetXaxis().SetTitle("m [GeV]")  

    global h_jet_mass_after_pt_and_m_cuts
    h_jet_mass_after_pt_and_m_cuts = ROOT.TH1F('h_jet_mass_after_pt_and_m_cuts','Jet mass of jets passing pt and mass cut',100,-1e-4,250)
    h_jet_mass_after_pt_and_m_cuts.GetXaxis().SetTitle("m [GeV]")     

    global h_first_jet_mass
    h_first_jet_mass = ROOT.TH1F('h_first_jet_mass','Jet mass of leading jet',100,-1e-4,250)
    h_first_jet_mass.GetXaxis().SetTitle("m [GeV]")  

    global h_second_jet_mass
    h_second_jet_mass = ROOT.TH1F('h_second_jet_mass','Jet mass of second jets',100,-1e-4,250)
    h_second_jet_mass.GetXaxis().SetTitle("m [GeV]")   

    global h_other_jet_mass
    h_other_jet_mass = ROOT.TH1F('h_other_jet_mass','Jet mass of other jets',100,-1e-4,250)
    h_other_jet_mass.GetXaxis().SetTitle("m [GeV]")   

    global h_jet_mass_pt 
    h_jet_mass_pt   = ROOT.TH2F('h_jet_mass_pt','',
    100,0,4000,
    100,-1e-4,250)
    h_jet_mass_pt.GetXaxis().SetTitle(" Jet p_t [GeV] ")
    h_jet_mass_pt.GetYaxis().SetTitle(" Jet mass [GeV]   ")
    h_jet_mass_pt.GetZaxis().SetTitle(" Jets ")

def process_events(file_name):
    global GeV
    GeV = 1000.0
    global l_truth
    global l_jet
    global l_jet_sub
    l_truth = logging.getLogger("truth logger")
    l_truth.setLevel(logging.ERROR)
    #l_truth.setLevel(logging.DEBUG) 
    l_jet = logging.getLogger("jet logger")
    l_jet.setLevel(logging.ERROR)
    #l_jet.setLevel(logging.DEBUG)
    l_jet_sub = logging.getLogger("jet sub logger")
    l_jet_sub.setLevel(logging.ERROR)
    #l_jet_sub.setLevel(logging.DEBUG)
    gROOT.ProcessLine(".x $ROOTCOREDIR/scripts/load_packages.C")
    #gROOT.ProcessLine('#include "xAODCutFlow/CutBookkeeper.h"')

    output_file_name = parse_file_name(file_name)

    treeName = "CollectionTree"
    f = ROOT.TFile.Open(file_name)
    t = ROOT.xAOD.MakeTransientTree(f, treeName)    
    f_out = ROOT.TFile(output_file_name, "recreate")  
    logging.info("Number of input events: %s" % t.GetEntries())
    
    #Initialize histograms
    init_jet_top_histograms()

    data = []
    # Loop over all events
    for entry in xrange(t.GetEntries()):
        
        if entry % 100 == 0 and entry != 0:
            logging.info("Processing event: "+str(entry))
        event = None
        t.GetEntry(entry)
        
        if ("_tt" in file_name):
            event = process_signal_event(t.TruthParticles,
                                 t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets)
            
            if(event != None):
                if(type(event).__module__ == np.__name__):
                    data.append(event)
                else:
                    data.append(event[0])
                    data.append(event[1])

        elif("jetjet" in file_name):
            event = process_background_event(t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets)
            if(event):
                data.extend(event)
    np.savez_compressed(output_file_name.replace(".root",""), data=data)
    logging.info("Saved numpy array as: "+output_file_name.replace(".root",""))

    num_jet_mass = h_jet_mass.Integral() 
    num_jet_mass_after_pt_cut = h_jet_mass_after_pt_cut.Integral()  
    num_jet_mass_after_pt_and_m_cuts = h_jet_mass_after_pt_and_m_cuts.Integral()
    if(num_jet_mass!= 0):
        pt_cut_efficiency = num_jet_mass_after_pt_cut/num_jet_mass
        print("pt cut efficiency: "+str(pt_cut_efficiency))
    if(num_jet_mass_after_pt_cut != 0):
        pt_and_m_cut_efficiency = num_jet_mass_after_pt_and_m_cuts/num_jet_mass_after_pt_cut
        print("pt and m cut efficiency:"+str(pt_and_m_cut_efficiency))
    #pprint(data)
    f_out.Write()
    f_out.Close()
    f.Close()  
    ROOT.xAOD.ClearTransientTrees() 

    return
