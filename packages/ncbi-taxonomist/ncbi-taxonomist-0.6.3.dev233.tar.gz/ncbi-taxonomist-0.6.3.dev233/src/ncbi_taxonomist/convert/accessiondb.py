"""
..
  Copyright 2019, 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


from typing import Dict, Type, Mapping


from ncbi_taxonomist.model import accession
from ncbi_taxonomist.convert import converter

class DbAccessionConverter(converter.ModelConverter):

  def __init__(self, model:Type[accession.AccessionData]):
    super().__init__(model)

  def convert_to_model(self, dbentry:Mapping[str,any])->Type[accession.AccessionData]:
    return self.model.new(dbentry)

  def convert_from_model(self, model:Type[accession.AccessionData])->Dict[str,str]:
    return model.get_attribues()
