
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

  """サイトマップインデックスの <sitemap> の内容を表現します。

  Attributes
  ----------
  loc : str
    サイトマップの <loc> の値です。
  last_mod : datetime.datetime
    サイトマップの <lastmod> の値です。
  """

  loc:str
  last_mod:datetime.datetime

class SitemapIndexFile (ISitemapFile):

  """単体のサイトマップインデックスファイルを表現するクラスです。

  Warnings
  --------
  本クラスは `SitemapIndex.save_files` メソッドにより生成されることを想定しています。
  よって手動での生成は推奨されません。
  """

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

  """サイトマップインデックスを表現するクラスです。

  Examples
  --------
  >>> import datetime
  >>> 
  >>> sitemap = Sitemap("./sample.xml")
  >>> sitemap.register("http://www.example.com/sitemap.xml", datetime.datetime(2025, 1, 23))
  >>> sitemap.save_files()
  [<sitemap.sitemap_index.SitemapIndexFile object at 0xXXXXXXXXXXXXXXXX>]
  """

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

    """サイトマップインデックスにサイトマップの URL を登録します。

    Notes
    -----
    登録済みの URL が指定されたとき、本メソッドは重複するレコードを作成するのではなく、既存のレコードを更新する処理を行います。

    Arguments
    ---------
    loc : str
      登録するサイトマップの URL です。
    last_mod : datetime.datetime
      登録するサイトマップの更新日時です。
    """

    self._closeable.must_be_open()
    self._cursor.execute("SELECT id FROM sitemap WHERE loc == ?", (loc,))
    if self._cursor.fetchone():
      self._cursor.execute("UPDATE sitemap SET last_mod_seconds = ? WHERE loc == ?", (last_mod.timestamp(), loc))
    else:
      self._cursor.execute("INSERT INTO sitemap(loc, last_mod_seconds) VALUES(?, ?)", (loc, last_mod.timestamp()))

  def unregister (self, loc:str):

    """サイトマップインデックスに登録されたサイトマップ情報を削除します。

    Notes
    -----
    削除するサイトマップが存在しない場合であっても、このメソッドは必ず成功します。

    Arguments
    ---------
    loc : str
      削除するサイトマップの URL です。
    """

    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM sitemap WHERE loc == ?", (loc,))

  def clear (self):

    """サイトマップに登録された全てのサイトマップ情報を削除します。"""

    self._closeable.must_be_open()
    self._cursor.execute("DELETE FROM sitemap")

  def get (self, loc:str) -> Sitemap|None:

    """サイトマップインデックスに登録された任意のサイトマップ情報を取得します。

    Arguments
    ---------
    loc : str
      取得するサイトマップの URL です。

    Returns
    -------
    Sitemap|None
      ページ情報の取得に成功したならば、その情報が設定された `Sitemap` オブジェクトを返します。
      逆にページ情報の取得に失敗したならば `None` が返されます。
    """

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

    """サイトマップインデックスに登録された全てのサイトマップ情報をリストにして返します。

    Returns
    -------
    list[URL]
      画像サイトマップに登録された全てのサイトマップ情報のリストです。
      本リストは整列済みの状態で返されます。
    """

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
