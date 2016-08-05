import numpy as np
import glob
import sys
import os
import argparse
from top_ml.utils import regex_search
from top_ml.dijet_weights import weights

'''
Merges numpy arrays of same type and applies weights
Weights are stored in dijet_weights.py 
'''

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merges numpy arrays of same type and applies weights")
    parser.add_argument("prefix", type=str,help="Beginning of stored file names")
    parser.add_argument("suffix", type=str, help="End of stored file names")
    parser.add_argument("--weights", type=str,
                        help="file with dictionary of weights", default="dijet_weights.py")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
    args = parser.parse_args()
    return args

def get_weight(file_name):
    weight = 0
    if "zprime" in file_name or "rsg" in file_name:
        weight = 1.0
    elif "JZ" in file_name:
        jzxw = int(regex_search(file_name, 'JZ(\d+)W').group(1))
        weight = weights[jzxw]
    else:
        raise ValueError("File name: "+file_name
                         +" matches no specification for weights \n"
                         +"Name must contain zprime, rsg, or JZ")
    return weight


if __name__ == '__main__':
    # -- Parse arguments
    path = "/data/jpearkes/top_tagging/outputs/"
    merged_path = "/data/jpearkes/top_tagging/merged/"
    args = parse_args()

    # -- Set up file paths
    file_loc = path+args.prefix+"*"+args.suffix+".npz"
    files = glob.glob(file_loc)

    # -- Check that files exist
    if len(files) == 0:
        raise ValueError("No files matching "+file_loc+" were found")
    print("Merging "+str(len(files))+" files found at: "+file_loc)
    print("Using weights found at: "+args.weights)

    # -- Start merging
    i = 0
    array_list = []
    for file_name in files:
        print("Loading " + file_name)
        info = np.load(file_name,encoding='latin1')
        weight = get_weight(file_name)
        print(weight)
        x_data = info['data']
        i += 1
        print("Array shape" + str(x_data.shape))
        print(str(i)+"/"+str(len(files)))
        shape = x_data.shape
        for row in range(shape[0]):
            x_data[row][0] = np.array(x_data[row][0])
            x_data[row][1] = np.array(x_data[row][1])
            x_data[row] = np.append(weight,x_data[row])
    array_list.extend(x_data)

    # -- Save merged arrays
    print("Saving arrays")
    np.savez(merged_path+args.prefix+"_all_"+args.suffix+".npz", data=array_list)
    print("Done saving")

    # -- Finish
    print("Merging complete")
