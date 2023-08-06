"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import sys
import json
import logging
import resource
from typing import List, Mapping, Type, Iterable

from ncbi_taxonomist import utils
from ncbi_taxonomist.cache import cache
from ncbi_taxonomist.collect import collector
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.convert import accessiondb
from ncbi_taxonomist.convert import ncbiaccession
from ncbi_taxonomist.db import dbimporter
from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.map import mapper
from ncbi_taxonomist.map import mapparser
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.resolve import resolver
from ncbi_taxonomist.resolve import resolveparser
from ncbi_taxonomist.subtree import subtreeanalyzer
import ncbi_taxonomist.groupmanager

class NcbiTaxonomist:

  cache = cache.Cache()

  def __init__(self, dbpath:str=None, email:str=None):
    self.logger = logging.getLogger(utils.resolve_log_nspace(NcbiTaxonomist))
    self.email:str = email
    self.db:Type[dbmanager.TaxonomyDb] = None
    if dbpath:
      self.db = dbmanager.TaxonomyDb(dbpath)
      self.logger.info("{}: Successfully connected".format(self.db.path))

  def map_taxa(self, taxids:Iterable[int]=None, names:Iterable[str]=None, remote:bool=False):
    """Map names to taxids and vice-versa. Print mappings as JSON to STDOUT."""
    tm = mapper.Mapper(self.db, self.email)
    if self.db and names:
      self.logger.debug("Map:{}::names:{}::{}".format(self.db.path, len(names), names))
      self.logger.info("Mapping {} names in {}".format(len(names), self.db.path,))
      names = NcbiTaxonomist.cache.update_query('taxa', tm.map_names(names, taxadb.TaxaDbConverter(taxon.Taxon())))
      taxids = NcbiTaxonomist.cache.remove_cached_taxids(taxids)

    if self.db and taxids:
      self.logger.debug("Map:{}::taxids:{}::{}".format(self.db.path, len(taxids), taxids))
      taxids = NcbiTaxonomist.cache.update_query('taxa', tm.map_taxids(taxids, taxadb.TaxaDbConverter(taxon.Taxon())))
      names = NcbiTaxonomist.cache.remove_cached_names(names)

    if remote and names:
      self.logger.debug("Map:{}::names:{}::{}".format("rem", len(names), names))
      names = NcbiTaxonomist.cache.update_query('taxa', tm.map_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon())))
      taxids = NcbiTaxonomist.cache.remove_cached_taxids(taxids)

    if remote and taxids:
      self.logger.debug("Map:{}::taxids:{}::{}".format("rem", len(taxids), taxids))
      taxids = NcbiTaxonomist.cache.update_query('taxa', tm.map_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon())))
      names = NcbiTaxonomist.cache.remove_cached_names(names)

    if taxids:
      self.logger.info("Failed to map taxids:{}::{}".format(len(taxids), taxids))
    if names:
      self.logger.info("Failed to map names:{}::{}".format(len(names), names))

  def map_accessions(self, accessions:Iterable[str], entrezdb:str, remote:bool=False):
    """Map accessions to taxids. Print mappings as JSON to STDOUT. """
    tm = mapper.Mapper(self.db, self.email)
    if self.db and accessions:
      self.logger.debug("Map:{}::{}:accs:{}:({})".format(self.db.path, entrezdb, len(accessions), accessions))
      accessions = NcbiTaxonomist.cache.update_query('accessions', tm.map_accessions(accessions, entrezdb,
                        accessiondb.DbAccessionConverter(accession.AccessionData())))

    if remote and accessions:
      self.logger.debug("Map:{}::{}:accs:{}:({})".format("rem", entrezdb, len(accessions), accessions))
      accessions = NcbiTaxonomist.cache.update_query('accessions', tm.map_accessions_remote(accessions, entrezdb,
                                                      ncbiaccession.NcbiAccessionConverter(accession.AccessionData())))
    if accessions:
      self.logger.info("Failed to map accessions:{}::{}".format(len(accessions), accessions))

  def collect(self, taxids:Iterable[int]=None, names:Iterable[str]=None):
    """Collect taxa information remotely from Entrez."""
    tc = collector.Collector(self.email)
    if names:
      self.logger.debug("Collect names::rem::{}::({})".format(len(names), names))
      tc.collect_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))
    if taxids:
      self.logger.debug("Collect taxids::rem::{}::({})".format(len(taxids), taxids))
      tc.collect_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def import_to_db(self, out_attrib:str):
    """
      Import data to local taxonomy database. Attribute names can be passed to
      filter them for piped processing.
    """
    dbimporter.import_stdin(self.db, out_attrib)

  def resolve(self, taxids:Iterable[int]=None, names:Iterable[str]=None, remote:bool=False):
    """
    Resolve lineages for names and taxids. If a local database is given, it
    will be checked first, followed by checking Entrez remotely if requested.
    Lineages are JSON arrays.
    """
    tr = resolver.Resolver(self.db, self.email)
    if self.db and names:
      self.logger.debug("resolve::{}::names::{} ({})".format(self.db.path, len(names), names))
      names = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_names(names, taxadb.TaxaDbConverter(taxon.Taxon())))
    if self.db and taxids:
      self.logger.debug("resolve::{}::taxids::{} ({})".format(self.db.path, len(taxids), taxids))
      taxids = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_from_cache(NcbiTaxonomist.cache, taxids=taxids))
      taxids = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_taxids(taxids, taxadb.TaxaDbConverter(taxon.Taxon())))
    if remote and names:
      self.logger.debug("resolve::{}::names::{} ({})".format("rem", len(names), names))
      names = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_from_cache(NcbiTaxonomist.cache, names=names))
      names = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon())))
    if remote and taxids:
      self.logger.debug("resolve::{}::taxids::{} ({})".format("rem", len(taxids), taxids))
      taxids = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_from_cache(NcbiTaxonomist.cache, taxids))
      taxids = NcbiTaxonomist.cache.update_query('lineages', tr.resolve_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon())))
    if taxids is None and names is None:
      tr.resolve_stdin()

    if taxids:
      self.logger.info("Failed to resolve taxids:{}::{}".format(len(taxids), taxids))
    if names:
      self.logger.info("Failed to resolve names:{}::{}".format(len(names), names))

  def resolve_accession_map(self, remote:bool=False):
    """Resolve lineages for accessions from STDIN. Lineages are JSON arrays."""
    accs:Dict[str,Type[accession.AccessionData]] = {}
    taxids:Dict[int,Type[taxon.Taxon]] = {}
    mapparser.parse_accession_map(accs, taxids)
    tr = resolver.Resolver(self.db, self.email)
    if self.db and accs:
      self.logger.debug("resolve::{}::accessions::{}".format(self.db.path, len(accs)))
      accs = NcbiTaxonomist.update_query('accessions', tr.resolve_accession_mapping(taxids, accs, taxadb.TaxaDbConverter(taxon.Taxon())))
    if remote and accs:
      self.logger.debug("resolve::{}::accessions::{}".format("rem", len(accs)))
      queries = tr.resolve_accession_mapping_remote(taxids, accs, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def get_subtree(self, taxids:list=None, names:list=None, rank:str=None,
                  upper_rank:str=None, lower_rank:str=None, remote:bool=False):
    """Fetch children for requested taxids or names. Solve the upper and lower
       rank limitations  after collecting a subtree"""
    if upper_rank is not None or lower_rank is not None:
      if upper_rank == lower_rank:
        rank = upper_rank
      else:
        rank = None
    if rank is not None:
      upper_rank = None
      lower_rank = None

    if self.db:
      sta = subtreeanalyzer.SubtreeAnalyzer(self.db, self.email)
      subtree = sta.collect_subtree(taxids, names, taxadb.TaxaDbConverter(taxon.Taxon()))
      if taxids:
        for i in taxids:
          sta.assemble_lineage(i, subtree, rank, upper_rank, lower_rank, taxadb.TaxaDbConverter(taxon.Taxon()))
      if names:
        mapping = self.db.names_to_taxid(names)
        for i in names:
          if i in mapping:
            sta.assemble_lineage(mapping[i], subtree, rank, upper_rank, lower_rank, taxadb.TaxaDbConverter(taxon.Taxon()), i)

    if taxids is None and names is None:
      pass
      #tr.resolve_stdin()

  def groupmanager(self):
    return ncbi_taxonomist.groupmanager.GroupManager(self.db)
