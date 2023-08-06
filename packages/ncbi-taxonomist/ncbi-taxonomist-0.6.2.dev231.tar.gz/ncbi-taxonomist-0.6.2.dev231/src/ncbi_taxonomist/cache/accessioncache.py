"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import io
import os
import sys
from typing import Iterable, List, Type


from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession


class AccessionCache:

  def __init__(self):
    self.accessions = {}

  def cache(self, accession:Type[accession.AccessionData]):
    accessions = accession.get_accessions()
    for i in accessions:
      if accessions[i] not in self.accessions:
        self.accessions[accessions[i]] = accession.taxon_id

  def remove_cached_accessions(accessions:Iterable[str])->List[str]:
    if not self.accessions:
      return accessions
    noncached = []
    while accessions:
      a = accessions.pop()
      if a not in self.accessions:
        noncached.append(a)
    return noncached

  def incache(self, name=None, taxid=None):
    return name in self.accessions

  def is_empty(self):
    if self.accessions:
      return False
    return True
