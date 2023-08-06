"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import json


from ncbi_taxonomist.model import taxon


def parse_taxa(taxa, queries)->None:
  parents:set[int] = set()
  for i in sys.stdin:
    t = taxon.Taxon().new_from_json(i.strip())
    parents.add(t.parent_id)
    if t.taxon_id not in taxa:
      taxa[t.taxon_id] = t

  for i in taxa:
    if i not in parents:
      queries.append(taxa[i].taxon_id)
