
import sqlite3
import datetime
import importlib.resources
import itertools
from io import TextIOBase, StringIO
from xml.etree import ElementTree as ETree
from enum import Enum
from typing import NamedTuple, ClassVar
from pathlib import Path
from closeable import ICloseable, Closeable
from xmlschema import XMLSchema
from .abc import ISitemap, ISitemapFile, ILoadable

class ChangeFreq (Enum):

  NONE = ""
  HOURLY = "hourly"
  DAILY = "daily"
  WEEKLY = "weekly"
  MONTHLY = "monthly"
  YEARLY = "yearly"
  ALWAYS = "always"
  NEVER = "never"

class URL (NamedTuple):

  loc:str
  last_mod:datetime.datetime
  priority:float = 0.5
  change_freq:ChangeFreq = ChangeFreq.NONE

class SitemapFile (ISitemapFile):

  def __init__ (self, file:Path|str, urls:list[URL]):
    self._file = Path(file)
    self._urls = urls

  @property
  def file (self) -> Path:
    return self._file

  def _as_element (self) -> ETree.Element:
    urlset_node = ETree.Element("urlset", {
      "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    })
    for loc, last_mod, priority, change_freq in self._urls:
      url_node = ETree.SubElement(urlset_node, "url")
      loc_node = ETree.SubElement(url_node, "loc")
      loc_node.text = loc
      last_mod_node = ETree.SubElement(url_node, "lastmod")
      last_mod_node.text = last_mod.date().isoformat()
      if priority != 0.5:
        priority_node = ETree.SubElement(url_node, "priority")
        priority_node.text = "{:.3f}".format(priority)
      if change_freq.value:
        change_freq_node = ETree.SubElement(url_node, "changefreq")
        change_freq_node.text = change_freq.value
    return urlset_node

  def save (self, use_indent:bool=False):
    element = self._as_element()
    if use_indent:
      ETree.indent(element)
    with open(self._file, "wb") as file:
      for part in ETree.tostringlist(element, encoding="utf-8", xml_declaration=True):
        file.write(part)

class Sitemap (ISitemap, ILoadable, ICloseable):

  def _db_prepare (self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE change_freq(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)")    
    for change_freq in ChangeFreq:
      cursor.execute("INSERT INTO change_freq(name) VALUES(?)", (change_freq.value,))
    cursor.execute("CREATE TABLE url(id INTEGER PRIMARY KEY AUTOINCREMENT, loc TEXT, last_mod_seconds INTEGER, priority REAL, change_freq_id INT REFERENCES change_freq(id))")
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

  def register (self, loc:str, last_mod:datetime.datetime, priority:float=0.5, change_freq:ChangeFreq=ChangeFreq.NONE):
    self._closeable.must_be_open()
    self._cursor.execute("SELECT id FROM url WHERE loc == ?", (loc,))
    if self._cursor.fetchone():
      self._cursor.execute("UPDATE url SET url.last_mod_seconds = ?, priority = ?, change_freq_id = (SELECT change_freq.id FROM change_freq WHERE change_freq.name = ?)", (last_mod.timestamp(), priority, change_freq.value))
    else:
      self._cursor.execute("INSERT INTO url(loc, last_mod_seconds, priority, change_freq_id) VALUES(?, ?, ?, (SELECT change_freq.id FROM change_freq WHERE change_freq.name = ?))", (loc, last_mod.timestamp(), priority, change_freq.value))

  def unregister (self, loc:str):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM url WHERE loc == ?", (loc,))

  def clear (self):
    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM url")

  def get (self, loc:str) -> URL|None:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT url.loc, url.last_mod_seconds, url.priority, change_freq.name FROM url INNER JOIN change_freq ON change_freq.id = url.change_freq_id WHERE url.loc == ?", (loc,))
    found_column = self._cursor.fetchone()
    if found_column:
      loc, last_mod_seconds, priority, change_freq_name = found_column
      last_mod = datetime.datetime.fromtimestamp(last_mod_seconds)
      change_freq = ChangeFreq(change_freq_name)
      return URL(loc, last_mod, priority, change_freq)
    else:
      return None

  def list_all (self) -> list[URL]:
    self._closeable.must_be_open()
    self._cursor.execute("SELECT url.loc, url.last_mod_seconds, url.priority, change_freq.name FROM url INNER JOIN change_freq ON url.change_freq_id = change_freq.id ORDER BY url.loc ASC")
    result = []
    for loc, last_mod_seconds, priority, change_freq_name in self._cursor.fetchall():
      last_mod = datetime.datetime.fromtimestamp(last_mod_seconds)
      change_freq = ChangeFreq(change_freq_name)
      result.append(URL(loc, last_mod, priority, change_freq))
    return result

  def save_files (self, use_indent:bool=False) -> list[ISitemapFile]:
    self._cursor.execute("SELECT url.loc, url.last_mod_seconds, url.priority, change_freq.name FROM url INNER JOIN change_freq ON url.change_freq_id = change_freq.id ORDER BY url.loc ASC")
    urls = ((loc, datetime.datetime.fromtimestamp(last_mod_seconds), priority, ChangeFreq(change_freq_name)) for loc, last_mod_seconds, priority, change_freq_name in self._cursor.fetchall())
    result = []
    for index, batched_urls in enumerate(itertools.batched(urls, 50000)):
      if 0 < index:
        save_file = self._file.with_stem("{:s}{:d}".format(self._file.stem, index +1))
      else:
        save_file = self._file
      sitemap_file = SitemapFile(save_file, batched_urls)
      sitemap_file.save(use_indent=use_indent)
      result.append(sitemap_file)
    return result

  _XML_SCHEMA_TO_PARSE:ClassVar[XMLSchema] = XMLSchema(importlib.resources.files("sitemap").joinpath("static/xsd/sitemap.xsd"), build=False)
  _XML_SCHEMA_TO_PARSE.build()

  def load (self, stream:TextIOBase):
    self._closeable.must_be_open()
    root = self._XML_SCHEMA_TO_PARSE.to_dict(stream)
    for url in root["url"]:
      loc_source = url["loc"]
      if loc_source:
        loc = loc_source
      else:
        raise ValueError()
      last_mod_source = url["lastmod"]
      if last_mod_source:
        last_mod = datetime.datetime.fromisoformat(last_mod_source)
      else:
        raise ValueError()
      priority_source = url.get("priority")
      if priority_source:
        priority = float(priority_source)
      else:
        priority = 0.5
      change_freq_source = url.get("changefreq")
      if change_freq_source:
        change_freq = ChangeFreq(change_freq_source)
      else:
        change_freq = ChangeFreq.NONE
      self.register(loc, last_mod, priority, change_freq)

  def loads (self, source:str):
    with StringIO(source) as stream:
      self.load(stream)
