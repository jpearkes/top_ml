'''Slims down samples by performing a pt cut'''

import sys
import os
import argparse
import numpy as np
from top_ml.column_definition import *

def parse_args():
    parser = argparse.ArgumentParser(
        description="Applies pt cut to all inputs in numpy array")
    parser.add_argument("file_name", type=str,help="Stored file names")
    parser.add_argument("--low", type=int,
                        help="lower threshold on pt cut", default=600)
    parser.add_argument("--high", type=int,
                        help="upped threshold on pt cut", default=2000)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # -- Parse arguments
    merged_path = "/data/jpearkes/top_tagging/merged/"
    slimmed_path = merged_path
    args = parse_args()

    # -- Set up file paths
    file_loc = args.file_name

    # -- Check that files exist
    if not os.path.isfile(file_loc):
        raise ValueError("File: "+file_loc+" does not exist."
                             +"Please provide correct path")

    # -- Load file
    print("Loading " + file_loc)
    info = np.load(file_loc)
    x_data = info['data']
    print("Initial array shape" + str(x_data.shape))

    # -- Perform pt cut
    rows = []
    for row in range(len(x_data)):
        if (x_data[row][get_column_no['jet pt']] > args.low 
            and x_data[row][get_column_no['jet pt']] < args.high ):
                rows.append(row)
    x_data = x_data[rows]
    print("Final array shape" + str(x_data.shape))

    # -- Save merged arrays
    print("Saving arrays")
    np.savez(file_loc.replace(".npz", "")+"_"+str(args.low)+"_"+str(args.high)+".npz", data=x_data)
    print("Done saving")

    # -- Finish
    print("Pt cut complete")