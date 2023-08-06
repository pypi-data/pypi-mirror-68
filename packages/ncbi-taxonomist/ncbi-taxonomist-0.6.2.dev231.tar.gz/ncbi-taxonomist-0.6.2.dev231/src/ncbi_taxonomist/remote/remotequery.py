"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import entrezpy.conduit


class RemoteTaxonomyQuery:

  conduit = None

  @staticmethod
  def query_taxids(taxids, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    pipe.add_fetch({'db':'taxonomy', 'id':taxids, 'mode':'xml'}, analyzer=analyzer)
    RemoteTaxonomyQuery.conduit.run(pipe)

  @staticmethod
  def query_names(names, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    sid = pipe.add_search({'db':'taxonomy', 'term':' OR '.join("\"{}\"".format(x) for x in names)})
    pipe.add_fetch({'mode':'xml'}, dependency=sid, analyzer=analyzer)
    RemoteTaxonomyQuery.conduit.run(pipe)

  @staticmethod
  def query_accessions(accessions, database, analyzer):
    pipe = RemoteTaxonomyQuery.conduit.new_pipeline()
    sid = pipe.add_search({'db':database, 'term':' OR '.join("\"{}\"".format(x) for x in accessions)})
    pipe.add_summary({'mode':'json'}, dependency=sid, analyzer=analyzer)
    return RemoteTaxonomyQuery.conduit.run(pipe).get_result()

  def __init__(self, email):
    RemoteTaxonomyQuery.conduit = entrezpy.conduit.Conduit(email)
