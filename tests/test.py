from testClass import testClass
from multiprocessing.dummy import Pool as ThreadPool
import os
from threading import Thread
import time

def runPararel(threads=2, data=[]):
    obj = testClass.getInstance()
    pool = ThreadPool(threads)
    pool.map(obj.pararelCal, data)
    pool.close()
    pool.join()
    del pool

def main():
    workers = int(input())
    cache = []
    while True:
        loadData = (open('../bin/data/data.txt', 'r').read()).split('\n')
        oldSize = (len(cache) - 1, 0)[len(cache) == 0] #Ternary operator == len(cache) == 0 ? 0 : len(cache)-1
        if(len(cache) < len(loadData)):
            for i in range(len(cache)-1, len(loadData)):
                cache.append(loadData[i])
            runPararel(workers, [i for i in cache[oldSize:]])
        else:
            time.sleep(1)
            print("zZz")
    print("Complete!")


if __name__ == "__main__":
    main()