#Marta Kajkowska
import argparse
from ascii_graph import Pyasciigraph

parser = argparse.ArgumentParser()
parser.add_argument('file', help="plik do wczytania")
parser.add_argument('-w', '--words', help="ilość wyrazów na histogramie", type=int, default=10)
parser.add_argument('-m', '--minimal', help="minimalna długość wyrazu", type=int, default=0)
args = parser.parse_args()
dictionary = {}
try:
    file = open(args.file, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        words = (line.strip().split())
        for word in words:
            if(len(word) >= args.minimal):
                if(word not in dictionary):
                    dictionary[word] = 1
                else:
                    dictionary[word] += 1
    dictionary = dict(sorted(dictionary.items(), reverse=True, key=lambda item: item[1]))
    dictionary_tuple = [(k, v) for k, v in dictionary.items()]
    histogram = Pyasciigraph()
    i = 0
    for line in histogram.graph('Wyrazy', dictionary_tuple):
        if i < args.words+2:
            print(line)
            i += 1
except:
    print("nie znaleziono pliku")
