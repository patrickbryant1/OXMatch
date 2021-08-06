import argparse
import sys
import os
import numpy as np
import pandas as pd
import glob
import pdb

parser = argparse.ArgumentParser(description = '''A simple script for matching sequences from two different MSAs based
                                                on the OX identifiers resulting from an hhblits search..''')

parser.add_argument('--a3m1', nargs=1, type= str, default=sys.stdin, help = 'Path to msa1 in a3m format.')
parser.add_argument('--a3m1', nargs=1, type= str, default=sys.stdin, help = 'Path to msa2 in a3m format.')
parser.add_argument('--outdir', nargs=1, type= str, default=sys.stdin, help = 'Path to output directory. Include /in end')


def read_a3m(infile,max_gap_fraction=0.9):
    '''Read a3m MSA'''
    mapping = {'-': 21, 'A': 1, 'B': 21, 'C': 2, 'D': 3, 'E': 4, 'F': 5,
             'G': 6,'H': 7, 'I': 8, 'K': 9, 'L': 10, 'M': 11,'N': 12,
             'O': 21, 'P': 13,'Q': 14, 'R': 15, 'S': 16, 'T': 17,
             'V': 18, 'W': 19, 'Y': 20,'U': 21, 'Z': 21, 'X': 21, 'J': 21}

    parsed = []#Save extracted msa
    species = []
    seqlen = 0
    lc = 0
    with open(infile, 'r') as file:
        for line in file:
            line = line.rstrip()

            if line.startswith('>'): #OX=OrganismIdentifier
                if 'OX=' in line:
                    OX= line.split('OX=')[1]
                    if len(OX)>0:
                        species.append(int(OX.split(' ')[0]))
                    else:
                        species.append(0)
                else:
                    species.append(0)
                continue
            line = line.rstrip()
            gap_fraction = line.count('-') / float(len(line))
            if gap_fraction <= max_gap_fraction:#Only use the lines with less than 90 % gaps
                parsed.append([mapping.get(ch, 22) for ch in line if not ch.islower()])
            else:
                if len(species)>1:
                    species = species[:-1] #Remove the previously stored species
                    continue
            #Check that the lengths match
            if len(parsed[-1])!=seqlen and lc>=1:
                parsed = parsed[:-1]
                species = species[:-1]
                continue
            seqlen = len(parsed[-1])
            lc+=1


    return np.array(parsed, dtype=np.int8, order='F'), np.array(species)


#################MAIN####################

#Parse args
args = parser.parse_args()
#Data
a3m1 = args.a3m1[0]
a3m2 = args.a3m2[0]
outdir = args.outdir[0]

#MSA1
msa1, OX1 = read_a3m(a3m1)
#MSA2
msa2, OX2 = read_a3m(a3m2)

#Get some statistics for msa1
nseqs_total1, l1 = msa1.shape
nseqs_OX1 = np.argwhere(OX1!=0).shape[0]
nunique_OX1 = np.unique(OX1).shape[0]-1 #Subtract 1 (no species)
#Get some statistics for msa2
nseqs_total2, l2 = msa2.shape
nseqs_OX2 = np.argwhere(OX2!=0).shape[0]
nunique_OX1 = np.unique(OX2).shape[0]-1 #Subtract 1 (no species)