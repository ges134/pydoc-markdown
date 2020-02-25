# -*- coding: utf8 -*-
# Copyright (c) 2019 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
`pydoc_markdown.interfaces`
===========================

This module defines the interfaces that can to be implemented for
Pydoc-Markdown to implement custom loaders for documentation data,
processors or renderers.
"""

from nr.databind.core import Struct, DeserializeAs, UnionType
from nr.interface import Interface, implements, default
from .reflection import Module, ModuleGraph
from .utils import load_entry_point


class Loader(Interface):
  """
  This interface describes an object that is capable of loading documentation
  data. The location from which the documentation is loaded must be defined
  with the configuration class.
  """

  ENTRYPOINT_NAME = 'pydoc_markdown.interfaces.Loader'
  DeserializeAs(UnionType.with_entrypoint_resolver(ENTRYPOINT_NAME))

  def load(self, graph):  # type: (Object, ModuleGraph) -> None
    """
    Fill the [[ModuleGraph]].
    """


class LoaderError(Exception):
  pass


class Processor(Interface):
  """
  A processor is an object that takes a #ModuleGraph object as an input and
  transforms it in an arbitrary way. This usually processes docstrings to
  convert from various documentation syntaxes to plain Markdown.
  """

  ENTRYPOINT_NAME = 'pydoc_markdown.interfaces.Processor'
  DeserializeAs(UnionType.with_entrypoint_resolver(ENTRYPOINT_NAME))

  def process(self, graph):  # type: (Object, ModuleGraph) -> None
    pass


class Renderer(Processor):
  """
  A renderer is an object that takes a #ModuleGraph as an input and produces
  output files or writes to stdout. It may also expose additional command-line
  arguments. There can only be one renderer at the end of the processor chain.

  Note that sometimes a renderer may need to perform some processing before
  the render step. To keep the possibility open that a renderer may implement
  generic processing that could be used without the actual renderering
  functionality, #Renderer is a subclass of #Processor.
  """

  ENTRYPOINT_NAME = 'pydoc_markdown.interfaces.Renderer'
  DeserializeAs(UnionType.with_entrypoint_resolver(ENTRYPOINT_NAME))

  @default
  def process(self, graph):  # type: (Object, ModuleGraph) -> None
    pass

  def render(self, graph):  # type: (Object, ModuleGraph) -> None
    pass