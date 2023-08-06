#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

from typing import Mapping, Type


class ModelConverter:

  def __init__(self, model):
    self.model = model

  def convert_to_model(self, attributes):
    raise NotImplementedError

  def convert_from_model(self, model, outdict=None):
    raise NotImplementedError

  def map_inattributes(self, mattribs:Mapping[str,any], indata:Mapping[str,any],
                       convmap:Mapping[str,str], switch:bool=False):
    for i in convmap:
      if i in indata and convmap[i] is None and indata[i]:
        if switch:
          mattribs[indata.pop(i)] = i
        else:
          mattribs[i] = indata.pop(i)
      if i in indata and convmap[i] is not None and indata[i]:
        if switch:
          mattribs[indata.pop(i)] = convmap[i]
        else:
          mattribs[convmap[i]] = indata.pop(i)
