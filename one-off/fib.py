import sys

def fib(n):
  if n == 0 or n == 1:
    return 1
  fibs = list()
  fibs.append(1)
  fibs.append(1)
  i = 2
  while i <= n:
    fibs.append(fibs[i-1] + fibs[i-2])
    i += 1
  return fibs[n]

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "Usage: fib.py n"
  try:
    n = int(sys.argv[1])
  except:
    print "Usage: fib.py n"
  print fib(n)
