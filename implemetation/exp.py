from cache import *
from itertools import product

import argparse

def parsearg():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('test_case', type=str)
    parser.add_argument('--size', type=int, nargs="+", default=[10])
    return parser.parse_args()

def main():
    args = parsearg()

    testing_polices = [LRUCache, FIFOCache, LFUCache, RRCache]
    access_history = open( args.test_case ).read().split("\n")
    print("# unique keys = ", len(set(access_history)))
    
    for policy, size in product(testing_polices, args.size):
        print( policy.__name__, size )
        miss = 0
        cache = policy(size=size)
        for e in access_history:
            if e not in cache:
                miss += 1
                cache[e] = -1 # store
            cache[e] # read
        print(f"miss rate {miss} / {len(access_history)} = ",
              miss / len(access_history), "\n")
    

if __name__ == '__main__':
    main()