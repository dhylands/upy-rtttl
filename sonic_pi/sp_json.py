#!/usr/bin/env python3
#outputs data for freqs and durations to a json format file
#gets input data from name parameter -n supp;ied on command line
#from song.py data file
#eg ./sp_json.py -n Entertainer
#output file intended to be read and used by Sonic Pi
from rtttl import RTTTL
import songs
import json
import argparse

def getData(name):   
    tune = RTTTL(songs.find(name))
    n=[]
    d=[]
    for freq, msec in tune.notes():
        n.append(freq)
        d.append(msec)
    data = {}
    data['freqs']=n
    data['durs']=d
    with  open("/Users/rbn/src/upy-rtttl/sptune.json","w+") as outfile:
        json.dump(data, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n",default = 'Entertainer',help='name of tune')
    args=parser.parse_args()
    print(args.n)
    getData(args.n)
