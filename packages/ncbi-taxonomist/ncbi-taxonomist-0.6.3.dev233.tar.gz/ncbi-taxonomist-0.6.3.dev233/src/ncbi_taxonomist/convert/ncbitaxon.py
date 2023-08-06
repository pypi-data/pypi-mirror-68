"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys


from ncbi_taxonomist.convert import converter
from ncbi_taxonomist.convert import convertermap

class NcbiTaxonConverter(converter.ModelConverter):

  exclude = set(['misspelling', 'authority'])

  def __init__(self, taxonmodel):
    super().__init__(taxonmodel)

  def convert_to_model(self, attributes):
    mattribs = {'names':{attributes.pop('scientific_name'):'scientific_name'}}
    self.map_inattributes(mattribs, attributes, convertermap.attributes)
    mattribs['names'].update(attributes['other_names'].pop('names', None))
    model = self.model.new(mattribs)
    if 'cde_names' in attributes['other_names']:
      self.add_cdenames(model, attributes['other_names'].pop('cde_names'))
    return model

  def add_cdenames(self, model, cdenames):
    for i in cdenames:
      if i['cde'] not in NcbiTaxonConverter.exclude:
        model.names[i['name']] = i['cde']
        if i['uniqname']:
          model.names[i['uniqname']] = 'uniqname'
