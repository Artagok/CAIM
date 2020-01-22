#!/bin/sh

python3.4 ExtractData.py --index arxiv --minfreq $1 --maxfreq $2 --numwords $3
python GeneratePrototypes.py --nclust 20
echo "===== MRK MEANS ===== " >> output_experiment3.txt
python3.4 MRKmeans.py --iter 20 >> output_experiment3.txt 
echo "===== PROCESS RESULTS =====" >> output_experiment3.txt
python3.4 ProcessResults.py --natt 10 >> output_experiment3.txt
