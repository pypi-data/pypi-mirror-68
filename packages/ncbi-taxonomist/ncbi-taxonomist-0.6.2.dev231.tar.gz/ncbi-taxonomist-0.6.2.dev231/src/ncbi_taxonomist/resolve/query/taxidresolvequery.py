"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable, List, Mapping, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.resolve.query import resolvequery


class TaxidResolveQuery(resolvequery.ResolveQuery):

  def __init__(self, queries:Iterable[int]):
    super().__init__(queries)

  def resolve(self, taxids:List[int], taxa:Mapping[int,Type[taxon.Taxon]])->None:
    for i in taxids:
      if i in self.queries:
        lin = TaxidResolveQuery.resolve_lineage(i, taxa)
        if lin:
          self.queries[i] = lin
          utils.json_stdout({'taxid':i, 'lin':[x.get_attributes() for x in lin]})

