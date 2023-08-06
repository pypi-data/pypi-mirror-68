"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import json
from typing import Dict, Iterable, Mapping, Set, Type

from ncbi_taxonomist import utils
from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.map import remotemapper
from ncbi_taxonomist.map import remoteaccessionmapper
from ncbi_taxonomist.map.query import taxidmapquery
from ncbi_taxonomist.map.query import namemapquery
from ncbi_taxonomist.map.query import accessionmapquery
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.convert import accessiondb
from ncbi_taxonomist.convert import ncbiaccession


class Mapper:

  def __init__(self, db:Type[dbmanager.TaxonomyDb], email:str):
    self.db = db
    self.email = email

  def map_names(self, names:Iterable[str],
                      converter:Type[taxadb.TaxaDbConverter])->Dict:
    nmq = namemapquery.NameMapQuery(names)
    self.db.get_taxa_by_name(names, converter, nmq)
    return nmq.queries

  def map_names_remote(self, names:Iterable[str],
                       converter:Type[ncbitaxon.NcbiTaxonConverter])->Dict:
    nmq = namemapquery.NameMapQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remotemapper.RemoteMapper(nmq, converter))
    return nmq.queries

  def map_taxids(self, taxids:Iterable[int], converter:Type[taxadb.TaxaDbConverter]):
    tmq = taxidmapquery.TaxidMapQuery(taxids)
    self.db.get_taxa_by_taxids(taxids, converter, tmq)
    return tmq.queries

  def map_taxids_remote(self, taxids:Iterable[int],
                        converter:Type[ncbitaxon.NcbiTaxonConverter])->Dict:
    tmq = taxidmapquery.TaxidMapQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remotemapper.RemoteMapper(tmq, converter))
    return tmq.queries

  def map_accessions(self, accessions:Iterable[str], entrezdb:str,
                     converter:Type[accessiondb.DbAccessionConverter])->Dict:
    amq = accessionmapquery.AccessionMapQuery(accessions)
    self.db.get_taxa_by_accessions(accessions, entrezdb, converter, amq)
    return amq.queries

  def map_accessions_remote(self, accessions:Iterable[str], entrezdb:str,
                            converter:Type[ncbiaccession.NcbiAccessionConverter])->Dict:
    amq = accessionmapquery.AccessionMapQuery(accessions)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_accessions(accessions, entrezdb, remoteaccessionmapper.RemoteAccessionMapper(amq, converter))
    return amq.queries
