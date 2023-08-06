"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Type, Mapping, List, AbstractSet, Iterable


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.resolve import lineageresolver


class ResolveQuery:

  @staticmethod
  def resolve_lineage(taxid:int, taxa:Mapping[int,Type[taxon.Taxon]])->List[Type[taxon.Taxon]]:
    return lineageresolver.resolve_lineage(taxid, taxa)

  def __init__(self, queries:Iterable):
    self.queries = {x:None for x in queries}

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[taxon.Taxon]]):
    raise NotImplementedError
