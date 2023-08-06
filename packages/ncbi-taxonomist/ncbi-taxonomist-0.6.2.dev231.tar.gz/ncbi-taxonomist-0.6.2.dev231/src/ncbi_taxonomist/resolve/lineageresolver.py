"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
from typing import Dict, Iterable, List, Mapping, Type

from ncbi_taxonomist.model import taxon

def find_taxon(taxid, taxa, alias):
  if taxid in taxa:
    return taxa[taxid]
  if not alias.get(taxid):
    return None
  return alias.get(taxid)

def assemble_lineage(taxid, taxa, alias, start, stop, single):
  """Assemble lineage from leaf/start rank to root/stop rank"""
  taxon = find_taxon(taxid, taxa, alias)
  if not taxon:
    return None

  collect = set_collect_flag(start, stop, single)
  #print("start:", start, ":: stop:", stop, "::", "rank: ", single, collect )
  lineage = []
  while taxon.parent_id:
    if single is not None and taxon.isrank(single):
      lineage.append(taxon)
      return lineage
    #print(taxon.get_rank(), start, stop, single, collect)
    if start is not None and taxon.isrank(start):
      #print("\tstarting", taxon.get_attributes())
      collect = True
    if stop is not None and taxon.isrank(stop):
        #print("\tstopping", taxon.get_attributes())
        lineage.append(taxon)
        return lineage
    if collect:
      #print("\tadding", taxon.get_attributes())
      lineage.append(taxon)
    taxon = find_taxon(taxon.parent_id, taxa, alias)

  if start is not None and taxon.isrank(start):
      lineage.append(taxon)
  elif stop is not None and taxon.isrank(stop):
    lineage.append(taxon)
  else:
    lineage.append(taxon)
  return lineage

def set_collect_flag(start, stop, single):
  """Set collection flag based on requested ranks"""
  if single is not None:
    return False
  if start is not None:
    return False
  return True

def resolve_lineages(taxids:Iterable[int], taxa:Mapping[int,Type[taxon.Taxon]], alias=None, start=None, stop=None, single=None)->Dict[int,List[Type[taxon.Taxon]]]:
  if not alias:
    alias = {}
  lineages:Dict[int,List[Type[taxon.Taxon]]] = {}
  for i in taxids:
    lineages[i] = resolve_lineage(i, taxa, alias, start, stop, single)
  return lineages

def resolve_lineage(taxid:int, taxa:Mapping[int,Type[taxon.Taxon]], alias=None, start=None, stop=None, single=None)->List[Type[taxon.Taxon]]:
  if not alias:
    alias = {}
  return assemble_lineage(taxid, taxa, alias, start, stop, single)

def check_resolve(lineages):
  """Check if lineage has been resolved. Assumes lineage root->lowest rank.
  The lowest rank (last element in list) is assumed to be the query

  :param dict lineages: resolved lineages (list with taxonmodel instances)
  :return bool:
  """
  for i in lineages:
    for j in lineages[i]:
      if j.rank == 'superkingdom':
        return True
    print("W: unresolved lineage: {}:{}:{}".format(i, lineages[i].name, lineages[i].scientific_name),
          file=sys.stderr)
    return False
