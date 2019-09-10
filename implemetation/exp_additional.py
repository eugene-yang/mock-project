import pandas as pd

from cache import *
from itertools import product

def main():
    test_cases = ["case_1.txt", "case_2.txt", "case_3.txt"]

    testing_polices = [LRUCache, FIFOCache, LFUCache, RRCache]

    results = []
    for case in test_cases:
        access_history = open( "../"+case ).read().split("\n")
        
        for policy, size in product(testing_polices, range(1, 31)):
            miss = 0
            cache = policy(size=size)
            for e in access_history:
                if e not in cache:
                    miss += 1
                    cache[e] = -1 # store
                cache[e] # read
            
            results.append({
                "case": case,
                "policy": policy.__name__,
                "size": size,
                "miss": miss,
                "miss_rate": miss / len(access_history)
            })
    
    pd.DataFrame(results).to_csv("results.csv", index=False)

if __name__ == '__main__':
    main()