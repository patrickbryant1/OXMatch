# OXMatch
A simple script for matching sequences from two different MSAs based on the OX identifiers resulting from an hhblits search.

Input: MSAs to be matched in a3m format
Output: Merged MSA i a3m format

Run like this:
A3M1=./test/1BML_B.a3m #Path to a3m1
A3M2=./test/1BML_D.a3m #Path to a3m2
MGF=0.9 #Max gap fraction allowed in each sequence
OUTDIR=./ #Output directory
python3 oxmatch.py --a3m1 $A3M1 --a3m2 $A3M2 --max_gap_fraction $MGF --outdir $OUTDIR
