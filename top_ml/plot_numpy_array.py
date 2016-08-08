""" Plots all outputs from numpy arrays automatically """

import argparse
import os
from top_ml.column_definition import *
from top_ml.utils import load_data,load_data2
import matplotlib.pyplot as plt
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merges numpy arrays of same type and applies weights")
    parser.add_argument("numpy_arrays", metavar='NUMPY_ARRAYS',type=str,
                        nargs='+',help="Name of numpy arrays to plot")
    parser.add_argument("--feature", metavar='FEATURE_ARRAYS',type=str,
                        nargs='+',help="Features to plot")
    parser.add_argument("-s", "--save", action="store_true",
                    help="save output files")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
    args = parser.parse_args()
    return args


def plot_features(x,features):
    
    label = np.array([int(x[row][get_column_no['label']]) for row in range(len(x))])
    weight = np.array([x[row][get_column_no['weight']] for row in range(len(x))])
    print(label[0:20])   
    sig_rows = np.where(label == 1) #hi
    bkg_rows = np.where(label == 0)
    print(sig_rows[0:20])
    print(bkg_rows[0:20])

    sig_weight = weight[sig_rows]
    bkg_weight = weight[bkg_rows]
    print("weights:")
    print(weight)


    features = [get_column_name[i] for i in range(10)]
    for f in features:

        feature = np.array([x[row][get_column_no[f]] for row in range(len(x))])
        sig_feature = feature[sig_rows]
        bkg_feature = feature[bkg_rows]
        print("label")
        print(label[0:20])
        print("weight")
        print(weight[0:20])
        print("feature")
        print(feature[0:20])
        hfont = {'fontname':'Helvetica'}
        plt.figure(f)
        plt.hist(feature[sig_rows],
                 weights=weight[sig_rows],
                 bins=100,
                 #range=[650, 1700],
                 label=['Signal'],
                 histtype='step',
                 color='red',
                 alpha=0.5)
        plt.hist(feature[bkg_rows],
                 weights=bkg_weight,
                 bins=100,
                 #range=[650, 1700],
                 label=['Background'],
                 histtype='step',
                 color='blue',
                 alpha=0.5)
        plt.legend(loc='upper right', prop={'size':12})
        #plt.title(feature)
        plt.xlabel(f)
        plt.ylabel("Jets")
        x1, x2, y1, y2 = plt.axis()
        plt.axis((x1, x2, y1, y2+y2*0.05))
        if x2>1000:
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        if y2>1000:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #name = "sig_bkg_pt"
    #logging.info("Saving figure as "+name+".png")
    #plt.savefig(name+".png")
    plt.show()
if __name__ == '__main__':

    #plt.rcParams[font.family]='cursive' 
     # -- Parse arguments
    path = "/home/jpearkes/top_tagging/plots/"
    args = parse_args()
    plt.cla()
    # -- Check that files exist
    if len(args.numpy_arrays) == 0:
        raise ValueError("No files were given")
    for f in args.numpy_arrays:
        if not os.path.isfile(f):
            raise ValueError("File: "+f+" does not exist."
                             +"Please provide correct path")
        x = load_data2(f)
        plot_features(x,args.feature)

    # -- Start merging

    # -- Save merged arrays
    if args.save:
        print("Saving arrays")
        
        print("Done saving")

    # -- Finish
    print("Plotting")
