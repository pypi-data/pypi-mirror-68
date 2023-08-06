"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import logging
import sqlite3
from typing import Iterable, Dict, List, Mapping, Tuple, Type


from ncbi_taxonomist import utils
from ncbi_taxonomist.convert import converter
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.db.table import taxa
from ncbi_taxonomist.db.table import names
from ncbi_taxonomist.db.table import accessions
from ncbi_taxonomist.db.table import groups
from ncbi_taxonomist.map.query import mapquery
from ncbi_taxonomist.model import datamodel
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.resolve.query import resolvequery
import ncbi_taxonomist.subtree.subtree


class TaxonomyDb:

  def __init__(self, dbpath:str):
    self.logger = logging.getLogger(utils.resolve_log_nspace(TaxonomyDb))
    self.path = dbpath
    self.logger.debug("{}: Create instance".format(self.path))
    self.connection = self.init_connection()
    self.taxatbl = taxa.TaxaTable(self.path).create(self.connection)
    self.nametbl = names.NameTable(self.path).create(self.connection)
    self.accessiontbl = accessions.AccessionTable(self.path).create(self.connection)
    self.grouptbl = groups.GroupTable(self.path).create(self.connection)
    self.logger.debug("{}: Database initialized".format(self.path))

  def init_connection(self)->sqlite3.Connection:
    self.logger.debug("{}: Connecting".format(self.path))
    connection = sqlite3.connect(self.path)
    connection.execute("PRAGMA foreign_keys=1")
    connection.row_factory = sqlite3.Row
    self.logger.debug("{}: Connected".format(self.path))
    return connection

  def close_connection(self)->None:
    self.logger.debug("{}: Closing connection".format(self.path))
    self.connection.close()

  def connect(self) -> sqlite3.Connection:
    if self.connection is None:
      return self.init_connection(self.path)
    return self.connection

  def add_taxa(self, taxa:Iterable[Tuple[int,str,int]])->None:
    self.taxatbl.insert(self.connection, taxa)

  def add_taxids(self, taxids:Iterable[Tuple[int,]])->None:
    self.taxatbl.insert_taxids(self.connection, taxids)

  def add_names(self, names:Iterable[Tuple[int,str,str]])->None:
    self.nametbl.insert(self.connection, names)

  def add_accessions(self, accessions:Iterable[Tuple[str,str,str,int]])->None:
    self.accessiontbl.insert(self.connection, accessions)

  def add_group(self, values:[Iterable[Tuple[int,str]]]):
    self.grouptbl.insert(self.connection, values)

  def collect_name_subtree(self, start_names, converter, torank=None):
    raise NotImplementedError

  def collect_subtree(self, taxid:int, converter:Type[taxadb.TaxaDbConverter], subtree=None)->List:
    """ Collect subtree for given taxon ids. """
    if subtree is None:
      subtree = ncbi_taxonomist.subtree.subtree.Subtree()
    if not subtree.isCollected(taxid):
      for i in self.taxatbl.get_subtree(self.connection, taxid):
        if not subtree.has_taxon(i['taxon_id']):
          subtree.add_taxon(converter.convert_to_model({'taxon_id': i['taxon_id'],
                                                                    'parent_id':i['parent_id'],
                                                                    'rank':i['rank']}))
        subtree.taxa[i['taxon_id']].update_names({i['name']:i['type']})
    return subtree

  def get_taxa_by_name(self, names:Iterable[str], converter:Type[converter.ModelConverter],
                       query:Type[mapquery.MapQuery]=None,
                       taxa:Mapping[int,datamodel.DataModel]=None)->Dict[int,datamodel.DataModel]:
    """Collect taxa by name and converter to appropriate model.

    .. todo:: Test if n.name='man' OR n.name='Bacteria OR ...' is better approach
    """
    if taxa is None:
      taxa = {}
    taxidqry = """SELECT taxon_id FROM names  WHERE name=?"""
    for i in names:
      taxid = self.connection.cursor().execute(taxidqry, (i,)).fetchone()
      if taxid is not None and taxid[0] not in taxa:
        taxa[taxid[0]] = None
    qry = """SELECT n.name, n.type, t.taxon_id, t.rank, t.parent_id FROM taxa t
             JOIN names n on t.taxon_id=n.taxon_id WHERE t.taxon_id=?"""
    for i in taxa:
      for j in self.connection.cursor().execute(qry, (i,)):
        if taxa[j['taxon_id']] is None:
          taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                            'parent_id':j['parent_id'],
                                                            'rank':j['rank']})
        taxa[j['taxon_id']].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(taxa[i])
    return taxa

  def names_to_taxid(self, names:Iterable[str])->Dict[str,int]:
    """Return mapping of given name to correspondong taxid."""
    mapping = {}
    for i in names:
      row = self.nametbl.name_to_taxid(self.connection, i).fetchone()
      if row:
        mapping[row['name']] = int(row['taxon_id'])
    return mapping

  def get_taxa_by_accessions(self, accs:Iterable[str], db:str, converter:Type[converter.ModelConverter],
                             query:Type[mapquery.MapQuery]=None)->Dict[int,datamodel.DataModel]:
    """Collect taxa by accession and converter to appropriate model."""
    uids = {}
    uidqry =  """SELECT db, uid FROM accessions WHERE accession=? AND db=?"""
    if not db:
      uidqry = """SELECT db, uid FROM accessions WHERE accession=? AND db LIKE ?)"""
      for i in accs:
        row = self.connection.cursor().execute(uidqry, (i, db))
        if row is not None:
          if rows['db'] not in uids:
            uids[rows['db']] = []
          uids[rows['db']].append(rows['uid'])
    stmt = """SELECT a.uid, a.accession, a.db, a.type, t.taxon_id
              FROM accessions a JOIN taxa t on a.taxon_id=t.taxon_id
              WHERE a.uid=? and a.db=?"""
    mappings = {}
    for i in uids:
      for j in uids[i]:
        for k in self.connection.cursor().execute(stmt, (j, i)):
          if k['uid'] not in mappings:
            mappings[k['uid']] = converter.convert_to_model({'accessions':{j['type']:j['accession']},
                                                             'taxon_id':j['taxon_id'], 'db':j['db'],
                                                             'uid': j['uid']})
          mappings[j['uid']].update_accessions({j['type']:j['accession']})
        if query and mappings:
          query.map_query(mappings[j])
    return mappings

  def get_taxa_by_taxids(self, taxids:Iterable[int], converter:Type[converter.ModelConverter],
                         query:Type[mapquery.MapQuery]=None)->Dict[int, datamodel.DataModel]:
    """Collect taxa by taxid and converter to appropriate model."""
    qry = """SELECT t.taxon_id, t.rank, t.parent_id, n.name, n.type
             FROM taxa t JOIN names n on t.taxon_id=n.taxon_id WHERE t.taxon_id=?"""
    taxa = {}
    for i in taxids:
      for j in self.connection.cursor().execute(qry, (i,)):
        if j['taxon_id'] not in taxa:
          taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                            'parent_id':j['parent_id'],
                                                            'rank':j['rank']})
        taxa[j['taxon_id']].update_names({j['name']:j['type']})
      if query and taxa:
        query.map_query(taxa[j['taxon_id']])
    return taxa

  def get_taxid_lineages(self, taxids:Iterable[int], converter:Type[converter.ModelConverter],
                         query:Type[resolvequery.ResolveQuery]=None)->Dict[int, datamodel.DataModel]:
    """Collect lineage taxa for multiple taxid."""
    taxa = {}
    for i in taxids:
      if i not in taxa:
        self.get_lineage(i, converter, taxa)
      if query and taxa:
        query.resolve(set([i]), taxa)
    return taxa

  def get_taxid_lineage(self, taxid:int, converter:Type[converter.ModelConverter],
                        query:Type[resolvequery.ResolveQuery]=None,
                        taxa:Mapping[int,datamodel.DataModel]=None)->Dict[int,datamodel.DataModel]:
    """Collect lineage taxa for a single taxid."""
    if taxa is None:
      taxa = {}
    self.get_lineage(taxid, converter, taxa)
    if query and taxa:
      query.resolve(set([taxid]), taxa)
    return taxa

  def get_lineage(self, taxid, converter:Type[converter.ModelConverter], taxa)->None:
    for j in self.taxatbl.get_lineage(self.connection, taxid, self.nametbl.name):
      if j['taxon_id'] not in taxa:
        taxa[j['taxon_id']] = converter.convert_to_model({'taxon_id': j['taxon_id'],
                                                          'parent_id':j['parent_id'],
                                                          'rank':j['rank']})
      taxa[j['taxon_id']].update_names({j['name']:j['type']})

  def remove_group(self, groupname):
    self.grouptbl.delete_group(self.connection, groupname)

  def remove_from_group(self, taxids, names, groupname):
    values = []
    seen_taxids = set()
    while taxids:
      values.append((taxids.pop(), groupname))
      seen_taxids.add(values[-1][0])

    if names:
      stmt = """SELECT taxon_id FROM names WHERE name=?"""
      for i in names:
        taxid = self.connection.cursor().execute(stmt, (i,)).fetchone()[0]
        if taxid is not None and taxid not in seen_taxids:
          values.append((taxid, groupname))
          seen_taxids.add(taxid)
    seen_taxids.clear()
    self.grouptbl.delete_from_group(self.connection, values)

  def retrieve_group_names(self):
    return self.grouptbl.retrieve_names(self.connection)

  def retrieve_group(self, groupname):
    return self.grouptbl.retrieve_group(self.connection, groupname)
