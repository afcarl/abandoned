#!/usr/bin/python

import sys
import math

def truncate(num, places):
  return (0.0 + int(num * pow(10,places))) / 100.0

def stdev(nums):
  sum = 0.0
  for num in nums:
    sum += num
  avg = sum / len(nums)
  ravg = truncate(avg, 2)
  print "ravg =", ravg
  sumsq = 0.0
  for num in nums:
    a = pow(num - ravg, 2)
    ra = truncate(a, 2)
    sumsq += ra
    print "(%f - %f)^2 = %f" % (num, ravg, ra)
  print "sumsq =", sumsq
  
  variation = sumsq / (len(nums) - 1)
  return math.sqrt(variation)

if __name__ == "__main__":
  try:
    print stdev([int(n) for n in sys.argv[1:]])
  except Exception, e:
    print e
    print "Usage: stdev.py x_1 x_2 ... x_n"
