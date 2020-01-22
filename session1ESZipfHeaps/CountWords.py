"""
.. module:: CountWords

CountWords
*************

:Description: CountWords

    Generates a list with the counts and the words in the 'text' field of the documents in an index

:Authors: bejar
    

:Version: 

:Created on: 04/07/2017 11:58 

"""

from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError

import matplotlib.pyplot as plt 
import argparse

__author__ = 'bejar'

INVALID = ['0','1','2','3','4','5','6','7','8','9',
           '.', ',', '_', '$', '@', '#', '"', '*'] 

def validWord(w):
    for c in INVALID:
        if w.find(c) != -1:
            return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = args.index

    try:
        client = Elasticsearch()
        voc = {}
        sc = scan(client, index=index, query={"query" : {"match_all": {}}})
        for s in sc:
            try:
                tv = client.termvectors(index=index, id=s['_id'], fields=['text'], doc_type=['_doc'])
                if 'text' in tv['term_vectors']:
                    for t in tv['term_vectors']['text']['terms']:
                        if t in voc:
                            voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                        else:
                            voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
            except TransportError:
                pass
        lpal = []

        for v in voc:
            lpal.append((v.encode("utf-8", "ignore"), voc[v]))


        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1]):
            if validWord(pal.decode("utf-8")):
                print(str(cnt) + ', ' +  pal.decode("utf-8"))
        print('--------------------')
        print(str(len(lpal)) + ' Words')
    except NotFoundError:
        print('Index ' + index + ' does not exists')