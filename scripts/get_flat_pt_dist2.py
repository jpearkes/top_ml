
import time
import logging
import sys
import pdb
import numpy as np
from matplotlib import pyplot as plt
from random import shuffle
"""
# extract flat pt distribution from signal
# - first get pt distribution for a particular binning
# - find smallest bin
# - cut there
# - add in signal label

# from flat pt distribution
# - extract eta distribution

# from background distribution
# - want number of events in a certain pt bin and an eta bin to match
# - go through array and fill for pt and eta if not full already

# plot pt,eta,phi distributions for signal and background for comparision

# shuffle and save output as hdf5 file
"""
class bin:
    """Bin checker """
    count = 0
    start = 0
    stop = 0
    full = False
    def __init__(self, start, stop, max_count):
        self.count = 0
        self.max_count = max_count
        self.start = start
        self.stop = stop
        if (self.count >= self.max_count):
            self.full = True
        else:
            self.full = False
    def in_bin(self, value):
        if value >= self.start and value < self.stop:
            return True
        else:
            return False
    def add_to_bin(self, value):
        if value >= self.start and value < self.stop:
            self.count += 1
        if self.count >= self.max_count:
            self.full = True
    def is_full(self):
        if self.count < max_count:
            return False
        if self.count >= max_count:
            self.full = True
            return True
    def print_object(self):
        logging.debug("["+str(self.start)+","+str(self.stop)+")")
        logging.debug("Count:"+str(self.count)+" out of "+str(self.max_count))
        logging.debug("Full? "+str(self.full))

class bin_2d:
    """Bin checker """
    count = 0
    start_x = 0
    stop_x = 0
    start_y = 0
    stop_y = 0
    full = False
    def __init__(self, start_x, stop_x, start_y, stop_y, max_count):
        self.count = 0
        self.max_count = max_count
        self.start_x = start_x
        self.stop_x = stop_x
        self.start_y = start_y
        self.stop_y = stop_y
        if (self.count >= self.max_count):
            self.full = True
        else:
            self.full = False
    def in_bin(self, value_x, value_y):
        if ((value_x >= self.start_x and value_x < self.stop_x)
            and (value_y >= self.start_y and value_y < self.stop_y):
            return True
        else:
            return False
    def add_to_bin(self, value):
        if ((value_x >= self.start_x and value < self.stop_x)
            and (value_y >= self.start_y and value_y < self.stop_y)):
            self.count += 1
        if self.count >= self.max_count:
            self.full = True
    def is_full(self):
        if self.count < max_count:
            return False
        if self.count >= max_count:
            self.full = True
            return True
    def print_object(self):
        logging.debug("["+str(self.start_x)+","+str(self.stop_x)+")")
        logging.debug("["+str(self.start_y)+","+str(self.stop_y)+")")
        logging.debug("Count:"+str(self.count)+" out of "+str(self.max_count))
        logging.debug("Full? "+str(self.full))

def load_data(file_name):
    start = time.time()
    logging.debug("loading array")
    x = np.load(file_name)
    x_data = x['data']# x['arr_0']
    shuffle(x_data)
    logging.debug("done loading")
    stop = time.time()
    logging.debug("Time for loading:"+str(stop-start))
    return x_data

def cut_pt(signal_events, bin_edges, minimum_bin):
    #pdb.set_trace()
    # Create list of bin objects
    start = time.time()
    bin_edges = bin_edges[:-2]
    pt_lst = [bin(bin_edges[i], bin_edges[i+1], minimum_bin) for i in range(bin_edges.size-1)]
    new_array = np.zeros((1, 2))
    new_array_list = []
    rows = signal_events.size

    # check if in bins
    for row in range(rows):
        for i in range(bin_edges.size-1):
            if not pt_lst[i].full and pt_lst[i].in_bin(signal_events[row][0]) and signal_events[row][0]<1800:
                pt_lst[i].add_to_bin(signal_events[row][0])
                new_array_list.append(signal_events[row])
        if row%1000 == 0:
            logging.debug(row)

    stop = time.time()
    logging.debug("time elapsed running through rows"+str(stop - start))
    #new_array = np.vstack(new_array_list)
    stop = time.time()
    logging.debug("time elapsed stacking"+str(stop - start))
    logging.debug("new array shape:")
    logging.debug(len(new_array_list))

    [pt_lst[i].print_object() for i in range(bin_edges.size-1)]

    return new_array_list

def find_minimum_bin(signal_hist, bin_edges):
    # still have to decide on how to implement this
    min_bin = 10000000000 # some very large number
    min_bin_i = 0
    for i in range(len(bin_edges)):
        bin = bin_edges[i]
        if bin > 650 and bin <= 1800:
            if signal_hist[i] < min_bin:
                min_bin = signal_hist[i]
                min_bin_i = i
                print("min bin"+str(min_bin))
    if (min_bin == 0):
        logging.error("MIN BIN = 0")
        min_bin = 10
    return min_bin, min_bin_i

def plot_histogram_info(name, flat_signal_hist, bin_edges):
    plt.cla()
    plt.figure()
    #print([new_array[i][0][0] for i in range(rows)])
    plt.hist(flat_signal_hist,
             #range=[min_x_calc,max_x_calc],
             bins=bin_edges,
             #bins=bin_edges,
             range=[650, 1800],
             #weights=[real_background[:,-2],real_signal[:,-2]],
             label=['Signal'],
             linewidth=0.0,
             edgecolor=None,
             #histtype='barstacked',
             color='blue',
             alpha=0.5)
    plt.legend(loc=1, prop={'size':12})
    plt.title(name+" transverse momentum distribution of signal events")
    plt.xlabel("pT [GeV]")
    plt.ylabel("Events")
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, y1, y2+y2*0.05))
    logging.info("Saving figure as "+"../plots/"+name+".png")
    plt.savefig("../plots/"+name+".png")
    return

def plot_histogram_info_eta(name, flat_signal_hist, bin_edges):
    plt.cla()
    plt.figure()
    #print([new_array[i][0][0] for i in range(rows)])
    plt.hist(flat_signal_hist,
             #range=[min_x_calc,max_x_calc],
             bins=100,
             #bins=bin_edges,
             range=[-2.7, 2.7],
             #weights=[real_background[:,-2],real_signal[:,-2]],
             label=['Signal'],
             linewidth=0.0,
             edgecolor=None,
             #histtype='barstacked',
             color='blue',
             alpha=0.5)
    plt.legend(loc=1, prop={'size':12})
    plt.title(name+" eta distribution of background events")
    plt.xlabel("Eta")
    plt.ylabel("Events")
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, y1, y2+y2*0.05))
    logging.info("Saving figure as "+"../plots/"+name+".png")
    plt.savefig("../plots/"+name+".png")
    return


def extract_flat_distribution_from_signal(file_name):
    signal_events = load_data(file_name)
    #logging.debug([signal_events[i][0][0] for i in range(len(signal_events))])
    signal_hist, bin_edges = np.histogram([signal_events[i][0] for i in range(len(signal_events))],
                                          bins=100, range=[650, 2600],
                                          normed=False, weights=None,
                                          density=None)
    plot_histogram_info("Original", [signal_events[i][0]
                                     for i in range(len(signal_events))], bin_edges)
    logging.debug("Signal histogram")
    logging.debug(signal_hist)
    logging.debug("Bin edges")
    logging.debug(bin_edges)
    minimum_bin, min_bin_i = find_minimum_bin(signal_hist, bin_edges) #find the bin in the range of
    flat_signal_hist = cut_pt(signal_events, bin_edges, minimum_bin)
    plot_histogram_info("Flat", [flat_signal_hist[i][0]
                                 for i in range(len(flat_signal_hist))], bin_edges)
    np.savez("signal", data=flat_signal_hist)
    return flat_signal_hist


def extract_flat_distribution_from_background(signal_events,background_file_name):
    background_events = load_data(background_file_name)
    signal_pt_hist, bin_pt_edges = np.histogram([signal_events[i][0]
                                                 for i in range(len(signal_events))],
                                                bins=100, range=[650, 2600],
                                                normed=False, weights=None,
                                                density=None)
    signal_eta_hist, bin_eta_edges = np.histogram([signal_events[i][1]
                                                   for i in range(len(signal_events))],
                                                  bins=100, range=[-2.7, 2.7],
                                                  normed=False, weights=None,
                                                  density=None)
    # fill bins in pt and eta
    pt_lst = [bin(bin_pt_edges[i], bin_pt_edges[i+1], signal_pt_hist[i])
              for i in range(bin_pt_edges.size-1)]
    eta_lst = [bin(bin_eta_edges[i], bin_eta_edges[i+1], signal_eta_hist[i])
               for i in range(bin_eta_edges.size-1)]
    pt_eta_lst = [bin_2d]

    new_array_list = []
    rows = len(background_events)
    print(rows)
    print(background_events.shape)
    # check if in bins
    for row in range(rows):
        if (all([pt_lst[i].full for i in range(bin_pt_edges.size-1)])
             and all([eta_lst[i].full in range(bin_eta_edges.size-1)])):
            break
        for i in range(bin_pt_edges.size-1):
            if (not pt_lst[i].full 
                and pt_lst[i].in_bin(background_events[row][0])
                and background_events[row][0]<1800
                and not eta_lst[i].full
                and eta_lst[i].in_bin(background_events[row][1]) :
                #for j in range(bin_eta_edges.size-1):
                #    if not eta_lst[j].full and eta_lst[j].in_bin(background_events[row][1]):
                        pt_lst[i].add_to_bin(background_events[row][0])
                        eta_lst[j].add_to_bin(background_events[row][1])
                        new_array_list.append(background_events[row])
        if row%1000 == 0:
            logging.debug(row)
    [pt_lst[i].print_object() for i in range(bin_pt_edges.size-1)]
    [eta_lst[i].print_object() for i in range(bin_pt_edges.size-1)]
    plot_histogram_info("matched_pt",
                        [new_array_list[i][0] for i in range(len(new_array_list))],
                        bin_pt_edges)
    plot_histogram_info_eta("matched_eta",
                            [new_array_list[i][1] for i in range(len(new_array_list))],
                            bin_pt_edges)
    np.savez("background",data = new_array_list)
    return new_array_list, bin_pt_edges, bin_eta_edges

def save_files(signal, background, bin_pt_edges, bin_eta_edges):
    plot_histogram_info("flat_sig", [signal[i][0] for i in range(len(signal))], bin_pt_edges)
    plot_histogram_info_eta("flat_sig_eta", [signal[i][1] for i in range(len(signal))], bin_eta_edges)
    plot_histogram_info("flat_bg", [background[i][0] for i in range(len(background))], bin_pt_edges)
    plot_histogram_info_eta("flat_bg_eta", [background[i][1] for i in range(len(background))], bin_eta_edges)

    signal =[np.insert(row,0, 1) for row in signal]
    background = [np.insert(row,0, 0) for row in background]
    print("signal length:"+str(len(signal)))
    print("background length:"+str(len(background)))

    full_array = signal+background
    print("full length:"+str(len(full_array)))
    #print(full_array)
    np.savez("signal_and_background", data=full_array)
    return 

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')
    if len(sys.argv) >= 2:
        script_name, test = sys.argv
    else:
        test = 0
    if test == 0:
        signal_file_name = "zprime_all_june.npz" #"master_zprime_array.npz"
        background_file_name = "dijet_all_june.npz"
    else:
        signal_file_name = "../outputs/test_efficiency/zprime2000_000001test_efficiency.npz"
        background_file_name = "../outputs/test_efficiency/dijetJZ8W_000006test_efficiency.npz"

    flat_signal_distribution = extract_flat_distribution_from_signal(signal_file_name)
    flat_background_distribution, bin_pt_edges, bin_eta_edges = extract_flat_distribution_from_background(flat_signal_distribution,
                                                                             background_file_name)
    #pdb.set_trace()
    save_files(flat_signal_distribution,flat_background_distribution, bin_pt_edges, bin_eta_edges)
    #plot_jet_histograms(flat_distribution,"main2")

