import ROOT
from ROOT import TCanvas, TF1, TLegend
import glob, re
import logging as l

def plot_histograms():

   def regex_search(file_name, regex):
      search = re.compile(regex) 
      value = search.search(file_name)
      return value

   def parse_file_names(files):
      energies = []
      for file_name in files:
         zprimexxx = regex_search(file_name,'zprime(\d+)')
         if(zprimexxx):
            energies.append(zprimexxx.group(1))
         else:
            l.ERROR("Error files names not consistent")
      l.debug("File names:"+str(files))
      l.debug("Energies: "+str(energies))
      return energies
   
   Files = glob.glob("outputs/zprime*000_*delta_r.root")
   energies = parse_file_names(Files)
   colours = [ROOT.kBlack,ROOT.kBlue, ROOT.kViolet, ROOT.kGreen, ROOT.kRed, ROOT.kOrange]
   print(colours)
   yx = zip(energies, Files, colours)
   yx.sort()
   print(yx)
   files = [x for y, x, z in yx]
   colours = [z for y, x, z in yx]
   print(files)
   energies.sort()
   print(energies)
   print(colours)
   #[files for (energies,files) in sorted(zip(Energies,Files),key=lambda pair: pair[0])]
    #[x for (y,x) in sorted(zip(Y,X), key=lambda pair: pair[0])] 
   #files = ["outputs/zprime5000_000005delta_r.root","outputs/zprime2250_000010delta_r.root"]#glob.glob("outputs/zprime*delta_r.root")
   #energies = ["5000","2250"]
   
   entries = ["delta_r", "h_delta_r_top_W", "h_delta_r_top_b"]
   l.debug("Files: "+str(files))
   l.debug("Files length: "+str(len(files)))
   
   t = [None]*len(files)
   f = [None]*len(files)
   c = [None]*len(entries)

   for j in xrange(len(entries)):
      c[j] = TCanvas( 'c'+str(j), entries[j], 200, 10, 700, 500)
      leg = TLegend(0.1,0.7,0.48,0.9)
      leg.SetHeader("Z' Mass [GeV]");
      #c[j].SetLogy();
      for i in xrange(len(files)):
         l.debug("File name:"+files[i])
         l.debug("Entry:"+entries[j])
         f[i] = ROOT.TFile.Open(files[i])
         t[i] = f[i].Get(entries[j])
         t[i].SetLineColor(colours[i])
         t[i].SetLineWidth(2);
         t[i].SetName(energies[i])
         leg.AddEntry(t[i],energies[i],"l");
         if (i==0):
            l.debug("i == 0")
            t[i].Draw()
            c[j].Update()
         else:
            l.debug("i != 0")
            t[i].Draw("SAME") #this is required to draw on same canvas
            c[j].Update()
      leg.Draw()
      c[j].Print("overlay_"+entries[j]+".png")
   #ATLASLabel(0.13,0.85,"Work in Progress",1);      



if __name__ == '__main__':
    # setup logger 
    l.basicConfig(level=l.DEBUG, format='%(levelname)s - %(message)s')#%(asctime)s - %(levelname)s - %(message)s')
    plot_histograms()


