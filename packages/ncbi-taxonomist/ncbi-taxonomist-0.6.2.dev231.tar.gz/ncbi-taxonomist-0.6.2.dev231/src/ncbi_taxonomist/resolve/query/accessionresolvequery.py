"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Type, List, Mapping, AbstractSet, Iterable


from ncbi_taxonomist import utils
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.resolve import lineageresolver

class AccessionResolveQuery:

  def __init__(self, taxids:Mapping[int,Iterable[str]], accs:Mapping[str,Type[accession.AccessionData]]):
    self.accs = accs
    self.qry_taxids = taxids

  def update_queries(self, accession):
    if accession not in self.accs:
      self.accs[accession] = None
    return self.accs[accession]

  def resolve(self, taxids:AbstractSet[int], taxa:Mapping[int,Type[taxon.Taxon]]):
    for i in taxids:
      if i in self.qry_taxids:
        lin = lineageresolver.resolve_lineage(i, taxa)
        for j in self.qry_taxids[i]:
          accs = self.update_queries(j)
          if accs:
            data = accs.get_attributes()
            data.update({'lin':[x.get_attributes() for x in lin]})
            utils.json_stdout({'accs':j, 'data':data})

