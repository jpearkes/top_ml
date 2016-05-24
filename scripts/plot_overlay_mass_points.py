"""
Overlays multiple histograms at different mass points
"""
import ROOT
from ROOT import TCanvas, TF1, TLegend
import glob
import re
import logging as l
from pprint import pprint

def plot_histograms():
    """ Overlays multiple histograms at different mass points"""
    def regex_search(file_name, regex):
        ''' Searches for a regex value in a line'''
        search = re.compile(regex)
        value = search.search(file_name)
        return value

    def parse_file_names(files):
        '''Parses file names to find mass points'''
        energies = []
        for file_name in files:
            zprimexxx = regex_search(file_name, 'zprime(\\d+)')
            if zprimexxx:
                energies.append(zprimexxx.group(1))
            else:
                l.error("Error files names not consistent")
        l.debug("File names:"+str(files))
        l.debug("Energies: "+str(energies))
        return energies

    files = glob.glob("outputs/zprime*_000000*z_prime.root")
    energies = parse_file_names(files)
    colours = [ROOT.kBlack, ROOT.kBlue, ROOT.kViolet, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]
    print(colours)
    energies_files = zip(energies, files)
    energies_files.sort()
    pprint(energies_files)
    energies_colours = zip(energies, colours)
    energies_colours.sort()
    pprint(energies_colours)
    files = [y for x, y in energies_files]
    colours = [y for x, y in energies_colours]
    print(files)
    print(energies)
    print(colours)

    entries = ["delta_r", "h_delta_r_top_W",
               "h_delta_r_top_b", "h_z_prime_pt",
               "h_z_prime_eta", "h_z_prime_phi", "delta_r_top_jet"]
    l.debug("Files: "+str(files))
    l.debug("Files length: "+str(len(files)))

    tree = [None]*len(files)
    feil = [None]*len(files)
    canvas = [None]*len(entries)
    ROOT.gStyle.SetOptStat(0)
    for j in xrange(len(entries)):
        canvas[j] = TCanvas('c'+str(j), entries[j], 200, 10, 700, 500)
        legend = TLegend(0.7, 0.15, 0.85, 0.35)
        legend.SetBorderSize(0)
        legend.SetHeader("Z' Mass [GeV]")
        #canvas[j].SetLogy();
        for i in reversed(xrange(len(files))):
            l.debug("File name:"+files[i])
            l.debug("Energy:"+energies[i])
            l.debug("Entry:"+entries[j])
            l.debug("colours:"+str(colours[i]))
            feil[i] = ROOT.TFile.Open(files[i])
            tree[i] = feil[i].Get(entries[j])
            tree[i].SetLineColor(colours[i])
            tree[i].SetLineWidth(2)
            tree[i].SetName(energies[i])
            legend.AddEntry(tree[i], energies[i], "l")
            if i == len(files):
                tree[i].Draw()
                canvas[j].Update()
            else:
                tree[i].Draw("SAME") #this is required to draw on same canvas
                canvas[j].Update()
        legend.Draw()
        canvas[j].Print("overlay_"+entries[j]+".root")
        canvas[j].Print("overlay_"+entries[j]+".png")
    #ATLASLabel(0.13,0.85,"Work in Progress",1);

if __name__ == '__main__':
    # setup logger
    l.basicConfig(level=l.DEBUG, format='%(levelname)s - %(message)s')
    #%(asctime)s - %(levelname)s - %(message)s')
    plot_histograms()


