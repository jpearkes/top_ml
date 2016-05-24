import ROOT
from ROOT import gROOT, gStyle, TCanvas, TGraph
import logging as l
from array import array


def clone_histo(histo):
    new_histo = ROOT.TH2F(histo.GetName()+'_normalized',histo.GetTitle(),histo.GetNbinsX(),0,2200,histo.GetNbinsY(),0,2)
    title = histo.GetXaxis().GetTitle()
    new_histo.GetXaxis().SetTitle("p_{T} [GeV]")
    #title = histo.GetYaxis().GetTitle()
    new_histo.GetYaxis().SetTitle("Delta R")#$\Delta$R")
    return new_histo

def normalize_histograms():
    gROOT.ProcessLine (".x $ROOTCOREDIR/scripts/load_packages.C");  

    treeName = "CollectionTree" # default when making transient tree anyway
    f = ROOT.TFile.Open("outputs/zprime_all_tests_2.root")
    f_out = ROOT.TFile("outputs/zprime_all_tests_normalized_2.root", "recreate")   
    f.ls()
    #gStyle.SetPalette(ROOT.kBird);
    gStyle.SetNumberContours(999);
    gStyle.SetOptStat(0);
    # for i in pt bin
    # integrate over delta R
    # divide each bin by integral
    entries = ["h_delta_r_top_W_2d","h_delta_r_top_W_daughters_2d",
               "h_delta_r_top_b_2d","h_delta_r_jet_W_2d",
               "h_delta_r_jet_W_daughters_2d","h_delta_r_jet_b_2d"]
    h_delta_r_2d = [None]*(len(entries))
    h_delta_r_2d_normalized = [None]*(len(entries)) 
    c = [None]*len(entries)
    g = [None]*len(entries)
    for entry in xrange(len(entries)):
        c[entry] = TCanvas( 'c'+str(entry), entries[entry], 200, 10, 700, 500)
        h_delta_r_2d[entry] = f.Get(entries[entry])
        h_delta_r_2d_normalized[entry] = clone_histo(h_delta_r_2d[entry])
        #ROOT.TH2F('h_delta_r_top_W_daughters_2d_normalized','Delta R between Top and W-daughters',100,0,2200,100,0,2)
    
        for x in xrange(h_delta_r_2d[entry].GetXaxis().GetNbins()):
            total = 0
            for y in xrange(h_delta_r_2d[entry].GetYaxis().GetNbins()):
                total += h_delta_r_2d[entry].GetBinContent(x,y)
            #print(total)
            if(total != 0):
                for y in xrange(h_delta_r_2d[entry].GetYaxis().GetNbins()):
                    normalized_value = h_delta_r_2d[entry].GetBinContent(x,y)/total
                    h_delta_r_2d_normalized[entry].SetBinContent(x,y, normalized_value) 
        h_delta_r_2d_normalized[entry].Draw("colz")
        #h_delta_r_2d_normalized[entry].SetContour(1)#,0.5)
        g[entry] = TGraph()
        for x in xrange(h_delta_r_2d[entry].GetXaxis().GetNbins()):
            quantile= array("d", [0.0])
            prob = array("d", [0.95])
            profile = h_delta_r_2d_normalized[entry].ProjectionY("_pfy", x, x+1)#-1)  
            #c[entry].Update() 
            profile.GetQuantiles(1 , quantile, prob)
            print("quantile:"+str(quantile))
            g[entry].SetPoint(x,x*2200.0/100.0,float(quantile[0]))
            print("prob:"+str(prob))
        g[entry].SetLineWidth(2)
        g[entry].Draw("SAME")
        #h_delta_r_2d_normalized[entry].SetContour(1)
        #h_delta_r_2d_normalized[entry].SetContourLevel(0, 0.05)
        c[entry].Update()
        c[entry].Print("normalized_"+entries[entry]+".pdf")
    

    f_out.Write()
    f_out.Close()
    f.Close()  
    ROOT.xAOD.ClearTransientTrees() 


if __name__ == '__main__':
    # setup loggers 
    l.basicConfig(level=l.INFO, format='%(levelname)s - %(message)s')#%(asctime)s - %(levelname)s - %(message)s')
    normalize_histograms()
