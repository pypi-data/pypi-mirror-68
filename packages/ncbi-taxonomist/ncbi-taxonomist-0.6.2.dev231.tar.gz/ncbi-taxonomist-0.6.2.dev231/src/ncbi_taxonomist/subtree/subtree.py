"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import io
import os
import sys
from typing import Set

class Subtree:

  class Node:

    def __init__(self, taxid, parent_id=None):
      self.taxid = taxid
      self.parent_id = parent_id
      self.children = set()

  def __init__(self):
    self.taxa = {}
    self.nodes = {}

  def add_taxon(self, taxon):
    if taxon.taxon_id not in self.taxa:
      self.taxa[taxon.taxon_id] = taxon
    if taxon.taxon_id not in self.nodes:
      self.nodes[taxon.taxon_id] = Subtree.Node(taxon.taxon_id)
    if taxon.parent_id is not None and taxon.parent_id not in self.nodes:
      self.nodes[taxon.parent_id] = Subtree.Node(taxon.parent_id)
    self.nodes[taxon.taxon_id].parent_id = taxon.parent_id
    if taxon.parent_id is not None:
      self.nodes[taxon.parent_id].children.add(taxon.taxon_id)

  def isCollected(self, taxid)->bool:
    return taxid in self.taxa

  def has_taxon(self, taxid):
    return taxid in self.taxa

  def get_taxon(self, taxid):
    return self.taxa[taxid]
