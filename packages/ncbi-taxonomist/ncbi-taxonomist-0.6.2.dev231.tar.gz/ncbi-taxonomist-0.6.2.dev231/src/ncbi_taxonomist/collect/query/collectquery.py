"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type, Mapping, AbstractSet, Iterable


from ncbi_taxonomist.model import taxon


class CollectQuery:

  def __init__(self, queries:Iterable):
    self.queries = set(queries)

  def collect(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[taxon.Taxon]]):
    raise NotImplementedError
