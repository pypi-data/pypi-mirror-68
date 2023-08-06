"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Iterable, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.resolve.query import resolvequery


class NameResolveQuery(resolvequery.ResolveQuery):

  def __init__(self, queries:Iterable[str]):
    super().__init__(queries)

  def get_name(self, names)->str:
    for i in names:
      if i in self.queries:
        return i
    return None

  def resolve(self, taxids:Iterable[int], taxa:Iterable[Type[taxon.Taxon]]):
    for i in taxids:
      name = self.get_name(taxa[i].get_names())
      if name:
        lin = NameResolveQuery.resolve_lineage(i, taxa)
        if lin:
          self.queries[name] = lin
          utils.json_stdout({'name':name,'lin':[x.get_attributes() for x in lin]})
