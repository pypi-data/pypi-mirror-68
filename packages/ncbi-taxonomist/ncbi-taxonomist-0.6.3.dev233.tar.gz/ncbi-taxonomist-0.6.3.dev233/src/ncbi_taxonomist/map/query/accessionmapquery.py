"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Dict, Iterable, Mapping, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.map.query import mapquery

class AccessionMapQuery(mapquery.MapQuery):

  def __init__(self, queries:Iterable[str]):
    super().__init__()
    self.queries = {x:None for x in queries}

  def update_queries(self, accession:Type[accession.AccessionData]) -> str:
    accessions = accession.get_accessions()
    for i in accessions:
      if accessions[i] in self.queries and not self.queries[accessions[i]]:
        self.queries[accessions[i]] = accession
        return accessions[i]
    return None

  def map_query(self, accession:Type[accession.AccessionData]) -> Dict[str, dict]:
    qryaccs = self.update_queries(accession)
    if qryaccs:
      utils.json_stdout({'accs': qryaccs, 'data': accession.get_attributes()})
