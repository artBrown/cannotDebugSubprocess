import inspect
import os
import sys
from collections import defaultdict
from typing import List
from math import inf
import regex as re

pairs = 'py/input/input01.txt'
def pairs2line(lines: str = '', runner: bool=False) -> int:
  e = []
  if runner:
    f = iter(lines.split())
    l0 = next(f)
    yield int(l0)
    for l in f:
      for p in re.findall(r'\[(\d+),(\d+)\]', l):
        e.append([int(p[0]),int(p[1])])
    yield e
  else:
    with open(lines) as f:
      l0 = next(f)
      yield int(l0)
      for l in f.readlines():
        for p in re.findall(r'\[(\d+),(\d+)\]', l):
          e.append([int(p[0]),int(p[1])])
      yield e

class Solution:
  def minTrioDegree(self, n: int, edges: List[List[int]]) -> int:
    g = defaultdict(set)
    for a, b in edges:
      g[a].add(b)
      g[b].add(a)
    d = {n: len(g[n]) for n in g}
    res = inf
    for n in g:
      for m in g[n]:
        for o in g[n] & g[m]:
          res = min(res, d[n] + d[m] + d[o] - 6)
          g[o].discard(n)
        g[m].discard(n)
    return res if res < inf else -1

if __name__ == '__main__':
  pid = len(sys.argv) == 2 and sys.argv[1]
  runner = pid == str(os.getppid())
  if runner:
    pairs = ''
    for res1 in sys.stdin:
      pairs += res1
  gen = pairs2line(pairs, runner)
  products_nodes = next(gen)
  products_edges = next(gen)
  res = Solution().minTrioDegree(products_nodes, products_edges)
  if runner:
    sys.stdout.write(str(res))
  else:
    print(res)
