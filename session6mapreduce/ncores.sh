# python3.4 ExtractData.py --index arxiv --minfreq 0.1 --maxfreq 0.3 --numwords $1
python GeneratePrototypes.py --nclust 10
echo "===== MRK MEANS ===== " > output_experiment2.txt
python3.4 MRKmeans.py --ncores $1 >> output_experiment2.txt 
echo "===== PROCESS RESULTS =====" >> output_experiment2.txt
python3.4 ProcessResults.py >> output_experiment2.txt


# nwords            ncores
# 100 250 500       2 4 8