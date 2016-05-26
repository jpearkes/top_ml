import numpy as np 
from pprint import pprint
import matplotlib as mpl
import matplotlib.pyplot as plt
import time 
import logging
import math



class bin:
    """Bin checker """
    count = 0 
    start = 0
    stop = 0
    full = False

    def __init__(self, start, stop):
        self.count = 0 
        self.start = start
        self.stop = stop
    def in_bin(self, number):
        if(number>=self.start and number< self.stop):
            self.count += 1
            if self.count > max_count:
                self.full = True
            return True
        else:
            return False
    def is_full(self):
        if self.count < max_count:
            return False 
        if self.count >= max_count:
            self.full = True
            return True 
    def print_object(self):
        logging.debug("["+str(self.start)+","+str(self.stop)+")")
        logging.debug("Count:"+str(self.count))
        logging.debug("Full? "+str(self.full))


def make_histogram(dist, name, x_min, x_max, bin_width, title, x_label):
    plt.cla()
    plt.figure()
    #print([new_array[i][0][0] for i in range(rows)])
    p = plt.hist( dist,
                  #range=[min_x_calc,max_x_calc],
                  bins = np.arange(x_min, x_max + bin_width, bin_width),
                  #weights = [real_background[:,-2],real_signal[:,-2]],
                  label = ['signal'],
                  linewidth = 0.0, 
                  edgecolor = None,
                  #histtype = 'barstacked',
                  color = 'blue',
                  alpha = 0.5 )
    plt.legend(loc=1,prop={'size':12})
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Events")
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x_min,x_max,y1,y2+5)) 
    logging.info("Saving figure as "+"../plots/"+name+".png") 
    plt.savefig("../plots/"+name+".png")
    return
 
def make_pt_histogram(dist):
    x_min = 0 
    x_max = 2500
    bin_width = 10
    title = "Distribution of transverse momentum for jets passing selection"
    name = "pt"
    x_label = "p_T [GeV]"
    make_histogram(dist, name, x_min, x_max, bin_width, title, x_label)
    return 

def make_eta_histogram(dist):
    x_min = -3
    x_max = 3
    bin_width = 0.1
    title = "Eta distribution for jets passing selection"
    name = "eta"
    x_label = "Eta"
    make_histogram(dist, name, x_min, x_max, bin_width, title, x_label)
    return 

def make_phi_histogram(dist):
    x_min = -math.pi
    x_max = math.pi
    bin_width = 0.1
    title = "Phi distribution for jets passing selection"
    name = "phi"
    x_label = "Phi [rad]"
    make_histogram(dist, name, x_min, x_max, bin_width, title, x_label)
    return 

def plot_jet_histograms(dist):
    rows,cols = dist.shape
    make_pt_histogram([dist[i][0][0] for i in range(rows)])
    make_eta_histogram([dist[i][0][1] for i in range(rows)])
    make_phi_histogram([dist[i][0][2] for i in range(rows)])
    return 

def get_flat_distribution(y):
    start = time.time()
    logging.debug(y.shape)
    rows,cols = y.shape
    x_min = 0 
    x_max = 2500
    bin_width = 100
    n_bins = int((x_max-x_min)/bin_width)
    lst = [bin(i,i+bin_width) for i in np.arange(x_min,x_max,bin_width)]
    new_array = np.zeros((1,2))
    new_array_list = []

    for row in xrange(rows):
        if row == 0:
            new_array_list.append(y[row])
            [lst[i].in_bin(y[0][0][0]) for i in range(n_bins)]
        else:
            for i in range(n_bins):
                if(lst[i].in_bin(y[row][0][0]) and not lst[i].full):
                    new_array_list.append(y[row])
            if(row%1000000 == 0):
                logging.debug(row)
    stop = time.time()
    logging.debug("time elapsed running through rows"+str(stop - start))
    new_array = np.vstack(new_array_list)
    stop = time.time()
    logging.debug("time elapsed stacking"+str(stop - start))
    logging.debug("new array shape:")
    logging.debug(new_array.shape)
    
    rows,cols = new_array.shape
    [lst[i].print_object() for i in range(n_bins)]
    np.savez(file_name+"flat", new_array)
    return new_array

def load_data(file_name):
    start = time.time()
    logging.debug("loading array")
    x = np.load(file_name)
    #y = x['data']

    y = x['arr_0']
    #y = y[0:5,:] # mini array for testing

    logging.debug("done loading")
    stop = time.time()
    logging.debug("Time for loading:"+str(stop-start))
    return y

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')  
    
    file_name = "master_zprime_array.npz"
    max_count = 16000 #87000 #################
    #file_name = "../outputs/zprime400_000001jet_inv_mass.npz"
    flat_distribution = get_flat_distribution(load_data(file_name))
    plot_jet_histograms(flat_distribution)






