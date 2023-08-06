"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import io
import os
import sys
from typing import Iterable, List, Set, Type


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession


class LineaegeCache:
  """Cache lineages using taxids only."""

  def __init__(self):
    self.taxids = set()

  def cache(self, taxid):
    self.taxids.add(taxid)

  def remove_cached_lineages_taxids(self, taxids:Iterable[int]=None)->List[int]:
    noncached = []
    while taxids:
      t = taxids.pop()
      if not is_cached_lineage(t):
        noncached.append(t)
    return noncached

  def incache(self, name=None, taxid=None):
    return taxid in self.taxids

  def get_cached_lineage_taxids(self, taxids:Iterable[int]=None)->Set[int]:
    cached = set()
    for i in taxids:
      if self.is_cached(i):
        cached.add(i)
    return cached

  def is_empty(self):
    if self.taxids:
      return False
    return True
