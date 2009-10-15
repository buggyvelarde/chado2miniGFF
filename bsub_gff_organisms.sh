#!/bin/bash
#BSUB -J minimalGFF
#BSUB -o /nfs/pathdata2/GFF/gffminimal/bsub.out.%J
#BSUB -q long
#BSUB -M 2097152
/usr/bin/python gff_organisms.py -savePath /nfs/pathdata2/GFF/gffminimal/ 
