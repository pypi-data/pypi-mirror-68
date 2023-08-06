"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import io
import os
import sys
from typing import Dict, Iterable, List, Set, Type


#from ncbi_taxonomist.cache import lineagecache
from ncbi_taxonomist.model import taxon


class TaxaCache:
  """Cache taxa and corresponding names. Taxa are cached as Taxon models and
     names reference the related taxid."""

  def __init__(self):
    self.taxa = {}
    self.names = {}

  def cache(self, taxon:Type[taxon.Taxon])->None:
    """Cache taxa and corresponding names"""
    if taxon.taxon_id not in self.taxa:
      self.taxa[taxon.taxon_id] = taxon
    for i in taxon.get_names():
      self.cache_name(i, taxon.taxon_id)

  def cache_name(self, name, taxid):
    if name not in self.names:
      self.names[name] = taxid

  def get_taxa(self, taxids:Iterable[int]=None)->Dict[int,Type[taxon.Taxon]]:
    if taxids:
      taxa = {}
      for i in taxids:
        if i in self.taxa:
          taxa[i] = self.taxa[i]
      return taxa
    return self.taxa

  def get_taxon(self, taxid)->Type[taxon.Taxon]:
    if taxid in self.taxa:
      return self.taxa[taxid]
    return None

  def names_to_taxid(self, names)->Set[int]:
    taxids = set()
    for i in names:
      if i in self.names:
        taxids.add(self.names[i])
    return taxids

  def incache(self, name=None, taxid=None)->bool:
    if taxid:
      return taxid in self.taxa
    return name in self.names

  def union(self, taxids, names)->Dict[int,Type[taxon.Taxon]]:
    union = {}
    for i in names:
      if i in self.names and self.names[i] in self.taxa:
        union[self.names[i]] = self.taxa[self.names[i]]
    for i in taxids:
      if (i not in union) and (i in self.taxa):
        union[i] = self.taxa[i]
    return union

  def is_empty(self):
    if self.taxa:
      return False
    return True
