"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import logging
from typing import Set, Type, Iterable

from ncbi_taxonomist import utils
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.model import taxon
from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.collect import remotecollector
from ncbi_taxonomist.collect.query import namecollectquery
from ncbi_taxonomist.collect.query import taxidcollectquery


class Collector:
  """Collect taxon information from Entrez server"""

  def __init__(self, email:str):
    self.logger = logging.getLogger(utils.resolve_log_nspace(Collector))
    self.email = email

  def collect(self, names, taxids):
    if names:
      self.logger.debug("Collect names::{}::({})".format(len(names), names))
      self.collect_names_remote(names, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))
    if taxids:
      self.logger.debug("Collect taxids::{}::({})".format(len(taxids), taxids))
      self.collect_taxids_remote(taxids, ncbitaxon.NcbiTaxonConverter(taxon.Taxon()))

  def collect_names_remote(self, names:Iterable[str], converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    ncq = namecollectquery.NameCollectQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remotecollector.RemoteCollector(ncq, converter))
    return ncq.queries

  def collect_taxids_remote(self, taxids:Iterable[int], converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[int]:
    tcq = taxidcollectquery.TaxidCollectQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remotecollector.RemoteCollector(tcq, converter))
    return tcq.queries
