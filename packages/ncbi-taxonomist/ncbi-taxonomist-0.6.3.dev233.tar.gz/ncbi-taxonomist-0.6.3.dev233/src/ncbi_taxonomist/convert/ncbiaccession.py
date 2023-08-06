"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
from typing import Dict, Mapping, Type


from ncbi_taxonomist.model import accession
from ncbi_taxonomist.convert import converter
from ncbi_taxonomist.convert import convertermap

class NcbiAccessionConverter(converter.ModelConverter):

  def __init__(self, accs_datamodel:Type[accession.AccessionData]):
    super().__init__(accs_datamodel)

  def convert_to_model(self, attributes:Mapping[str,any], srcdb) -> Type[accession.AccessionData]:
    mattribs = {'uid':attributes.pop('uid'), 'db': srcdb, 'accessions': {}}
    self.map_inattributes(mattribs, attributes, convertermap.attributes)
    if srcdb not in convertermap.accessions:
      print("{}: database not supported".format(srcdb), file=sys.stdout)
      return None
    if srcdb in convertermap.accessions:
      for i in convertermap.accessions[srcdb]:
        if i in attributes:
          mattribs['accessions'][i] = attributes.pop(i)
    return self.model.new(mattribs)

  def convert_from_model(self, model:Type[accession.AccessionData], outdict=None)->Dict[str,str]:
    attrib = model.attributes()
    attrib.update({'accessions':{'uid':model.uid}})
    return attrib
