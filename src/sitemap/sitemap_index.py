
import sqlite3
import datetime
import importlib.resources
from io import TextIOBase, StringIO
from xml.etree import ElementTree as ETree
from enum import Enum
from typing import NamedTuple, ClassVar
from pathlib import Path
from closeable import ICloseable, Closeable
from xmlschema import XMLSchema
from .abc import ISitemap, ISitemapFile, ILoadable

class Sitemap (NamedTuple):

  loc:str
  last_mod:datetime.datetime

class SitemapIndexFile (ISitemapFile):

  def __init__ (self, file:Path|str, sitemaps:list[Sitemap]):
    self._file = Path(file)
    self._sitemaps = sitemaps

  @property
  def file (self) -> Path:
    return self._file

  def _as_element (self) -> ETree.Element:
    sitemap_index_node = ETree.Element("sitemapindex", {
      "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    })
    for loc, last_mod in self._sitemaps:
      sitemap_node = ETree.SubElement(sitemap_index_node, "sitemap")
      sitemap_loc_node = ETree.SubElement(sitemap_node, "loc")
      sitemap_loc_node.text = loc
      sitemap_last_mod_node = ETree.SubElement(sitemap_node, "lastmod")
      sitemap_last_mod_node.text = last_mod.date().isoformat()
    return sitemap_index_node

  def save (self, use_indent:bool=False):
    element = self._as_element()
    if use_indent:
      ETree.indent(element)
    with open(self._file, "wb") as file:
      for part in ETree.tostringlist(element, encoding="utf-8", xml_declaration=True):
        file.write(part)

class SitemapIndex (ISitemap, ILoadable, ICloseable):

  def _db_prepare (self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE sitemap(id INTEGER PRIMARY KEY AUTOINCREMENT, loc TEXT, last_mod_seconds INTEGER)")
    return connection, cursor

  def __init__ (self, file:Path|str):
    self._file = Path(file)
    self._connection, self._cursor = self._db_prepare()
    self._closeable = Closeable(self._close_handler)

  def __enter__ (self):
    return self

  def __exit__ (self, exc_type, exc_value, traceback):
    self._closeable.close()

  @property
  def closed (self) -> bool:
    return self._closeable.closed

  def _close_handler (self):
    self._cursor.close()
    self._connection.close()

  def close (self):
    self._closeable.close()

  def register (self, loc:str, last_mod:datetime.datetime):
    self._closeable.must_be_open()
    self._cursor.execute("SELECT id FROM sitemap WHERE loc == ?", (loc,))
    if self._cursor.fetchone():
      self._cursor.execute("UPDATE sitemap SET last_mod_seconds = ? WHERE loc == ?", (last_mod.timestamp(), loc))
    else:
      self._cursor.execute("INSERT INTO sitemap(loc, last_mod_seconds) VALUES(?, ?)", (loc, last_mod.timestamp()))

  def unregister (self, loc:str):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM sitemap WHERE loc == ?", (loc,))

  def clear (self):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM sitemap")

  def get (self, loc:str) -> Sitemap|None:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT loc, last_mod_seconds FROM sitemap WHERE loc == ?", (loc,))
    found_column = self._cursor.fetchone()
    if found_column:
      loc, last_mod_seconds = found_column
      last_mod = datetime.datetime.fromtimestamp(last_mod_seconds)
      return Sitemap(loc, last_mod)
    else:
      return None

  def list_all (self) -> list[Sitemap]:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT loc, last_mod_seconds FROM sitemap ORDER BY loc ASC")
    result = []
    for loc, last_mod_seconds in self._cursor.fetchall():
      last_mod = datetime.datetime.fromtimestamp(last_mod_seconds)
      result.append(Sitemap(loc, last_mod))
    return result

  def save_files (self, use_indent:bool=False) -> list[ISitemapFile]:
    self._cursor.execute("SELECT loc, last_mod_seconds FROM sitemap ORDER BY loc ASC")
    sitemaps = [(loc, datetime.datetime.fromtimestamp(last_mod_seconds)) for loc, last_mod_seconds in self._cursor.fetchall()]
    result = []
    if sitemaps:
      sitemap_index_file = SitemapIndexFile(self._file, sitemaps)
      sitemap_index_file.save(use_indent=use_indent)
      result.append(sitemap_index_file)
    return result

  _XML_SCHEMA_TO_PARSE:ClassVar[XMLSchema] = XMLSchema(importlib.resources.files("sitemap").joinpath("static/xsd/sitemap.xsd"), build=False)
  _XML_SCHEMA_TO_PARSE.add_schema(importlib.resources.files("sitemap").joinpath("static/xsd/siteindex.xsd"))
  _XML_SCHEMA_TO_PARSE.build()

  def load (self, stream:TextIOBase):
    self._closeable.must_be_open()
    root = self._XML_SCHEMA_TO_PARSE.to_dict(stream)
    for sitemap in root["sitemap"]:
      loc_source = sitemap["loc"]
      if loc_source:
        loc = loc_source
      else:
        raise ValueError()
      last_mod_source = sitemap["lastmod"]
      if last_mod_source:
        last_mod = datetime.datetime.fromisoformat(last_mod_source)
      else:
        raise ValueError()
      self.register(loc, last_mod)

  def loads (self, source:str):
    with StringIO(source) as stream:
      self.load(stream)
