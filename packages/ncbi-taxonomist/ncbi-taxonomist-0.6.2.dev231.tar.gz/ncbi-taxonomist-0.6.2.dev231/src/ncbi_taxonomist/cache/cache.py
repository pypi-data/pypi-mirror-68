"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import io
import os
import sys
from typing import Dict, Iterable, List, Mapping, Set, Type


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession
import ncbi_taxonomist.cache.taxacache
import ncbi_taxonomist.cache.accessioncache
import ncbi_taxonomist.cache.lineagecache


class Cache:
  """
  Handle caching of taxa, accessions and lineages. Taxa are stored as
  :class:`ncbi_taxonomist.model.taxon.Taxon`. Lineages and accessions
  are stored referencing the corresponding taxid in the Taxa cache.
  """

  taxa = ncbi_taxonomist.cache.taxacache.TaxaCache()
  accessions = ncbi_taxonomist.cache.accessioncache.AccessionCache()
  lineages = ncbi_taxonomist.cache.lineagecache.LineaegeCache()

  def __init__(self):
    pass

  def cache_lineage(self, lineage):
    if lineage:
      for i in lineage:
        Cache.taxa.cache(i)
        Cache.lineages.cache(i.taxon_id)

  def remove_cached_strings_from(self, cache, values:Iterable[str])->List[str]:
    if cache.is_empty():
      return values
    noncached = []
    while values:
      val = values.pop()
      if not cache.incache(name=val):
        noncached.append(val)
    return noncached

  def remove_cached_taxids(self, values:Iterable[int])->List[int]:
    if Cache.taxa.is_empty():
      return values
    noncached = []
    while values:
      val = values.pop()
      if not Cache.taxa.incache(taxid=val):
        noncached.append(val)
    return noncached

  def remove_cached_names(self, names:Iterable[str])->List[str]:
    return self.remove_cached_strings_from(Cache.taxa, names)

  def remove_cached_accessions(self, accessions:Iterable[str])->List[str]:
    return self.remove_cached_strings_from(Cache.accessions, accessions)

  def names_to_taxids(self, names)->Set[int]:
    if not names:
      return set()
    return Cache.taxa.names_to_taxids(names)

  def get_taxa(self, taxids:Iterable[int]=None)->Dict[int,Type[taxon.Taxon]]:
    return Cache.taxa.get_taxa()

  def union_taxid_names(self, taxids:Iterable[int], names:Iterable[str])->Dict[int,Type[taxon.Taxon]]:
    if taxids is None:
      taxids = []
    if names is None:
      names = []
    return Cache.taxa.union(taxids, names)

  def cache_taxa(self, taxa):
    for i in taxa:
      Cache.taxa.cache(taxon)

  def update_query(self, cache, queries:[Mapping[any,Type[taxon.Taxon]]])->List[any]:
    """Remove obtained data from query. Not obtained data has None as value."""
    failed = []
    while queries:
      q = queries.popitem()
      if q[1]:
        if cache == 'taxa':
          Cache.taxa.cache(q[1])
        elif cache == 'accessions':
          Cache.accessions.cache(q[1])
        elif cache == 'lineages':
          self.cache_lineage(q[1])
        else:
          sys.exit("Error. Invalid cache name {}. Abort".format(cache))
      else:
        failed.append(q[0])
    return failed
