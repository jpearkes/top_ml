#! /usr/bin/env python
""" Runs over input DAODs """
import sys
import logging
from top_ml import process_events

if __name__ == '__main__':

    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s - %(message)s')   

    # Parse args
    if len(sys.argv) >= 2:
        # Read in filename as input
        name, file_name = sys.argv
    else:
        # Use a default filename
        # zprime tt 400
        #file_name = "/data/wfedorko/mc15_13TeV.301322.Pythia8EvtGen_A14NNPDF23LO_zprime400_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07896478_00/DAOD_EXOT7.07896478._000001.pool.root.1"
        # zprime tt 1000
        #file_name = "/data/wfedorko/mc15_13TeV.301325.Pythia8EvtGen_A14NNPDF23LO_zprime1000_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618490_00/DAOD_EXOT7.07618490._000001.pool.root.1"
        # zprime tt 2000
        #file_name = "/data/wfedorko/mc15_13TeV.301329.Pythia8EvtGen_A14NNPDF23LO_zprime2000_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618440_00/DAOD_EXOT7.07618440._000001.pool.root.1"
        # zprime tt 2250
        #file_name = "/data/wfedorko/mc15_13TeV.301330.Pythia8EvtGen_A14NNPDF23LO_zprime2250_tt.merge.DAOD_EXOT7.e4061_s2608_s2183_r7326_r6282_p2495_tid07618509_00/DAOD_EXOT7.07618509._000010.pool.root.1"
        # zprime tt 3000
        #file_name = "/data/wfedorko/mc15_13TeV.301333.Pythia8EvtGen_A14NNPDF23LO_zprime3000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618517_00/DAOD_EXOT7.07618517._000001.pool.root.1"
        # zprime tt 4000
        #file_name = "/data/wfedorko/mc15_13TeV.301334.Pythia8EvtGen_A14NNPDF23LO_zprime4000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618446_00/DAOD_EXOT7.07618446._000001.pool.root.1"
        # zprime tt 5000
        #file_name = "/data/wfedorko/mc15_13TeV.301335.Pythia8EvtGen_A14NNPDF23LO_zprime5000_tt.merge.DAOD_EXOT7.e3723_s2608_s2183_r7326_r6282_p2495_tid07618499_00/DAOD_EXOT7.07618499._000005.pool.root.1"
        # dijet
        file_name = "/data/wfedorko/mc15_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.merge.DAOD_EXOT7.e3668_s2576_s2132_r7267_r6282_p2495_tid07618436_00/DAOD_EXOT7.07618436._000001.pool.root.1"

    logging.info("Input file: "+file_name)
    process_events(file_name)
