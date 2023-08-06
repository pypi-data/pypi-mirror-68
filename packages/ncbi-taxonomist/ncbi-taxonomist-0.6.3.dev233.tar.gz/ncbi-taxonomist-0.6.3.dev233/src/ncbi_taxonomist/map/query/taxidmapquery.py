"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Iterable, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.map.query import mapquery


class TaxidMapQuery(mapquery.MapQuery):

  def __init__(self, queries:Iterable[int]):
    super().__init__()
    self.queries = {x:None for x in queries}

  def update_queries(self, taxon:Type[taxon.Taxon]) -> bool:
    if taxon.taxon_id in self.queries:
      self.queries[taxon.taxon_id] = taxon
      return True
    return False

  def map_query(self, taxon:Type[taxon.Taxon]):
    if self.update_queries(taxon):
      utils.json_stdout({'taxid':taxon.taxon_id, 'taxon':taxon.get_attributes()})
