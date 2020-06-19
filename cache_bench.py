from nmigen import *
from back.cache import L1Cache

# This tutorial aims to capture how to use Minerva's
# L1Cache
# https://github.com/lambdaconcept/minerva/blob/master/minerva/cache.py

cache = L1Cache(nways=2, nlines=16, nwords=4, base=0, limit=2**32)

# connect cache to memory
mem = Memory(width=32, depth=16)