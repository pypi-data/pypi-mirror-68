"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from typing import Type, Iterable


from ncbi_taxonomist.model import taxon


class MapQuery:

  def __init__(self):
    pass

  def map_query(self, taxon:Type[taxon.Taxon]):
    raise NotImplementedError
