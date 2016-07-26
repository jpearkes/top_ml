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
from top_ml.column_definition import *


def debug_string_particle(truth):
    ''' Creates pdg id pt,eta,phi string for printing '''
    string = pdgid_to_name(
        truth.pdgId()) + debug_string(truth)
    return string


def debug_string(truth):
    ''' Creates pt,eta,phi string for printing '''
    string = ": pt = %g, eta = %g, phi = %g" % (
        truth.pt(), truth.eta(), truth.phi())
    return string


def calculate_delta_r_from_particle(W, truth):
    ''' Calculates delta r between two particles '''
    delta_r = W.p4().DeltaR(truth.p4())
    return delta_r


def sort_topos(topos):
    ''' Sorts topoclusters (jet constituents) by pt '''
    topo_list = [None] * (topos.size())
    topo_list = [topos.at(topo) for topo in xrange(topos.size())]
    topo_list.sort(key=lambda topo: topo.pt(), reverse=True)
    return topo_list


def get_w(truth):
    ''' Recursive function to obtain daughters of top '''

    W = None
    b = None

    l_truth.debug("Number of children: " + str(truth.nChildren()))

    for i in xrange(truth.nChildren()): 

        child = truth.child(i)
        l_truth.debug("----" + str(pdgid_to_name(child.pdgId())))

        # iterate recursively until right before top decay
        if child.isTop():
            get_w(child)  

        if truth.pdgId() == 6: # top 
            if child.pdgId() == 24: # W+
                l_truth.debug("W filled")
                W = child
                # get_w_daughters(W)
            if child.pdgId() == 5: # b
                l_truth.debug("b filled")
                b = child

        if truth.pdgId() == -6 : # anti-top
            if child.pdgId() == -24 : # W-
                l_truth.debug("W filled")
                W = child
            if child.pdgId() == -5 : # anti-b
                l_truth.debug("b filled")
                b = child

    if W and b:
        return W, b
    else:
        return None, None


def get_w_daughters(truth):
    ''' Recursive function to get truth particles from W '''
    x = []
    l_truth.debug("---- W children" + str(truth.nChildren()))
    for i in xrange(truth.nChildren()):
        child = truth.child(i)
        l_truth.debug("---- ----" + str(pdgid_to_name(child.pdgId())))
        if child.isW() :
            x = get_w_daughters(child)  # iterate recursively
        elif child.isQuark():
            x.append(child)
    l_truth.debug("x = " + str(x))
    return x


def check_hadronic_decay(top):
    ''' Gets hadronic decay products '''
    W, b = get_w(top) # check for hadronic decay

    daughters = []
    if W:
        daughters = get_w_daughters(W)
    if len(daughters) > 0 : # has daughters
        daughters.insert(0, b) # daughters = [b,W_1,W_2]
        return top, daughters
    else:
        return None, None


def truth_particle_loop(truth_particles):
    ''' Extract the relevant truth particles '''
    l_truth.debug("Number of truth particles: " + str(truth_particles.size()))

    z = None
    top = None
    top_products = None
    anti_top = None
    anti_top_products = None

    # Get final state particles
    for i in xrange(truth_particles.size()):
        truth = truth_particles.at(i)
        # if truth.pdgId() == 32 : # Z'
        #    z = truth
        #    l_truth.debug(debug_string_particle(z))
        if truth.pdgId() == 6 :  # top
            top = truth
            l_truth.debug(debug_string_particle(top))
            top, top_products = check_hadronic_decay(top)
        if truth.pdgId() == -6 :  # anti-top
            anti_top = truth
            l_truth.debug(debug_string_particle(anti_top))
            anti_top, anti_top_products = check_hadronic_decay(anti_top)

    return top, top_products, anti_top, anti_top_products


def top_jet_loop(jets, top, anti_top):
    ''' Finds jets that are closest to the two truth tops '''


    # Initialize delta Rs to high number 
    smallest_delta_r_to_top = 100
    smallest_delta_r_to_anti_top = 100
    delta_r_to_top = 100
    delta_r_to_anti_top = 100

    
    for i in xrange(jets.size()):
        # pt cut is made in the xAOD derivation, we are making 2.0 eta cut
        if jets.at(i).pt() > EXOT_PT_CUT and abs(jets.at(i).eta()) < MAX_ETA:

            jet = jets.at(i)

            l_jet.info(
                "Jet " +
                str(i) +
                "-------------------------------------")
            l_jet.info(debug_string(jet))
            l_jet.debug("Top?" + str(top))
            l_jet.debug("Anti-top?" + str(anti_top))

            # calculate delta Rs
            if top :
                delta_r_to_top = calculate_delta_r_from_particle(top, jet)
                l_jet.debug("Delta r to top: " + str(delta_r_to_top))
            if anti_top :
                delta_r_to_anti_top = calculate_delta_r_from_particle(
                    anti_top, jet)
                l_jet.debug("Delta r to anti-top: " + str(delta_r_to_anti_top))

            # store smallest delta R
            if delta_r_to_top < smallest_delta_r_to_top :
                smallest_delta_r_to_top = delta_r_to_top
                top_jet = jet
                l_jet.debug(
                    "Smallest delta r to top: " +
                    str(smallest_delta_r_to_top))
            if delta_r_to_anti_top < smallest_delta_r_to_anti_top:
                smallest_delta_r_to_anti_top = delta_r_to_anti_top
                anti_top_jet = jet
                l_jet.debug(
                    "Smallest delta r to antitop: " +
                    str(smallest_delta_r_to_anti_top))

            fill_jet_mass_histos(jet,i)
                
    # set jets to None if delta R is too big (no match)
    if smallest_delta_r_to_top > MAX_DELTA_R:
        top_jet = None
    if smallest_delta_r_to_anti_top > MAX_DELTA_R:
        anti_top_jet = None

    # fill relevant histograms
    fill_jet_histograms(top, top_jet, smallest_delta_r_to_top,
                        anti_top, anti_top_jet, smallest_delta_r_to_anti_top)
    
    print("top_jet"+str(top_jet)+", anti_top_jet"+str(anti_top_jet))


    return top_jet, anti_top_jet


def create_vector(jet, truth, signal_type):
    """ Creates the vector to store in final numpy array"""
    # One per jet
    x_jet =  np.zeros(get_column_no['constit start pt'])

    # Implementation may seem a little weird, but prevents 
    # hardcoded values and allows for changes in what to store
    x_jet[get_column_no['label']] = signal_type
    x_jet[get_column_no['jet mass']] =jet.m()
    x_jet[get_column_no['jet pt']] =  jet.pt()/GEV
    x_jet[get_column_no['jet eta']] = jet.eta()
    x_jet[get_column_no['jet phi']] = jet.phi()
    x_jet[get_column_no['Tau32_wta']] = (jet.getAttribute("Tau3_wta")
                                         /jet.getAttribute("Tau2_wta")
                                         if jet.getAttribute("Tau2_wta")
                                         != 0 else -999)
    x_jet[get_column_no['Split23']] = jet.getAttribute("Split23")
    x_jet[get_column_no['Dip12']] =   jet.getAttribute("Dip12")
    x_jet[get_column_no['Qw']] =      jet.getAttribute("Qw")
    x_jet[get_column_no['D2']] =      (jet.getAttribute("ECF3")*jet.getAttribute("ECF1")**3
                                        /jet.getAttribute("ECF2")**3
                                         if jet.getAttribute("ECF2") != 0 else -999)

    if signal_type == 1:
        b, W_1, W_2 = truth
        x_jet[get_column_no['b pt']]    = b.pt() / GEV
        x_jet[get_column_no['b eta']]   = b.eta()
        x_jet[get_column_no['b phi']]   = b.phi()
        x_jet[get_column_no['W_1 pt']]  = W_1.pt() / GEV
        x_jet[get_column_no['W_1 eta']] = W_1.eta()
        x_jet[get_column_no['W_1 phi']] = W_1.phi()
        x_jet[get_column_no['W_2 pt']]  = W_2.pt() / GEV
        x_jet[get_column_no['W_2 eta']] = W_2.eta()
        x_jet[get_column_no['W_2 phi']] = W_2.phi()

    # Loop over all jet constituents
    topos = jet.getConstituents()
    l_jet_sub.info("Size of topos: " +
                   str(topos.size()) +
                   ", Valid? " +
                   str(topos.isValid()))  # roughly half of these are invalid
    y_jet = None
    if topos.isValid():
        topos = sort_topos(topos)
        jet_mass = None
        jet_topo_pt = None
        y_jet = np.zeros((len(topos), 3))

        for index in xrange(len(topos)):
            topo = topos[index] 
            y_jet[index] = np.array([topo.pt() / GEV, topo.eta(), topo.phi()])
            rawCluster = topo.rawConstituent()
            if index == 0:
                jet_mass = rawCluster.p4()
                jet_topo_pt = topo.pt()
            else:
                jet_mass = jet_mass + rawCluster.p4()
                jet_topo_pt = jet_topo_pt + topo.pt()
            # print("topo")
            # print(topo.p4())
            # h_calo_towers_jet_constit[ry].Fill(topo.eta(),
            #                                    topo.phi(),
            #                                    topo.pt()/GEV)

        fill_topo_histograms(jet, jet_topo_pt, jet_mass)

    if y_jet is not None:
        z_jet = np.hstack((x_jet, np.ravel(y_jet)))
        # print(x_jet)
        # print(y_jet)
        # print(x_jet.shape)
        # print(y_jet.shape)
        # pprint(z_jet)
        # print(np.ravel(z_jet))
        return np.ravel(z_jet)
    else:
        return None


def save_jet_constituents(top_jet, top_truth, anti_top_jet, anti_top_truth):
    ''' Returns correctly formatted numpy arrays '''
    top_vec = None
    if anti_top_jet and top_jet :
        top_vec = create_vector(
            top_jet, top_truth, 1), create_vector(
            anti_top_jet, anti_top_truth, 1)
    if anti_top_jet and not top_jet :
        top_vec = create_vector(anti_top_jet, anti_top_truth, 1)
    if top_jet and not anti_top_jet :
        top_vec = create_vector(top_jet, top_truth, 1)
    return top_vec


def process_signal_event(truth_particles, jets):
    """ Extract the truth particles and then compare with the jets """
    top = None
    top_truth = None
    anti_top = None
    anti_top_truth = None
    top_jet = None
    anti_top_jet = None
    event = None

    # Get the truth tops and decay products
    top, top_truth, anti_top, anti_top_truth = truth_particle_loop(
        truth_particles)
    #pdb.set_trace()
    # Find the jets that match the tops
    top_jet, anti_top_jet = top_jet_loop(jets, top, anti_top)
    
    # Extract variables from the truth particles and jets
    event = save_jet_constituents(
        top_jet,
        top_truth,
        anti_top_jet,
        anti_top_truth)
    return event


def process_background_event(jets):
    ''' Returns all jets passing pt cut '''
    vec = []
    new_vec = None
    for i in xrange(jets.size()):
        # pt cut is made in the xAOD derivation, we are making 2.0 eta cut
        if jets.at(i).pt() > EXOT_PT_CUT and abs(jets.at(i).eta()) < MAX_ETA :
            jet = jets.at(i)
            h_jet_pt_cut.Fill(jet.pt() / GEV)
            h_jet_eta_cut.Fill(jet.eta())
            h_jet_phi_cut.Fill(jet.phi())
            new_vec = create_vector(jet, None, 0)

            fill_jet_mass_histos(jet,i)

            if vec:
                vec.append(new_vec)
            else:
                vec = [new_vec]
    return vec


def init_jet_top_histograms():
    ''' Initializes histograms for visualization with ROOT'''
    eta_range = (-3, 3)
    phi_range = (-math.pi, math.pi)
    eta_block_size = 0.1
    phi_block_size = 0.1
    n_bins_eta = int((eta_range[1] - eta_range[0]) / eta_block_size)
    n_bins_phi = int((phi_range[1] - phi_range[0]) / phi_block_size)

    global h_delta_r_top_jet
    h_delta_r_top_jet = ROOT.TH1F(
        'h_delta_r_top_jet',
        'Delta R between top quark and matching jet',
        100,
        0,
        math.pi)
    h_delta_r_top_jet.GetXaxis().SetTitle("$\Delta$ R")

    global h_delta_pt_top_jet
    h_delta_pt_top_jet = ROOT.TH1F(
        'h_delta_pt_top_jet',
        'Delta pt between top and matching jet', 100, -2500, 2500)
    h_delta_pt_top_jet.GetXaxis().SetTitle("p_T [GEV]")

    global h_inv_mass_jet
    h_inv_mass_jet = ROOT.TH1F(
        'h_inv_mass_jet',
        'Invariant mass of two top jets passing selection',
        100,
        0,
        5000)
    h_inv_mass_jet.GetXaxis().SetTitle("Mass [GEV]")

    global h_inv_mass_top
    h_inv_mass_top = ROOT.TH1F(
        'h_inv_mass_top',
        'Invariant mass of two tops ',
        100,
        0,
        5000)
    h_inv_mass_top.GetXaxis().SetTitle("Mass [GEV]")

    global h_delta_pt_delta_r
    h_delta_pt_delta_r = ROOT.TH2F('h_delta_pt_delta_r',
                                   'Delta Pt compared with Delta R',
                                   100, -2500, 2500,
                                   100, 0, 0.75)
    h_delta_pt_delta_r.GetXaxis().SetTitle(" Delta Pt [GEV] ")
    h_delta_pt_delta_r.GetYaxis().SetTitle(" Delta R   ")
    h_delta_pt_delta_r.GetZaxis().SetTitle(" Events  ")

    global h_topo_pt
    h_topo_pt = ROOT.TH1F(
        'h_topo_pt',
        'Transverse momentum of jets calculated from topoclusters',
        250,
        0,
        2500)
    h_topo_pt.GetXaxis().SetTitle("p_T [GEV]")

    global h_jet_pt_cut
    h_jet_pt_cut = ROOT.TH1F(
        'h_jet_pt_cut',
        'Transverse momentum of jets passing selection',
        250,
        0,
        2500)
    h_jet_pt_cut.GetXaxis().SetTitle("p_T [GEV]")

    global h_jet_eta_cut
    h_jet_eta_cut = ROOT.TH1F(
        'h_jet_eta_cut',
        'Eta distribution of jets passing selection',
        n_bins_eta,
        eta_range[0],
        eta_range[1])
    h_jet_eta_cut.GetXaxis().SetTitle("Eta")

    global h_jet_phi_cut
    h_jet_phi_cut = ROOT.TH1F(
        'h_jet_phi_cut',
        'Phi distribution of jets passing selection',
        n_bins_phi,
        phi_range[0],
        phi_range[1])
    h_jet_phi_cut.GetXaxis().SetTitle("Phi [rad]")

    global h_jet_mass
    h_jet_mass = ROOT.TH1F(
        'h_jet_mass', 'Jet mass of jets passing selection', 100, -1e-4, 250)
    h_jet_mass.GetXaxis().SetTitle("m [GEV]")

    global h_jet_mass_from_raw
    h_jet_mass_from_raw = ROOT.TH1F(
        'h_jet_mass_from_raw',
        'Jet mass of jets passing selection', 100, -1e-4, 250)
    h_jet_mass_from_raw.GetXaxis().SetTitle("m [GEV]")

    global h_jet_mass_after_pt_cut
    h_jet_mass_after_pt_cut = ROOT.TH1F(
        'h_jet_mass_after_pt_cut',
        'Jet mass of jets passing pt cut', 100, -1e-4, 250)
    h_jet_mass_after_pt_cut.GetXaxis().SetTitle("m [GEV]")

    global h_jet_mass_after_pt_and_m_cuts
    h_jet_mass_after_pt_and_m_cuts = ROOT.TH1F(
        'h_jet_mass_after_pt_and_m_cuts',
        'Jet mass of jets passing pt and mass cut', 100, -1e-4, 250)
    h_jet_mass_after_pt_and_m_cuts.GetXaxis().SetTitle("m [GEV]")

    global h_first_jet_mass
    h_first_jet_mass = ROOT.TH1F(
        'h_first_jet_mass', 'Jet mass of leading jet', 100, -1e-4, 250)
    h_first_jet_mass.GetXaxis().SetTitle("m [GEV]")

    global h_second_jet_mass
    h_second_jet_mass = ROOT.TH1F(
        'h_second_jet_mass', 'Jet mass of second jets', 100, -1e-4, 250)
    h_second_jet_mass.GetXaxis().SetTitle("m [GEV]")

    global h_other_jet_mass
    h_other_jet_mass = ROOT.TH1F(
        'h_other_jet_mass', 'Jet mass of other jets', 100, -1e-4, 250)
    h_other_jet_mass.GetXaxis().SetTitle("m [GEV]")

    global h_jet_mass_pt
    h_jet_mass_pt = ROOT.TH2F('h_jet_mass_pt', '',
                              100, 0, 4000,
                              100, -1e-4, 250)
    h_jet_mass_pt.GetXaxis().SetTitle(" Jet p_t [GEV] ")
    h_jet_mass_pt.GetYaxis().SetTitle(" Jet mass [GEV]   ")
    h_jet_mass_pt.GetZaxis().SetTitle(" Jets ")

def fill_jet_mass_histos(jet,i):
    if i == 0:
        h_first_jet_mass.Fill(jet.m() / GEV)
    elif i == 1:
        h_second_jet_mass.Fill(jet.m() / GEV)
    else:
        h_other_jet_mass.Fill(jet.m() / GEV)
    return 

def fill_jet_histograms(top, top_jet, smallest_delta_r_to_top,
                        anti_top, anti_top_jet, smallest_delta_r_to_anti_top):
    ''' Fills histograms related to jet pt, mass and delta r '''
    
    if top_jet :
        h_delta_r_top_jet.Fill(smallest_delta_r_to_top)
        h_delta_pt_top_jet.Fill((top.pt() - top_jet.pt()) / GEV)
        h_jet_pt_cut.Fill(top_jet.pt() / GEV)
        h_jet_eta_cut.Fill(top_jet.eta())
        h_jet_phi_cut.Fill(top_jet.phi())
    if anti_top_jet:
        h_delta_r_top_jet.Fill(smallest_delta_r_to_anti_top)
        h_delta_pt_top_jet.Fill((anti_top.pt() - anti_top_jet.pt()) / GEV)
        h_jet_pt_cut.Fill(anti_top_jet.pt() / GEV)
        h_jet_eta_cut.Fill(anti_top_jet.eta())
        h_jet_phi_cut.Fill(anti_top_jet.phi())
    
    if top_jet and anti_top_jet:
        h_inv_mass_jet.Fill((top_jet.p4() + anti_top_jet.p4()).M() / GEV)
    if top and anti_top:
        h_inv_mass_top.Fill((top.p4() + anti_top.p4()).M() / GEV)
    
    if top and top_jet:
        h_delta_pt_delta_r.Fill(
            (top.pt() - top_jet.pt()) / GEV,
            smallest_delta_r_to_top)
    if anti_top and anti_top_jet:
        h_delta_pt_delta_r.Fill(
            (anti_top.pt() - anti_top_jet.pt()) / GEV,
            smallest_delta_r_to_anti_top)
    return

def fill_topo_histograms(jet, jet_topo_pt, jet_mass):
    ''' Fills histograms '''
    h_jet_mass.Fill(jet.m() / GEV)
    h_topo_pt.Fill(jet_topo_pt / GEV)
    h_jet_mass_from_raw.Fill(jet_mass.M() / GEV)
    if jet.pt() > JET_FLAT_CUT_LOW and jet.pt() < JET_FLAT_CUT_HIGH:
        h_jet_mass_after_pt_cut.Fill(jet.m() / GEV)
        if jet.m() > JET_MASS_CUT:
            h_jet_mass_after_pt_and_m_cuts.Fill(jet.m() / GEV)
    h_jet_mass_pt.Fill(jet.pt() / GEV, jet.m() / GEV)
    # if jet_mass<= 0.0:
    #     print ("jet_mass"+str(jet_mass.M()/GEV))
    #     print("num constituents "+str(len(topos)))
    #     print("jet pt "+str(jet.pt()))

def check_efficiencies():
    ''' Calculates and prints efficiencies of cuts '''
    num_jet_mass = h_jet_mass.Integral()
    num_jet_mass_after_pt_cut = h_jet_mass_after_pt_cut.Integral()
    num_jet_mass_after_pt_and_m_cuts = h_jet_mass_after_pt_and_m_cuts.Integral()
    if num_jet_mass != 0:
        pt_cut_efficiency = num_jet_mass_after_pt_cut / num_jet_mass
        print("pt cut efficiency: " + str(pt_cut_efficiency))
    if num_jet_mass_after_pt_cut != 0:
        pt_and_m_cut_efficiency = (
            num_jet_mass_after_pt_and_m_cuts / num_jet_mass_after_pt_cut)
        print("pt and m cut efficiency:" + str(pt_and_m_cut_efficiency))
    return 

def process_events(file_name):
    
    # Setup global constants
    global GEV
    global MAX_DELTA_R 
    global MAX_ETA
    global EXOT_PT_CUT
    global JET_FLAT_CUT_LOW
    global JET_FLAT_CUT_HIGH
    global JET_MASS_CUT

    GEV = 1000.0
    MAX_DELTA_R = 0.75
    MAX_ETA = 2.0
    EXOT_PT_CUT = 150e3
    JET_FLAT_CUT_LOW = 650e3
    JET_FLAT_CUT_HIGH = 1800e3
    JET_MASS_CUT =  100e3

    global l_truth
    global l_jet
    global l_jet_sub

    # Setup loggers
    l_truth = logging.getLogger("truth logger")
    l_jet = logging.getLogger("jet logger")
    l_jet_sub = logging.getLogger("jet sub logger")

    l_truth.setLevel(logging.ERROR)
    l_jet.setLevel(logging.ERROR)
    l_jet_sub.setLevel(logging.ERROR)

    gROOT.ProcessLine(".x $ROOTCOREDIR/scripts/load_packages.C")

    output_file_name = parse_file_name(file_name)

    treeName = "CollectionTree"
    f = ROOT.TFile.Open(file_name)
    t = ROOT.xAOD.MakeTransientTree(f, treeName)
    f_out = ROOT.TFile(output_file_name, "recreate")
    logging.info("Number of input events: %s" % t.GetEntries())

    # Initialize histograms
    init_jet_top_histograms()

    data = []

    # Loop over all events
    #for entry in xrange(t.GetEntries()):
    for entry in xrange(1000):
        t.GetEntry(entry)

        if entry % 100 == 0 and entry != 0:
            logging.info("Processing event: " + str(entry))
        
        event = None

        if "_tt" in file_name: # signal
            event = process_signal_event(
                t.TruthParticles,
                t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets)
            # (t.AntiKt10LCTopoJets)
            # print("Warning using untrimmed")

            if event is not None:
                if type(event).__module__ == np.__name__:
                    data.append(event)
                else:
                    data.append(event[0])
                    data.append(event[1])

        elif "jetjet" in file_name : # background
            event = process_background_event(
                t.AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets)
            if event:
                data.extend(event)
  
    # Save numpy array
    np.savez_compressed(output_file_name.replace(".root", ""), data=data)
    logging.info(
        "Saved numpy array as: " +
        output_file_name.replace(
            ".root",
            ".npz"))  

    check_efficiencies()

    f_out.Write()
    f_out.Close()
    f.Close()
    ROOT.xAOD.ClearTransientTrees()

    return
