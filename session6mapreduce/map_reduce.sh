#!/bin/sh

echo "ExtractData.py --index news --minfreq $1 --maxfreq $2 --numwords $3" > output_experiment1.txt
python3.4 ExtractData.py --index arxiv --minfreq $1 --maxfreq $2 --numwords $3
python GeneratePrototypes.py --nclust 10
echo "===== MRK MEANS ===== " >> output_experiment1.txt
python3.4 MRKmeans.py >> output_experiment1.txt 
echo "===== PROCESS RESULTS =====" >> output_experiment1.txt
python3.4 ProcessResults.py >> output_experiment1.txt

# minfreq maxfreq n_first_words
# ncores

# 0.01  0.05    200
# 0.05  0.1     200
# 0.1   0.3     200
# 0.3   0.5     200
# 0.5   0.7     200
# 0.7   1.0     200