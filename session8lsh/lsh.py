#!/usr/bin/env python
"""
Simple module implementing LSH
"""
import numpy
import sys
import argparse
import time

__version__ = '0.2.1'
__author__ = 'marias@cs.upc.edu'

k = 0
m = 0

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' %
              (method.__name__, args, kw, te - ts))
        #global m
        #print('%d %2.2f' % (m, te-ts))
        return result

    return timed


class lsh(object):
    """
    implements lsh for digits database in file 'images.npy'
    """

    def __init__(self, k, m):
        """ k is nr. of bits to hash and m is reapeats """
        # data is numpy ndarray with images
        self.data = numpy.load('images.npy')
        self.k = k
        self.m = m

        # determine length of bit representation of images
        # use conversion from natural numbers to unary code for each pixel,
        # so length of each image is imlen = pixels * maxval
        self.pixels = 64
        self.maxval = 16
        self.imlen = self.pixels * self.maxval

        # need to select k random hash functions for each repeat
        # will place these into an m x k numpy array
        numpy.random.seed(12345)
        self.hashbits = numpy.random.randint(self.imlen, size=(m, k))

        # the following stores the hashed images
        # in a python list of m dictionaries (one for each repeat)
        self.hashes = [dict() for _ in range(self.m)]

        # now, fill it out
        self.hash_all_images()

        return

    def hash_all_images(self):
        """ go through all images and store them in hash table(s) """
        # Achtung!
        # Only hashing the first 1500 images, the rest are used for testing
        for idx, im in enumerate(self.data[:1500]):
            for i in range(self.m):
                str = self.hashcode(im, i)

                # store it into the dictionary.. 
                # (well, the index not the whole array!)
                if str not in self.hashes[i]:
                    self.hashes[i][str] = []
                self.hashes[i][str].append(idx)
        return

    def hashcode(self, im, i):
        """ get the i'th hash code of image im (0 <= i < m)"""
        pixels = im.flatten()
        row = self.hashbits[i]
        str = ""
        for x in row:
            # get bit corresponding to x from image..
            pix = int(x) // int(self.maxval)
            num = x % self.maxval
            if num <= pixels[pix]:
                str += '1'
            else:
                str += '0'
        return str

    def candidates(self, im):
        """ given image im, return matching candidates (well, the indices) """
        res = set()
        for i in range(self.m):
            code = self.hashcode(im, i)
            if code in self.hashes[i]:
                res.update(self.hashes[i][code])
        return res


# =========================================================================== #
# In our representation distance coincides with the Hamming distance
# d(x,y) = iE{1..d} sum(|xi - yi|)
def distance(img1, img2): return sum(map(sum, abs(img1 - img2)))
# Brute Force Search: compares given image with the rest of the 
# set of images (the first 1500)
def bruteForce(me, index):
    # img we want to compare to all others
    img = me.data[index]
    # minIdx = 0 and minDist = dist(img, img[0])
    minDist = distance(img, me.data[0])
    minIdx = 0
    # compare with all the 1499 remaining images
    for i in range(1,1500):
        d = distance(img, me.data[i])
        if d < minDist:
            minDist = d
            minIdx = i 
    return (minDist, minIdx)
#
def search(me, index, candidates):
    # No candidates for image given
    if len(candidates) == 0:
        return -1,-1

    minDist = -1 
    minIdx = 0
    img = me.data[index]
    
    for c in candidates:
        d =  distance(img, me.data[c])
        (minDist, minIdx) = (d,c) if minDist < 0 else (minDist, minIdx)
        (minDist, minIdx) = (d,c) if d < minDist else (minDist, minIdx)
    
    return minDist, minIdx
# =========================================================================== #

@timeit
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=20, type=int)
    parser.add_argument('-m', default=5, type=int)
    args = parser.parse_args()

    print("Running lsh.py with parameters k =", args.k, "and m =", args.m)

    #global k
    #global m 
    k = args.k
    m = args.m

    start = time.time()
    me = lsh(args.k, args.m)
    end  = time.time()
    print("INI: %2.2f" % (end - start))

    #cand_acc = 0
    time_brute = 0.0
    time_hash = 0.0
    not_found = 0
    diff = 0

    # show candidate neighbors for first 10 test images
    s = time.time()
    for r in range(1500, 1510):

        im = me.data[r]
        cands = me.candidates(im)
        #cand_acc += len(cands)
        #print("There are %4d candidates for image %4d" % (len(cands), r))

        start = time.time()
        db, ib = bruteForce(me, r)
        end = time.time()
        time_brute += (end - start)
        #print("Brute Force\t Image %4d => nearest neighbor: %4d at distance: %4d" % (r, ib, db))

        start = time.time()
        dl, il = search(me, r, cands)
        end = time.time()
        time_hash += (end - start)
        msg = ("LSH\t\t Image %4d => nearest neighbor: %4d at distance: %4d" % (r, il, dl), "No candidate for image %4d" % (r))[dl < 0]
        #print(msg)
        #print("")
        
        if (dl < 0):
            not_found += 1
        else:
            diff += (dl - db)

    e = time.time()
    print("FOR: %2.2f" % (e - s))
    print("Brute Force: %2.2f | LSH: %2.2f" % (time_brute, time_hash))
    print("LSH-Not-Founds: %d | Diff: %d " % (not_found, diff))
    #print('%d %2.2f' % (m, cand_acc/10.0))

    return


if __name__ == "__main__":
    sys.exit(main())
