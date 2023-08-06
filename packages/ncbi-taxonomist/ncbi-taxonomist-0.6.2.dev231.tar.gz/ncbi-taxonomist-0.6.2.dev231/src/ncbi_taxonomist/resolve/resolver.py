"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Set, Type, Iterable, Mapping


from ncbi_taxonomist.db import dbmanager
from ncbi_taxonomist.model import accession
from ncbi_taxonomist.remote import remotequery
from ncbi_taxonomist.convert import taxadb
from ncbi_taxonomist.convert import ncbitaxon
from ncbi_taxonomist.convert import accessiondb
from ncbi_taxonomist.resolve import remoteresolver
from ncbi_taxonomist.resolve import resolveparser
from ncbi_taxonomist.resolve import lineageresolver
from ncbi_taxonomist.resolve.query import nameresolvequery
from ncbi_taxonomist.resolve.query import taxidresolvequery
from ncbi_taxonomist.resolve.query import accessionresolvequery


class Resolver:

  def __init__(self, db:Type[dbmanager.TaxonomyDb], email:str):
    self.db = db
    self.email = email

  def resolve_taxids(self, taxids:Iterable[int], converter:Type[taxadb.TaxaDbConverter])->Dict:
    if not taxids:
      return None
    trq = taxidresolvequery.TaxidResolveQuery(taxids)
    self.db.get_taxid_lineages(taxids, converter, trq)
    return trq.queries

  def resolve_taxids_remote(self, taxids:Iterable[int],
                            converter:Type[ncbitaxon.NcbiTaxonConverter])->Dict:
    if not taxids:
      return None
    trq = taxidresolvequery.TaxidResolveQuery(taxids)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids(taxids, remoteresolver.RemoteResolver(trq, converter))
    return trq.queries

  def resolve_names(self, names:Iterable[str], converter:Type[taxadb.TaxaDbConverter])->Dict:
    if not names:
      return None
    taxids = [x for x in self.db.get_taxa_by_name(names, converter)]
    nrq = nameresolvequery.NameResolveQuery(names)
    self.db.get_taxid_lineages(taxids, converter, nrq)
    return nrq.queries

  def resolve_names_remote(self, names:Iterable[str],
                           converter:Type[ncbitaxon.NcbiTaxonConverter])->Dict:
    if not names:
      return None
    nrq = nameresolvequery.NameResolveQuery(names)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_names(names, remoteresolver.RemoteResolver(nrq, converter))
    return nrq.queries

  def resolve_accession_mapping(self, taxids:Mapping[int,Iterable[str]],
                                      accs:Mapping[str,Type[accession.AccessionData]],
                                      converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[str]:
    """Resolve taxid lineages from an accession mapping. Find taxids in local
    database, resolve their lineage, and add to corresponding accessions."""
    if not accs:
      return None
    arq = accessionresolvequery.AccessionResolveQuery(taxids, accs)
    self.db.get_taxid_lineages([x for x in taxids], converter, arq)
    return arq.accs

  def resolve_accession_mapping_remote(self, taxids:Mapping[int, Iterable[str]],
                                       accs:Mapping[str,Type[accession.AccessionData]],
                                       converter:Type[ncbitaxon.NcbiTaxonConverter])->Set[str]:
    """Resolve taxid lineages from an accession mapping. Find taxids remotely,
    and resolve their lineage, and add to corresponding accessions."""
    if not accs:
      return None
    arq = accessionresolvequery.AccessionResolveQuery(taxids, accs)
    rtq = remotequery.RemoteTaxonomyQuery(self.email)
    rtq.query_taxids([x for x in taxids], remoteresolver.RemoteResolver(arq, converter))
    return arq.accs

  def resolve_stdin(self):
    """Resolve lineages for taxa piped via STDIN from a preceding taxonomist
    command."""
    taxa:Dict[int,Type[taxon.Taxon]] = {}
    queries:List[int] = []  #taxa identified as starting point for resolving
    resolveparser.parse_taxa(taxa, queries)
    if not queries:
      return None
    taxidresolvequery.TaxidResolveQuery(queries).resolve(queries, taxa)

  def resolve_from_cache(self, cache, taxids=None, names=None):
    #print("Trying resolve from cache")
    if names:
      nrq = nameresolvequery.NameResolveQuery(names)
      #print("\tnames: {}, {}".format(names, [x for x in cache.union_taxid_names(taxids, names)]))
      nrq.resolve([x for x in cache.union_taxid_names(taxids, names)], cache.get_taxa())
      return nrq.queries
    #print("\ttaxids: {}, {}".format(taxids, [x for x in cache.union_taxid_names(taxids, names)]))
    trq = taxidresolvequery.TaxidResolveQuery(taxids)
    trq.resolve([x for x in cache.union_taxid_names(taxids, names)], cache.get_taxa())
    return trq.queries
