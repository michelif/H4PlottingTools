#!/bin/python

import sys
import re
import time
import argparse
import os
import subprocess
import array
import string
import ROOT
import math

from ROOT import std
from optparse import OptionParser

vstring = std.vector(std.string)
vfloat = std.vector(float)

#----function to book histos
def bookHistos(histos,run):
    histos["maximum_B1"]=ROOT.TH1F("maximum_B1","maximum_B1",1000,0,16000)
    histos["maximum_B1_zoom"]=ROOT.TH1F("maximum_B1_zoom","maximum_B1_zoom",100,0,100)
    histos["amp_sum_matrix_B1"]=ROOT.TH1F("amp_sum_matrix_B1","amp_sum_matrix_B1",500,0,600)
    histos["n_swiss_cross_neighbours_B1"]=ROOT.TH1F("n_swiss_cross_neighbours_B1","n_swiss_cross_neighbours_B1",5,-0.5,4.5)
    histos["swiss_cross_B1"]=ROOT.TH1F("swiss_cross_B1","swiss_cross_B1",100,-10,10)
    histos["n_channels_3by3_B1"]=ROOT.TH1F("n_channels_3by3_B1","n_channels_3by3_B1",5,-0.5,4.5)
    histos["amp_sum_3by3_B1"]=ROOT.TH1F("amp_sum_3by3_B1","amp_sum_3by3_B1",500,0,600)
    histos["n_samples_above_25perc_max_B1"]=ROOT.TH1F("n_samples_above_25perc_max_B1","n_samples_above_25perc_max_B1",25,-0.5,24.5)
    histos["n_samples_above_50perc_max_B1"]=ROOT.TH1F("n_samples_above_50perc_max_B1","n_samples_above_50perc_max_B1",25,-0.5,24.5)
    histos["n_samples_above_75perc_max_B1"]=ROOT.TH1F("n_samples_above_75perc_max_B1","n_samples_above_75perc_max_B1",25,-0.5,24.5)
    histos["tot_25perc_max_B1"]=ROOT.TH1F("tot_25perc_max_B1","tot_25perc_max_B1",200,-0.5,199.5)
    histos["tot_50perc_max_B1"]=ROOT.TH1F("tot_50perc_max_B1","tot_50perc_max_B1",200,-0.5,199.5)
    histos["tot_75perc_max_B1"]=ROOT.TH1F("tot_75perc_max_B1","tot_75perc_max_B1",200,-0.5,199.5)
    histos["sample_max_minus1_over_sample_max_B1"]=ROOT.TH1F("sample_max_minus1_over_sample_max_B1","sample_max_minus1_over_sample_max_B1",50,-3,3)
    histos["sample_max_minus2_over_sample_max_B1"]=ROOT.TH1F("sample_max_minus2_over_sample_max_B1","sample_max_minus2_over_sample_max_B1",50,-3,3)
    histos["sample_max_minus3_over_sample_max_B1"]=ROOT.TH1F("sample_max_minus3_over_sample_max_B1","sample_max_minus3_over_sample_max_B1",50,-3,3)
    histos["sample_max_plus1_over_sample_max_B1"]=ROOT.TH1F("sample_max_plus1_over_sample_max_B1","sample_max_plus1_over_sample_max_B1",50,-3,3)
    histos["sample_max_plus2_over_sample_max_B1"]=ROOT.TH1F("sample_max_plus2_over_sample_max_B1","sample_max_plus2_over_sample_max_B1",50,-3,3)
    histos["sample_max_plus3_over_sample_max_B1"]=ROOT.TH1F("sample_max_plus3_over_sample_max_B1","sample_max_plus3_over_sample_max_B1",50,-3,3)
    histos["t_undershoot_minus_t_sample_max_B1"]=ROOT.TH1F("t_undershoot_minus_t_sample_max_B1","t_undershoot_minus_t_sample_max_B1",100,0,100)
    histos["t_3sigma_noise_minus_t_sample_max_B1"]=ROOT.TH1F("t_3sigma_noise_minus_t_sample_max_B1","t_3sigma_noise_minus_t_sample_max_B1",30,-0.5,29.5)

    histos["maximum_B2"]=ROOT.TH1F("maximum_B2","maximum_B2",1000,0,16000)
    histos["maximum_B2_zoom"]=ROOT.TH1F("maximum_B2_zoom","maximum_B2_zoom",100,0,100)
    histos["amp_sum_matrix_B2"]=ROOT.TH1F("amp_sum_matrix_B2","amp_sum_matrix_B2",500,0,600)
    histos["n_swiss_cross_neighbours_B2"]=ROOT.TH1F("n_swiss_cross_neighbours_B2","n_swiss_cross_neighbours_B2",5,-0.5,4.5)
    histos["swiss_cross_B2"]=ROOT.TH1F("swiss_cross_B2","swiss_cross_B2",100,-10,10)
    histos["n_channels_3by3_B2"]=ROOT.TH1F("n_channels_3by3_B2","n_channels_3by3_B2",5,-0.5,4.5)
    histos["amp_sum_3by3_B2"]=ROOT.TH1F("amp_sum_3by3_B2","amp_sum_3by3_B2",500,0,600)
    histos["n_samples_above_25perc_max_B2"]=ROOT.TH1F("n_samples_above_25perc_max_B2","n_samples_above_25perc_max_B2",25,-0.5,24.5)
    histos["n_samples_above_50perc_max_B2"]=ROOT.TH1F("n_samples_above_50perc_max_B2","n_samples_above_50perc_max_B2",25,-0.5,24.5)
    histos["n_samples_above_75perc_max_B2"]=ROOT.TH1F("n_samples_above_75perc_max_B2","n_samples_above_75perc_max_B2",25,-0.5,24.5)
    histos["tot_25perc_max_B2"]=ROOT.TH1F("tot_25perc_max_B2","tot_25perc_max_B2",200,-0.5,199.5)
    histos["tot_50perc_max_B2"]=ROOT.TH1F("tot_50perc_max_B2","tot_50perc_max_B2",200,-0.5,199.5)
    histos["tot_75perc_max_B2"]=ROOT.TH1F("tot_75perc_max_B2","tot_75perc_max_B2",200,-0.5,199.5)
    histos["sample_max_minus1_over_sample_max_B2"]=ROOT.TH1F("sample_max_minus1_over_sample_max_B2","sample_max_minus1_over_sample_max_B2",50,-3,3)
    histos["sample_max_minus2_over_sample_max_B2"]=ROOT.TH1F("sample_max_minus2_over_sample_max_B2","sample_max_minus2_over_sample_max_B2",50,-3,3)
    histos["sample_max_minus3_over_sample_max_B2"]=ROOT.TH1F("sample_max_minus3_over_sample_max_B2","sample_max_minus3_over_sample_max_B2",50,-3,3)
    histos["sample_max_plus1_over_sample_max_B2"]=ROOT.TH1F("sample_max_plus1_over_sample_max_B2","sample_max_plus1_over_sample_max_B2",50,-3,3)
    histos["sample_max_plus2_over_sample_max_B2"]=ROOT.TH1F("sample_max_plus2_over_sample_max_B2","sample_max_plus2_over_sample_max_B2",50,-3,3)
    histos["sample_max_plus3_over_sample_max_B2"]=ROOT.TH1F("sample_max_plus3_over_sample_max_B2","sample_max_plus3_over_sample_max_B2",50,-3,3)
    histos["t_undershoot_minus_t_sample_max_B2"]=ROOT.TH1F("t_undershoot_minus_t_sample_max_B2","t_undershoot_minus_t_sample_max_B2",100,0,100)
    histos["t_3sigma_noise_minus_t_sample_max_B2"]=ROOT.TH1F("t_3sigma_noise_minus_t_sample_max_B2","t_3sigma_noise_minus_t_sample_max_B2",30,-0.5,29.5)


    for x in histos.keys():
        nbins = histos[x].GetNbinsX()
        histos[x+"_spike"]=ROOT.TH1F(x+"_spike",x+"_spike",nbins,histos[x].GetXaxis().GetBinLowEdge(1),histos[x].GetXaxis().GetBinUpEdge(nbins))

#-----main function-----
def main():
    ROOT.gROOT.SetBatch(True)
    ROOT.gROOT.Macro( os.path.expanduser( '~/rootlogon.C' ) )
    ROOT.gSystem.Load("../H4Analysis/CfgManager/lib/libCFGMan.so")
    parser = argparse.ArgumentParser (description = 'Draw plots from ROOT files')
    parser.add_argument("-r", "--run", default='100',metavar='run',type=int,
                      help="run number")
    parser.add_argument("-p", "--prefix", default='',metavar='prefix',type=str,
                      help="prefix")
    parser.add_argument("-i", "--inputDir", default='/eos/cms/store/caf/user/micheli/H2spikes/ntuples_20190926_12314/',metavar='inputDir',type=str,
                      help="prefix")

    args = parser.parse_args()
    run = args.run
    prefix = args.prefix
    inputDir = args.inputDir

    print "opening file ",inputDir+"spikes_"+str(run)+".root"

    file=ROOT.TFile(inputDir+"spikes_"+str(run)+".root")
    tree=file.Get("h4")

    outPath="plots/"+str(run)+"/"

    
    if not os.path.exists(outPath):
        os.mkdir(outPath)

    
    outfile=ROOT.TFile(outPath+"plots_"+prefix+"_"+str(run)+".root","recreate")
#----histo definition---- 
    histos={}
    bookHistos(histos,run)
    
#----loop over entries-----
    for entry in tree:
        if entry.index % 4000 ==0:
            print "Analyzing event:"
            print entry.index

        
#fill histos
        histos["maximum_B1"].Fill(entry.maximum[entry.B1])        
        histos["maximum_B1_zoom"].Fill(entry.maximum[entry.B1])        
        if entry.maximum[entry.B1]<25:
            histos["amp_sum_matrix_B1"].Fill(entry.amp_sum_matrix[entry.B1]);
            histos["n_swiss_cross_neighbours_B1"].Fill(entry.n_swiss_cross_neighbours[entry.B1]);
            histos["swiss_cross_B1"].Fill(entry.swiss_cross[entry.B1]);
            histos["n_channels_3by3_B1"].Fill(entry.n_channels_3by3[entry.B1]);
            histos["amp_sum_3by3_B1"].Fill(entry.amp_sum_3by3[entry.B1]);
            histos["n_samples_above_25perc_max_B1"].Fill(entry.n_samples_above_25perc_max[entry.B1]);
            histos["n_samples_above_50perc_max_B1"].Fill(entry.n_samples_above_50perc_max[entry.B1]);
            histos["n_samples_above_75perc_max_B1"].Fill(entry.n_samples_above_75perc_max[entry.B1]);
            histos["tot_25perc_max_B1"].Fill(entry.tot_25perc_max[entry.B1]);
            histos["tot_50perc_max_B1"].Fill(entry.tot_50perc_max[entry.B1]);
            histos["tot_75perc_max_B1"].Fill(entry.tot_75perc_max[entry.B1]);
            histos["sample_max_minus1_over_sample_max_B1"].Fill(entry.sample_max_minus1_over_sample_max[entry.B1]);
            histos["sample_max_minus2_over_sample_max_B1"].Fill(entry.sample_max_minus2_over_sample_max[entry.B1]);
            histos["sample_max_minus3_over_sample_max_B1"].Fill(entry.sample_max_minus3_over_sample_max[entry.B1]);
            histos["sample_max_plus1_over_sample_max_B1"].Fill(entry.sample_max_plus1_over_sample_max[entry.B1]);
            histos["sample_max_plus2_over_sample_max_B1"].Fill(entry.sample_max_plus2_over_sample_max[entry.B1]);
            histos["sample_max_plus3_over_sample_max_B1"].Fill(entry.sample_max_plus3_over_sample_max[entry.B1]);
            histos["t_undershoot_minus_t_sample_max_B1"].Fill(entry.t_undershoot_minus_t_sample_max[entry.B1]);
            histos["t_3sigma_noise_minus_t_sample_max_B1"].Fill(entry.t_3sigma_noise_minus_t_sample_max[entry.B1]);
        elif math.fabs(entry.time_maximum[entry.B1]-356)<2:
            histos["amp_sum_matrix_B1_spike"].Fill(entry.amp_sum_matrix[entry.B1]);
            histos["n_swiss_cross_neighbours_B1_spike"].Fill(entry.n_swiss_cross_neighbours[entry.B1]);
            histos["swiss_cross_B1_spike"].Fill(entry.swiss_cross[entry.B1]);
            histos["n_channels_3by3_B1_spike"].Fill(entry.n_channels_3by3[entry.B1]);
            histos["amp_sum_3by3_B1_spike"].Fill(entry.amp_sum_3by3[entry.B1]);
            histos["n_samples_above_25perc_max_B1_spike"].Fill(entry.n_samples_above_25perc_max[entry.B1]);
            histos["n_samples_above_50perc_max_B1_spike"].Fill(entry.n_samples_above_50perc_max[entry.B1]);
            histos["n_samples_above_75perc_max_B1_spike"].Fill(entry.n_samples_above_75perc_max[entry.B1]);
            histos["tot_25perc_max_B1_spike"].Fill(entry.tot_25perc_max[entry.B1]);
            histos["tot_50perc_max_B1_spike"].Fill(entry.tot_50perc_max[entry.B1]);
            histos["tot_75perc_max_B1_spike"].Fill(entry.tot_75perc_max[entry.B1]);
            histos["sample_max_minus1_over_sample_max_B1_spike"].Fill(entry.sample_max_minus1_over_sample_max[entry.B1]);
            histos["sample_max_minus2_over_sample_max_B1_spike"].Fill(entry.sample_max_minus2_over_sample_max[entry.B1]);
            histos["sample_max_minus3_over_sample_max_B1_spike"].Fill(entry.sample_max_minus3_over_sample_max[entry.B1]);
            histos["sample_max_plus1_over_sample_max_B1_spike"].Fill(entry.sample_max_plus1_over_sample_max[entry.B1]);
            histos["sample_max_plus2_over_sample_max_B1_spike"].Fill(entry.sample_max_plus2_over_sample_max[entry.B1]);
            histos["sample_max_plus3_over_sample_max_B1_spike"].Fill(entry.sample_max_plus3_over_sample_max[entry.B1]);
            histos["t_undershoot_minus_t_sample_max_B1_spike"].Fill(entry.t_undershoot_minus_t_sample_max[entry.B1]);
            histos["t_3sigma_noise_minus_t_sample_max_B1_spike"].Fill(entry.t_3sigma_noise_minus_t_sample_max[entry.B1]);



        histos["maximum_B2"].Fill(entry.maximum[entry.B2])        
        histos["maximum_B2_zoom"].Fill(entry.maximum[entry.B2])        
        if entry.maximum[entry.B2]<25:
            histos["amp_sum_matrix_B2"].Fill(entry.amp_sum_matrix[entry.B2]);
            histos["n_swiss_cross_neighbours_B2"].Fill(entry.n_swiss_cross_neighbours[entry.B2]);
            histos["swiss_cross_B2"].Fill(entry.swiss_cross[entry.B2]);
            histos["n_channels_3by3_B2"].Fill(entry.n_channels_3by3[entry.B2]);
            histos["amp_sum_3by3_B2"].Fill(entry.amp_sum_3by3[entry.B2]);
            histos["n_samples_above_25perc_max_B2"].Fill(entry.n_samples_above_25perc_max[entry.B2]);
            histos["n_samples_above_50perc_max_B2"].Fill(entry.n_samples_above_50perc_max[entry.B2]);
            histos["n_samples_above_75perc_max_B2"].Fill(entry.n_samples_above_75perc_max[entry.B2]);
            histos["tot_25perc_max_B2"].Fill(entry.tot_25perc_max[entry.B2]);
            histos["tot_50perc_max_B2"].Fill(entry.tot_50perc_max[entry.B2]);
            histos["tot_75perc_max_B2"].Fill(entry.tot_75perc_max[entry.B2]);
            histos["sample_max_minus1_over_sample_max_B2"].Fill(entry.sample_max_minus1_over_sample_max[entry.B2]);
            histos["sample_max_minus2_over_sample_max_B2"].Fill(entry.sample_max_minus2_over_sample_max[entry.B2]);
            histos["sample_max_minus3_over_sample_max_B2"].Fill(entry.sample_max_minus3_over_sample_max[entry.B2]);
            histos["sample_max_plus1_over_sample_max_B2"].Fill(entry.sample_max_plus1_over_sample_max[entry.B2]);
            histos["sample_max_plus2_over_sample_max_B2"].Fill(entry.sample_max_plus2_over_sample_max[entry.B2]);
            histos["sample_max_plus3_over_sample_max_B2"].Fill(entry.sample_max_plus3_over_sample_max[entry.B2]);
            histos["t_undershoot_minus_t_sample_max_B2"].Fill(entry.t_undershoot_minus_t_sample_max[entry.B2]);
            histos["t_3sigma_noise_minus_t_sample_max_B2"].Fill(entry.t_3sigma_noise_minus_t_sample_max[entry.B2]);
        elif math.fabs(entry.time_maximum[entry.B2]-356)<2:
            histos["amp_sum_matrix_B2_spike"].Fill(entry.amp_sum_matrix[entry.B2]);
            histos["n_swiss_cross_neighbours_B2_spike"].Fill(entry.n_swiss_cross_neighbours[entry.B2]);
            histos["swiss_cross_B2_spike"].Fill(entry.swiss_cross[entry.B2]);
            histos["n_channels_3by3_B2_spike"].Fill(entry.n_channels_3by3[entry.B2]);
            histos["amp_sum_3by3_B2_spike"].Fill(entry.amp_sum_3by3[entry.B2]);
            histos["n_samples_above_25perc_max_B2_spike"].Fill(entry.n_samples_above_25perc_max[entry.B2]);
            histos["n_samples_above_50perc_max_B2_spike"].Fill(entry.n_samples_above_50perc_max[entry.B2]);
            histos["n_samples_above_75perc_max_B2_spike"].Fill(entry.n_samples_above_75perc_max[entry.B2]);
            histos["tot_25perc_max_B2_spike"].Fill(entry.tot_25perc_max[entry.B2]);
            histos["tot_50perc_max_B2_spike"].Fill(entry.tot_50perc_max[entry.B2]);
            histos["tot_75perc_max_B2_spike"].Fill(entry.tot_75perc_max[entry.B2]);
            histos["sample_max_minus1_over_sample_max_B2_spike"].Fill(entry.sample_max_minus1_over_sample_max[entry.B2]);
            histos["sample_max_minus2_over_sample_max_B2_spike"].Fill(entry.sample_max_minus2_over_sample_max[entry.B2]);
            histos["sample_max_minus3_over_sample_max_B2_spike"].Fill(entry.sample_max_minus3_over_sample_max[entry.B2]);
            histos["sample_max_plus1_over_sample_max_B2_spike"].Fill(entry.sample_max_plus1_over_sample_max[entry.B2]);
            histos["sample_max_plus2_over_sample_max_B2_spike"].Fill(entry.sample_max_plus2_over_sample_max[entry.B2]);
            histos["sample_max_plus3_over_sample_max_B2_spike"].Fill(entry.sample_max_plus3_over_sample_max[entry.B2]);
            histos["t_undershoot_minus_t_sample_max_B2_spike"].Fill(entry.t_undershoot_minus_t_sample_max[entry.B2]);
            histos["t_3sigma_noise_minus_t_sample_max_B2_spike"].Fill(entry.t_3sigma_noise_minus_t_sample_max[entry.B2]);


    for x in histos.keys():
        c1 = ROOT.TCanvas()
        if "spike" not in x:
            histos[x].SetLineWidth(2)
            histos[x].GetXaxis().SetTitle(x)
            histos[x+"_spike"].GetXaxis().SetTitle(x)
            histos[x+"_spike"].SetLineColor(ROOT.kRed)
            histos[x+"_spike"].SetMarkerColor(ROOT.kRed)
            histos[x+"_spike"].SetLineWidth(2)
            histos[x+"_spike"].SetMarkerStyle(1)
            if histos[x].GetMaximum()<histos[x+"_spike"].GetMaximum():
                histos[x].DrawNormalized()
                histos[x+"_spike"].DrawNormalized("samehiste")
            else:
                histos[x+"_spike"].DrawNormalized("histe")
                histos[x].DrawNormalized("samehist")
            for format in ".png",".pdf",".C":
                c1.SaveAs(outPath+str(x)+format)
                c1.SetLogy()
                c1.SaveAs(outPath+str(x)+"_log"+format)
                c1.SetLogy(0)
            c1.Delete()

    outfile.Write()
    outfile.Close()

### MAIN ###
if __name__ == "__main__":
    main()
