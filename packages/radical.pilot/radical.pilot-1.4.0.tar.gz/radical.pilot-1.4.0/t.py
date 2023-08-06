#!/usr/bin/env python

import os
import time
import multiprocessing as mp


def test():
    N = [1] * 1024
    M =  N  * 1024
    L =  M  * 1024
    time.sleep(5)


# n = 1024 * 1024 * 32
# l = list([i for i in range(n)])

n = [1] * 1024
m =  n  * 1024
l =  m  * 1024

time.sleep(3)

p = mp.Process(target=test)
p.start()
p.join()

