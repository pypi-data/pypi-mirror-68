"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import io
import os
import sys
from typing import Dict, Set, Type, Iterable, List, Mapping

from ncbi_taxonomist import utils
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.resolve import lineageresolver
import ncbi_taxonomist.subtree.subtree

class SubtreeAnalyzer:

  def __init__(self, db:Type[dbmanager.TaxonomyDb], email:str):
    self.db = db
    self.email = email

  def assemble_lineage(self, taxid, subtree, rank, upper_rank, lower_rank, converter, name=None)->List[List]:
    lineages = []
    paths = self.backtrack(subtree.taxa, subtree.nodes, subtree.nodes[taxid],
                            self.set_rank_cutoff(rank, lower_rank), [], set())
    for i in paths:
      clipped = self.clip(subtree, i, rank, upper_rank, lower_rank, converter)
      if clipped:
        if rank and self.test_single(clipped, rank):
          lineages.append(clipped)
        elif upper_rank and lower_rank:
          if self.test_rank(clipped[-1], upper_rank) and self.test_rank(clipped[0], lower_rank):
            lineages.append(clipped)
        elif upper_rank  and self.test_rank(clipped[-1], upper_rank):
          lineages.append(clipped)
        elif lower_rank and self.test_rank(clipped[0], lower_rank):
          lineages.append(clipped)
        else:
          if rank is None and upper_rank is None and lower_rank is None:
            lineages.append(clipped)
    for i in lineages:
      if name:
        utils.json_stdout({'name': name, 'subtrees': [x.get_attributes() for x in i]})
      else:
        utils.json_stdout({'taxid': taxid, 'subtrees': [x.get_attributes() for x in i]})

  def test_single(self, path, rank):
    if (len(path) != 1) or not path[0].isrank(rank):
      return False
    return True

  def test_rank(self, taxon, rank):
    if not taxon.isrank(rank):
      return False
    return True

  def clip(self, subtree, path, rank, upper_rank, lower_rank, converter):
    if upper_rank is not None and lower_rank is not None:  # taxa between upper and lower rank for given taxid
      if (path[0].get_rank() == upper_rank) and (path[-1].get_rank() == lower_rank):
        return path
    if path[0].get_parent() is not None:
      self.db.get_taxid_lineage(path[0].get_parent(), converter, taxa=subtree.taxa)
    return lineageresolver.resolve_lineage(path[-1].taxon_id, subtree.taxa, start=lower_rank, stop=upper_rank, single=rank)

  def set_rank_cutoff(self, rank, lower_rank):
    """Set lowest rank to look for. If none is given, find lowest, i.e. rank
       without children"""
    if rank is not None:
      return rank
    if lower_rank is not None:
      return lower_rank
    return None

  def backtrack(self, taxa, nodes, node, rank_cutoff, path, visited)->List[List]:
    """Find all lineages above starting node."""
    path = path + [taxa[node.taxid]]
    visited.add(node.taxid)
    if self.return_path(taxa, node, rank_cutoff):
      return [path]
    paths = []
    for i in node.children:
      if i not in visited:
        paths += self.backtrack(taxa, nodes, nodes[i], rank_cutoff, path, visited)
    return paths

  def return_path(self, taxa, node, rank_cutoff):
    """Tests if we can break backtracking. The boolean test could be likely
       inverted but has clearer conditions."""
    if(((rank_cutoff is None) and (not node.children)) or not node.children or
       (rank_cutoff and taxa[node.taxid].rank == rank_cutoff)):
      return True
    return False

  def collect_subtree(self, taxids:Iterable[int], names:Iterable[int], converter:Type[taxadb.TaxaDbConverter]):
    """ Collect subtree for given taxon ids. """
    subtree = ncbi_taxonomist.subtree.subtree.Subtree()
    if names:
      for i in self.db.get_taxa_by_name(names, converter):
        self.db.collect_subtree(i, converter, subtree)
    if taxids:
      for i in taxids:
        self.db.collect_subtree(i, converter, subtree)
    return subtree
