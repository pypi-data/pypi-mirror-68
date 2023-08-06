#!/usr/bin/env python3
"""
..
  Copyright 2020

.. moduleauthor:: Jan Piotr Buchmann <jpb@members.fsf.org>
"""

import io
import os
import sys
import json
from typing import Iterable,  Mapping, Tuple, Type

import ncbi_taxonomist.utils
import ncbi_taxonomist.group.parser
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.convert import taxadb

class GroupManager:

  def __init__(self, db)->None:
    self.db = db

  def add(self, taxids:Iterable[int], names:Iterable[str], groupname:str)->None:
    values = []
    if taxids is None and names is None:
      gp = ncbi_taxonomist.group.parser.GroupParser()
      values = gp.parse(groupname)
    else:
      seen_taxids = set(taxids)
      while taxids:
        values.append((taxids.pop(), groupname))
        seen_taxids.add(values[-1][0])
      if names:
        for i in self.db.get_taxa_by_name(names, taxadb.TaxaDbConverter(taxon.Taxon())):
          if i.taxon_id not in seen_taxids:
            seen_taxids.add(i.taxon_id)
            values.append((i.taxon_id, groupname))
      seen_taxids.clear()
    self.db.add_group(values)

  def remove(self, taxids:Iterable[int], names:Iterable[str], groupname:str)->None:
    if taxids is None and names is None and groupname is not None:
      self.db.remove_group(groupname)
    else:
      self.db.remove_from_group(taxids, names, groupname)

  def move(self, srcgroup, targetgroup, taxids, names):
    pass

  def retrieve_groups(self, groupnames:Iterable[str])->None:
    if groupnames is not None:
      for i in groupnames:
        self.retrieve_group(i)
    else:
      self.retrieve_group(None)

  def retrieve_group(self, groupname):
    groups = {}
    prev = None
    for i in self.db.retrieve_group(groupname):
      if i['name'] not in groups:
        if groups:
          ncbi_taxonomist.utils.json_stdout({'group:': prev, 'taxa': [x for x in groups[prev]]})
        prev = i['name']
        groups[i['name']] = []
      groups[i['name']].append(i['taxon_id'])
    if groups:
      ncbi_taxonomist.utils.json_stdout({'group:': prev, 'taxa': [x for x in groups[prev]]})

  def list_groups(self):
    for i in self.db.retrieve_group_names():
      print(i['name'])


